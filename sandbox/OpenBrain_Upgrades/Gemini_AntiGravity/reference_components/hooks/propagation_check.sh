#!/usr/bin/env bash
# PostToolUse hook: fires after Edit|Write, checks if a rule/hook file was modified.
# Reads JSON from stdin (Claude Code PostToolUse payload).

input=$(cat)
file_path=$(echo "$input" | jq -r '.tool_input.file_path // empty' 2>/dev/null)

if echo "$file_path" | grep -qiE 'rules/.*\.md|hooks/.*\.sh|hookify.*\.md|CLAUDE\.md'; then
  echo "PROPAGATION CHECK: You modified a rule/hook file. Update the propagation manifest at C:\\workspace\\.claude\\propagation_manifest.md if needed."
fi
