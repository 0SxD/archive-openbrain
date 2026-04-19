## Memory Discipline — Autonomous, No Permission Needed

Write to brain files WITHOUT asking Creator. Never announce consolidation. Just do it.

### When to Write
- After every major task: findings → relevant project brain's short_term.md
- Every ~10 tool calls or when context feels long: check for unsaved work, save it
- Before heavy context operations (research agents, large file reads): save current state first
- After every significant action, learning, or decision: write it down immediately — don't batch
- After every decision: record the decision AND the reasoning

### Core Principle
Memory system sits ABOVE compression. The brain layer is what SURVIVES.
Everything not in the brain gets lost. Everything in the brain persists.
Write BEFORE compression — not after. Consolidate actively, don't wait.

### Targets
- project brain: `[project]/memory/short_term.md`
- cross-project: `~/.claude/OPEN_BRAIN.md`
- session log: `<WORKSPACE>\logs\claude_code_log.md`

### Rules
- No passive accumulation — write with schema (statement + confidence + source + status + last_verified_date). Redundant vague entries rot context into noise (source: Agents_Arcs "passive accumulation fallacy", arXiv:2601.04170).
- Don't batch — save as you go.
- If context is approaching compression: IMMEDIATELY save everything.
- After consolidation, spot-check by reading the file back (not every time).
- Every entry promoted to long_term.md MUST include: Statement, Confidence (0-1), Source, Status (verified/disputed/needs_review), Last Verified Date (YYYY-MM-DD).
