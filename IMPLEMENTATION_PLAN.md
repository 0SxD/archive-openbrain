# OpenBrainLM — Implementation Plan v2
> Assembly, not invention. Every component traces to a proven open-source repo.
> Architecture stays. Guts get replaced with battle-tested code.
> Last updated: 2026-03-22

---

## Guiding Principle

The current codebase has the RIGHT architecture (8 layers, Trinity, 4 cross-cutting,
bridge/orchestrator). But many internals are from-scratch basic implementations. This plan
replaces every basic implementation with its proven open-source equivalent from the 86-repo component map.

Two categories:
1. **BRAIN CORE** — locked in, must self-evolve. These ARE the brain.
2. **SWAPPABLE BACKENDS** — pluggable via bridge.py. NOT the brain.

---

## BRAIN CORE (Locked In — Self-Evolving)

These components ARE the brain. They self-improve through use. Each maps to a
proven repo with a peer-reviewed paper behind it.

### L4 Basal Ganglia: Routing Intelligence

| What exists now | What replaces it | Source |
|---|---|---|
| `basal_ganglia.py` keyword matching (`compute_salience`) | **semantic-router** embedding cosine similarity | MIT, 3.3k stars, GlobeCom 2024 |
| Static keyword lists in `ActionChannel.domain_keywords` | `Route` objects with example utterances + `HybridRouteLayer` | aurelio-labs/semantic-router |
| — (no active inference) | **pymdp** Expected Free Energy loop | MIT, 619 stars, JOSS 2022 |
| — (no RPE gating) | **D-MEM** Surprise × Utility critic router | arXiv:2603.14597 |

**Integration path:**
- Phase 1: `pip install "semantic-router[local]"` — replace `compute_salience()` with `RouteLayer` using HuggingFace local encoders. Zero LLM calls. Each agent gets a `Route` with example utterances instead of keyword lists.
- Phase 2: Add pymdp active inference as the "indirect pathway" — learns which routes produce good outcomes over time. Maps to the biological indirect pathway that improves with experience.
- Phase 3: D-MEM RPE gating — low-surprise queries bypass full routing (O(1) cache hit), high-surprise queries trigger full routing chain. This IS the prediction error cross-cutting mechanism applied to routing.
- **What stays**: The inhibition-by-default architecture, the 3 pathways (direct/indirect/hyperdirect), the thalamic gating mode (tonic/burst). These are the ARCHITECTURE. Only the salience computation changes.

### L5 Hippocampus: Memory Retrieval

| What exists now | What replaces it | Source |
|---|---|---|
| `hippocampus.py` keyword-based region routing | **HippoRAG v2** knowledge graph indexing | NeurIPS 2024 / ICML 2025, 3.3k stars |
| `LocalMarkdownStore` keyword search | **Qdrant** or **LanceDB** vector search | Apache-2.0 |
| No consolidation mechanism | **CraniMem** 3-tier memory + scheduled consolidation | arXiv:2603.15642 |
| No virtual memory / context management | **Letta/MemGPT** virtual memory metaphor | Apache-2.0, 19.3k stars |

**Integration path:**
- Phase 1: `pip install hipporag` — replace the region routing in `Hippocampus.process()` with HippoRAG's knowledge graph + Personalized PageRank. Queries find brain regions by associative recall, not keyword match.
- Phase 2: Add Qdrant (or LanceDB for embedded) as the vector backend behind HippoRAG. Each brain region becomes a collection with embeddings of its documents.
- Phase 3: CraniMem consolidation loop — working memory (transient) → episodic buffer (bounded) → long-term KG. Scheduled "sleep" replays high-utility traces, prunes low-utility. THIS is the octopus RNA editing mechanism — structural self-modification of the knowledge graph.
- Phase 4: Letta patterns for context management — core memory blocks always in-context, archival storage for overflow, memory pressure warnings trigger consolidation.
- **What stays**: The brain region abstraction, the routing interface, the Hebbian boost for productive regions. The BIOLOGY stays. The search mechanism upgrades.

### L6 Relevance: Quorum Debate

