# The 8-Layer Brain: Architecture, Agents, and the Component Map

> OpenBrainLM Concept Paper 4 of 4
> Architect | 2026-03-22

---

## The Question

[Doc 1](01_THE_DIALECTIC_LOOP.md) gives you adversarial verification where both sides wield shared evidence.
[Doc 2](02_THE_TRINITY_AND_MEMORY.md) gives you recursive self-checking, memory consolidation, and a sleep cycle.
[Doc 3](03_THE_SELF_LEARNING_BRAIN.md) gives you self-evolution, knowledge promotion, and live repair.

But WHERE do these mechanisms live? What is the actual brain they operate in?

This document describes the physical architecture: 8 operational layers derived from 3 biological substrates (octopus, insect hive, human), 8 cognitive agents named for the functions they ARE, 8 brain regions organized by domain, a spinal cord that makes the whole system LM-agnostic, and the component map showing how every piece builds from ~11 proven open-source dependencies selected from 86 evaluated repositories.

Nothing in it is new. Everything in it is assembled from biology that already works.

---

## Part 1: Three Substrates, One Brain

The architecture draws from three biological systems, each covering the others' weaknesses:

| Substrate | What It Provides | What It Lacks |
|---|---|---|
| **Octopus** | Distributed autonomy — 2/3 of neurons in the arms, each arm thinks independently | No long-term memory, no social coordination |
| **Insect Hive** | Collective intelligence — simple rules produce emergent complex behavior, fault tolerance | No individual reasoning, no creativity |
| **Human** | Executive planning, memory consolidation, threat detection, creativity, ethical judgment | Single point of failure, cognitive biases |

The synthesis:
- **Octopus SHAPE**: Each agent is an autonomous arm with its own ganglion (local brain). The central brain sets goals; arms figure out HOW.
- **Insect PROTOCOL**: Agents communicate through artifacts left in the environment (stigmergy), not direct messages. Decisions emerge through quorum, not command.
- **Human COGNITION**: Memory consolidation (hippocampus), action selection (basal ganglia), threat detection (amygdala), invention (default mode network).
- **Aristotle's PHILOSOPHY**: Logos and Pathos fight by wielding Ethos — the same shared evidence, the same criteria — to convince each other. The fight IS the thinking. The dialectic produces verified decisions at every layer.

---

## Part 2: The 8 Operational Layers

Each layer is derived from a real biological mechanism. They are stacked bottom-to-top, from sensing to dreaming:

```
┌─────────────────────────────────────────────────────────────────┐
│  L8   PATHOS LAYER (Default Mode Network — Human)               │
│       Background invention. Dreams but cannot act.              │
├─────────────────────────────────────────────────────────────────┤
│  L7   CHROMATOPHORE LAYER (Skin Display — Octopus)              │
│       Real-time state visualization. Instant feedback.          │
├─────────────────────────────────────────────────────────────────┤
│  L6   RELEVANCE DETECTION (Amygdala + Quorum — Human + Insect)  │
│       2-stage: fast crude alarm → slow accurate consensus.      │
├─────────────────────────────────────────────────────────────────┤
│  L5   MEMORY LAYER (Hippocampus + Prefrontal — Human)           │
│       3-tier consolidation: working → short-term → long-term.   │
├─────────────────────────────────────────────────────────────────┤
│  L4   ACTION SELECTION (Basal Ganglia + Thalamus — Human)       │
│       Inhibition-based routing. Default = suppress all.         │
│       Actions are RELEASED, not activated.                      │
├─────────────────────────────────────────────────────────────────┤
│  L3   STIGMERGY + SWARM (Pheromones + Emergence — Insect)       │
│       Communicate through artifacts. Simple rules → complexity. │
├─────────────────────────────────────────────────────────────────┤
│  L2   GANGLION LAYER (Arm Autonomy — Octopus)                   │
│       Each agent has its own local brain. Acts independently.   │
├─────────────────────────────────────────────────────────────────┤
│  L1   ACTIVE SENSING (Self-Discovery — Octopus + Rat Whiskers)  │
│       Active probe, not passive receive. Discover, don't assume.│
└─────────────────────────────────────────────────────────────────┘

Cross-cutting mechanisms (not layers — they permeate everything):
  ◆ Prediction Error Filter (Friston) — route based on surprise
  ◆ Hebbian Plasticity (STDP) — connection strengths adapt over time
  ◆ Interoception — system health monitoring
  ◆ Cerebellum Timing — predictive scheduling
```

