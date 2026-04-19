# OpenBrainLM — Operational Layers v2 (Corrected 8-Layer Architecture)
> "An insect hive mind in the shape of an octopus"
> Each layer is derived from a real biological mechanism. Nothing invented. Everything assembled.
> v2: Corrected from 10 → 8 layers based on Eliasmith (2013), adversarial audit, and Aristotle's Ethics.
> Merges: L3+L5 → Stigmergy+Swarm, L4+BG → Action Selection, L7+L8 → Relevance Detection.
> Adds: 4 cross-cutting mechanisms (not layers).

---

## Layer Map (Bottom → Top)

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

---

## L1 — ACTIVE SENSING (Octopus + Rat Whiskers)

**Biology:** Octopuses lack proprioception — they don't have an internal map of where their arms are. Each arm must discover itself and its environment through touch and chemoreception every time. Rats use active whisking (not passive touch) — they MOVE their whiskers to probe, sweeping 5-15 Hz to build spatial maps. Both strategies: active probe, not passive receive.

**Principle:** Don't assume you know. Actively probe. The environment is the ground truth, not your memory of it.

**Source:** Eliasmith (2013), Ch 7 — SPAUN visual input hierarchy actively processes, not passively receives.

**OpenBrainLM Implementation:**
- Every agent session starts with a mandatory 3-step boot:
  1. Read governance files (CLAUDE.md, AGENT_RULES.md, OPEN_BRAIN.md)
  2. Read assigned brain region(s) — actively query, don't assume contents
  3. Scan working directory for current state (git status, file listing, recent changes)
- Agents do NOT carry forward assumptions from previous sessions
- Like the octopus arm tasting and the rat whisker probing: agents read before writing, always
- The codebase IS the ground truth, not memory of the codebase
- OPEN_BRAIN.md is loaded into EVERY brain region — each arm tastes the whole organism

**What this replaces:** Agents that assume they know the project state and skip reading current files.

**Existing components:** CLAUDE.md (read-first rule), MEMORY.md (re-loaded each session), agent definitions specifying "read before writing."

---

## L2 — GANGLION LAYER (Octopus)

**Biology:** 2/3 of an octopus's ~500 million neurons are in the arms, not the central brain. Each arm has its own ganglion that processes sensory input and executes motor commands locally. The central brain sets goals; arms figure out HOW. Arms can continue operating even when severed from the brain.

**Principle:** Push intelligence to the edge. The center says WHAT, the periphery decides HOW.

**Source:** Eliasmith (2013), Ch 7 — SPAUN's cortical modules (visual, motor, working memory) each have independent processing, coordinated by basal ganglia selection (L4).

**OpenBrainLM Implementation:**
- Each of the 8 cognitive agents IS a ganglion — self-contained with its own expertise, tools, and assigned brain regions
- The orchestrator sets goals: "research basal ganglia inhibition models"
- The agent (explorer) decides HOW: which papers to read, which queries to run, what to cite
- Agents are NOT puppets. They have autonomy within their domain.
- Each agent's `.md` definition file = its ganglion firmware
- Agent response thresholds: each ganglion has a "preferred direction" (NEF tuning curve) — it fires most strongly for queries in its domain

**Agent-to-Ganglion Mapping (8 core cognitive agents):**
| Ganglion (Arm) | Agent | Biological Analogue | Brain Regions |
|---|---|---|---|
| Arm 1 — Memory | hippocampus | Hippocampus | open_brain_memory |
| Arm 2 — Learning | explorer | Exploratory circuits | neural_arc, rag_vector_search |
| Arm 3 — Validation | verifier | Prediction error (Friston) | zero_trust |
| Arm 4 — Defense | immune | Immune system | adversarial_security, barrier |
| Arm 5 — Oversight | prefrontal | Prefrontal cortex | zero_trust |
| Arm 6 — Evolution | morphogen | Octopus RNA editing | agents_arcs, evolutionary_ml |
| Arm 7 — Storage | consolidator | Glial cells | open_brain_memory |
| Arm 8 — Health | homeostasis | Autonomic nervous system | — |
| Central Brain | orchestrator | Goal-setting, dispatch | OPEN_BRAIN.md |