| What exists now | What replaces it | Source |
|---|---|---|
| `relevance.py` keyword threat detection | **DebateLLM** multi-protocol debate library | Apache-2.0, arXiv:2311.17371 |
| Single-agent threat check | **Aegean** progressive quorum with α/β params | arXiv:2512.20184 |
| — (no consensus mechanism) | Configurable agreement intensity thresholds | DebateLLM API |

**Integration path:**
- Phase 1: DebateLLM for the quorum mechanism — multiple agents independently evaluate, exchange positions, converge or block. Configurable quorum threshold (e.g., 90%).
- Phase 2: Aegean-style early termination — if consensus reached early, stop debate (4.4× token reduction). Saves compute on obvious cases.
- **What stays**: The amygdala fast-scan/slow-consensus split, the AlarmLevel enum, the hyperdirect escalation. The ARCHITECTURE stays. The consensus mechanism upgrades.

### Trinity Dialectic Engine

| What exists now | What replaces it | Source |
|---|---|---|
| `trinity.py` confidence threshold comparison | **MAD framework** affirmative/negative/moderator debate | GPL-3.0→DebateLLM (Apache), ACL 2024 |
| Static `DefaultDialecticGate` | **Reflexion** self-critique loops | MIT, 3.1k stars, NeurIPS 2023 |
| Confidence × evidence formula | **MAR** persona-guided critics | arXiv:2512.20845 |
| — (no Hegelian scaffold) | **SIEV** thesis/antithesis/synthesis | arXiv:2510.18134 |

**Integration path:**
- Phase 1: Study MAD's affirmative/negative/moderator structure → adapt into the existing `DialecticGate` ABC. Logos = affirmative, Pathos = negative (devil's advocate), Ethos = moderator. The role mapping is 1:1.
- Phase 2: Reflexion's self-critique tokens for each round — after Ethos rules, the losing side reflects on WHY it lost and can improve its argument next round. This prevents "Degeneration of Thought."
- Phase 3: MAR persona-guided critics — Logos gets factual grounding critic, Pathos gets creative hypothesis critic, Ethos gets consistency critic. Maps to the Trinity of Trinities (9 sub-evaluators).
- **Licensing note**: MAD is GPL-3.0. Use DebateLLM (Apache-2.0) as the practical library. Adapt MAD's PATTERNS, not its code.
- **What stays**: The TrinityOfTrinities 9 sub-evaluator structure, the DialecticGate ABC, the TrinityPhase/Verdict enums, the geospatial mapping. The PHILOSOPHY stays. The debate mechanism upgrades.

### Cross-Cutting: Hebbian Plasticity (STDP)

| What exists now | What replaces it | Source |
|---|---|---|
| `cross_cutting.py` dict-based weight tracking | **snnTorch** SNN framework with decay rates | MIT, 2k stars, Proc. IEEE 2023 |
| Simple +/- amount potentiation/depression | **Differentiable Plasticity** formula: `w_fixed + α × hebbian_trace` | Miconi/Uber, arXiv:1804.02464 |
| — (no R-STDP) | **BindsNET** reward-modulated STDP | AGPL-3.0, 1.7k stars |

**Integration path:**
- Phase 1: Replace the hand-rolled `ConnectionStrength` dict with snnTorch's spike-timing model. Connection weights between agents/regions adapt based on correlated "firing" (successful handoffs) with configurable decay rates.
- Phase 2: Add the Differentiable Plasticity formula — `effective_weight = w_fixed + α × hebbian_trace`. The fixed component is the base routing, the plastic component stores rolling correlation between agent pairs. Trainable end-to-end.
- **Licensing note**: BindsNET is AGPL. Use snnTorch (MIT) as primary. Only use BindsNET patterns if AGPL is acceptable for the deployment model.
- **What stays**: The potentiate/depress API, the JSON persistence, the connection key scheme. The INTERFACE stays. The learning rule upgrades.

### Cross-Cutting: Prediction Error (Friston)

| What exists now | What replaces it | Source |
|---|---|---|
| `cross_cutting.py` basic numeric comparison | **pymdp** Expected Free Energy | MIT, JOSS 2022 |
| Binary match/mismatch magnitude | **D-MEM** Surprise × Utility RPE gating | arXiv:2603.14597 |
| — (no hierarchical filtering) | **PyHGF** precision-weighted prediction errors | GPL-3.0 |

