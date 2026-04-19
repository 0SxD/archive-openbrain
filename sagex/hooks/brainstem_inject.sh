#!/bin/bash
# Strategy 1: SOAR-model PreToolUse hook
# Re-broadcasts core principles into active context before every tool call.
# Counteracts "Lost in the Middle" (Liu et al., 2023) and Context Rot (Chroma, 2025).
# Token cost: ~150 tokens per tool call. Architecturally mandatory.

BRAINSTEM="$HOME/.claude/brainstem.md"

if [ -f "$BRAINSTEM" ]; then
  CONTEXT=$(cat "$BRAINSTEM")
  # Output JSON with additionalContext
  printf '{"hookSpecificOutput":{"hookEventName":"PreToolUse","additionalContext":"%s"}}' \
    "$(echo "$CONTEXT" | sed 's/"/\\"/g' | sed ':a;N;$!ba;s/\n/\\n/g')"
else
  # Brainstem missing — allow but warn
  printf '{"hookSpecificOutput":{"hookEventName":"PreToolUse","additionalContext":"WARNING: brainstem.md not found. Core principles not loaded."}}'
fi
