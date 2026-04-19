# Drift Detection — Implementation Mapping
> Source: Agents_Arcs notebook (1a7bcc9d), sessions c0ccc767 + bdc64bee, 2026-03-24
> Verified against: arXiv 2601.04170, 2602.22302, 2603.02345, 2505.02709
> Prior research: agents_arcs_memory_audit_2026-03-24.md

---

## 6 Patterns → Our System

### 1. Auto-Policing Agents (Codex Pattern)
**What it is:** Background agents scan codebase for deviations from "golden principles" and open
targeted refactoring PRs autonomously. The repository polices its own entropy.

**Lifecycle wiring:** Asynchronous background loop — NOT tied to any single agent turn.
Runs on a schedule (cron-like), independent of active sessions.

**Our system mapping:**
- Golden principles = our `propagation_manifest.md` + `.claude/rules/` files
- The background agent reads those files, diffs against live codebase state
- When drift found: opens a PR or writes a structured correction to a queue file
- Existing partial equivalent: `github-guardian` agent (defensive) — needs a drift-scan mode added
- Gap: no scheduled background scan currently exists. Would require a cron-dispatched Sonnet agent.

**Cannot be a hookify rule** — requires reasoning across the entire codebase, not a single tool event.

---

### 2. External Holdout Scenarios (StrongDM Pattern)
**What it is:** Behavioral specs stored OUTSIDE the codebase, invisible to the agent during dev.
Acts as an ML holdout set — agent cannot game or overfit to the tests.

**Lifecycle wiring:** Post-build **Stop hook** — fires when agent attempts to end session.
Hidden tests run against output; if failed, completion is rejected and failures injected back into context.

