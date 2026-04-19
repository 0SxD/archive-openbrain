# Concurrency Control for Multi-Agent Systems — Research
> Date: 2026-03-24
> Sources: arXiv:2510.18893, arXiv:2601.13671, arXiv:2502.14743, Agents_Arcs NotebookLM (1a7bcc9d, 156 sources),
>          Gas Town architecture (Steve Yegge), AutoGen concurrent agents docs, git worktrees pattern survey

---

## Industry Patterns Found

### Pattern 1: Worktree Isolation (Branch Sandbox) — DOMINANT PATTERN
**Source: Agents_Arcs notebook (1a7bcc9d), git worktrees survey, Codex/Cursor/ccswarm implementations**

The #1 production pattern. Every parallel agent gets its own git worktree — a separate filesystem directory
pointing to the same `.git` object store but on its own branch. Zero shared files during the active build
phase. No file locking needed because there is no contention.

Mechanics:
- `git worktree add -b feature-X ../agent-X-work main` — creates isolated sandbox per agent
- Each agent has its own working directory, HEAD, staging area, file index
- Agents cannot see each other's in-progress changes
- Ceiling: 5–7 concurrent agents on a single machine before rate limits and review bottleneck dominate

Limitation: Does not prevent post-merge conflicts. Two agents editing the same function in separate worktrees
will conflict at integration time. The tooling to warn about this pre-merge does not yet exist reliably.

**Implementations seen in production:** Codex desktop app, Cursor 2.0, ccswarm (specialized pools:
Frontend/Backend/DevOps/QA each in own worktree).

---

### Pattern 2: The Refinery Agent (Sequential Merge Queue)
**Source: Agents_Arcs notebook (1a7bcc9d) — Gas Town architecture by Steve Yegge**

A dedicated single-threaded "Refinery" agent acts as the exclusive merge serializer. Worker agents are
entirely ignorant of each other. Each worker:
1. Claims a task
2. Executes in total isolation (own worktree)
3. Pushes proposed change to a queue
4. Terminates immediately

The Refinery then:
- Reads the queue sequentially
- Resolves any file-level conflicts
- Rebases (not merges) into main — preserving linear history
- No concurrent writes ever reach main

Gas Town three-tier hierarchy:
- Mayor (global coordinator) → Witness (worker manager per rig) → Polecats (ephemeral workers)
- Refinery is a peer to Witness — dedicated merge processor, not a worker
- State persists in `.beads/issues.jsonl` (JSONL append-only log) — survives agent restarts
- GUPP principle: agents execute immediately on hook, no confirmation, no waiting

This is the pattern to adopt for OpenBrainLM's hookify layer.

---

### Pattern 3: JSON Task Queue with Status Flags — ANTHROPIC'S OWN PATTERN
**Source: Agents_Arcs notebook (1a7bcc9d) — Anthropic agent teams architecture, C compiler case study**

Agents coordinate exclusively through a shared structured JSON backlog. Never write directly to shared files.
Status lifecycle: `pending` → `in_progress` → `completed` (or `passing`/`failing`)

Protocol:
1. Initializer agent decomposes project → populates JSON task list (all items start `pending`)
2. Worker reads list, claims ONE `pending` task → atomically sets status to `in_progress`
3. Worker executes in isolation, never touching other tasks
4. Worker writes output to its own artifact path, updates status to `completed`, then terminates

Why JSON specifically: AI models are less likely to corrupt structured data formats than prose files.
Why claim-then-terminate: prevents agents fighting over locks, eliminates "serial dependencies" that
cause 20 agents to produce the output of 2–3.

**Proven at scale:** Anthropic ran 16 parallel Opus 4.6 agents for 2 weeks to build a 100,000-line
C compiler autonomously. Parsers, code generators, and optimizers ran simultaneously with zero
stepping on each other.

---

### Pattern 4: CRDT Observation-Driven Coordination (CodeCRDT)
**Source: arXiv:2510.18893 — CodeCRDT: Observation-Driven Coordination for Multi-Agent LLM Code Generation (Oct 2025)**

Most technically sophisticated pattern. Uses Yjs CRDT library with three data types:
- `Y.Text` — code document, character-level convergence via operation ID total order
- `Y.Map` — TODO assignments, Last-Writer-Wins (LWW) semantics per key
- `Y.Array` — append-only audit trail, causally ordered

TODO Claim Protocol (optimistic write-verify, lock-free):
1. Scan `Y.Map` for pending TODOs with `assignedTo == null`
2. Write `TODO_k.assignedTo ← agentId`
3. Wait 50ms for CRDT sync
4. Re-read: if `assignedTo == self` → claim succeeded. If another agent's ID → retry next TODO.

Architecture: Hybrid centralized-distributed. Central Hocuspocus WebSocket relay for persistence/
observability. Agents operate concurrently, no central task coordinator. Coordination emerges from
shared state observation (stigmergy pattern).

Results (600 trials):
- 100% convergence, 0 merge failures at character level
- 5–10% semantic conflicts (duplicate declarations, type mismatches) — handled by Evaluator agent
  applying TypeScript diagnostics auto-fixes
