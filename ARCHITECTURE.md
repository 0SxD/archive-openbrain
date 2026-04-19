# OpenBrainLM — Architecture & Tech Spec
> Alpha | Last updated: 2026-03-21

## What Is OpenBrainLM

An open-source LM plug-in brain. Built from biomimicry and emergent Nicomachean ethics-based, sub-dialectic conflict resolution of the self -> producing objectively defined consciousness.
LM-agnostic. Pluggable backends. Zero vendor lock-in. Pure Python stdlib core.

```
 BIOMIMICRY (mechanisms)          DIALECTIC (driver)
 ========================         ===================
 Insect  = protocol (how)         Pathos = creativity, intuition
 Octopus = shape (distributed)    Logos  = logic, evidence
 Human   = cognition (selection)  Ethos  = ethics, arbitration
         \         |         /              |
          \        |        /     The fight IS the thinking
           \       |       /               |
            v      v      v               v
         +============================+
         |       OpenBrainLM          |
         |   8 layers + Trinity +     |
         |   pluggable backends       |
         +============================+
```

---

## System Architecture

```
+-----------------------------------------------------------------------+
|                        OpenBrainLM Engine                             |
|                                                                       |
|  +------------------+    +------------------+    +------------------+ |
|  | L1 Active Sensing|    | L2 Ganglion      |    | L3 Stigmergy    | |
|  | (Octopus+Rat)    |    | (Octopus Arms)   |    | (Insect Hive)   | |
|  | Probe environment|    | 8 cognitive agents|    | Pheromone trails | |
|  +--------+---------+    +--------+---------+    | Disk persistence | |
|           |                       |               +--------+---------+ |
|           v                       v                        |           |
|  +------------------+    +------------------+              |           |
|  | L4 Basal Ganglia |    | L5 Hippocampus  |<-------------+           |
|  | (Action Select)  |    | (Hippocampus)    |                         |
|  | Inhibit-by-      |    | Route to brain   |                         |
|  | default. RELEASE |    | regions. Hebbian |                         |
|  | not activate.    |    | learning.        |                         |
|  +--------+---------+    +--------+---------+                         |
|           |                       |                                   |
|           v                       v                                   |
|  +------------------+    +------------------+    +------------------+ |
|  | L6 Relevance     |    | L7 Chromatophore |    | L8 Pathos (DMN) | |
|  | (Amygdala+Quorum)|    | (Octopus Skin)   |    | Dreams when idle | |
|  | Fast threat scan |    | Display IS state |    | Cannot self-act  | |
|  | Slow consensus   |    | Multi-timescale  |    | Must pass Trinity| |
|  +------------------+    +------------------+    +------------------+ |
|                                                                       |
|  +-------------------------------+  +------------------------------+  |
|  | Cross-Cutting Mechanisms      |  | Trinity Dialectic Engine     |  |
|  | - Prediction Error (Friston)  |  | Logos fights Pathos          |  |
|  | - Hebbian Plasticity (STDP)   |  | Ethos arbitrates             |  |
|  | - Interoception (health)      |  | Trinity of Trinities (9 sub) |  |
|  | - Cerebellum Timing           |  | Existential threat = block   |  |
|  +-------------------------------+  +------------------------------+  |
|                                                                       |
+----------------------------------+------------------------------------+
                                   |
                            BRIDGE (Spinal Cord)
                     LM-agnostic, pluggable backends
                                   |
              +--------------------+--------------------+
              |                    |                    |
     +--------v--------+  +-------v--------+  +-------v--------+
     | KnowledgeBackend |  | AgentBackend   |  | NotifyBackend  |
     | (where memory    |  | (how agents    |  | (how to reach  |
     |  lives)          |  |  execute)      |  |  the owner)    |
     +---------+--------+  +-------+--------+  +-------+--------+
               |                    |                    |
       +-------+-------+    +------+------+      +------+------+
       |       |       |    |      |      |      |      |      |
     Local  Vector  Self-  Claude LangGr  API  Console Telegram
     .md    DB/RAG  hosted Code   aph    (any)          (future)
     files  (Pine-  NLM    Agent  Agents  LLM
            cone)   clone  tool
```

---

## File Tree