10 more agents will be derived from neurology + Nicomachean Ethics taxonomy.

**What this replaces:** Monolithic agents that try to do everything. Each arm does one thing well.

---

## L3 — STIGMERGY + SWARM (Insect — merged from original L3 + L5)

**Biology:** Ants communicate through stigmergy — modifying the environment to signal others. Pheromone trails, nest architecture, food caches. The SAME mechanism that enables communication (stigmergy) IS the mechanism that enables emergence (swarm intelligence). These were never separate biological systems — they are one system.

**Why merged:** The original architecture split swarm (L3) and stigmergy (L5) as separate layers. But in biology, stigmergy IS how swarm intelligence works. An ant colony's emergent intelligence is BECAUSE of pheromone communication. Splitting them was artificial.

**Principle:** Simple rules + artifact communication → emergent complex behavior. No central coordinator needed.

**Source:** Bhowmick (2021), Ch 6 — stigmergy communication strategies, neural architecture mapping. Seeley (2010) — honeybee democracy, collective decision-making.

**OpenBrainLM Implementation:**

**Stigmergy (how agents communicate):**
- Agents don't message each other directly. They leave artifacts:
  - Research reports in `research/` = trail pheromone ("I found something here, follow this path")
  - Memory entries in `memory/` = nest pheromone ("This is home territory, remember this")
  - Brain region entries = food caches
  - Log entries in `logs/` = scent marks
  - Audit reports = alarm pheromone ("Danger, unverified, don't trust yet")
  - OPEN_BRAIN.md entries = queen pheromone ("This is important, more agents should know")
- Stronger trails (more artifacts, higher quality) attract more agent attention
- Trails DECAY: research >1 month old triggers refresh (evaporation rate ≈ 1 month)

**Pheromone Taxonomy (formalized):**
| Pheromone Type | Artifact | Decay Rate | Conflict Resolution |
|---|---|---|---|
| Trail | `research/*.md` | 1 month | Stronger trail (more citations) wins |
| Alarm | Quarantine Layer entries | Until verified or 2 weeks | Newest alarm supersedes |
| Nest | `memory/*.md` | Persistent (update, never delete) | Explicit override only |
| Queen | `OPEN_BRAIN.md` | Persistent | Owner override only |
| Recruitment | Task signals, background agent dispatch | Session-scoped | Priority queue |

**Swarm (how complex behavior emerges):**
- Each agent follows 5 universal swarm rules:
  1. Read before writing (active sensing, L1)
  2. Cite every claim (trail pheromone)
  3. If uncertain, quarantine — don't act (alarm pheromone)
  4. Leave artifacts for the next agent (stigmergy)
  5. Never modify another agent's domain without coordination
- Complex behavior emerges from these simple rules:
  - explorer writes findings → consolidator ingests → immune verifies → prefrontal audits the verification
  - No single agent orchestrated this chain. Each follows its own rules.

**What this replaces:** Separate swarm and stigmergy layers. Also replaces any need for direct agent-to-agent messaging.

---

## L4 — ACTION SELECTION (Basal Ganglia + Thalamus — Human)

**Biology:** The basal ganglia is the brain's action selector, NOT through excitation but through INHIBITION. The default state: the GPi (Globus Pallidus internal) INHIBITS all actions through tonic firing. An action is selected when the direct pathway (striatum → GPi) RELEASES inhibition on that specific action. Three pathways:
1. **Direct** (Go): Striatum inhibits GPi → GPi stops inhibiting thalamus → action released
2. **Hyperdirect** (Global Stop): STN excites GPi → GPi inhibits ALL actions → everything suppressed
3. **Indirect** (No-Go): Striatum → GPe → STN → GPi → selective suppression, feedback loop

The thalamus then GATES information flow: once an action is released from suppression, the thalamus routes signals between cortical areas.

**Principle:** Default = everything suppressed. Actions are RELEASED from inhibition, not activated. This is fundamentally safer than an activation model — nothing happens unless explicitly released.

