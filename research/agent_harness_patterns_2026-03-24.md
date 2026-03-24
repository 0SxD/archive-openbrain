# Agent Harness Patterns — Research
> Source: Agents_Arcs notebook (1a7bcc9d, 156 sources) — session IDs 83fd9132 + 750f34a9
> Date: 2026-03-24
> Queried by: Claude Code (Sonnet 4.6)

---

## What Is a Harness

A harness is the durable orchestration layer that sits above individual agents and manages
the full lifecycle: dispatch, execution, result capture, persistence, and recovery. It is
what ensures the system as a whole makes progress even when individual agents terminate,
context windows compact, or sessions restart.

The Agents_Arcs sources do not use the word "harness" directly. The equivalent construct
is described as the **external scaffold** — the combination of files, hooks, task queues,
and bootup rituals that together guarantee agent results are never lost to context compaction.

Key insight from sources: the harness is NOT inside any single agent's context window.
It is the external environment the agent reads from and writes to.

---

## Production Harness Implementations

### Pattern: Initializer → Worker → Judge (the canonical production pattern)

Documented in Agents_Arcs (156 sources) as the industry-converged architecture:

**Initializer**
- Reads high-level user prompt
- Expands it into a structured JSON task list / backlog
- Writes domain memory: initiation script, progress log, constraints
- Defines rules of engagement for workers
- Intentionally terminates — leaves a machine-readable scaffold behind

**Worker (amnesiac)**
- Wakes up, reads domain memory (the external scaffold)
- Claims exactly ONE pending task from the JSON list
- Implements, tests, pushes output to an external task queue
- Terminates immediately — never holds state across cycles

**Judge / Refinery**
- Sole purpose: reads the queue of worker outputs
- Evaluates results, resolves file/code conflicts
- Merges finalized changes into the main project
- The only entity that touches shared state — eliminates contention

### The External Scaffold (what survives context compaction)

Sources describe this as a "single organic molecule state" composed of:
1. Git commit history — durable, append-only, version-controlled
2. Progress log files — timestamped, machine-readable
3. JSON task queue — pending / in-progress / complete status per task
4. Domain memory files — written by Initializer, read by every subsequent agent

This is NOT the agent's internal memory. It is the file system. Context window = volatile.
External scaffold = durable. The harness is the discipline of keeping all meaningful state
in the scaffold.

---

## Key Components

### 1. Lifecycle Management (Episodic Termination)

- Workers are STATELESS. Run → capture → terminate → fresh agent next cycle.
- No continuous running. Context window fills → wipe → fresh agent reads scaffold and resumes.
- Mechanism: `non-deterministic idempotence` — the path agents take may vary, but the
  workflow outcome is guaranteed because state lives outside any single context window.

### 2. Result Persistence (Context Compaction Survival)

- Workers do NOT write directly to master brain files.
- Workers write to an **asynchronous JSON task queue**.
- The Judge/Refinery agent (separate context, separate spawn) processes the queue and
  merges into main files.
- This prevents file-locking contention when parallel workers complete simultaneously.
- "Redundancy OK" in memory discipline is flagged as a trap by sources: accumulation
  without schema leads to "context rot." Replace with schema-driven compaction.

### 3. Task Queue Management

- JSON task list is the authoritative state of work.
- Each entry: task_id, description, status (pending/in_progress/complete), owner, output_path.
- Workers atomically claim one task (mark in_progress) before starting.
- Workers write output to a designated path, mark complete, then terminate.
- Prevents double-claiming by parallel workers.

### 4. Agent Dispatch Tracking

- Every dispatched agent must be logged before it runs (not after).
- Log entry: agent_id, task_id, dispatch_time, expected_output_path.
- Rule 06 from sources: "check for unreported agent results BEFORE responding to any message."
- The harness enforces this by making the dispatch log readable by the orchestrator on
  every bootup.

### 5. Recovery After Session Restart (Bootup Ritual)

Sources cite the bootup ritual as mandatory for context-compaction survival:
1. Fresh agent spawns
2. Reads external progress files (the scaffold)
3. Finds next pending task in JSON list
4. Resumes — no human intervention needed

The propagation manifest supports this but must NOT be injected into sub-agents
(causes context bloat and signal dilution). Progressive disclosure: orchestrator reads
manifest, workers receive only the specific snippet for their task.

---

## Four Critical Missing Mechanisms (gaps flagged by sources)

Sources explicitly audited the existing 8-rule system and identified these gaps:

### Gap 1 — Objective Verification Gate
- Problem: agents can write hallucinated solutions as "complete" with confidence.
- Fix: a PreToolUse or PostToolUse hook that **structurally forbids** marking a task
  complete unless an external test/linter/execution script passes first.
