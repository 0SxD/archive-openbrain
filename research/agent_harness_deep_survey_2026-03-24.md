# Agent Harness — Deep Survey (GitHub + arXiv)
> Date: 2026-03-24
> Scope: Off-the-shelf implementations + academic papers
> Researcher: Claude Code (Sonnet 4.6)
> Builds on: `agent_harness_patterns_2026-03-24.md` (Agents_Arcs NLM, 156 sources)

---

## Definitions (from arXiv:2603.05344 — OPENDEV, Bui 2026)

The most precise published distinction between harness and scaffold:

> **Scaffolding**: assembles the agent (system prompt, tool schemas, subagent registry) BEFORE the first prompt.
>
> **Harness**: orchestrates tool dispatch, context management, and safety enforcement AT RUNTIME.
>
> "Where scaffolding is concerned with constructing the agent before the first prompt, the harness is concerned with everything that happens after: dispatching tools, compacting context, enforcing safety invariants, and persisting state across turns."

This maps exactly to OpenBrainLM's existing architecture:
- Scaffolding = Initializer agent + propagation manifest + CLAUDE.md construction
- Harness = hookify rules + dispatch_log + task_queue + result_inbox (the missing piece)

---

## Off-the-Shelf Harnesses (GitHub)

### 1. Claude Agent SDK (Anthropic)
- **URL**: https://github.com/anthropics/claude-agent-sdk-python
- **License**: Anthropic Commercial Terms (not MIT/Apache — NOT freely reusable as a library)
- **Harness Pattern**: Provides the agent loop, tool execution, hooks, subagent spawning, and session management as a programmable SDK. The harness IS the SDK.
- **Key harness components**:
  - **Hooks**: `PreToolUse`, `PostToolUse`, `Stop`, `SessionStart`, `SessionEnd`, `UserPromptSubmit` — callback-based interception at every lifecycle event
  - **Sessions**: session_id capture + `resume=session_id` for cross-session context persistence. Sessions stored server-side by Anthropic.
  - **Subagents**: `AgentDefinition` with isolated tool access + `parent_tool_use_id` field for tracking subagent message provenance
  - **Permissions**: `allowed_tools` whitelist, `permission_mode` for auto/manual approval
- **Task persistence**: NOT provided as a file-based queue. State is in-process and session-based. External file writes must be implemented by the caller.
- **Session recovery**: `resume=session_id` resumes from server-stored session. Does NOT survive if session expires.
- **Dispatch logging**: Not built-in. Caller must implement via PostToolUse hook.
- **Agent failure detection**: Not built-in. Caller must catch exceptions from the async generator.
- **Gap for OpenBrainLM**: The SDK provides hooks and subagent spawning but NOT durable task queues or dispatch logs. We must layer those on top.
- **Assessment**: Use the SDK for agent execution. Build the durable harness layer (task_queue, dispatch_log, result_inbox) ourselves on top.

### 2. Anthropic Long-Running Agent Harness Pattern (engineering post)
- **URL**: https://www.anthropic.com/engineering/effective-harnesses-for-long-running-agents
- **License**: Open pattern description (not a library)
- **Harness Pattern**: Two-agent system — Initializer (runs once) + Coding Agent (runs in subsequent sessions)
- **Key components**:
  - `feature_list.json` — ~200+ discrete features each marked passing/failing. This IS the task queue.
  - `claude-progress.txt` — append-only session log documenting agent work. The dispatch log.
  - Git history — secondary source of truth for completed work
  - `init.sh` — environment bootstrap script for session recovery
- **Session recovery sequence**: `pwd` → read progress log + git log → check feature_list.json for highest-priority incomplete → run `init.sh` → execute e2e tests
- **Result capture**: Git commits after each feature + progress file updates. NOT in-memory.
- **Failure detection**: Browser automation (Puppeteer MCP) verifies features end-to-end. Strongly-worded constraints prevent premature completion declarations.
- **Key insight**: `feature_list.json` = task queue with status fields. `claude-progress.txt` = dispatch log. Both are file-system durable, not in-memory.
- **Assessment**: This IS the pattern from Agents_Arcs, confirmed by Anthropic's own engineering team. Use it directly.