**Source:** Eliasmith (2013), Ch 5 — basal ganglia action selection in SPAUN. Stewart, Choo, & Eliasmith (2010) — spiking neuron implementation of BG.

**Why this is THE missing piece (from adversarial audit):** The original L4 was pure routing (thalamic relay). But routing without selection is just a switch — it doesn't decide WHAT to route. The basal ganglia model adds the selection mechanism: competing actions mutually inhibit each other, and only the winner gets released.

**OpenBrainLM Implementation:**

**The inhibition model:**
```
Default state: ALL agent channels are SUPPRESSED (GPi tonic inhibition)

When a query arrives:
1. Each agent channel computes a "salience" score (how relevant is this to me?)
2. Channels with salience above threshold enter the DIRECT pathway (request release)
3. Channels compete via mutual inhibition (only one winner)
4. Winner's inhibition is released → thalamus gates information to that agent
5. If threat detected: HYPERDIRECT pathway fires → ALL channels re-suppressed → escalate to L6

Burst mode (novel/surprising input):
  - Thalamus fires in BURST mode → broader routing, more agents activated
  - Used for novel queries where the right agent is uncertain

Tonic mode (routine/familiar input):
  - Thalamus fires in TONIC mode → precise routing, single agent
  - Used for routine queries with clear domain match
```

**Routing Rules (via released inhibition):**
| Signal Type | Released Channel | Mode |
|---|---|---|
| "Research X" | explorer | Tonic (familiar) |
| "Verify claim Y" | verifier | Tonic |
| Novel cross-domain query | Multiple agents | Burst |
| "Check for threats" | immune → prefrontal | Tonic chain |
| "Modify architecture" | SUPPRESSED (requires L6 quorum to release) | Hyperdirect block |
| "I doubt X" | Barrier (direct to screening) | Tonic bypass |

**Computational implementation (from research):**
- Phase 1: Use `semantic-router` (Aurelio AI, MIT) for embedding-based salience scoring
- Phase 2: PyMDP (active inference POMDP) for learned routing that improves over time
- Phase 3: Full R-GCN (typed-edge graph convolution) for relational routing

**What this replaces:** Ad-hoc routing. The inhibition model ensures NO action happens by default — every action requires explicit release. This is architecturally safer than an activation model.

---

## L5 — MEMORY LAYER (Hippocampus + Prefrontal — Human)

**Biology:** The hippocampus converts short-term memories into long-term storage during sleep. It replays the day's experiences, decides what to keep, strengthens important connections (Hebbian potentiation), and discards noise (synaptic homeostasis). The prefrontal cortex provides working memory — gated integrator circuits that hold information temporarily.

**Principle:** Active processing is required to move knowledge from working memory to permanent storage. It doesn't happen automatically.

**Source:** Eliasmith (2013), Ch 6 — gated integrators for working memory, STDP for long-term potentiation. Ch 7 — SPAUN's working memory module uses Ordinal Serial Encoding (OSE).

**OpenBrainLM Implementation:**

**3-Tier Memory Architecture:**
| Tier | Analog | Implementation | Capacity | Lifespan |
|---|---|---|---|---|
| Working | Prefrontal (gated integrators) | Session context + OPEN_BRAIN.md | 200 lines | Session |
| Short-term | Hippocampal buffer | `research/*.md`, `memory/*.md` | Unbounded | 1 month decay |
| Long-term | Cortical consolidation | Brain regions (8 registered) | Expandable | Persistent |

**Consolidation cycle (the "sleep" equivalent):**
1. End of session → check barrier (screening + doubt parking lot)
2. Review all session artifacts in `research/`
3. Decide: promote to brain region (keep), leave in research (pending), or flag as stale
4. Update OPEN_BRAIN.md — compress, move overflow to open_brain_memory region
5. Update MEMORY.md — add new entries, remove stale ones
6. Log session
7. **Update OPEN_BRAIN.md copy in ALL brain regions** (octopus arm awareness rule)

