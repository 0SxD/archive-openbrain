---
name: coding-harness
description: Dispatch a Sonnet coding agent, run 5-gate audit pipeline, present results. Invoke when Opus has a coding task ready for execution. This is the local coding harness — the primary agent species for this workspace.
---

# Coding Harness — Full Lifecycle

## Overview

This skill codifies the dispatch → code → audit → merge loop. Opus orchestrates and audits.
Sonnet agents execute. All gates use installed PLUGINS. No custom code without Creator's permission.

Based on the "Coding Harness" agent species (source: Gemini/NotebookLM research, 2026-03-25).

## Phase 1: Contract Definition (Opus — no agents dispatched yet)

Before dispatching ANY coding agent, Opus defines in writing:

1. **Task:** What exactly needs to be built/changed (file path, function, behavior)
2. **Done criteria:** Specific, testable conditions that define "done"
3. **Must-not:** Explicit constraints (no custom wrappers, no novel patterns, use library X)
4. **Escalation:** Conditions where Sonnet should STOP and report rather than proceed
5. **Context files:** ONLY the files Sonnet needs (minimum viable context — NOT the full CLAUDE.md or rules)
6. **Worktree:** If parallel work, assign a worktree via worktree-isolation skill

Write pre-dispatch entry to `memory/.harness/dispatch_log.jsonl`:
```json
{
  "timestamp": "ISO8601",
  "task_id": "TASK-{n}",
  "agent": "sonnet",
  "task_summary": "...",
  "target_files": ["..."],
  "status": "dispatched"
}
```

## Phase 2: Execution (1 Sonnet agent)

Dispatch via Agent tool:
- **model:** sonnet (explicit — NEVER inherit Opus)
- **mode:** acceptEdits
- **prompt:** Contract from Phase 1 + ONLY the specified context files
- Agent codes in isolation. Completes. Returns.

Do NOT inject full CLAUDE.md, full rules, or full memory into the agent prompt.

## Phase 3: Stage 1 — Local Audit (5-gate pipeline via PLUGINS)

When Sonnet returns:
1. Report to Creator: "Agent came back — running Stage 1 audit"
2. Do NOT present results yet

Dispatch gate agents (each = fresh Sonnet, zero-context, reports to Opus):

| Gate | Plugin(s) | What it checks |
|---|---|---|
| 1. Semgrep | `semgrep` plugin | Static analysis, security vulnerabilities |
| 2. CodeRabbit | `coderabbit` plugin | Logic issues, code quality, AI-generated code patterns |
| 3. Code-review | `code-review` + `pr-review-toolkit` plugins | Architecture, design, best practices |
| 4. Security | `security-guidance` plugin | OWASP top 10, injection, XSS, secure-by-default |
| 5. Clone comparison | Manual diff | Compare against reference clones in `_repos/` |
| 6. Custom (conditional) | Per Creator's criteria | Additional pass/fail if Creator specifies |

### Hard Gates (automatic FAIL if violated):
- **No custom code** without Creator's explicit permission. If agent wrote custom code where a library exists → flag it, ask Creator.
- **No hallucinated APIs.** If agent called a function that doesn't exist in the library → FAIL.
- **No partial implementations.** If done criteria not met → FAIL.

### Violation Handling:
- On ANY violation: Opus asks Creator via question. Agents do NOT decide exceptions.
- Creator approves or rejects. Creator's decision is final.
- Questions are good. ASK when uncertain.

Each gate agent writes: `agent_sync/audit_result_{task_id}_{gate}.md`
Opus writes: `agent_sync/audit_summary_{task_id}.md`

Max 2 gate agents concurrent.

## Phase 4: Audit Loop (MANDATORY — not optional)

```
execute → audit → FAIL?
                    ↓ YES
              fix → re-audit
                    ↓ FAIL again?
              same issue? → STOP → research why → different approach
              new issue?  → fix → re-audit
                    ↓ FAIL a 3rd time?
              STOP → escalate to Creator with: what failed, why, what was tried
```

Rules:
1. A fix without a passing re-audit is NOT a pass.
2. Both the executor AND the auditor must pass for work to be done.
3. If the same issue recurs after fix: do NOT loop again. STOP. Research WHY. Try a fundamentally different approach.
4. Max 2 re-audit cycles per gate before escalating to Creator.
5. Opus tells Sonnet HOW to fix — Sonnet does the fix. Opus does NOT rewrite code (unless it's a trivial one-liner).

## Phase 5: Stage 2 — GitHub PR Airlock (requires Creator approval)

Only after ALL Stage 1 gates PASS (or Creator-approved exceptions):

1. Commit to feature branch (pre-commit hook fires semgrep as first-line defense)
2. Push branch → open PR (**Creator must explicitly approve** — rule 00, no public actions without approval)
3. GitHub Actions triggers:
   - Remote semgrep scan (full repo, not just changed files)
   - CodeRabbit automated PR review (fresh LLM context, uncontaminated)
4. Address PR review comments
5. Creator reviews → Creator merges to main
6. Main branch = verified master export. Agent never has direct write access.
7. **All repos PRIVATE** unless Creator explicitly approves public.

## Phase 6: Logging

Update `memory/.harness/dispatch_log.jsonl`:
```json
{
  "task_id": "TASK-{n}",
  "stage1_verdict": "PASS|FAIL",
  "gates": {
    "semgrep": "PASS|FAIL",
    "coderabbit": "PASS|FAIL",
    "code_review": "PASS|FAIL",
    "security": "PASS|FAIL",
    "clone_comparison": "PASS|FAIL"
  },
  "re_audit_count": 0,
  "austin_exceptions": [],
  "stage2_pr": "URL or pending",
  "status": "complete|escalated"
}
```

## Constraints

- Max 2 concurrent agents at any time (1 executor + 1 auditor, or 2 auditors)
- Never run a second coding dispatch while audit is pending on the first
- All gates use INSTALLED PLUGINS — not raw MCP calls
- Sonnet executes. Opus audits and orchestrates. Opus does NOT write code.
- MCP = intelligence layer only. No MCP on the hot path.
