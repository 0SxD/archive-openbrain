#!/usr/bin/env bash
# precompact_save.sh — lightweight Stop hook, runs on every session end / compaction
# Writes atomic JSON state snapshot to memory/.harness/session_state.json
# Works from any project dir under <WORKSPACE>\

HARNESS_DIR="<WORKSPACE>/OpenBrainLM/memory/.harness"
STATE_FILE="$HARNESS_DIR/session_state.json"
TASK_DIR="$HARNESS_DIR"

mkdir -p "$HARNESS_DIR"

# Count active task files (any .json except session_state.json itself)
task_count=$(find "$TASK_DIR" -maxdepth 1 -name "*.json" ! -name "session_state.json" 2>/dev/null | wc -l | tr -d ' ')

# Count unsaved findings: lines added to short_term.md since last snapshot (proxy: total line count)
stm="<WORKSPACE>/OpenBrainLM/memory/short_term.md"
findings_count=0
[ -f "$stm" ] && findings_count=$(wc -l < "$stm" | tr -d ' ')

timestamp=$(date -u +"%Y-%m-%dT%H:%M:%SZ")

cat > "$STATE_FILE" <<EOF
{
  "timestamp": "$timestamp",
  "active_tasks": $task_count,
  "unsaved_findings_lines": $findings_count,
  "short_term_path": "$stm",
  "note": "snapshot written by precompact_save.sh on Stop event"
}
EOF