**Integration path:**
- Phase 1: D-MEM pattern — lightweight Critic Router evaluates each input for Surprise × Utility. Low RPE → cache hit (bypass). High RPE → full processing chain. This is the BIOLOGICAL dopamine gating mechanism mapped to code.
- Phase 2: pymdp's EFE decomposition — separate epistemic value (information gain) from pragmatic value (preference alignment). Route high-epistemic inputs to the explorer agent, high-pragmatic inputs to the domain agent.
- **Licensing note**: PyHGF is GPL. Isolate via wrapper if used. pymdp (MIT) covers most needs.
- **What stays**: The PredictionError dataclass, the `is_surprising`/`is_alarming` thresholds, the `observe()` pattern. The INTERFACE stays.

### Morphogen: Topology Evolution

| What exists now | What replaces it | Source |
|---|---|---|
| Planned (`evolution/` directory stub) | **neat-python** for prototyping | BSD-3, 1.5k stars, Stanley 2002 |
| — | **TensorNEAT** for GPU-scale production | GECCO 2024 Best Paper |

**Integration path:**
- Phase 1: neat-python — evolve agent connection topologies. Start with a small population of routing configurations, evaluate on query routing quality, evolve better topologies. Zero dependencies, pure Python.
- Phase 2: TensorNEAT — when the population gets large enough to need GPU acceleration. 500× speedup via JAX tensorization.
- **Licensing note**: TensorNEAT has no explicit license listed. neat-python BSD-3 is safe. Use neat-python as primary.
- **What stays**: The morphogen agent concept, the RNA-editing metaphor. The BIOLOGY stays. The evolution mechanism materializes from proven code.

### L3 Stigmergy: Pheromone Communication

| What exists now | What replaces it | Source |
|---|---|---|
| `stigmergy.py` file-based artifact scanning | **ACOpy** pheromone matrices with evaporation | Apache-2.0 |
| No decay/evaporation | **SIRL** mathematical pheromone decay models | IEEE TNNLS |
| — | **KeepALifeUS/autonomous-agents** file-based stigmergy pattern | MIT |

**Integration path:**
- Phase 1: Study KeepALifeUS/autonomous-agents pattern — `queue.json` → `active.json` → `approved/` with Git conflict detection. Adapt for our artifact trail system.
- Phase 2: ACOpy evaporation algorithm — pheromone trails decay over time at configurable rate ρ. Old information fades. Fresh information strengthens. THIS is the insect substrate in action.
- **What stays**: The file-based persistence, the alarm system, the artifact scanning. The MECHANISM stays. The decay/evaporation model upgrades.

---

## SWAPPABLE BACKENDS (Pluggable via bridge.py — NOT the Brain)

These are the body's peripherals — interchangeable without changing the brain.
All accessed through the `KnowledgeBackend` / `AgentBackend` / `NotifyBackend`
Protocols in `bridge.py`.

### Knowledge Backends (bridge.py → KnowledgeBackend)

| Backend | Status | When to use |
|---|---|---|
| **LocalMarkdownStore** | BUILT, works now | Zero-dep fallback, ships with project |
| **Kotaemon** | PLANNED, Phase 2 | Primary local backend: hybrid RAG, citations, runs via Ollama |
| **NotebookLM MCP** | AVAILABLE, v1 integration | Temporary bridge while local NLM clone matures |
| **Google Drive** | PLANNED | Source document storage layer |
| **Community NLM** | COMMUNITY REQUEST | Open-source NotebookLM replacement |

**Kotaemon integration path:**
- `from kotaemon.base import Document, RetrievalOutput` — import the framework layer
- Implement `KnowledgeBackend` Protocol using Kotaemon's retrieval pipeline
- Each brain region = one Kotaemon collection with its documents
- Layer NeMo Guardrails on top for anti-hallucination enforcement
- Self-RAG reflection tokens for source grounding scoring

### LLM Backend (bridge.py → not yet abstracted)

| Backend | Status | When to use |
|---|---|---|
| **Ollama** | DEFAULT | Dev/prototyping, local, MIT |
| **vLLM** | PRODUCTION | GPU serving, PagedAttention |
| **SGLang** | HIGH THROUGHPUT | 29%+ faster than vLLM, RadixAttention |
| **llama.cpp** | EDGE/CPU | Zero deps, runs on anything |