### 3. Microsoft Agent Framework (AutoGen + Semantic Kernel merger)
- **URL**: https://github.com/microsoft/agent-framework
- **License**: MIT (open source)
- **Status**: Public preview as of 2026-02-09
- **Harness Pattern**: Graph-based Workflow with typed edges, executor nodes, built-in checkpointing
- **Key harness components**:
  - `WorkflowBuilder` — assembles workflow graph with explicit execution order
  - `FileCheckpointStorage(storage_path="./checkpoints")` — automatic file-based checkpoint persistence
  - `checkpoint_storage` parameter on `WorkflowBuilder` — enables auto-checkpointing at every superstep boundary
  - `ctx.set_executor_state()` / `ctx.set_state()` — executor-local and cross-executor state
  - `workflow.run_stream(checkpoint_id=..., checkpoint_storage=...)` — resume from any checkpoint
  - `checkpoint_storage.list_checkpoints()` — enumerate available recovery points
  - Request/Response Gate — pause workflow for human input, resume after approval
- **Session recovery**: Resume from any superstep boundary via `checkpoint_id`. When resuming from a checkpoint with pending requests, those requests are re-emitted as events.
- **Dispatch logging**: OpenTelemetry-based observability built in (not a file-based dispatch log)
- **Agent failure detection**: Fault-tolerant via checkpoint resume — failed workflows restart from last checkpoint, not from beginning
- **What it does NOT provide**: The Initializer → Worker → Judge lifecycle pattern. Workflows are stateful graphs, not episodic agents.
- **Assessment**: Best-in-class checkpointing for graph-based workflows. MIT licensed. Overkill for OpenBrainLM's file-based harness but the `FileCheckpointStorage` pattern is directly adoptable.

### 4. LangGraph (LangChain)
- **URL**: https://github.com/langchain-ai/langgraph
- **License**: MIT
- **Harness Pattern**: Low-level agent runtime based on directed graph (StateGraph). Nodes = agents/functions, edges = control flow. Centralized `StateGraph` maintains context.
- **Key harness components**:
  - `StateGraph` / `MessagesState` — centralized state container, persistent across nodes
  - `checkpointer` — pluggable persistence backend (in-memory, SQLite, PostgreSQL via LangGraph Platform)
  - `interrupt()` — pause execution for human-in-the-loop at any node
  - Conditional edges — route to different nodes based on agent output
  - Parallel execution — multiple agents handle same input, results merge at downstream node
- **Task persistence**: State deltas passed between nodes, not full conversation history. Minimal token usage.
- **Session recovery**: "Durable execution — agents persist through failures and can run for extended periods, resuming from where they left off"
- **Dispatch logging**: Not file-based. State flows through graph edges.
- **Performance note**: Fastest framework with fewest tokens (passes only state deltas, not full history)
- **Assessment**: Best choice for graph-orchestrated multi-agent workflows. MIT. Already in OpenBrainLM Phase 3 dependency list (`IMPLEMENTATION_PLAN.md`). Confirmed good choice.

### 5. CrewAI
- **URL**: https://github.com/crewAIInc/crewAI
- **License**: MIT
- **Harness Pattern**: Role-based agents with sequential, parallel, or conditional task execution. `CrewAI Flows` = event-driven scaffold with state management across steps.
- **Key harness components**:
  - `Crew` — orchestrator that manages agent roster and task assignments
  - `Task` — atomic unit with dependencies, context passing, and output
  - `Flow` — event-driven workflow with persistent state between steps
  - `load_threads_callback` / `save_threads_callback` — persistence hooks for conversation history (e.g., DB/file storage)
- **Task persistence**: Callback-based. Caller implements the persistence store.
- **Session recovery**: Via `load_threads_callback` — reload thread state from whatever store was used
- **Dispatch logging**: Not built-in. Must implement via callbacks.
- **Assessment**: Higher-level and easier than LangGraph for role-based multi-agent workflows. Less control over harness internals. Use for rapid prototyping.

### 6. Agency Swarm (VRSEN)
- **URL**: https://github.com/VRSEN/agency-swarm
- **License**: MIT
- **Harness Pattern**: Role-based agencies (CEO, Virtual Assistant, Developer etc.) built on OpenAI Assistants API. Communication via explicit directional `communication_flows`.
- **Key harness components**:
  - `Agency` — defines agent roster + `communication_flows` (directional, not free-form)
  - `send_message` tool — the only way agents communicate (no shared state)
  - `load_threads_callback` / `save_threads_callback` — session persistence hooks
  - `PersistentShellTool`, `IPythonInterpreter` — stateful tool execution
