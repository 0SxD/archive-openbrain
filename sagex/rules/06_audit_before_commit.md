---
name: audit-before-commit
description: "No git commit without a fresh audit receipt from the ZCR + Semgrep triad."
---

# Rule 06 — Audit Before Commit

## The Rule

`git commit` is blocked without a valid `.audit_receipt.json` that:

1. Covers all staged files
2. Is less than 1 hour old
3. Contains a PASS verdict from the audit triad (ZCR + Semgrep)

## The triad

1. **ZCR** — zero-context reviewer reads code cold, no project context
2. **Semgrep** — static analysis with auto config
3. **Orchestrator** — cross-references both outputs, issues final verdict

## Enforcement

`audit_gate_check.sh` fires as PreToolUse hook on `Bash(git commit*)`.
If no valid receipt exists → exit code 2 → commit blocked.

## After audit passes

Write receipt via the audit receipt script, then commit is unblocked.
