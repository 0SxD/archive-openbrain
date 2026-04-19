# Agent Handle Persistence Across Compaction — Research
> Source: Agents_Arcs notebook (1a7bcc9d) — session 7107d06b — 2026-03-24
> Queried: Gemini 2.5 grounded on 156 sources

---

## Problem

When Claude Code context compacts (summarizes old messages to reduce context window usage),
all background agent task handles are lost. The orchestrator can no longer call TaskOutput
to retrieve results from workers that were dispatched before compaction. Workers may still
be running, or may have completed with results that are now inaccessible. This creates
a silent data loss pattern: work completes but the orchestrator never sees it.

---

## Patterns Found

### Pattern 1 — "Molecule" Scaffold / Non-Deterministic Idempotence
**Source: Steve Yegge "Gas Town" framework (cited in Agents_Arcs)**

The workflow state is captured as a "single organic molecule" on a tiny external scaffold
(file system, database, or queue) — completely outside the agent's context window.

- Workers are treated as ephemeral "molecules" — chains of tasks continually saved to external storage
- If the agent crashes, context window fills, or gets interrupted: the scaffold holds all state
- Next session reads the molecular state and picks up exactly where the last one left off
- No handle needed — state is reconstituted from the external scaffold, not from in-memory handles

**Key principle:** Workflow survival is guaranteed because state lives entirely outside the agent.

---

### Pattern 2 — Episodic Context-Wiping Loops ("Ralph" Pattern)
**Source: Agents_Arcs — loop scripts pattern**

For tasks long enough to inevitably bloat the context window:

- Run the AI in a loop using Git commits and local files as the actual memory
- When context window fills: intentionally wipe it clean
- Spawn a fresh agent, which reads external files to see what was accomplished, and resumes
- No continuous session dependency — the loop script manages continuity, not the agent's handle

**Key principle:** Context compaction is not a failure condition — it is an expected cycle event.
Design the system so a fresh agent can always reconstruct full state from external files.

---

### Pattern 3 — Structured Domain Memory Artifacts (Anthropic Harness Pattern)
**Source: Anthropic long-running agent harness (cited in Agents_Arcs)**

Forces agents to act incrementally using structured external artifacts:

- Initializer creates: strict JSON feature/task list + initiation script + progress log
- Worker's "institutional memory" = the progress file + Git history (NOT the orchestrator's memory)
- Worker reads files → picks ONE pending task → implements → updates JSON status flag → commits → terminates
- Orchestrator never needs an active handle: the JSON task list IS the live state

**Key principle:** The JSON task list + Git history replace the in-memory handle entirely.
Any orchestrator (even a brand new one with no prior context) can resume by reading the files.

---

### Pattern 4 — Refinery Merge Queue
**Source: Steve Yegge "Gas Town" / Agents_Arcs**

When many parallel workers are dispatched:

- Workers remain completely ignorant of one another
- Each worker executes in isolation → pushes proposed output to an **external queue** → terminates
- A dedicated "Refinery" agent (separate role) reads the queue, resolves conflicts, merges to main
- No orchestrator polling loop needed — the queue is durable; the Refinery reads it on its own schedule

**Key principle:** Replace orchestrator polling with a durable queue + dedicated merge agent.
Workers write to the queue regardless of whether the orchestrator is alive.

---

### Pattern 5 — Proactive Database Loops
**Source: Agents_Arcs — /loop + OpenBrain PostgreSQL pattern**

For non-coding workflows (research, monitoring, data collection):

- Agent awakens on a schedule (cron or /loop)
- Reads a persistent database (PostgreSQL via MCP) to understand current state
- Executes task → writes findings directly to a database table → terminates
- Results compound across cycles; survives session expiry, laptop close, or context compaction

**Key principle:** Database-backed persistence means results are durable the moment they are written,
independent of whether any orchestrator is alive to receive them.

---

### On Initializer Early Termination (Critical Clarification)

The Agents_Arcs notebook explicitly states: **the Initializer is designed to terminate before workers complete.**
This is correct behavior, not a failure mode.

- Initializer's role: bootstrap domain memory (JSON task list, progress log, rules) → terminate
- Workers: spawn independently, read the shared state, pick a task, update state, terminate
- No single agent needs to remain active — the externalized state IS the workflow
- "Non-deterministic idempotence" = the path may vary but the outcome is guaranteed by external state

**Implication for our system:** The problem is NOT that the orchestrator terminates or loses handles.
The problem is that workers are writing results back to the context window (via TaskOutput) instead
of to an external durable store. The fix is architectural: workers must write to files/DB/queue first,
handle retrieval second (or not at all).

---

## Verified Against

- Agents_Arcs notebook (1a7bcc9d), Gemini 2.5 grounded on 156 sources — session 7107d06b
- Patterns internally consistent across both query responses (same session, no contradiction)
- Anthropic harness pattern independently corroborated by our existing CLAUDE.md rules
  (Initializer → amnesiac Workers → Judge pattern already in use)
- Steve Yegge "Gas Town" and "Ralph" patterns: notebook-sourced, not independently verified
  against primary sources in this session — treat as confidence 0.75 pending primary source check

---

## Recommended Fix

**Root cause:** Workers deliver results via TaskOutput into the orchestrator's context window.
When context compacts, the handle and the result both disappear.

**Fix — two-layer write protocol (workers write first, always):**

1. Every dispatched worker writes its result to a file before returning via TaskOutput.
   Canonical path pattern: `[project]/memory/agent_results/[task_id]_[timestamp].json`

2. The orchestrator reads results from disk, not from TaskOutput alone.
   TaskOutput becomes a notification ("I wrote my result to disk") not the delivery mechanism.

3. For parallel worker fans: use the Refinery pattern.
   Workers write to `agent_results/queue/`, a Refinery agent merges on its own schedule.

4. Session bootstrap reads the queue directory first, before doing anything else.
   Any result written before compaction is recoverable on the next session start.

**Implementation note:** This is a one-file-per-task pattern, not a database. It is the
minimum viable durable store that survives context compaction with zero new dependencies.
Upgrade to PostgreSQL/MCP if result volume grows or cross-session querying is needed.

**Confidence:** 0.85 (high — pattern confirmed by multiple independent frameworks in the notebook;
Refinery and molecule patterns not yet verified against primary sources)

---

## Action Items

- [ ] Add `agent_results/queue/` directory to OpenBrainLM memory architecture spec
- [ ] Update worker dispatch template: always include "write result to disk before returning"
- [ ] Verify Steve Yegge "Gas Town" paper/post as primary source (Agents_Arcs cites it but no URL given)
- [ ] Consider: does the existing Initializer → Worker pattern already do file writes? Audit current agents.