- **Task persistence**: Via save/load callbacks. Not opinionated about storage format.
- **Session recovery**: Callback-based, same as CrewAI.
- **Assessment**: Good for OpenAI Assistants-based deployments. Directional communication_flows pattern is clean. MIT. But tightly coupled to OpenAI Assistants API.

### 7. Mission Control (builderz-labs)
- **URL**: https://github.com/builderz-labs/mission-control
- **License**: MIT (self-hosted, zero external dependencies)
- **Harness Pattern**: Orchestration DASHBOARD — manages agent fleets, dispatches tasks, tracks costs, coordinates multi-agent workflows. SQLite-powered.
- **Key components**:
  - Agent fleet registration (CrewAI, AutoGen, custom via normalized adapter interface)
  - Heartbeat monitoring
  - Task dispatch queue
  - Cost tracking
  - Multi-agent coordination
- **Assessment**: This is the closest thing to a standalone harness dashboard. MIT + SQLite. If OpenBrainLM needs a management layer rather than just a harness, this is directly usable.

### 8. OPENDEV (Bui, arXiv:2603.05344)
- **URL**: Work in progress — paper only, no public repo yet
- **License**: Open-source Rust CLI (per paper, not yet released)
- **Harness Pattern**: Seven-subsystem compound AI architecture (see arXiv section below)
- **Assessment**: Most academically rigorous harness design found. Not yet available as a library.

### 9. Confucius Code Agent (arXiv:2512.10398)
- **URL**: Not a public library — academic paper
- **Harness Pattern**: Confucius Orchestrator + hierarchical memory + Architect agent for compression
- **Assessment**: Hierarchical memory and compression pattern directly applicable to OpenBrainLM. Not a standalone library.

---

## Academic Papers

### Paper 1: OPENDEV — Building AI Coding Agents for the Terminal
- **Title**: Building AI Coding Agents for the Terminal: Scaffolding, Harness, Context Engineering, and Lessons Learned
- **arXiv ID**: 2603.05344
- **Authors**: Nghi D. Q. Bui
- **Date**: March 5, 2026
- **Status**: Work in progress
- **Key Contribution**: First paper to formally define and separate "harness" from "scaffolding" for LLM agents. Provides a seven-subsystem harness architecture with named components.
- **Seven harness subsystems**:
  1. Prompt Composition Engine — assembles system prompt sections by priority
  2. Tool Registry — dispatches tool calls with MCP lazy discovery
  3. Safety System — five independent defense-in-depth layers
  4. Context Engineering — five-stage progressive compaction
  5. Memory and Session Services — JSON conversation histories with auto-save
  6. Subagent Orchestration — isolated spawning with filtered tool access
  7. Message Injection Queue — thread-safe queue for follow-up messages during execution
- **Named execution pattern**: Extended ReAct Loop — six phases: pre-check, thinking, self-critique, action, tool execution, post-processing
- **Context compaction**: Five-stage progressive compaction in Phase 0 (before thinking begins). Proactive, not reactive.
- **Session persistence**: Four stores — Config Manager, Session Manager (JSON histories), Provider Cache, Operation Log (shadow git snapshots for rollback)
- **Safety**: Five independent layers. Layer 5 = lifecycle hooks via JSON stdin protocol with exit code 2 blocking — directly mirrors OpenBrainLM's hookify pattern.
- **Relevance to OpenBrainLM**: HIGH. The seven-subsystem model maps onto OpenBrainLM layers. The hooks/safety layer validates the hookify approach. The Message Injection Queue is a new component we lack.