### Layer-by-Layer

**L1 — Active Sensing (Octopus + Rat Whiskers)**
Octopuses lack proprioception — each arm must discover its environment through touch and chemoreception every time. Rats use active whisking at 5-15 Hz, MOVING their whiskers to probe. Both strategies: active probe, not passive receive. In OpenBrainLM, every agent session starts with a mandatory boot: read governance, read assigned brain regions, scan the working directory. The codebase IS the ground truth, not memory of it.

**L2 — Ganglion Layer (Octopus)**
Two-thirds of an octopus's ~500 million neurons are in the arms, not the central brain. Each arm has its own ganglion that processes sensory input and executes motor commands locally. Arms continue operating even when severed. In OpenBrainLM, each of the 8 cognitive agents IS a ganglion — self-contained with its own expertise and assigned brain regions. The orchestrator says WHAT; the agent decides HOW.

**L3 — Stigmergy + Swarm (Insect Hive)**
Ants communicate through stigmergy — modifying the environment to signal others. Pheromone trails, nest architecture, food caches. The mechanism that enables communication IS the mechanism that enables emergence. In OpenBrainLM, agents don't message each other directly. They leave artifacts: research reports (trail pheromone), memory entries (nest pheromone), audit reports (alarm pheromone), OPEN_BRAIN.md entries (queen pheromone). Trails decay — research older than 1 month triggers refresh. Complex behavior emerges from 5 simple rules each agent follows.

**L4 — Action Selection (Basal Ganglia + Thalamus)**
The basal ganglia selects actions through INHIBITION, not excitation. The default state: the GPi inhibits ALL actions through tonic firing. An action is selected when the direct pathway RELEASES inhibition on that specific action. Three pathways: Direct (Go — release one action), Hyperdirect (Global Stop — suppress everything), Indirect (No-Go — selective suppression with feedback). In OpenBrainLM, all agent channels are suppressed by default. Each channel computes a salience score; channels compete via mutual inhibition; only the winner gets released. If threat is detected, the hyperdirect pathway fires and ALL channels are re-suppressed.

**L5 — Memory Layer (Hippocampus)**
The hippocampus converts short-term memories into long-term storage during sleep, replaying experiences, deciding what to keep, and strengthening important connections. Three tiers: working memory (current session), short-term buffer (until next sleep), long-term storage (permanent, append-only). The consolidation cycle, Hebbian connection strengths, and knowledge promotion all operate here. See [Doc 2](02_THE_TRINITY_AND_MEMORY.md) for the full memory architecture and [Doc 3](03_THE_SELF_LEARNING_BRAIN.md) for the promotion protocol.

**L6 — Relevance Detection (Amygdala + Quorum)**
Two-stage pipeline. Stage 1 (amygdala): the immune agent sees every plan before execution, fires on unverified claims or destructive actions — fast, crude, high false-positive rate (by design — better to block and verify). Stage 2 (quorum): minimum 2 agents evaluate independently; the immune agent MUST be one of them. Absolute threshold, not majority: unanimous for CRITICAL actions, 2/3 for HIGH. This maps to the honeybee quorum sensing mechanism where 10-15 scout bees must independently verify a site before the swarm commits (Seeley, 2010).

**L7 — Chromatophore Layer (Octopus)**
Octopus chromatophores are pigment cells that expand or contract in milliseconds. The display IS the state — you don't ask the octopus how it feels; you can see it. Multi-timescale: chromatophores (instant alerts), iridophores (session summaries), leucophores (trend lines). In OpenBrainLM, the chromatophore layer renders which agents are active, which brain regions were accessed, barrier occupancy, connection strength heatmaps, and audit status.

**L8 — Pathos Layer (Default Mode Network)**
The DMN activates when the brain is NOT focused on external tasks — daydreaming, mind-wandering, future planning. It's where creativity happens: connecting unrelated memories, seeing cross-domain patterns, imagining possibilities. In OpenBrainLM, Pathos runs during idle time. It can notice connections and propose improvements. But it CANNOT act — every proposal must pass through the dialectic where Logos wields the same shared Ethos to challenge the proposal, and Pathos wields it back to defend. Only VERIFIED proposals become actionable.