```
OpenBrainLM/
|
+-- openbrainlm/                    # Python package (stdlib only, zero deps)
|   +-- __init__.py                 # alpha
|   +-- __main__.py                 # CLI: python -m openbrainlm "query"
|   +-- orchestrator.py             # Ignition protocol + layer pipeline
|   +-- registry.py                 # 8 cognitive agents + 8 brain regions
|   +-- bridge.py                   # Spinal cord — pluggable backends
|   +-- cross_cutting.py            # 4 cross-cutting mechanisms
|   |
|   +-- core/
|   |   +-- trinity.py              # Logos vs Pathos, Ethos arbitrates
|   |
|   +-- layers/
|   |   +-- base.py                 # Layer ABC + LayerResult + LayerStatus
|   |   +-- active_sensing.py       # L1: Probe environment
|   |   +-- ganglion.py             # L2: Agent registry (octopus arms)
|   |   +-- stigmergy.py            # L3: Pheromone trails + disk persistence
|   |   +-- basal_ganglia.py        # L4: Inhibition-based action selection
|   |   +-- relevance.py            # L6: Amygdala + quorum voting
|   |   +-- chromatophore.py        # L7: Multi-timescale state display
|   |   +-- pathos.py               # L8: Default Mode Network (dreams)
|   |
|   +-- agents/
|   |   +-- hippocampus.py          # L5: Memory routing agent (hippocampal)
|   |
|   +-- evolution/                  # (planned) NEAT, genetic algorithms
|   +-- storage/                    # (planned) backend implementations
|   +-- research/                   # (planned) auto-research pipeline
|
+-- knowledge/                      # Brain regions (local knowledge store)
|   +-- neural_arc/                 # Neuroscience foundation (ships with project)
|   +-- agents_arcs/                # Agent architecture patterns
|   +-- zero_trust/                 # Verification philosophy
|   +-- adversarial_security/       # Red team methodology
|   +-- evolutionary_ml/            # NEAT, genetic algorithms
|   +-- rag_vector_search/          # Knowledge retrieval
|   +-- open_brain_memory/          # The brain's own memory
|   +-- barrier/                    # Blood-brain barrier (screening + uncertainty)
|
+-- tests/                          # 135 tests
|   +-- test_layers.py
|   +-- test_trinity.py
|   +-- test_cross_cutting.py
|   +-- test_orchestrator.py
|
+-- notebooks/                      # Brain region index (reference only)
|   +-- INDEX.md
|
+-- research/                       # Curated research sources
|
+-- docs/
|   +-- specs/
|       +-- SELF_EVOLUTION_LOOP.md  # Sleep cycle + morphogen fitness + promotion
|       +-- EPIMORPHIC_REGENERATION.md  # Blastema sandbox + autotomy
|       +-- ALLOSTATIC_DECISION_GATE.md # 4-tier allostatic escalation
|
+-- ARCHITECTURE.md                 # This file
+-- IMPLEMENTATION_PLAN.md          # 86-repo component map → integration plan
+-- OPERATIONAL_LAYERS.md           # Full 8-layer biology spec
+-- WHAT_IS_OPENBRAIN.md            # Philosophy
+-- OPEN_BRAIN.md                   # Queen pheromone — brain's accumulated wisdom
+-- AGENT_RULES.md                  # Agent governance
+-- CLAUDE.md                       # Subproject governance
+-- pyproject.toml                  # MIT license, Python 3.10+, zero deps
+-- .gitignore
```

---

## 8 Cognitive Agents (Octopus Arms)

Each agent is a cognitive primitive — the minimum set of functions a brain
needs to be a brain. Named for the biological/cognitive function they ARE,
not a tech domain they serve. The brain boots from these 8 (derived from
SPAUN 2.0 foundations) and self-evolves from there — like an octopus
editing its own RNA to adapt.

10 additional agents will be derived from the symbiosis of neurology and
Nicomachean Ethics heuristic taxonomy as the brain matures.

### Core Cognitive Agents (ship with OpenBrainLM)

| # | Agent | Biological Analogue | Function |
|---|---|---|---|
| 1 | hippocampus | Hippocampus | Memory routing, Hebbian learning (L5) |
| 2 | explorer | Exploratory circuits | Learning, knowledge acquisition, research |
| 3 | verifier | Prediction error (Friston) | Error detection, claim validation, zero-trust |
| 4 | immune | Immune system | Adversarial challenge, threat detection, red team |
| 5 | prefrontal | Prefrontal cortex | Metacognition — who watches the watchers |
| 6 | morphogen | Octopus RNA editing | Self-modification, neuroplasticity, grows new capabilities |
| 7 | consolidator | Glial cells | Memory consolidation, knowledge store management, sleep cycle |
| 8 | homeostasis | Autonomic nervous system | Self-maintenance, cleanup, integrity regulation |