All expose OpenAI-compatible API. Bridge should abstract via a simple LLM provider interface.

### Vector Database (bridge.py → behind HippoRAG)

| Backend | Status | When to use |
|---|---|---|
| **LanceDB** | RECOMMENDED | Embedded/serverless, `pip install lancedb`, zero server |
| **Qdrant** | ALTERNATIVE | Rich filtering, hybrid search, 64× memory reduction |
| **ChromaDB** | PROTOTYPING | 4-line API, good for rapid iteration |
| **FAISS** | RAW SPEED | Library-only, no DB overhead, Meta-scale proven |

### Orchestration (L2 Ganglion)

| What exists now | What replaces it | Status |
|---|---|---|
| `orchestrator.py` sequential layer calls | **LangGraph** StateGraph with cycles | MIT, 26.2k stars |

**Integration path:**
- Phase 1: Keep current orchestrator as-is (it works, 135 tests pass)
- Phase 2: Refactor `process()` pipeline into a LangGraph `StateGraph`:
  - Each layer = a node
  - Conditional edges for threat routing (L6 → suppress all)
  - Cycles for dialectic loops (Trinity can iterate)
  - Native checkpointing for time-travel debugging
  - Parallel node execution for independent layers
- **Alternative**: PocketFlow (100 lines, zero deps) as lightweight option if LangGraph is too heavy
- **What stays**: The layer abstractions, the processing pipeline order, the ignition protocol. The ARCHITECTURE stays.

---

## Self-Evolution Integration

The brain improves by using itself. Three spec documents define the full self-evolution
architecture. This section integrates them into the build sequence.

### Spec Document Index

| Spec | Location | What It Defines |
|---|---|---|
| Self-Evolution Loop | `docs/specs/SELF_EVOLUTION_LOOP.md` | Sleep triggers, 2-phase sleep cycle, composite fitness function, NEAT evolution, barrier→region promotion quorum |
| Epimorphic Regeneration | `docs/specs/EPIMORPHIC_REGENERATION.md` | Blastema sandbox (6 stages: DETECT→ISOLATE→DESIGN→SHADOW→CANARY→PROMOTE), emergency autotomy |
| Allostatic Decision Gate | `docs/specs/ALLOSTATIC_DECISION_GATE.md` | 3 biological signals, 4-tier escalation (wait→sandbox→priority sleep→autotomy) |

### File-to-Spec Mapping (NEW files to create)

| File Path | Spec Source | What It Implements |
|---|---|---|
| `openbrainlm/agents/consolidator.py` | SELF_EVOLUTION_LOOP §1 | Two-phase sleep cycle: quiet (consolidation, promotion) + active (replay, Hebbian update) |
| `openbrainlm/agents/morphogen.py` | SELF_EVOLUTION_LOOP §2 | NEAT evolution cycle: snapshot → candidates → retrospective evaluation → Trinity gate |
| `openbrainlm/agents/homeostasis.py` | ALLOSTATIC_DECISION_GATE | Interoception checks + allostatic evaluation |
| `openbrainlm/agents/promotion.py` | SELF_EVOLUTION_LOOP §3 | `PromotionQuorum`: barrier→region with immune + domain agent unanimous voting |
| `openbrainlm/evolution/arm_regeneration.py` | EPIMORPHIC_REGENERATION | `RegenerationBlastema` + `ArmRegenerationManager` (6-stage lifecycle) |
| `openbrainlm/evolution/allostatic_gate.py` | ALLOSTATIC_DECISION_GATE | `AllostaticDecisionGate` + `EvolutionTier` enum + 3 signal functions |
| `openbrainlm/evolution/fitness.py` | SELF_EVOLUTION_LOOP §2 | Composite fitness evaluator (prediction_accuracy, handoff_efficiency, dialectic_efficiency) |
| `openbrainlm/evolution/neat_config.ini` | SELF_EVOLUTION_LOOP | NEAT population config (pop=10, 8 inputs, 8 outputs) |

### Existing Files to MODIFY