### The 4 Cross-Cutting Mechanisms

These are not layers — they operate ACROSS all 8 layers simultaneously:

| Mechanism | Biology | What It Does |
|---|---|---|
| **Prediction Error** (Friston) | Free energy minimization | Each layer predicts what it expects to observe. When reality diverges, the surprise magnitude determines routing: low → routine, medium → flag, high → suppress and investigate |
| **Hebbian Plasticity** (STDP) | "Neurons that fire together wire together" | Connection strengths between agents adapt: successful handoffs strengthen the path, rejected handoffs weaken it. Spike-timing-dependent: the ORDER matters |
| **Interoception** | Internal body sensing | Continuous monitoring: context utilization, token budget, agent availability, memory pressure, research staleness |
| **Cerebellum Timing** | Predictive motor scheduling | Track agent execution times, build timing models, trigger consolidation before memory pressure forces it |

---

## Part 3: The 8 Cognitive Agents

Every agent is named for the biological/cognitive function it IS — not a tech domain it serves. These are cognitive primitives, the bare minimum for a brain to be a brain:

| Agent | Biological Analogue | Function | Brain Regions |
|---|---|---|---|
| **hippocampus** | Hippocampus | Memory routing — routes queries to brain regions by semantic salience, Hebbian learning strengthens productive paths | open_brain_memory |
| **explorer** | Exploratory circuits | Learning — discovers, researches, synthesizes new knowledge from external sources | neural_arc, rag_vector_search |
| **verifier** | Prediction error (Friston) | Error detection — zero-trust claim validation, checks if what the brain believes is true | zero_trust |
| **immune** | Immune system | Adversarial challenge — red team, hostile twin, attacks every plan and finds weaknesses | adversarial_security, barrier |
| **prefrontal** | Prefrontal cortex | Metacognition — who watches the watchers, audits the verifier, audits the immune system | zero_trust |
| **morphogen** | Octopus RNA editing | Self-modification — builds new agents, modifies architecture, evolves the brain during sleep | agents_arcs, evolutionary_ml |
| **consolidator** | Glial cells | Memory consolidation — manages long-term storage, promotes verified knowledge, handles sleep cycle | open_brain_memory |
| **homeostasis** | Autonomic nervous system | Self-maintenance — cleanup, deduplication, integrity checks, the brain's autonomic regulation | — |

The central brain (orchestrator) sets goals and dispatches. It is not an agent — it is the ignition protocol that wires the ganglia, channels, and memory regions together.

10 additional agents will be derived from the symbiosis of neurology and Nicomachean Ethics heuristic taxonomy as the brain matures.

---

## Part 4: The 8 Brain Regions

Long-term memory is organized into brain regions — curated knowledge stores organized by domain, not by date or file type. The hippocampus agent routes queries to regions by semantic salience, not keyword match. Hebbian learning makes this better over time: regions that produce useful results for a query type get stronger connections.

| Region | Name | What Lives Here | Primary Agents |
|---|---|---|---|
| **neural_arc** | Neural_ARC | Neuroscience foundations — brain anatomy, biomimicry, consciousness, SPAUN, octopus biology | explorer, hippocampus |
| **agents_arcs** | Agents / Arcs | Agent architecture patterns — multi-agent orchestration, context engineering, self-modification | morphogen, prefrontal |
| **zero_trust** | Zero Trust Architecture | Verification philosophy — zero trust, evidence requirements, prediction error, audit methodology | verifier, prefrontal |
| **adversarial_security** | Adversarial Security / Immune | Red team methodology — threat models, attack vectors, hostile review, defense patterns | immune, verifier |
| **evolutionary_ml** | Evolutionary ML | Self-evolution foundations — NEAT, neuroevolution, genetic algorithms, RNA editing, fitness functions | explorer, morphogen |
| **rag_vector_search** | RAG / Vector Search | Knowledge retrieval architecture — embeddings, vector databases, semantic search, knowledge graphs | explorer |
| **open_brain_memory** | Open Brain Long-Term Memory | The brain's own persistent memory — consolidated knowledge, episodic records, connection strengths | consolidator, hippocampus |
| **barrier** | Blood-Brain Barrier | Screening and uncertainty staging — quarantine for unverified input, doubt parking lot | immune |

