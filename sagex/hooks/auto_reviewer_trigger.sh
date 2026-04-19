#!/usr/bin/env bash
# PostToolUse: Auto-Reviewer Trigger
# ====================================
# Fires after Write|Edit completes successfully.
# If the written file is a .py file, injects a deterministic instruction
# into the agent's context telling it to spawn the zero-context reviewer.
#
# Architecture: PostToolUse hook cannot spawn agents directly — it injects
# an instruction that the agent MUST follow. The brainstem PreToolUse hook
# reinforces this obligation on every subsequent tool call.
#
# Source: Zero-Context Reviewer pattern (OAP, Orchestral AI)

INPUT=$(cat)

# Guard: jq must be available for path extraction
if ! command -v jq &>/dev/null; then
  echo "WARNING: jq not installed. Cannot determine file path for audit trigger." >&2
  exit 0
fi

# Extract file path from tool result (fallback to .path for Edit tool compatibility)
FILE_PATH=$(echo "$INPUT" | jq -r '.tool_input.file_path // .tool_input.path // empty' 2>/dev/null)

# Only trigger for .py and .sh files
if echo "$FILE_PATH" | grep -qiE '\.(py|sh)$'; then
    # Check it's not in an exempt directory
    if echo "$FILE_PATH" | grep -qiE '(memory/|\.claude/|research/|__pycache__/)'; then
        exit 0
    fi

    cat <<'AUDIT_EOF'
3-PART ZERO-CONTEXT AUDIT REQUIRED
====================================
You just wrote/edited: [FILE_PATH_BELOW]

ALL THREE auditors must run in ZERO-CONTEXT mode — no project goals, no user intent, no chat history. Only raw code.

1. ZERO-CONTEXT LLM REVIEWER
   Dispatch as: subagent_type "zero-context-reviewer"
   Pass ONLY the file path. The agent receives NO conversation history by design.
   Its mandate: "Adversarial, zero-context security and logic reviewer. No information
   about project goals or user intent. Evaluate strictly for logic errors, security
   vulnerabilities, unhandled edge cases, and systemic risks. Assume the surrounding
   system is hostile."

2. SEMGREP (Deterministic Zero-Context)
   Run: semgrep scan [FILE_PATH_BELOW] --config auto
   Semgrep is inherently zero-context — AST + regex patterns only, no conversation window.
   Do NOT let the building agent write or modify Semgrep rules used for the audit.
   The agent that writes the code must NEVER write the test it will be judged by.

3. CODERABBIT (AI Plugin — Zero-Context Mode)
   Dispatch as: subagent_type "coderabbit:code-reviewer"
   Pass ONLY file paths and raw diffs. Do NOT pass PR titles, descriptions, commit
   messages, or project goals. CodeRabbit is configured via .coderabbit.yaml to ignore
   conversational context and review purely for security and correctness.

After ALL 3 complete, write the audit receipt:
  bash <WORKSPACE>/OpenBrainLM/.claude/hooks/write_audit_receipt.sh \
    "<semgrep_pass>" "<coderabbit_id>" "<zero_context_notes>"

WITHOUT this receipt, git commit will be BLOCKED by the audit gate hook (Layer 2).
This is not optional — the pre-commit gate is deterministic.
AUDIT_EOF
    printf 'File to audit: %s\n' "$FILE_PATH"

    # Exit 2 = hard block. Agent must dispatch 3-auditor pipeline before writing code files.
    exit 2
fi

exit 0