### Paper 2: Architecting Resilient LLM Agents
- **Title**: Architecting Resilient LLM Agents: A Guide to Secure Plan-then-Execute Implementations
- **arXiv ID**: 2509.08646
- **Authors**: Ron F. Del Rosario, Klaudia Krawiecka, Christian Schroeder de Witt
- **Date**: September 10, 2025
- **Key Contribution**: Security-focused harness design using Plan-then-Execute (P-t-E) pattern. Separating planning from execution as a defense mechanism against prompt injection.
- **Core pattern**: Planner (strategic) + Executor (tactical). Control-flow integrity = inherent security benefit.
- **Implementation blueprints** for three frameworks: LangGraph (stateful re-planning), CrewAI (declarative tool scoping), AutoGen (Docker sandboxing)
- **Key patterns**: Principle of Least Privilege, task-scoped tool access, sandboxed code execution, DAG-based parallel execution, HITL verification gates
- **Relevance to OpenBrainLM**: P-t-E = Plan Mode (Planner subagent, read-only tools) + Normal Mode (Executor, full tools). Validates OpenBrainLM's dual-mode design.

### Paper 3: The Orchestration of Multi-Agent Systems
- **Title**: The Orchestration of Multi-Agent Systems: Architectures, Protocols, and Enterprise Adoption
- **arXiv ID**: 2601.13671
- **Authors**: Apoorva Adimulam, Rajesh Gupta, Sumit Kumar
- **Date**: January 20, 2026
- **Key Contribution**: Unified framework integrating planning, policy enforcement, state management, and quality operations into a coherent orchestration layer. Documents two complementary protocols: MCP (tool/data access) + Agent2Agent (peer coordination, negotiation, delegation).
- **Relevance to OpenBrainLM**: Agent2Agent protocol (peer delegation, not just orchestrator → worker) is a pattern we haven't considered. Relevant for L3 Stigmergy layer.

### Paper 4: Confucius Code Agent
- **Title**: Confucius Code Agent: Scalable Agent Scaffolding for Real-World Codebases
- **arXiv ID**: 2512.10398
- **Date**: December 2025
- **Key Contribution**: Hierarchical memory scaffold that survives context compression. Key pattern: when context approaches threshold, an "Architect" agent activates to create structured summaries — preserving goals, decisions, TODOs, error traces — before compression occurs.
- **Memory architecture**:
  - Session hierarchy: nested directories (instance → hierarchical_memory → specific_task → notes)
  - Visibility scopes: session/entry/runnable access levels
  - Rolling window: recent messages kept uncompressed, historical sections replaced with compact abstracts
  - Note-Taking Agent: distills trajectories into structured Markdown with "hindsight notes" (failure modes + resolutions)
  - Meta-Agent: automates build-test-improve loop via evaluation-driven iteration
- **Key finding**: "success in real-world software engineering depends not only on the underlying LLM, but also on the agent scaffold"
- **Relevance to OpenBrainLM**: The Architect agent pattern (proactive compression before threshold) + hindsight notes pattern directly applicable to OpenBrainLM's consolidator agent. HIGH relevance.

### Paper 5: Multi-Agent LLM Orchestration for Incident Response
- **Title**: Multi-Agent LLM Orchestration Achieves Deterministic, High-Quality Decision Support for Incident Response
- **arXiv ID**: 2511.15755
- **Author**: Philip Drammeh
- **Date**: November 2025
- **Key Contribution**: Empirical proof that multi-agent orchestration produces deterministic, production-grade quality. 100% actionable recommendation rate vs 1.7% single-agent. Zero quality variance across 348 trials.
- **Metric introduced**: Decision Quality (DQ) — validity + specificity + correctness. A formal harness evaluation metric.
- **Relevance to OpenBrainLM**: The DQ metric is directly usable as an evaluation criterion for OpenBrainLM's verifier agent outputs.

### Paper 6: Agentic AI Architectures and Taxonomies
- **Title**: Agentic Artificial Intelligence (AI): Architectures, Taxonomies, and Evaluation of Large Language Model Agents
- **arXiv ID**: 2601.12560
- **Authors**: Arunkumar V, Gangadharan G.R., Rajkumar Buyya
- **Date**: January 2026
- **Key Contribution**: Unified taxonomy: Perception → Brain → Planning → Action → Tool Use → Collaboration. Documents industry shift to MCP + Native Computer Use as open standards replacing fixed API integrations.
- **Open challenges**: hallucination in action, infinite loops, prompt injection — all of which the harness must address.
- **Relevance to OpenBrainLM**: Taxonomy validates OpenBrainLM's 8-layer architecture maps onto the accepted academic model.

---

## Industry-Standard Harness Pattern (2026 Synthesis)

Based on all sources, the industry has converged on the following stack as of early 2026:

### Tier 1: The Durable Scaffold (survives context compaction and session restart)
All production harnesses agree this must live outside any agent's context window:

| Component | What It Is | Typical Form |
|---|---|---|
| Task queue | Authoritative list of work units with status | JSON file or SQLite DB |
| Dispatch log | Append-only log of every agent spawned | JSON file or DB table |
| Result inbox | Where workers write outputs before terminating | Directory of JSON files |
| Progress narrative | Human-readable log of what happened | Markdown or text file |
| Git history | Secondary source of truth for completed work | Git repo |

This is confirmed by: Anthropic engineering post, Agents_Arcs 156-source corpus, Gas Town (Yegge), CodeCRDT (arXiv:2510.18893), OPENDEV (arXiv:2603.05344).

### Tier 2: The Lifecycle Pattern (Initializer → Worker → Judge)
All production systems use episodic, amnesiac workers:

1. **Initializer** — reads user goal, writes task queue, writes domain memory, terminates
2. **Worker** — reads scaffold, claims ONE task (atomic), executes, writes to result inbox, terminates
3. **Refinery/Judge** — reads result inbox, resolves conflicts, merges to main branch, terminates

Confirmed by: Anthropic harness post (`feature_list.json` + two-agent system), Agents_Arcs notebook (Initializer-Worker-Judge), OPENDEV (Session Manager), Microsoft Agent Framework (WorkflowBuilder + executor nodes).

### Tier 3: The Hook Layer (PreToolUse → PostToolUse → Stop)
Production harnesses intercept at three mandatory points:

| Hook | Purpose | What it blocks/captures |
|---|---|---|
| PreToolUse | Safety + destructive action intercept | rm/DROP/--force patterns, scope violations |
| PostToolUse | Result capture + dispatch log update | Ensures results written before context expires |
| Stop/SessionEnd | Orphan detection + consolidation gate | Blocks stop if unreported agents exist |

Confirmed by: OPENDEV 5-layer safety system, Claude Agent SDK hooks API, OpenBrainLM hookify rules (partially implemented).

### Tier 4: Context Engineering (not just prompting)
OPENDEV (2603.05344) formally establishes five-stage progressive compaction as industry standard:
- Stage 0 = proactive check BEFORE thinking begins (not reactive)
- Rolling uncompressed window + compressed historical sections
- Architect/consolidator agent activates when threshold approached (not after crossing it)

Confirmed by: OPENDEV, Confucius Code Agent hierarchical memory, Agents_Arcs prefix caching discipline.

### Tier 5: The Verification Gate
Every production harness has an objective verification gate — NOT just LLM self-critique:
- Anthropic: Puppeteer MCP browser automation verifies features end-to-end
- OPENDEV: exit code 2 blocking via lifecycle hook
- arXiv:2509.08646: HITL gates for irreversible actions
- Agents_Arcs: "structurally forbids marking complete unless external test/linter passes"

### What Is NOT Yet Standardized
- Cross-session agent identity (how does a worker "know" it is a continuation of a prior worker)
- Harness observability metrics (DQ from arXiv:2511.15755 is new and not yet adopted)
- Agent2Agent protocol (arXiv:2601.13671) — peer delegation without orchestrator — nascent

---

## Recommendation for OpenBrainLM

### Build vs Buy Assessment

| Component | Decision | Rationale |
|---|---|---|
| Agent execution loop | **Use** Claude Agent SDK | SDK provides hooks, subagents, sessions. We layer on top. |
| Durable task queue | **Build** (file-based) | 3-field JSON (task_id, status, output_path). No library needed. Anthropic's own pattern. |
| Dispatch log | **Build** (file-based) | Append-only JSON. Already partially designed in existing research. |
| Result inbox | **Build** (file-based) | Directory of JSON files. Worker writes before returning. |
| Graph-based workflows | **Use** LangGraph (MIT) | Already in Phase 3 dependency list. Confirmed fastest + most flexible. |
| Checkpointing | **Use** Microsoft Agent Framework (MIT) | `FileCheckpointStorage` pattern is directly adoptable, even if not using the full SDK |
| Context compaction | **Build** consolidator agent | Architect pattern from Confucius (arXiv:2512.10398). Proactive, threshold-triggered. |
| Hook layer | **Build** (already started) | hookify rules extend to PostToolUse result capture + Stop orphan detection. |
| Observability dashboard | **Consider** Mission Control (MIT/SQLite) | If fleet management becomes a need. Not urgent for Phase 1. |