The append-only rule applies: knowledge is never deleted. When superseded, the new entry is added with a reference to what it replaces. The old entry stays. Deletion creates invisible knowledge gaps — if you delete something that was wrong, you also delete the record that you once believed it was right.

---

## Part 5: The Spinal Cord — LM-Agnostic by Design

The bridge (`bridge.py`) is the spinal cord: it doesn't make decisions — it relays them. The brain decides WHAT to do through the dialectic and the 8 layers. The spinal cord executes HOW.

Three pluggable backends make the entire system LM-agnostic:

```
┌──────────────────────────────────────────────────────────────┐
│                      BRAIN (decision engine)                  │
│    Trinity Dialectic + 8 Layers + 8 Agents + 8 Regions       │
├──────────────────────────────────────────────────────────────┤
│                     SPINAL CORD (bridge.py)                   │
│    Protocol interfaces — the brain never knows what's below  │
├──────────────────┬──────────────────┬────────────────────────┤
│  KnowledgeBackend│  AgentBackend    │  NotifyBackend         │
│  ─────────────── │  ─────────────── │  ─────────────────     │
│  LocalMarkdown   │  StubAgent       │  ConsoleNotifier       │
│  VectorStore     │  LLMDispatcher   │  TelegramNotifier      │
│  Kotaemon        │  GraphDispatcher │  (Slack, Discord, ...) │
│  (any via Proto) │  (any via Proto) │  (any via Protocol)    │
└──────────────────┴──────────────────┴────────────────────────┘
```

**KnowledgeBackend** — where the brain stores and retrieves knowledge. Default: `LocalMarkdownStore` (open source, works offline, zero dependencies). Future: Kotaemon for document Q&A with embeddings, vector databases, or any system via the Protocol interface.

**AgentBackend** — how the brain dispatches agents. Default: `StubAgentBackend` (standalone, no LLM required). Future: any LLM API (provider-agnostic), or any graph orchestrator (LangGraph, CrewAI, etc.).

**NotifyBackend** — how the brain communicates with the owner. Default: `ConsoleNotifier`. Future: Telegram, Slack, Discord, email.

The brain doesn't know or care which backends are active. It sends decisions through the spinal cord. The spinal cord adapts. This means: the same brain architecture runs with a local markdown store on a laptop, or with a GPU-accelerated vector database in the cloud, or with any LLM from any provider. The brain is the brain. The spinal cord is the interface.

---

## Part 6: The Component Map — Assembly, Not Invention

86 open-source repositories were evaluated across all 8 layers and cross-cutting mechanisms. The architecture builds from approximately **11 actual dependencies** — the other 75 are evaluated alternatives, fallback options, or rejected candidates.

### Brain Core (Locked In — Must Self-Evolve)

These are the parts that ARE the brain — not swappable, they self-improve through the evolution mechanisms described in [Doc 3](03_THE_SELF_LEARNING_BRAIN.md):

| Component | Primary Tool | License | Paper |
|---|---|---|---|
| **L4 Routing** (direct pathway) | semantic-router | MIT | Manias et al., IEEE GlobeCom 2024 |
| **L4 Routing** (indirect pathway) | pymdp (active inference) | MIT | JOSS 2022, arXiv:2201.03904 |
| **L5 Memory Retrieval** | HippoRAG v2 | Open | NeurIPS 2024, ICML 2025 |
| **L5 Consolidation** | CraniMem + Letta | Apache-2.0 | arXiv:2603.15642, arXiv:2310.08560 |
| **L6 Quorum** | DebateLLM + Aegean pattern | Apache-2.0 | arXiv:2311.17371, arXiv:2512.20184 |
| **L8 Trinity Dialectic** | MAD framework patterns | GPL-3.0 (isolated) | ACL 2024 |
| **Hebbian Plasticity** | snnTorch (STDP) | MIT | Proceedings of the IEEE 2023 |
| **Morphogen Evolution** | neat-python → TensorNEAT | BSD-3 | Stanley & Miikkulainen 2002, GECCO 2024 |
| **Prediction Error** | D-MEM (RPE gating) | — | arXiv:2603.14597 |

### Swappable Backends (Pluggable via Spinal Cord)