- This is distinct from the confidence bouncer (which is LLM self-critique).

### Gap 2 — Refinery / Merge Queue Agent
- Problem: Rule 01 bans shared state but provides no mechanism for combining
  parallel worker outputs.
- Fix: Dedicated "Refinery" agent — sole job is async conflict resolution and merge.
  Workers → queue → Refinery → main branch. Never workers → main branch directly.

### Gap 3 — Destructive Action Intercept
- Problem: no hard security boundary at tool-execution layer.
- Fix: PreToolUse hook that scans bash payloads for destructive patterns (rm -rf,
  DROP TABLE, etc.) and blocks before execution.

### Gap 4 — Prefix Caching Discipline
- Problem: loading full manifests + rules + memory at every session inflates token cost.
- Fix: strict prompt-ordering layout — static identity/rules at top (cached prefix),
  variable state (short-term memory, active tool outputs, current prompt) at bottom.
  Ensures the cached prefix remains stable across turns.

---

## Recommended Harness for OpenBrainLM

### Minimum Viable Harness — Files That Must Exist

```
[project]/.harness/
  dispatch_log.json        — append-only log of every agent dispatched
  task_queue.json          — authoritative task list (pending/in_progress/complete)
  result_inbox/            — workers write here, Refinery reads here
    [task_id]_result.json  — structured output: task_id, status, findings, output_paths
```

These files live OUTSIDE any agent's context window. They are the scaffold.

### Hook Sequence (Minimum Viable)

**PreToolUse — Destructive Intercept**
- Fires before every Bash tool call
- Scans payload for: rm, del, DROP, truncate, --force, -rf
- Blocks if found, logs the attempt, escalates to human
- Already partially implemented as hookify rules — needs hardening

**PostToolUse — Result Capture**
- Fires after every Agent tool completion
- Reads the agent's output
- Writes a structured entry to `result_inbox/[task_id]_result.json`
- Updates `dispatch_log.json` with completion timestamp and status
- This is the hook that ensures results are never lost to context compaction

**Stop Hook — Consolidation Gate**
- Fires when orchestrator is about to stop
- Verifies all dispatched agents in `dispatch_log.json` have a corresponding result_inbox entry
- Blocks stop if any agents are unreported
- THEN consolidates to short_term.md

### Handoff Sequence: Dispatch → Result Capture

```
1. Orchestrator creates task entry in task_queue.json (status: pending)
2. Orchestrator writes dispatch_log.json entry (agent_id, task_id, time, output_path)
3. Orchestrator dispatches Worker via Agent tool
4. Worker reads task from task_queue.json (claims it: status → in_progress)
5. Worker executes, writes output to result_inbox/[task_id]_result.json
6. Worker marks task_queue.json entry complete, terminates
7. PostToolUse hook fires → verifies result_inbox entry exists → updates dispatch_log
8. Refinery agent (separate spawn) reads result_inbox/, merges into main brain files
9. Stop hook verifies dispatch_log has no orphaned dispatches before session end
```

### Key Design Decisions (sourced from Agents_Arcs)

- Workers write to `result_inbox/` NOT directly to memory files. Eliminates file-locking.
- Orchestrator does NOT re-read the full manifest. It reads `dispatch_log.json` only.
- Sub-agents receive only their specific task context — NOT the propagation manifest.
- The Refinery is a separate agent spawn — never inlined into the orchestrator loop.
- task_queue.json is the single source of truth for "what work has been done." Git history
  is the secondary source of truth. The context window is NOT a source of truth.

---

## Citations

All findings grounded in Agents_Arcs notebook (1a7bcc9d), 156 sources, queried 2026-03-24:
- Session 83fd9132: hooks audit, concurrency patterns, manifest weaknesses
- Session 750f34a9: Initializer-Worker-Judge pattern, non-deterministic idempotence,
  external scaffold mechanics, 4 missing mechanism gaps

Named patterns from sources (cited inline in notebook):
- "Refinery / merge-queue agent" — concurrency control for parallel workers
- "Non-deterministic idempotence" — context-compaction survival principle
- "Progressive disclosure" — sub-agent context minimization (vs. full manifest injection)
- "Schema-driven compaction" — replaces "redundancy OK" in memory discipline
- "Objective verification gate" — test-driven memory updates (vs. LLM self-critique only)
- "Prefix caching discipline" — static-top / variable-bottom prompt layout

External corroboration (not directly queried, cited by notebook sources):
- Galileo AI research: one stale agent poisoned 87% of downstream decisions within hours
- Anthropic ACE paper (arXiv:2510.04618): "prompts and memory must update via execution
  feedback across sessions"
- "The one big agents.md approach inevitably fails because when everything is marked as
  important, really nothing is." (same source)
