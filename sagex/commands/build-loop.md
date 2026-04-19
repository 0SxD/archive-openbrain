---
description: "Coder → Auditor → Retry loop. Dispatches Sonnet coder, runs ZCR + Semgrep audit, loops until PASS or max rounds. Opus breaks deadlocks."
---

## /sagex:build-loop

Execute this task using the coder/auditor/orchestrator loop:

**Task:** $ARGUMENTS

### Loop Protocol

1. **Dispatch Sonnet coder** with the task and a write permit
2. Coder MUST use audited code or exact documentation solutions — no inventing
3. Coder MUST cite approved sources from `config/approved_sources.json` for the active project
4. On coder completion → dispatch **ZCR audit** (zero-context, no assumptions)
5. On ZCR completion → run **Semgrep scan** (static analysis, auto config)
6. If BOTH pass → commit with audit receipt → DONE
7. If EITHER fails → feed specific findings back to coder as fix instructions
8. **Max 3 rounds.** If round 3 still fails → STOP and report all findings to Opus
9. Between rounds, log: round number, what failed, what the coder changed

### Coder Rules
- Open-source repo solutions ONLY (cite the repo URL)
- No custom implementations when a library exists
- Every .py write requires fresh research.md entry with approved-domain URLs
- Code must be auditable without modification

### Auditor Rules
- ZCR: zero-context review — no assumptions about intent, read code cold
- Semgrep: static analysis with auto config
- Both must independently PASS for the round to succeed
- Auditors know the no-custom-code and approved-source rules

### Deadlock Resolution
- If the same finding appears 2+ rounds with no progress → Opus intervenes
- Opus reviews all round logs and either: fixes directly, redefines the task, or escalates to Sage