These are NOT the brain — they are infrastructure that the brain uses through the bridge:

| Component | Primary Tool | License | Purpose |
|---|---|---|---|
| **Knowledge Backend** (default) | LocalMarkdownStore | MIT (built-in) | Keyword search, zero dependencies |
| **Knowledge Backend** (Phase 2) | Kotaemon | Apache-2.0 | Document Q&A with embeddings |
| **Vector Database** | Qdrant / LanceDB | Apache-2.0 | Embedding storage for brain regions |
| **LLM Serving** (local) | Ollama → vLLM/SGLang | MIT/Apache-2.0 | Local inference |
| **Orchestration** (Phase 4) | LangGraph | MIT | Stateful graph with cycles and checkpoints |
| **Context Management** | Letta/MemGPT | Apache-2.0 | Virtual memory metaphor for context |

### License Policy

Core brain = MIT, Apache-2.0, or BSD-3 only. No exceptions.

Three evaluated tools carry GPL-3.0 licenses: MAD (debate framework), BindsNET (spiking networks), and PyHGF (hierarchical Gaussian filters). These are isolated via wrapper — never imported directly into core code. For each, a permissive-licensed alternative exists:
- MAD → DebateLLM (Apache-2.0) for the core debate protocol
- BindsNET → snnTorch (MIT) for Hebbian plasticity
- PyHGF → pymdp (MIT) for prediction error signals

---

## Part 7: How a Query Flows Through the Brain

Here is a concrete example — "Research a new capability" — showing all 8 layers and the dialectic in action:

```
L1  Agent boots, actively probes environment
    (octopus arm tasting — active sensing, not passive receive)

L2  Explorer ganglion evaluates the domain independently
    (arm autonomy — the central brain said WHAT, the arm decides HOW)

L3  Explorer leaves artifact: research/capability_evaluation.md
    (stigmergy — trail pheromone, "I found something here")

L4  Basal ganglia computes salience scores across all channels
    Verifier channel wins → inhibition released
    Thalamus gates explorer's artifact to verifier
    (inhibition-based selection — default was suppress all)

L6  Stage 1: Immune agent (amygdala) fast-scans the claims
    Stage 2: Verifier + immune both evaluate independently
    Both must approve — quorum requires unanimity
    (2-stage relevance: fast crude alarm → slow accurate consensus)

L5  If approved: hippocampus routes to the right brain region
    Hebbian weight for explorer→verifier path increases
    (memory consolidation + connection strengthening)

L7  Chromatophore displays: new knowledge VERIFIED, stored in neural_arc
    (real-time state visualization — the display IS the state)

L8  During idle time, Pathos notices a connection between this
    new knowledge and something in evolutionary_ml
    Pathos proposes the connection →
      Logos wields Ethos: "Where's the evidence for this link?"
      Pathos wields Ethos: "The evidence is in the shared citations"
      Ethos rules: which side's use of the evidence is stronger?
    If VERIFIED → new cross-domain insight is stored
    (background invention, verified before it can act)
```

---

## Part 8: The Phase Sequence

The architecture ships in phases, each building on the last:

| Phase | Name | What Ships |
|---|---|---|
| **1** | Local-First | **DONE.** 8 layers, 8 agents, 8 regions, CLI, 135 tests, bridge, LocalMarkdownStore. Zero external dependencies. |
| **2** | Reference Implementations | Replace basic implementations with proven libraries: semantic-router (L4), HippoRAG v2 (L5), DebateLLM (L6), snnTorch (STDP), D-MEM (RPE), ACOpy (L3), Kotaemon (knowledge backend). |
| **3a** | Sleep Cycle | Consolidator agent (2-phase sleep), promotion quorum (barrier→region), morphogen with NEAT + composite fitness. **The brain sleeps and wakes up better.** |
| **3b** | Epimorphic Regeneration | Blastema sandbox (shadow→canary→promote), allostatic decision gate (4-tier escalation), emergency autotomy. **The brain repairs itself while awake.** |
| **4** | Orchestrator Upgrade | LangGraph StateGraph with cycles, Letta context management, full self-evolution loop wired end-to-end. **The brain knows its name.** |
| **5** | Community Release | Hostile audit, license clean, MIT ship, GitHub. |

