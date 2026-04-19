#!/usr/bin/env bash
# PostToolUse hook: captures Agent tool dispatch + results to dispatch_log.jsonl
# Runs on every PostToolUse for Agent tool — must be fast

DISPATCH_LOG="<WORKSPACE>/OpenBrainLM/memory/.harness/dispatch_log.jsonl"
INPUT=$(cat)

TOOL_NAME=$(echo "$INPUT" | jq -r '.tool_name // empty' 2>/dev/null)
[ "$TOOL_NAME" != "Agent" ] && exit 0

TS=$(date -u +"%Y-%m-%dT%H:%M:%SZ")

if command -v jq &>/dev/null; then
  AGENT_NAME=$(echo "$INPUT" | jq -r '.tool_input.agent_name // .tool_input.description // "unknown"' 2>/dev/null)
  DESCRIPTION=$(echo "$INPUT" | jq -r '.tool_input.description // .tool_input.prompt // ""' 2>/dev/null | head -c 200)
  echo "{\"timestamp\":\"$TS\",\"agent_name\":\"$AGENT_NAME\",\"description\":\"$DESCRIPTION\",\"status\":\"completed\"}" >> "$DISPATCH_LOG"
else
  echo "{\"timestamp\":\"$TS\",\"agent_name\":\"unknown\",\"description\":\"jq_unavailable\",\"status\":\"completed\"}" >> "$DISPATCH_LOG"
fi

exit 0