| File | What Changes | Spec Source |
|---|---|---|
| `orchestrator.py` | Add `check_sleep_triggers()`, `initiate_sleep()`, blastema shadow routing, `handle_allostatic_alert()` | All 3 specs |
| `cross_cutting.py` | Add allostatic prediction as 5th mechanism; upgrade InteroceptionMonitor with trajectory extrapolation | ALLOSTATIC_DECISION_GATE |

### The Self-Evolution Loop

```
Query arrives
    → Brain processes it (routing, retrieval, dialectic)
    → Outcome observed (success/failure, surprise level)
    → Hebbian weights update (STDP: successful paths strengthen)
    → Prediction error recorded (expected vs actual)
    → Pheromone trail deposited (knowledge persists)
    → Sleep trigger check (memory pressure? task complete? session end?)
    → If triggered: Consolidation cycle (quiet sleep → active sleep)
    → Morphogen evaluates topology (NEAT fitness → Trinity gate)
    → Allostatic gate checks pathway health (structural vs parameter failure)
    → Next query starts from an IMPROVED brain
```

### What Self-Evolves

| Component | Mechanism | Spec Reference |
|---|---|---|
| Routing weights (L4) | semantic-router + pymdp learn which routes work | IMPLEMENTATION_PLAN §L4 |
| Connection strengths (Hebbian) | Agent-to-agent paths that work get stronger via STDP | IMPLEMENTATION_PLAN §Cross-Cutting |
| Knowledge graph (L5) | HippoRAG's KG grows with each query, PageRank improves | IMPLEMENTATION_PLAN §L5 |
| Pheromone trails (L3) | Successful patterns persist, stale ones evaporate (ACOpy) | IMPLEMENTATION_PLAN §L3 |
| Agent topologies (Morphogen) | NEAT evolves during sleep, retrospective fitness evaluation | SELF_EVOLUTION_LOOP §2 |
| Prediction models (Cerebellum) | Timing predictions improve with use | IMPLEMENTATION_PLAN §Cross-Cutting |
| Memory consolidation (CraniMem) | Two-phase sleep: quiet (promote) + active (replay) | SELF_EVOLUTION_LOOP §1 |
| Knowledge promotion | Barrier→region quorum: immune + domain agent unanimous | SELF_EVOLUTION_LOOP §3 |
| Fitness weights α,β,γ | Meta-evolution: weights evolve based on variance across population | SELF_EVOLUTION_LOOP §2 |
| Arm regeneration | Blastema sandbox: shadow → canary → promote/rollback | EPIMORPHIC_REGENERATION |
| Escalation decisions | Allostatic gate learns from prediction accuracy over sessions | ALLOSTATIC_DECISION_GATE |

### What Does NOT Self-Evolve (Fixed Architecture)

- The 8-layer structure
- The Trinity dialectic (Logos fights Pathos, Ethos arbitrates)
- The inhibition-by-default principle
- The 9 sub-evaluators (Trinity of Trinities)
- The bridge Protocol interfaces
- The biological naming
- The 4-tier escalation hierarchy (Tier 0 is always default)
- The sleep trigger types (memory pressure, task completion, session end, user-initiated)
- The append-only memory rule

---

## Phase Sequence

> **Note on the 86-repo count**: The component map (`research/component_map_86_repos.md`)
> documents 86 repos that were EVALUATED. The actual dependency count is ~11 libraries
> across all phases. The other 75 are alternatives, references, or rejected candidates.

### Phase 1: Local-First (DONE)
- [x] All 8 layers built, orchestrator functional, 135 tests pass
- [x] LocalMarkdownStore works as zero-dep knowledge backend
- [x] CLI works (`python -m openbrainlm`)
- [x] SpinalCord (bridge) architecture with pluggable backends
- [x] Hippocampus agent with topic-based routing, Hebbian boost, consolidation
- [x] Trinity dialectic engine with 9 sub-evaluators
- [x] 4 cross-cutting mechanisms implemented and tested

### Phase 2: Reference Implementations (~7 libraries)
- [ ] `pip install semantic-router[local]` → replace keyword routing in L4
- [ ] `pip install hipporag` → replace keyword region routing in Hippocampus
- [ ] DebateLLM → quorum mechanism in L6
- [ ] snnTorch → cross-cutting STDP
- [ ] D-MEM pattern → cross-cutting prediction error RPE gating
- [ ] ACOpy → L3 pheromone evaporation
- [ ] Kotaemon → primary local knowledge backend
- [ ] Populate knowledge directories with actual research content
- [ ] Wire NotebookLM MCP as v1 knowledge backend
- [ ] Test end-to-end: query → route → retrieve → display