**Our system mapping:**
- Hidden test directory: `~/.claude/holdouts/` or `<WORKSPACE>\OpenBrainLM\.holdouts\` (outside agent view)
- Agent instructions forbid reading that path
- `.claude/settings.json` maps `Stop` event → `evaluate_scenarios.sh`
- Script: runs behavioral assertions, dumps failure logs back to agent context if failed
- Gap: holdout directory and scenarios don't exist yet. Stop hook scaffold is ready.

**CAN be a hookify Stop rule** — the hook fires post-completion, runs a script, blocks or allows exit.

---

### 3. Writer-Critic Validation Loops
**What it is:** Two agents with opposing mandates — writer generates, critic independently challenges.
Debate is resolved before output propagates. Catches drift before it merges.

**Lifecycle wiring:** Wired into the execution phase — after generation, before finalization.
Uses a shared scratchpad (internal message board) for peer-to-peer debate.

**Our system mapping:**
- Existing equivalent: hostile-twin / auditor pattern in our rules (already documented)
- Gap: not currently wired as formal infrastructure — hostile-twin runs as a prompt instruction, not
  a dedicated sub-agent with its own context window
- Minimal wiring: define `critic.md` and `writer.md` agent spec files in `.claude/agents/`
- Orchestrator spawns both, provides shared scratchpad, waits for consensus before committing
- Requires Claude Code Agent Teams infrastructure (`experimental_agent_teams` in settings.json)

**Requires dedicated agent infrastructure** — dynamic debate cannot be done by a static hook script.

---

### 4. Extensive Observability and Traceability
**What it is:** Granular audit trail of ALL tool calls, inputs, docs retrieved, intermediate outputs,
confidence scores, validation pass/fail. Assumes "subtle failure world" — probabilistic systems
fail silently, not with crashes.

**Lifecycle wiring:** **PostToolUse hook** — fires after every tool execution.
Silently captures inputs + results and writes to audit log. Does NOT pollute agent context window.

**Our system mapping:**
- Hook fires PostToolUse → script writes to `<WORKSPACE>\logs\agent_audit_trail.jsonl`
- Fields: timestamp, tool_name, inputs, outputs, agent_id, session_id, status
- Critical design rule: audit log must NOT be written back into agent context (bloat + noise)
- Existing partial equivalent: `claude_code_log.md` — but unstructured and incomplete
- Gap: no PostToolUse hook writing structured JSONL. Needs a 20-line bash/python script.

**CAN be a hookify PostToolUse rule** — pure logging, no reasoning required.

---

### 5. Automated Rubric Passes
**What it is:** Define explicit quality rubric (1-5 scale, pass/fail criteria, failure mode examples).
Wire an LLM to score output against rubric before human review. Outputs structured JSON feedback.
Acts as a pre-human quality gate.

**Lifecycle wiring:** **Stop hook** (when session ends or agent marks work "ready") OR
**conditional PreToolUse hook** (intercepts a specific "commit" or "publish" command).

**Our system mapping:**
- Stop hook → rubric checker script → calls LLM with rubric + output → receives JSON score
- If score below threshold: hook rejects completion, injects specific failure feedback into context
- Existing equivalent: `/verification-before-completion` plugin in our standard sequence
- Gap: plugin is manual — needs to be wired as an automatic Stop hook, not a prompted step
- Rubric content: CLAUDE.md rules + AGENT_RULES.md define the behavioral criteria to score against

**CAN be a hookify Stop rule** — event-driven, fires on session end or commit intercept.

---

### 6. Zero-Trust Behavioral Monitoring
**What it is:** Treat agents as untrusted actors. Enforce least privilege. Hard-code constraint
hierarchy. If accomplishing goal requires violating a constraint → STOP and ask human.
Real-time anomaly detection at decision boundaries.

**Lifecycle wiring:** **PreToolUse hook** — fires immediately BEFORE every tool execution.
Acts as a bouncer: intercepts tool payload, checks against permission policies and destructive
command blocklist, blocks or passes.

**Our system mapping:**
- Already partially implemented: `hookify.block-unverified-math.local.md`,
  `hookify.sandbox-bash-write-bypass.local.md`, `hookify.sandbox-nt-api-change.local.md`
- Gap: no unified blocklist for destructive commands (rm -rf, git push --force, etc.)
- Needs: PreToolUse hook checking EVERY bash/write tool call against a deny pattern list
- Escalation path: if blocked, hook writes the intercepted command + reason to a queue file,
  surfaces clarifying question to agent context

**CAN be a hookify PreToolUse rule** — synchronous intercept, no reasoning required.
**Most critical to implement first** — hard security boundary, prevents irreversible damage.

---

## What Can Be Hookify Rules

These 4 patterns map directly to Claude Code hook events and can be implemented as `.local.md`
hookify rule files (lightweight, event-driven, no persistent agent required):

| Pattern | Hook Event | Implementation |
|---|---|---|
| Zero-trust monitoring | PreToolUse | Destructive command blocklist + escalation |
| Observability/traceability | PostToolUse | Structured JSONL audit log writer |
| Rubric passes | Stop | LLM rubric scorer, blocks completion on fail |
| External holdout scenarios | Stop | Hidden test runner, blocks exit on fail |

**Implementation order for hookify rules:**
1. Zero-trust PreToolUse (blocking destructive commands — highest safety ROI, no false negatives allowed)
2. Observability PostToolUse (audit trail — necessary foundation for debugging all other patterns)
3. Rubric Stop hook (quality gate — catches behavioral drift before it lands)
4. Holdout Stop hook (behavioral verification — requires holdout scenario library to be built first)

---

## What Needs Dedicated Agents

These 2 patterns require persistent agent infrastructure — they cannot be expressed as
instantaneous hook scripts:

### Auto-Policing Agent
**Why it needs an agent:** Requires reasoning across the entire codebase + all rules files.
Must diff current state against golden principles, then author targeted PRs. This is a
multi-step cognitive task, not a pattern match.

**Minimal architecture:**
- Scheduled Sonnet agent (cron-dispatched, NOT continuous)
- Reads: `propagation_manifest.md`, `rules/` directory, live codebase state
- Outputs: structured drift report → queue file → github-guardian picks up and opens PR
- Run frequency: daily or on major merges
- Ephemeral: run → capture report → terminate. No shared state.

### Writer-Critic Loop
**Why it needs an agent:** Dynamic debate between two opposing agents cannot be done by a
static script. Requires two context windows, a shared scratchpad, and a parent orchestrator
waiting for consensus.

**Minimal architecture:**
- Orchestrator spawns `writer` Sonnet + `critic` Sonnet simultaneously
- Shared scratchpad: a queue file or in-memory message bus (live_message_bus.py exists in strategy/)
- Writer produces artifact, critic challenges it, they iterate until consensus
- Only consensus output is passed to orchestrator for commit
- Existing equivalent: hostile-twin pattern in rules — upgrade to formal agent infrastructure
- Note: current hostile-twin is a prompt instruction, not a wired agent. That IS the gap.

---

## Priority Order

Based on safety ROI, implementation cost, and dependency chain:

**P0 — Must have before any prod use:**
1. **Zero-trust PreToolUse hook** — blocks irreversible destructive actions. ~20 lines. Immediate.
2. **Observability PostToolUse hook** — audit trail. Foundation for all debugging. ~20 lines. Immediate.

**P1 — Before first real agent team deployment:**
3. **Rubric Stop hook** — quality gate, prevents behavioral drift from landing. Needs rubric spec written.
4. **Writer-Critic loop** — upgrade hostile-twin from prompt instruction to wired agent infrastructure.

**P2 — After P1 is stable:**
5. **External holdout scenarios** — requires building a holdout scenario library first. Medium effort.
6. **Auto-policing background agent** — highest ongoing value but highest setup cost. Build after
   the observability foundation (P0 #2) is collecting data to inform what the agent should scan for.

---

## ASI Framework — arXiv Verification

The Agent Stability Index (arXiv:2601.04170, January 2026) proposes 12 dimensions to quantify
behavioral drift. The 4 most directly mappable to our hook system:

| ASI Dimension | Our Hook Equivalent |
|---|---|
| Response consistency | Rubric Stop hook (scores output stability) |
| Tool usage patterns | Observability PostToolUse (logs every tool call) |
| Reasoning pathway stability | Auto-policing agent (diffs against golden principles) |
| Inter-agent agreement rates | Writer-critic loop (consensus tracking) |

Three mitigation strategies from ASI paper map to our patterns:
- Episodic memory consolidation → our Trinity Consolidation lifecycle (already implemented)
- Drift-aware routing → auto-policing agent (flags drift, routes to refactoring)
- Adaptive behavioral anchoring → zero-trust PreToolUse + rubric Stop (hard anchors)

Agent Behavioral Contracts (arXiv:2602.22302) validates the hook-first approach:
- ABC framework achieves 88-100% hard constraint compliance with <10ms overhead per action
- Bounded behavioral drift to D* < 0.27 across extended sessions
- This is the theoretical backing for our PreToolUse/PostToolUse hook strategy

---

## Citations

- arXiv:2601.04170 — Agent Drift: Quantifying Behavioral Degradation in Multi-Agent LLM Systems
  https://arxiv.org/abs/2601.04170

- arXiv:2602.22302 — Agent Behavioral Contracts: Formal Specification and Runtime Enforcement
  https://arxiv.org/abs/2602.22302

- arXiv:2603.02345 — RIVA: Leveraging LLM Agents for Reliable Configuration Drift Detection
  https://arxiv.org/abs/2603.02345

- arXiv:2505.02709 — Technical Report: Evaluating Goal Drift in Language Model Agents
  https://arxiv.org/abs/2505.02709

- arXiv:2603.16586 — Runtime Governance for AI Agents: Policies on Paths
  https://arxiv.org/html/2603.16586

- Agents_Arcs notebook (1a7bcc9d) — 156 sources, sessions c0ccc767 + bdc64bee, 2026-03-24
  https://notebooklm.google.com/notebook/1a7bcc9d-4397-4d6b-8fb2-d85ab86363ce

- Prior research base: agents_arcs_memory_audit_2026-03-24.md, agents_arcs_hooks_audit_2026-03-24.md