**Consolidation Quality Gates:**
- Was it verified by immune agent? → Promote to domain brain region
- Was it only screened? → Leave in barrier, do NOT promote
- Is it stale (>1 month)? → Flag for refresh, not deletion (append-only ledger)
- Does it contradict existing memory? → Flag conflict, don't silently overwrite

**Hebbian connection strength (STDP — cross-cutting mechanism applied here):**
- When Agent A's output is used by Agent B → strengthen A→B connection weight
- When Agent A's output is rejected/corrected → weaken A→B connection weight
- Over time, the most productive agent-to-agent pipelines become stronger
- Implementation: track handoff success rates in `memory/connection_strengths.json`

**What this replaces:** Random, unstructured memory management. This formalizes WHEN and HOW knowledge moves between tiers.

---

## L6 — RELEVANCE DETECTION (Amygdala + Quorum — Human + Insect, merged from original L7 + L8)

**Biology:** The amygdala detects threats FASTER than conscious thought via a "low road" shortcut that bypasses cortex. False positives acceptable — better to flinch at a stick than ignore a snake. BUT the amygdala alone has a high false positive rate. In honeybees, the quorum sensing mechanism (Seeley 2010) provides SLOW, ACCURATE consensus: scout bees independently evaluate and must reach an absolute threshold of 10-15 scouts before the swarm commits.

**Why merged:** Fast crude detection (amygdala) + slow accurate consensus (quorum) are TWO STAGES of the same pipeline: relevance detection. The amygdala is the "Stage 1 fast alarm." The quorum is the "Stage 2 slow confirmation." Together they form a complete relevance detection system with adjustable sensitivity.

**Principle:** Two-stage threat/relevance pipeline. Stage 1: fast, crude, high false positive (amygdala). Stage 2: slow, accurate, threshold-based consensus (quorum). Both stages must agree for high-stakes actions.

**Source:** LeDoux (1996) — amygdala dual-pathway model. Seeley (2010) — honeybee quorum sensing with absolute threshold. Eliasmith (2013), Ch 5 — basal ganglia hyperdirect pathway as emergency stop.

**OpenBrainLM Implementation:**

**Stage 1 — Amygdala (fast alarm, <1 second):**
- **immune agent** = the amygdala. It sees every plan before execution.
- Fires on: unverified claims, missing citations, destructive actions, contradictions with verified knowledge
- Response: ALARM signal → suppresses action via L4 hyperdirect pathway
- False positive rate: HIGH (by design — better to block and verify than to let through)

**Stage 2 — Quorum (slow confirmation, requires multiple agents):**
- Minimum 2 agents evaluate independently (scout verification)
- immune agent MUST be one of the evaluators (adversarial check)
- Absolute threshold (not majority): unanimous for CRITICAL, 2/3 for HIGH
- If quorum fails: action is BLOCKED, routed to owner

**Combined Pipeline:**
| Amygdala Stage 1 | Quorum Stage 2 | Result |
|---|---|---|
| LOW alarm | Not triggered | Proceed with logged warning |
| MEDIUM alarm | 2 agents evaluate | Proceed if 2/2 agree safe |
| HIGH alarm | 3+ agents evaluate | Proceed if unanimous |
| CRITICAL alarm | All agents + owner | Proceed ONLY with owner approval |

**Quorum participants by action type:**
| Action | Required Voters | Threshold |
|---|---|---|
| Deploy | verifier + immune + prefrontal + owner | Unanimous |
| Publish | immune + verifier + owner | Unanimous |
| New capability | morphogen + immune | 2/2 |
| Barrier → brain region | immune + domain agent | 2/2 |
| Architecture change | prefrontal + immune + owner | Unanimous |

**What this replaces:** Separate amygdala and quorum layers. The two-stage pipeline is more biologically accurate and computationally cleaner.

---

## L7 — CHROMATOPHORE LAYER (Octopus)

**Biology:** Octopus chromatophores are pigment cells controlled by muscles that expand or contract in milliseconds. The display IS the state. You don't need to ask the octopus how it feels; you can see it. Multi-timescale: chromatophores (ms), iridophores (seconds), leucophores (minutes) provide layered state information.

