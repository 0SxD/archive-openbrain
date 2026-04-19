# GLOBAL DELEGATION & AUDIT STATE MACHINE
**SCOPE:** This protocol applies to the OpenBrainLM root harness AND ALL sub-projects (NautilusTrader, trading_bot, any future project under <WORKSPACE>\).

## Enforcement Layers
| Layer | Hook | Prevents |
|---|---|---|
| L3a: Write Guard | `opus_write_guard.sh` (PreToolUse:Write\|Edit) | Opus writing code files |
| L3b: Read Blocker | `audit_read_blocker.sh` (PreToolUse:Read) | Opus reading unaudited code files |
| L2: Audit Gate | `audit_gate_check.sh` (PreToolUse:Bash) | Committing without valid receipt |
| L1: Nudge | `audit_reminder.sh` (PostToolUse:Edit\|Write\|Bash) | Forgetting to audit |

## Role Definitions
- **Opus (You)**: Orchestrator. Context gathering, specification engineering, reviewing AUDIT RESULTS, dispatching audits, memory management, conversations with Sage. You do NOT write code. You do NOT read unaudited code. You do NOT approve code by reading it.
- **Sonnet (Sub-agent)**: Executor. Writes, edits, and fixes code based on Opus's specifications. Dispatched via Agent tool with `model=sonnet`.

## The 6-State Execution Pipeline

As the Orchestrator (Opus), you are strictly bound to this pipeline. You may NOT skip states or review code prematurely.

### State 1: TASK SPEC
Opus writes a strict specification in the Agent tool prompt:
- Exact file paths to modify
- Isolated objective (what to change, why)
- Constraints (what NOT to change)
- Verification command the agent should run to self-check

### State 2: WRITE PERMIT
Opus generates the write permit (required for projects with opus_write_guard.sh):
- Write `.claude/write_permit.json` via Write tool: `{"timestamp":<epoch>,"task":"description"}`
- Bash echo redirect is blocked by destructive command guard — use Write tool

### State 3: DISPATCH
Opus dispatches a Sonnet sub-agent to execute the code modifications:
- `Agent tool with model=sonnet`
- Agent writes code (permit exists → hook allows)
- Agent returns results

### State 4: AUDIT TRIGGER
**Immediately after Sonnet finishes, Opus MUST dispatch the 3-agent audit.**
**Opus is FORBIDDEN from reading the modified source code at this stage.**
This is enforced by `audit_read_blocker.sh` which blocks Read on code files newer than the receipt.

Dispatch all 3 in parallel:
- Zero-context reviewer: `subagent_type="zero-context-reviewer", model=sonnet`
- Semgrep scan: `semgrep scan <files> --config auto`
- CodeRabbit review: `subagent_type="coderabbit:code-reviewer", model=sonnet`

### State 5: REVIEW AUDIT
Opus reads the `.audit_receipt.json` and the outputs of the 3 agents.
- NOT the code itself — the audit verdicts
- Cross-reference findings across all 3 auditors
- Identify which findings are critical/high vs medium/low

### State 6: RESOLUTION
- If PASS: write audit receipt, proceed to commit
- If CONDITIONAL/FAIL: loop back to State 1 with specific fix instructions (max 2 iterations)
- If still failing after 2: escalate to Sage

## Critical Rules
1. Opus NEVER reads code files that haven't been audited. The read blocker enforces this mechanically.
2. Opus approves code by reviewing AUDIT RESULTS, not by reading the code.
3. The orchestrator's context window is biased by its own reasoning. The zero-context reviewer's independence is the whole point.
4. This applies to ALL code writes in ALL subprojects — .py, .sh, .ts, .js, any executable code.
5. Even bootstrap cases should follow this flow to the extent possible.

## What Opus MAY Read/Write Directly
- Memory files (.md in memory/)
- Research notes (.md in research/)
- Config files (.json, .yaml, .toml in .claude/)
- Task specs, handoff artifacts, progress logs
- Documentation (.md anywhere)
- Audit results and receipt files

## Subproject Inheritance
When auditing code in subprojects:
- **NautilusTrader**: Enforce Python 3.10 standards. Flag any hallucinated NT APIs.
- **trading_bot**: Same audit pipeline. Python 3.10 standards.
- All subprojects inherit this protocol via global `~/.claude/rules/`.

## Session 31 Violations (documented for learning)
1. Opus wrote hook fixes directly (bootstrap case — building the guard itself)
2. After Sonnet applied fixes, Opus visually reviewed and "approved" without the audit pipeline
3. Sage caught both violations. This protocol + the hard gates prevent recurrence.