### Specific Components to Build Now (Priority Order)

1. **`memory/.harness/task_queue.json`** — Anthropic's `feature_list.json` pattern. Fields: task_id, description, status, owner, output_path, created_at, completed_at.
2. **`memory/.harness/dispatch_log.jsonl`** — Append-only JSONL. Fields: agent_id, task_id, dispatch_time, expected_output_path, result_received_at.
3. **`memory/.harness/result_inbox/`** — Workers write `[task_id]_[timestamp].json` here before terminating.
4. **PostToolUse hook extension** — Reads result_inbox after every Agent tool call. Updates dispatch_log. Blocks if result missing.
5. **Stop hook extension** — Scans dispatch_log for orphaned dispatches (dispatched but no result). Blocks stop. Then consolidates.
6. **Consolidator agent trigger** — Fires when context token count approaches 70% of limit (proactive, not reactive). Produces Architect-style summary per Confucius pattern.

### What We Already Have (Validated)
- Initializer → Worker → Judge pattern: confirmed correct by multiple sources
- hookify destructive intercept (PreToolUse): confirmed correct, needs hardening
- Memory file hierarchy (short_term → long_term → NotebookLM archival): confirmed correct
- Confidence bouncer + schema-driven verification: confirmed correct

### What Was Wrong / Updated
- "Redundancy OK" in memory discipline: **REPLACED** with schema-driven compaction (Agents_Arcs finding, confirmed by Confucius and OPENDEV)
- Context compaction should be PROACTIVE (before threshold), not reactive (after threshold): update consolidation trigger timing

---

## Citations

### GitHub Repositories
- Claude Agent SDK (Python): https://github.com/anthropics/claude-agent-sdk-python
- Claude Agent SDK (TypeScript): https://github.com/anthropics/claude-agent-sdk-typescript
- Claude Agent SDK (Demos): https://github.com/anthropics/claude-agent-sdk-demos
- Anthropic Long-Running Agent Harness (engineering post): https://www.anthropic.com/engineering/effective-harnesses-for-long-running-agents
- Claude Agent SDK Docs: https://platform.claude.com/docs/en/agent-sdk/overview
- Microsoft Agent Framework: https://github.com/microsoft/agent-framework
- Microsoft Agent Framework Docs: https://learn.microsoft.com/en-us/agent-framework/overview/
- Microsoft AutoGen → Agent Framework Migration: https://learn.microsoft.com/en-us/agent-framework/migration-guide/from-autogen/
- LangGraph: https://github.com/langchain-ai/langgraph
- LangGraph Docs: https://www.langchain.com/langgraph
- CrewAI: https://github.com/crewAIInc/crewAI
- Agency Swarm: https://github.com/VRSEN/agency-swarm
- Mission Control: https://github.com/builderz-labs/mission-control

### arXiv Papers
- arXiv:2603.05344 — OPENDEV: Building AI Coding Agents for the Terminal (Bui, March 2026)
- arXiv:2512.10398 — Confucius Code Agent: Scalable Agent Scaffolding (December 2025)
- arXiv:2509.08646 — Architecting Resilient LLM Agents: Plan-then-Execute (Del Rosario et al., September 2025)
- arXiv:2601.13671 — Orchestration of Multi-Agent Systems: Architectures and Protocols (Adimulam et al., January 2026)
- arXiv:2511.15755 — Multi-Agent LLM Orchestration for Incident Response (Drammeh, November 2025)
- arXiv:2601.12560 — Agentic AI: Architectures, Taxonomies, Evaluation (Arunkumar et al., January 2026)
- arXiv:2510.18893 — CodeCRDT: Yjs CRDT + TODO Claim Protocol (cited in concurrency research)
- arXiv:2510.04618 — Anthropic ACE paper: prompts and memory must update via execution feedback

### Prior Research in This Project
- `research/agent_harness_patterns_2026-03-24.md` — Agents_Arcs NLM (sessions 83fd9132 + 750f34a9)
- `research/concurrency_control_2026-03-24.md` — worktree isolation + Refinery merge queue
- `research/agent_handle_persistence_2026-03-24.md` — context compaction survival patterns