Phase 1 alone gives you a working brain with verified decisions, memory, and the dialectic. Each subsequent phase adds biological capability — sleep, evolution, regeneration, self-awareness — but the architecture works at every stage.

---

## What Self-Evolves vs What Doesn't

| Evolves | Does NOT Evolve |
|---|---|
| Agent→agent connection weights (Hebbian STDP) | The 8 core agents themselves |
| Which agents connect to which | The 8-layer structure |
| Routing weights and thresholds (semantic-router + pymdp) | The Trinity dialectic (Logos fights Pathos, Ethos arbitrates) |
| Pheromone trails (successful patterns persist, stale ones evaporate) | The inhibition-by-default principle |
| Agent topologies during sleep (NEAT evolution) | The 9 sub-evaluators (Trinity of Trinities) |
| Knowledge graph (HippoRAG's KG grows with each query) | The sleep/wake cycle |
| Prediction models (cerebellum timing improves) | The append-only memory rule |
| Fitness function weights α, β, γ (meta-evolution) | The bridge Protocol interfaces |
| Memory consolidation (CraniMem 2-phase sleep) | The 4 cross-cutting mechanism types |
| Knowledge promotion (barrier → region quorum) | The biological naming convention |

The core agents are the **genome** — fixed like the octopus's body plan. What evolves is how they **wire together** — like the octopus editing its RNA to change how neurons connect, not which neurons exist.

---

## Why This Architecture

Every LLM system today is one of three things: a chatbot (single agent, no memory), a pipeline (agents in sequence, no feedback), or a committee (agents vote, no adversarial tension). None of them have:

1. **Adversarial verification** where both sides wield the same evidence (Dialectic Loop)
2. **Recursive self-checking** that catches the checker's blind spots (Trinity of Trinities)
3. **Persistent memory** that consolidates during sleep, not during active processing (Hippocampal model)
4. **Self-evolution** where the brain that wakes up has better wiring than the brain that went to sleep (NEAT + morphogen)
5. **Knowledge gatekeeping** where nothing enters the brain without adversarial challenge AND domain verification (Blood-brain barrier)
6. **Live self-repair** where the system grows replacement components while continuing to operate (Blastema sandbox)
7. **Inhibition-based routing** where the default is suppress-all and actions must be released (Basal ganglia)
8. **Artifact communication** where complex behavior emerges from simple rules without central coordination (Stigmergy)

None of these mechanisms are invented. Every one is derived from biology that already works — octopus distributed processing, insect stigmergy, hippocampal consolidation, basal ganglia inhibition, RNA editing, blastema regeneration, blood-brain barrier gatekeeping — and from philosophy that already works — Aristotle's productive tension between creativity and rigor, where both sides must wield the same evidence to convince the other.

The framework scales from simple research verification (just the dialectic loop) all the way to building consciousness (all four layers together). The same pattern at every level. What changes is the stakes, the evidence depth, and how many layers of self-checking you need.

Nothing in it is new. Everything in it works.

---

> Sources:
> - Eliasmith, C. (2013), *How to Build a Brain*, Oxford University Press (SPAUN 2.0)
> - Aristotle, *Nicomachean Ethics*, Books I-II, VI (~350 BCE)
> - Stanley, K.O. & Miikkulainen, R. (2002), "Evolving Neural Networks through Augmenting Topologies," *Evolutionary Computation*
> - Friston, K. (2010), "The free-energy principle: a unified brain theory?" *Nature Reviews Neuroscience*
> - Seeley, T.D. (2010), *Honeybee Democracy*, Princeton University Press
> - Hebb, D.O. (1949), *The Organization of Behavior*
> - Liscovitch-Brauer et al. (2017), "Trade-off between Transcriptome Plasticity and Genome Evolution in Cephalopods," *Cell*
> - Bhowmick, S. (2021), *Bio-Inspired Swarm Robotics*, stigmergy formalization
> - Sterling, P. (2012), "Allostasis: A model of predictive regulation," *Physiology & Behavior*
> - LeDoux, J. (1996), *The Emotional Brain* — amygdala dual-pathway model
> - Raichle, M.E. (2001), "A default mode of brain function," *PNAS*
> - Full component map: 86 repos evaluated, ~11 dependencies — see `research/component_map_86_repos.md`
> - Implementation: OpenBrainLM (MIT License)