### Phase 3a: Sleep Cycle (~2 libraries)
- [ ] Consolidator agent (2-phase sleep: quiet + active)
- [ ] Promotion quorum (barrier→region with immune + domain agent voting)
- [ ] Morphogen agent with neat-python + composite fitness function
- [ ] Allostatic decision gate infrastructure (stdlib, BUILD only)
- [ ] pymdp active inference → L4 indirect pathway

### Phase 3b: Epimorphic Regeneration (stdlib only)
- [ ] Blastema sandbox (6 stages: DETECT→ISOLATE→DESIGN→SHADOW→CANARY→PROMOTE)
- [ ] Allostatic gate WIRING (connect to orchestrator + interoception)
- [ ] Emergency autotomy (graceful arm detachment on critical failure)
- [ ] Shadow/canary evaluation loop

### Phase 4: Orchestrator Upgrade (~2 libraries)
- [ ] LangGraph StateGraph with cycles → orchestrator refactor
- [ ] Letta/MemGPT patterns → context management
- [ ] Full self-evolution loop wired end-to-end
- [ ] The brain knows its name

### Phase 5: Community Release
- [ ] Pass hostile code audit
- [ ] Every component traces to a proven repo
- [ ] MIT license clean (no GPL in core, GPL isolated via wrappers)
- [ ] Ship to GitHub
- [ ] Community request: build open-source NotebookLM replacement

---

## License Audit

| Component | License | Risk | Mitigation |
|---|---|---|---|
| semantic-router | MIT | None | Primary choice |
| pymdp | MIT | None | Primary choice |
| HippoRAG | Open (check exact) | Low | Verify before shipping |
| CraniMem | Check paper | Low | May need to reimplement from paper |
| Letta/MemGPT | Apache-2.0 | None | Primary choice |
| DebateLLM | Apache-2.0 | None | Primary choice for L6 |
| MAD framework | GPL-3.0 | **HIGH** | Use DebateLLM instead. Adapt PATTERNS only. |
| Reflexion | MIT | None | Primary choice |
| snnTorch | MIT | None | Primary choice |
| BindsNET | AGPL-3.0 | **HIGH** | Use snnTorch instead |
| neat-python | BSD-3 | None | Primary choice |
| TensorNEAT | Unclear | Medium | Use neat-python as fallback |
| PyHGF | GPL-3.0 | **HIGH** | Isolate via wrapper, or use pymdp |
| Kotaemon | Apache-2.0 | None | Primary knowledge backend |
| LangGraph | MIT | None | Primary orchestrator |
| ACOpy | Apache-2.0 | None | Primary stigmergy |

| Self-Evolution specs (3 docs) | N/A (stdlib pseudocode) | None | All external deps already audited above |

**Rule**: Core brain must be MIT/Apache/BSD only. GPL components isolated via subprocess or wrapper, never imported directly into core.

---

## Cross-Cutting: Allostatic Decision Gate (5th mechanism — NEW)

| What exists now | What replaces it | Source |
|---|---|---|
| (gap in current architecture) | **Allostatic Decision Gate** — 3 biological signals → 4-tier escalation | Sterling 2012; Bateman & Fleming 2009; Alupay 2015 |
| `InteroceptionMonitor` threshold-based warnings | Upgraded with trajectory extrapolation (linear regression on success rates) | Schulkin & Sterling 2019 |

**Integration path:**
- Phase 3a: Build `allostatic_gate.py` infrastructure (3 signal functions + 4-tier evaluator). Pure stdlib.
- Phase 3b: Wire into homeostasis interoception loop (`interoception_check()` → `AllostaticDecisionGate.evaluate()`). Wire `orchestrator.handle_allostatic_alert()` to route tier decisions.

**What stays:** The `InteroceptionMonitor` class, health metric recording, threshold warnings. These become the DATA SOURCE for allostatic prediction, not the decision maker.