**Principle:** State should be visible, not hidden. Multiple timescales: instant alerts, session summaries, trend lines.

**OpenBrainLM Implementation:**
- **Chromatophore layer** renders real-time system state:
  - Which agents are active (arms moving)
  - Which brain regions were last accessed (memory activity)
  - Barrier occupancy (screening threat level)
  - Research pipeline status (what's being processed)
  - Audit status (PASS/BLOCKED/PENDING)
  - Connection strength heatmap (which agent→agent paths are strongest)
- **Multi-timescale display:**
  | Timescale | Analog | Display |
  |---|---|---|
  | Instant (ms) | Chromatophore | Alert flashes: red=BLOCK, amber=screening, green=PASS |
  | Session (min) | Iridophore | Active agents, current task, memory tier activity |
  | Trend (hours/days) | Leucophore | Agent handoff patterns, research pipeline throughput |

**What this replaces:** Having to ask "what's happening?" The system's state is always visible.

---

## L8 — PATHOS LAYER (Default Mode Network — Human)

**Biology:** The Default Mode Network (DMN) activates when the brain is NOT focused on external tasks — daydreaming, mind-wandering, future planning. It's where creativity happens: connecting unrelated memories, seeing patterns across domains, imagining possibilities. The DMN is suppressed during focused work and activates during rest.

**The Aristotle Connection (Nicomachean Ethics, c. 350 BCE):**
Aristotle's three modes of persuasion — Ethos, Logos, Pathos — map directly to the Trinity engine:
- **Ethos** (ἦθος, character/virtue) = the verification gate. "Is this claim trustworthy? Does it come from a credible source? Is it consistent with our established character?" Aristotle: virtue is acquired through HABITUATION, not just knowledge (Book II). The Ethos gate improves through practice, not instruction.
- **Logos** (λόγος, reason/logic) = the analytical engine. Pure rational inference, formal logic, mathematical proof. The intellect operating on verified premises.
- **Pathos** (πάθος, emotion/feeling) = the creative background process. The "semi-rational appetites" (Aristotle) — they respond to reason but are not themselves rational. They generate proposals that MUST pass through Ethos before becoming actionable.
- **Phronesis** (φρόνησις, practical wisdom) = the BRIDGE between moral and intellectual virtue. The Ethos gate in action: knowing not just WHAT is true, but what is WORTH PURSUING. This is the quality that improves with experience — the system's judgment.

**Principle:** Invention happens in the background, not on demand. But invention CANNOT act — it can only propose. Multiple probes simultaneously, dynamic coupling between dreams and reality.

**Source:** Raichle (2001) — DMN discovery. Aristotle, *Nicomachean Ethics*, Books I-II, VI. Eliasmith (2013), Ch 7 — SPAUN's transform computation module.

**OpenBrainLM Implementation:**
- **Pathos = the DMN.** It runs when no active task is assigned.
- Background research (explorer agent) = DMN activity
- Pathos can:
  - Notice connections between brain regions that aren't explicitly linked
  - Propose new research directions
  - Suggest architectural improvements
  - Cross-pollinate findings across domains
  - Run multiple probes simultaneously (unlike focused work which is single-threaded)
- Pathos CANNOT:
  - Modify any file
  - Execute any action
  - Bypass Ethos/Logos verification
  - Push to any external system
- **The dream cycle (Trinity in action):**
  1. **Pathos proposes:** "What if we combined X from neural_arc with Y from evolutionary_ml?"
  2. **Ethos gathers:** "Does X actually work? Does Y exist? What does the literature say?" (habituation — the system has PRACTICED verification)
  3. **Logos connects:** "If X and Y, then Z follows. Here's the proof."
  4. Only after Ethos ↔ Logos iterate to completion does the proposal become actionable
  5. **Phronesis decides:** "Is Z worth pursuing? Does it serve the system's goals?"
  6. Back to Ethos: the new whole needs its own pieces verified

**What this replaces:** On-demand-only thinking. The Pathos layer means the system can improve itself in the background — but NEVER act on dreams without verification.

---

## Cross-Cutting Mechanisms (not layers — they permeate everything)

These four mechanisms are NOT layers. They operate ACROSS all 8 layers simultaneously.

### ◆ Prediction Error Filter (Friston)

**Source:** Friston (2010), "The free-energy principle." Smith, Friston, & Whyte (2022), active inference tutorial.

**Mechanism:** Every layer generates PREDICTIONS about what it expects to observe. When actual observations diverge from predictions (prediction error), the error signal is routed based on magnitude:
- Low error → routine processing (tonic mode)
- Medium error → flag for attention (L6 amygdala stage 1)
- High error → suppress action, investigate (L4 hyperdirect pathway)

**Implementation:** Each agent maintains an implicit model of "what I expect." When results surprise, the surprise magnitude determines routing. This replaces hardcoded threat rules with learned expectations.

### ◆ Hebbian Plasticity (STDP)

**Source:** Eliasmith (2013), Ch 6 — STDP learning. Hebb (1949) — "neurons that fire together wire together."

**Mechanism:** Connection strengths between agents adapt over time:
- When Agent A's output is successfully used by Agent B → A→B weight increases
- When Agent A's output is rejected by Agent B → A→B weight decreases
- Over time, productive pipelines strengthen and unproductive ones weaken
- This is SPIKE-TIMING-DEPENDENT: the ORDER matters. A must fire BEFORE B for potentiation.

**Implementation:** Track handoff success/failure rates. Store as `memory/connection_strengths.json`. Use weights to influence L4 action selection (stronger connections = higher salience for that routing path).

### ◆ Interoception (System Health)

**Source:** Craig (2002) — interoceptive awareness. Barrett & Simmons (2015) — interoceptive predictions.

**Mechanism:** Continuous monitoring of system health metrics:
- Context window utilization (how close to compression?)
- Token budget remaining (cost awareness)
- Agent availability (which arms are responsive?)
- Memory pressure (how full are brain regions? MEMORY.md line count?)
- Research staleness (how old is the freshest artifact in each domain?)

**Implementation:** L1 boot includes health check. L7 dashboard displays interoceptive state. L4 routing considers agent availability before dispatch.

### ◆ Cerebellum Timing (Predictive Scheduling)

**Source:** Ito (2008) — cerebellum as prediction machine. Wolpert, Miall, & Kawato (1998) — internal models for motor control.

**Mechanism:** Predictive scheduling of operations:
- If Agent A typically takes 30 seconds → start Agent B's prep work 25 seconds in
- If consolidation cycle takes 2 minutes → trigger it before context window fills
- If GCP compute takes 30 minutes → schedule overnight, notify in morning

**Implementation:** Track agent execution times. Build simple timing models. Use for preemptive action — start consolidation before memory pressure forces it.

---

## The Hybrid: Why Hive-Mind + Octopus + Human

| System | What It Provides | Weakness Covered By |
|---|---|---|
| **Octopus** | Distributed autonomy (arms think for themselves) | No long-term memory → Human hippocampus |
| **Insect Hive** | Collective intelligence, fault tolerance, stigmergy | No individual reasoning → Human prefrontal cortex |
| **Human** | Executive planning, memory consolidation, threat detection, creativity | Single point of failure → Insect redundancy |

**The synthesis:**
- Octopus SHAPE: each agent is an autonomous arm with its own ganglion
- Insect PROTOCOL: agents communicate through artifacts (stigmergy), decide through quorum
- Human COGNITION: memory consolidation (hippocampus), action selection (basal ganglia), threat detection (amygdala), invention (DMN/Pathos)
- Aristotle's PHILOSOPHY: Ethos (character/virtue), Logos (reason), Pathos (emotion/creativity), Phronesis (practical wisdom)

---

## Layer Interaction Example: "Research a new capability"

```
L1  Agent boots, actively probes environment (active sensing)
L2  Explorer ganglion evaluates the research domain independently (arm autonomy)
L3  Explorer leaves artifact: research/capability_evaluation.md (stigmergy)
L4  Basal ganglia releases verifier channel (action selection via inhibition release)
    Thalamus gates explorer's artifact to verifier (information routing)
L6  Stage 1: Amygdala checks — is this claim verified? (fast alarm)
    Stage 2: Quorum — verifier + immune both must approve (slow consensus)
L5  If approved: memory updated, brain region entry created (consolidation)
    Hebbian: explorer→verifier connection strength increases (STDP, cross-cutting)
L7  Chromatophore shows new knowledge in green (state display)
L3  Simple rules created complex multi-agent verification (swarm emergence)
```

---

## Implementation Priority

| Priority | Layer | Status | Next Step |
|---|---|---|---|
| 1 | L2 Ganglion | BUILT (8 cognitive agents) | Self-evolve 10 more from neurology + ethics taxonomy |
| 2 | L3 Stigmergy+Swarm | BUILT | Decay EXISTS (`Pheromone.decay_days`, `current_strength()`). Next: ACOpy evaporation algorithm |
| 3 | L4 Action Selection | BUILT | Implement semantic routing (embeddings) |
| 4 | L6 Relevance Detection | BUILT | 2-stage pipeline EXISTS (`amygdala_scan()`, `initiate_quorum()`). Next: DebateLLM consensus |
| 5 | L5 Memory | BUILT | Hebbian tracking EXISTS (`cross_cutting.py`). Next: HippoRAG v2 integration. Formal consolidation: `docs/specs/SELF_EVOLUTION_LOOP.md` |
| 6 | L1 Active Sensing | BUILT | Formalize 3-step boot + OPEN_BRAIN.md in all regions |
| 7 | L7 Chromatophore | BUILT | Multi-timescale EXISTS (instant/session/trend in `chromatophore.py`). Next: dashboard rendering |
| 8 | L8 Pathos | BUILT (Trinity defined) | Background research pipeline |
| X | Cross-cutting: STDP | BUILT (basic dict-based, `cross_cutting.py`) | Next: upgrade to snnTorch. 6 tests pass. |
| X | Cross-cutting: Prediction Error | BUILT (numeric comparison, `cross_cutting.py`) | Next: upgrade to D-MEM RPE gating. 4 tests pass. |
| X | Cross-cutting: Interoception | BUILT (`cross_cutting.py`) | Next: trajectory extrapolation (allostatic gate). 3 tests pass. |
| X | Cross-cutting: Cerebellum | BUILT (basic timing, `cross_cutting.py`) | Next: Kalman filter prediction. 3 tests pass. |

---

## Computational Backbone (from HOW research — `research/brain_build_how_research.md`)

| Stack Layer | Tool/Framework | Purpose |
|---|---|---|
| Agent Graph | LangGraph (MIT) | Stateful graph with cycles, conditional edges, checkpoints |
| Query Routing | semantic-router → PyMDP → R-GCN | Embedding similarity → active inference → learned routing |
| Wiring Evolution | NEAT-Python (BSD) / TreEvo | Evolve agent connections, not hand-design them |
| Control Theory | PyMDP (MIT) | Active inference POMDP for learned routing decisions |
| Vector Memory | Pinecone | Embedding storage for brain region + query vectors |

---

> Architecture corrected 2026-03-21, based on:
> - Eliasmith (2013), *How to Build a Brain* — SPAUN, NEF, basal ganglia
> - Aristotle (c. 350 BCE), *Nicomachean Ethics* — Ethos/Logos/Pathos/Phronesis
> - Bhowmick (2021), *Bio-Inspired Swarm Robotics* — stigmergy formalization
> - Seeley (2010), *Honeybee Democracy* — quorum sensing thresholds
> - Friston (2010), "The free-energy principle" — prediction error
> - Adversarial audit (2026-03-20) — grade B-, corrections applied
> - Research synthesis (2026-03-21) — 5 HOW research threads, 20 papers
>
> "Nothing new. Everything assembled from existing biology and philosophy." — The Open Brain Way