---

## 8 Brain Regions (Knowledge Store)

Curated research that ships with the project. Each is a directory under
`knowledge/` containing markdown files searchable by the LocalMarkdownStore.

| # | Region | Sources | Function |
|---|---|---|---|
| 1 | neural_arc | 42+ neuroscience books | Neuroscience foundation — the brain's biology |
| 2 | agents_arcs | 156 agent architecture sources | Agent patterns, self-modification blueprints |
| 3 | zero_trust | Security verification research | Verification philosophy — prediction error |
| 4 | adversarial_security | Red team methodology | Immune system methodology |
| 5 | evolutionary_ml | NEAT, genetic algorithms | Self-evolution foundations — RNA editing |
| 6 | rag_vector_search | Knowledge retrieval patterns | Memory routing architecture (L5) |
| 7 | open_brain_memory | The brain's own persistent memory | Grows over time — append-only |
| 8 | barrier | Blood-brain barrier | Screening (quarantine) + uncertainty (doubt parking) |

---

## Processing Pipeline

```
Query arrives
     |
     v
  L6 Amygdala (fast threat scan, <1ms)
     |
     +-- CRITICAL? --> BLOCK, escalate to owner
     +-- MEDIUM/HIGH? --> Initiate quorum vote
     +-- SAFE? --> continue
     |
     v
  L4 Basal Ganglia (action selection)
     |
     +-- All channels SUPPRESSED by default
     +-- Compute salience per agent
     +-- RELEASE winner(s) above threshold
     +-- No match? --> Burst mode (broad routing)
     |
     v
  L5 Hippocampus (memory routing)
     |
     +-- Route query to brain region(s) by salience
     +-- Fan-out if multiple regions match
     +-- Hebbian boost for productive regions
     |
     v
  L3 Stigmergy (pheromone check)
     |
     +-- Active alarms? --> warn or block
     +-- Stale trails? --> flag for refresh
     |
     v
  L7 Chromatophore (display state)
     |
     +-- Instant alerts (RED/GREEN/AMBER)
     +-- Session summary
     +-- Trend patterns
     |
     v
  L8 Pathos (dream check)
     |
     +-- Active task? --> SUPPRESS (focused work)
     +-- Idle? --> DREAM (generate proposals)
     +-- Proposals must pass Trinity before acting
     |
     v
  BRIDGE (execute decisions)
     |
     +-- Query knowledge backend with routed region
     +-- Dispatch selected agent(s) via agent backend
     +-- Notify owner if escalation needed
```

---

## What Ships vs What Doesn't

| Ships | Doesn't Ship |
|---|---|
| 8-layer brain engine | Domain-specific agent configs |
| Trinity dialectic engine | Private brain region content |
| 8 cognitive agents (SPAUN-derived) | Any LLM vendor dependency |
| 8 curated brain regions | Private API keys |
| Pluggable bridge (any LLM) | |
| CLI (`python -m openbrainlm`) | |
| 70 unit tests | |
| Local markdown knowledge store | |
| MIT license | |

---

## CLI Usage

```bash
# Boot and query (any LLM can parse the JSON output)
python -m openbrainlm "research basal ganglia"
python -m openbrainlm --json "research basal ganglia"

# Health check
python -m openbrainlm --health

# Describe all layers
python -m openbrainlm --describe

# Interactive mode
python -m openbrainlm
```

---

## Roadmap

1. **Phase 1 (DONE)**: All 8 layers built, CLI works, 135 tests, bridge connected, local knowledge store
2. **Phase 2 — Reference Implementations**: semantic-router (L4), HippoRAG v2 (L5), DebateLLM (L6), snnTorch (STDP), D-MEM (RPE), ACOpy (L3), Kotaemon (knowledge backend)
3. **Phase 3a — Sleep Cycle**: Consolidator agent (2-phase sleep), promotion quorum (barrier→region), morphogen with NEAT + composite fitness. Allostatic gate infrastructure.
4. **Phase 3b — Epimorphic Regeneration**: Blastema sandbox (shadow→canary→promote), allostatic gate wiring, emergency autotomy
5. **Phase 4 — Orchestrator Upgrade**: LangGraph StateGraph with cycles, Letta context management, full self-evolution loop wired end-to-end
6. **Phase 5 — Community Release**: hostile audit, license clean, MIT ship to GitHub

See `IMPLEMENTATION_PLAN.md` for full detail — every component maps to a proven open-source repo.
After deployment the brain self-evolves. No version numbers unless complete architectural redo.