- 21.1% speedup on parallelizable tasks; 39.4% slowdown on tightly-coupled tasks
- Semantic conflicts require a separate reconciliation layer regardless of CRDT choice

---

### Pattern 5: Queue-Based Result Collection (AutoGen)
**Source: Microsoft AutoGen concurrent agents documentation**

AutoGen uses Python `asyncio.Queue` as the coordination primitive:
- Worker agents publish results to topic-specific channels
- A `ClosureAgent` collector subscribes and puts results into `asyncio.Queue`
- No direct state mutation — all writes go through the queue
- Sequential consumption of the queue by the coordinator serializes final writes

Three sub-patterns:
- Single message → multiple processors (fan-out, read-only)
- Multiple message types → dedicated processors via topic routing
- Direct messaging via `AgentId` with `await` (sequential within a conversation)

---

### Pattern 6: LangGraph Superstep + Reducer Pattern
**Source: LangGraph documentation, forum best practices**

LangGraph models parallelism as "supersteps" — groups of nodes that run concurrently in one atomic
execution unit. Concurrency control through:
- **Reducers**: functions that merge parallel state updates. `operator.add` for lists (append-safe).
  Custom reducers for conflict resolution logic.
- **Atomic superstep semantics**: if one parallel node fails, the entire superstep fails — no partial
  state commits. Prevents inconsistent states.
- **Persistence**: SQLite/Redis/Postgres checkpointers with row-level locking or optimistic concurrency.
- `max_concurrency` parameter caps simultaneous nodes.

LangGraph does NOT solve file-system write conflicts directly — it manages in-memory state. For file
writes, callers must still use one of the above patterns.

---

## Key Finding: What Does NOT Work

From Agents_Arcs (156 sources): shared file state with multiple writers causes "serial dependencies"
where 20 agents produce the output of 2–3. Agents fight over tools, spend time waiting for locks.
This is why the industry converged on isolation-first (worktrees) + serialized merge (Refinery/queue)
rather than trying to manage concurrent access to shared files.

---

## Recommended Implementation for OpenBrainLM

### Tier 1: Isolation (prevent conflicts at source)
- Each parallel agent gets its own git worktree
- Command: `git worktree add -b agent-{task-id} ../agent-{task-id}-work main`
- Agents never write to the same working directory

### Tier 2: Coordination (claim work without contention)
- Central JSON task file: `memory/task_queue.json`
- Schema per task: `{ "id": str, "status": "pending|in_progress|completed", "assigned_to": str|null, "artifact_path": str, "claimed_at": iso8601 }`
- Worker claim protocol: read → find pending → write in_progress with agent_id → re-read to verify
  (same optimistic write-verify as CodeCRDT TODO Claim)
- Workers write output to `artifact_path` (unique per task, never shared)
- Workers set status to `completed` and terminate

### Tier 3: Merge (serialize integration)
- Single Refinery agent (not a worker) runs after all workers complete
- Sequential rebase (not merge) into main, one artifact at a time
- Runs semantic validation (lint/type-check) before each integration
- Conflicts at this layer are expected ~5–10% of the time (CodeCRDT finding) — Refinery flags them
  rather than auto-resolving

### Hookify Integration
- `hookify.sandbox-verify-before-write.local.md` already exists — extend it to check:
  1. Is the agent writing to its own worktree path? (not shared main)
  2. Is the task claimed in `task_queue.json`? (not double-claimed)
- Add a `hookify.refinery-merge-gate.local.md` rule: no agent may write to main branch directly —
  all writes route through Refinery

### State Persistence
- Adopt Gas Town's `.beads/issues.jsonl` pattern: append-only JSONL log of all task state transitions
- Survives agent restarts (GUPP principle: agents resume from log, no confirmation needed)

---

## Citations

1. **CodeCRDT** (primary technical source): arXiv:2510.18893
   https://arxiv.org/abs/2510.18893

2. **Multi-Agent Coordination Survey**: arXiv:2502.14743
   https://arxiv.org/abs/2502.14743

3. **Orchestration of Multi-Agent Systems**: arXiv:2601.13671
   https://arxiv.org/abs/2601.13671

4. **Gas Town Architecture** (Refinery pattern source): Steve Yegge
   https://gist.github.com/johnlindquist/4174127de90e1734d58fce64c6b52b62

5. **Git Worktrees for Parallel AI Agents**: Upsun Developer Center
   https://devcenter.upsun.com/posts/git-worktrees-for-parallel-ai-coding-agents/

6. **AutoGen Concurrent Agents**: Microsoft AutoGen docs
   https://microsoft.github.io/autogen/stable//user-guide/core-user-guide/design-patterns/concurrent-agents.html

7. **Agents_Arcs NotebookLM** (156 sources, Anthropic C compiler case study, Gas Town synthesis):
   notebook id: 1a7bcc9d, session: f40fbb08

8. **LangGraph Parallelization**: LangChain docs + community forum
   https://forum.langchain.com/t/best-practices-for-parallel-nodes-fanouts/1900
