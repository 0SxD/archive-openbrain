#!/bin/bash
# audit_gate_check.sh — PreToolUse hook for git commit interception
# Validates .audit_receipt.json before any git commit is allowed.
# Also injects audit state file content (if present) on every Bash call.
# Input: Claude Code PreToolUse JSON on stdin
# Exit 0: allow | Exit 2: block
#
# Architecture (Session 31 fix):
#   PostToolUse hooks have stdout suppressed on exit 0. The audit_reminder.sh
#   (PostToolUse) writes state to .claude/active_audit_state.md. This PreToolUse
#   hook reads it and outputs to stderr (which IS surfaced to the agent).

set -euo pipefail

# Read stdin
input=$(cat)

# Guard: jq must be available — if missing, gate DENIES (fail-closed, not fail-open)
if ! command -v jq &>/dev/null; then
  echo "AUDIT GATE DENY: jq is not installed. Cannot validate audit receipt." >&2
  exit 2
fi

# Extract the command field from tool_input
command=$(echo "$input" | jq -r '.tool_input.command // ""')

# --- Single repo_root resolution (used by both state injection and gate) ---
# Fail-open for state injection (non-git dirs should not crash the hook)
# Fail-closed for git commit gate (checked explicitly below)
repo_root=$(git rev-parse --show-toplevel 2>/dev/null || true)

# --- State file injection (fires on ALL Bash calls) ---
# Read and surface the audit state file so the agent sees the nudge
if [ -n "$repo_root" ]; then
  state_file="$repo_root/.claude/active_audit_state.md"
  if [ -f "$state_file" ]; then
    # Race protection: file may vanish between -f check and cat
    cat "$state_file" 2>/dev/null >&2 || true
  fi
fi

# Only activate the hard gate on git commit commands — allow everything else
# Anchored to command position: start-of-string or after shell separators (;, &, &&, |, ||)
# and subshell openers ((, backtick). Avoids false positives from "git commit" in quoted arguments.
# NOTE: \b requires GNU grep (shipped with Git Bash on Windows). Not portable to BSD grep.
if ! echo "$command" | grep -qE '(^\s*|[;&|`(]+\s*)git\s+commit\b'; then
  exit 0
fi

# --- git commit detected — run the audit gate ---

# repo_root must exist for commit validation
if [ -z "$repo_root" ]; then
  echo "AUDIT GATE DENY: Could not determine git repo root." >&2
  exit 2
fi

receipt_path="$repo_root/.audit_receipt.json"

# Check receipt file exists
if [ ! -f "$receipt_path" ]; then
  echo "AUDIT GATE DENY: No .audit_receipt.json found at $receipt_path" >&2
  echo "Run the 3-part audit (Semgrep + CodeRabbit + Zero-Context Review) and write the receipt before committing." >&2
  exit 2
fi

receipt=$(cat "$receipt_path")

# --- Validate: timestamp_epoch (must be a number and < 3600 seconds old) ---
timestamp_epoch=$(jq -r '.timestamp_epoch // "missing"' <<< "$receipt")

if [ "$timestamp_epoch" = "missing" ] || [ "$timestamp_epoch" = "null" ]; then
  echo "AUDIT GATE DENY: receipt missing required field 'timestamp_epoch'." >&2
  exit 2
fi

# Verify it is numeric
if ! echo "$timestamp_epoch" | grep -qE '^[0-9]+$'; then
  echo "AUDIT GATE DENY: 'timestamp_epoch' is not a valid epoch number (got: $timestamp_epoch)." >&2
  exit 2
fi

current=$(date +%s)
age=$((current - timestamp_epoch))

# Allow up to 60s of clock skew (NTP re-sync) before flagging as spoofing
# Threshold: -60s here must match audit_reminder.sh line 31 (-ge -60)
if [ "$age" -lt -60 ]; then
  echo "AUDIT GATE DENY: receipt timestamp is in the future (${age}s ahead). Possible spoofing." >&2
  exit 2
fi

if [ "$age" -gt 3600 ]; then
  echo "AUDIT GATE DENY: Audit receipt is expired (${age}s old — max allowed: 3600s / 1 hour)." >&2
  echo "Re-run the full 3-part audit and write a fresh receipt." >&2
  exit 2
fi

# --- Validate: semgrep_pass (must be boolean true) ---
semgrep_pass=$(jq -r '.semgrep_pass // "missing"' <<< "$receipt")

if [ "$semgrep_pass" = "missing" ] || [ "$semgrep_pass" = "null" ]; then
  echo "AUDIT GATE DENY: receipt missing required field 'semgrep_pass'." >&2
  exit 2
fi

if [ "$semgrep_pass" != "true" ]; then
  echo "AUDIT GATE DENY: 'semgrep_pass' is not true (got: $semgrep_pass). Fix Semgrep findings before committing." >&2
  exit 2
fi

# --- Validate: coderabbit_approval_id (must be non-empty string, not "null") ---
# Three cases: "missing" (field absent), "null" (JSON null), "" (empty string)
coderabbit_id=$(jq -r '.coderabbit_approval_id // "missing"' <<< "$receipt")

if [ "$coderabbit_id" = "missing" ] || [ "$coderabbit_id" = "null" ] || [ -z "$coderabbit_id" ]; then
  echo "AUDIT GATE DENY: 'coderabbit_approval_id' is missing, null, or empty. CodeRabbit approval required." >&2
  exit 2
fi

# --- Validate: zero_context_reviewer_notes (must be a string > 50 chars) ---
reviewer_notes=$(jq -r '.zero_context_reviewer_notes // "missing"' <<< "$receipt")

if [ "$reviewer_notes" = "missing" ] || [ "$reviewer_notes" = "null" ]; then
  echo "AUDIT GATE DENY: receipt missing required field 'zero_context_reviewer_notes'." >&2
  exit 2
fi

notes_length=${#reviewer_notes}
if [ "$notes_length" -le 50 ]; then
  echo "AUDIT GATE DENY: 'zero_context_reviewer_notes' is too short (${notes_length} chars — minimum 51 required)." >&2
  echo "Provide substantive zero-context reviewer notes before committing." >&2
  exit 2
fi

# --- All checks passed ---
echo "Audit Gate PASSED. Receipt age: ${age}s | semgrep: PASS | coderabbit: $coderabbit_id | reviewer notes: ${notes_length} chars" >&2
exit 0
