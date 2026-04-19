# OpenBrainLM — Self-Evolution Loop Specification
> Addendum to OPERATIONAL_LAYERS.md v2
> Closes the three missing feedback loops: consolidation triggers, morphogen fitness, knowledge promotion.
> "The brain that only replaces stubs is a brain that was built. The brain that closes these loops is a brain that grows."

---

## Why This Document Exists

OPERATIONAL_LAYERS.md defines WHAT the 8 layers do. The implementation plan defines WHICH repos replace the stubs. This document defines HOW the self-improvement loop actually closes — the three mechanisms that turn a static architecture into a living brain:

1. **Consolidation triggers** — WHO initiates sleep, WHEN, and what happens during it
2. **Morphogen fitness** — HOW the brain evaluates its own wiring and evolves it
3. **Knowledge promotion** — WHO decides research graduates from barrier to brain region

Without these three, you have 8 layers that process queries. With them, you have a brain that gets better at processing queries every time it sleeps.

---

## 1. CONSOLIDATION TRIGGERS — The Sleep Protocol

### Biology

The hippocampus doesn't consolidate on a clock. Sleep is triggered by three signals: adenosine accumulation (fatigue/resource depletion), task completion (safety — the animal has found shelter), and circadian cues (environmental). During sleep, sharp-wave ripples replay the day's experiences at ~20× speed, selectively strengthening important traces and pruning noise (Wilson & McNaughton, 1994). The octopus exhibits two sleep states — "quiet sleep" and "active sleep" with rapid chromatophore changes (Medeiros et al., 2021) — suggesting consolidation happens in phases, not all at once.

### Principle

Sleep is event-driven, not timer-driven. Three triggers, two phases. The brain never defers consolidation to "when it wakes up" — it consolidates BEFORE entering dormancy.

### Triggers (from WHITEPAPER.md §2.4, now formalized)

| Trigger | Signal Source | Biological Analog | Urgency |
|---|---|---|---|
| **Memory pressure** | homeostasis agent detects working memory > 80% capacity OR context window > 70% utilized | Adenosine accumulation (fatigue) | HIGH — consolidate immediately or risk data loss |
| **Task completion** | orchestrator receives final result from agent pipeline, no pending queries | Safety — animal reaches shelter | NORMAL — consolidate when convenient |
| **Session end** | CLI exit, API timeout, explicit `--sleep` command | Circadian signal | NORMAL — mandatory before dormancy |
| **User-initiated** | Owner issues explicit sleep command: `python -m openbrainlm --sleep` | Voluntary nap — the octopus choosing to rest | NORMAL — on-demand evolution |

### Chain of Command

```
TRIGGER fires (any of the 4 above)
     │
     ▼
HOMEOSTASIS agent detects trigger (interoception — L1 health check)
     │
     ▼
HOMEOSTASIS sends RECRUITMENT pheromone to orchestrator
     │  (recruitment pheromone = "consolidator needed")
     │
     ▼
ORCHESTRATOR dispatches CONSOLIDATOR agent
     │  (L4 action selection RELEASES consolidator channel)
     │
     ▼
CONSOLIDATOR executes the Sleep Cycle (see below)
     │
     ▼
ORCHESTRATOR dispatches MORPHOGEN agent (Phase 2 — evolution)
     │  (only if sleep was triggered by task completion or user-initiated,
     │   NOT by memory pressure — under pressure, consolidate only, don't evolve)
     │
     ▼
MORPHOGEN executes Evolution Cycle (see §2 below)
     │
     ▼
HOMEOSTASIS verifies post-sleep health metrics
     │  (interoception: memory pressure resolved? connection_strengths updated?)
     │
     ▼
BRAIN enters dormancy OR resumes active processing
```

### The Sleep Cycle (Consolidator Agent)

Two phases, matching octopus "quiet sleep" and "active sleep":

**Phase 1 — Quiet Sleep (consolidation):**
1. Read `memory/connection_strengths.json` — snapshot current Hebbian weights
2. Scan `research/*.md` — identify all session artifacts
3. For each artifact, check consolidation quality gates:
   - Verified by immune agent? → candidate for PROMOTION (see §3)
   - Only screened? → stays in barrier
   - Stale (>1 month since last access)? → flag for refresh, DO NOT delete
   - Contradicts existing long-term memory? → flag conflict, route to L6 quorum
4. Execute promotions (see §3 for the full protocol)
5. Update `memory/session_log.json` — append session summary
6. Compress OPEN_BRAIN.md if over capacity → overflow to `open_brain_memory` region
7. Sync OPEN_BRAIN.md to ALL brain regions (octopus arm awareness rule)

**Phase 2 — Active Sleep (replay + strengthening):**
1. Replay session handoffs at accelerated speed (replay = re-evaluate decisions from logs):
   - For each agent→agent handoff in session log:
     - Was the downstream agent's output used? → increment `success` in connection_strengths
     - Was it rejected/corrected? → increment `failure`
     - Recalculate weight: `weight = success / (success + failure)`
2. Update `memory/connection_strengths.json` with new weights
3. Update `memory/prediction_baselines.json` — recalculate expected prediction errors per agent
4. Write `memory/sleep_report.md` — what was consolidated, what was promoted, what changed

**Output artifacts (stigmergy):**
- Updated `memory/connection_strengths.json`
- Updated `memory/prediction_baselines.json`
- Updated `memory/session_log.json`
- `memory/sleep_report.md` (trail pheromone — next session reads this)
- Promoted entries in brain regions (if any passed quality gates)

### Implementation (for coding agent)

```python
# orchestrator.py — sleep dispatch
class Orchestrator:
    def check_sleep_triggers(self, state: BrainState) -> SleepTrigger | None:
        """Called after every agent pipeline completion and on health check intervals."""
        if state.working_memory_utilization > 0.80:
            return SleepTrigger.MEMORY_PRESSURE
        if state.pending_queries == 0 and state.last_query_completed:
            return SleepTrigger.TASK_COMPLETION
        if state.session_ending:
            return SleepTrigger.SESSION_END
        return None

    def initiate_sleep(self, trigger: SleepTrigger):
        """Dispatch consolidator, then optionally morphogen."""
        # Phase 1+2: Consolidation
        consolidator_result = self.dispatch("consolidator", {
            "trigger": trigger,
            "session_artifacts": self.collect_session_artifacts(),
            "connection_strengths": self.load_connection_strengths(),
        })

        # Phase 3: Evolution (only if not under memory pressure)
        if trigger != SleepTrigger.MEMORY_PRESSURE:
            self.dispatch("morphogen", {
                "sleep_report": consolidator_result.sleep_report,
                "connection_strengths": consolidator_result.updated_strengths,
                "session_history": self.load_session_history(),
            })

        # Post-sleep health check
        self.dispatch("homeostasis", {"action": "post_sleep_verify"})
```

```python
# consolidator.py — the sleep cycle
class ConsolidatorAgent:
    def execute(self, context: dict) -> ConsolidationResult:
        """Two-phase sleep: quiet (consolidate) then active (replay)."""

        # === PHASE 1: QUIET SLEEP ===
        promotions = []
        for artifact in context["session_artifacts"]:
            gate_result = self.check_quality_gates(artifact)
            if gate_result == QualityGate.PROMOTE:
                promotions.append(artifact)
            elif gate_result == QualityGate.CONFLICT:
                self.flag_for_quorum(artifact)
            # STALE and PENDING stay where they are

        # Execute promotions via L6 quorum (see §3)
        for artifact in promotions:
            self.request_promotion_quorum(artifact)

        # Compress OPEN_BRAIN.md if needed
        self.compress_if_over_capacity()
        self.sync_open_brain_to_all_regions()

        # === PHASE 2: ACTIVE SLEEP (replay) ===
        strengths = context["connection_strengths"]
        for handoff in self.replay_session_handoffs():
            edge = f"{handoff.source}→{handoff.target}"
            if handoff.output_was_used:
                strengths[edge]["success"] += 1
            else:
                strengths[edge]["failure"] += 1
            total = strengths[edge]["success"] + strengths[edge]["failure"]
            strengths[edge]["weight"] = strengths[edge]["success"] / total

        # Update prediction baselines
        baselines = self.recalculate_prediction_baselines(strengths)

        return ConsolidationResult(
            updated_strengths=strengths,
            prediction_baselines=baselines,
            promotions_requested=len(promotions),
            sleep_report=self.generate_sleep_report(),
        )
```

---

## 2. MORPHOGEN FITNESS — The Evolution Cycle

### Biology

The octopus edits its own RNA in response to environmental changes — not random mutation, but targeted self-modification that produces a structurally different organism adapted to what it encounters (Liscovitch-Brauer et al., 2017). This is neuroplasticity at the code level. The key distinction: RNA editing is continuous but EXPRESSION of edits happens during specific developmental windows. The octopus doesn't rewrite itself mid-hunt. It rewrites itself during rest.

NEAT (Stanley & Miikkulainen, 2002) evolves both topology AND weights simultaneously, starting minimal and complexifying only when complexity improves fitness. This mirrors the biological principle: don't add structure without evidence that the new structure helps.

### Principle

Evolution is retrospective, not real-time. The morphogen agent runs during sleep, evaluates topology mutations against historical data, and the best candidates get promoted. Dream → check → act. Never dream → act.

### The Fitness Function

Morphogen needs a fitness signal to evaluate candidate topologies. The signal is **composite**, drawn from three sources that already exist in the system:

```
fitness(topology) = α × prediction_accuracy
                  + β × handoff_efficiency
                  + γ × dialectic_efficiency
```

Where:

#### Component 1: Prediction Accuracy (α = 0.4 default)

**Source:** pymdp's free energy computation (cross-cutting prediction error filter)

**Signal:** When the routed agent's output matches what was expected (low surprise), the routing topology that produced that match is rewarded.

```python
prediction_accuracy = 1.0 - mean_prediction_error

# prediction_error per query = |expected_outcome - actual_outcome|
# expected_outcome comes from pymdp's generative model (A matrix)
# actual_outcome comes from the agent's actual response quality
#   (did the downstream consumer accept it? was it used in final output?)
```

**What it rewards:** Topologies where the right agent gets the right query.
**What it punishes:** Topologies where queries bounce between agents or get misrouted.

#### Component 2: Handoff Efficiency (β = 0.4 default)

**Source:** `memory/connection_strengths.json` (Hebbian STDP tracking)

**Signal:** The mean success rate across all active agent-to-agent handoff pathways in the topology.

```python
handoff_efficiency = mean(
    strengths[edge]["weight"]
    for edge in topology.active_edges
    if strengths[edge]["success"] + strengths[edge]["failure"] > min_samples
)

# Only count edges with enough data (min_samples = 5)
# Edges with insufficient data get neutral score (0.5)
```

**What it rewards:** Topologies with strong, proven agent pipelines.
**What it punishes:** Topologies with weak or untested connections.

#### Component 3: Dialectic Efficiency (γ = 0.2 default)

**Source:** Trinity engine logs

**Signal:** How quickly the dialectic resolves to VERIFIED. Fewer rounds = more efficient topology (the right information reached the right evaluators faster).

```python
dialectic_efficiency = 1.0 / mean_dialectic_rounds

# mean_dialectic_rounds = average number of Logos↔Pathos iterations
#   before Ethos reached VERIFIED across all session queries
# If any query DEADLOCKED (reached 10 rounds): that query scores 0.0
# Cap at 1.0 (1 round = perfect efficiency, unlikely but possible)
```

**What it rewards:** Topologies where agents provide the right evidence early, reducing dialectic iterations.
**What it punishes:** Topologies where the Trinity frequently deadlocks or takes many rounds.

#### Weight Evolution (meta-evolution)

The weights α, β, γ are themselves subject to evolution:

```python
# Initial defaults
alpha, beta, gamma = 0.4, 0.4, 0.2

# After every evolution cycle, the morphogen adjusts weights based on
# which component had the highest variance across the population:
# High variance = high discriminative power = weight should increase
# Low variance = all topologies score similarly = weight is less useful
variance_alpha = variance([t.prediction_accuracy for t in population])
variance_beta = variance([t.handoff_efficiency for t in population])
variance_gamma = variance([t.dialectic_efficiency for t in population])

total_variance = variance_alpha + variance_beta + variance_gamma
alpha = variance_alpha / total_variance
beta = variance_beta / total_variance
gamma = variance_gamma / total_variance
```

This means the brain learns WHAT TO OPTIMIZE FOR, not just how to optimize. If prediction accuracy is the bottleneck (high variance = some topologies are much better than others at this), the brain focuses evolution there. If handoff efficiency is already uniformly high, the brain stops wasting evolution cycles on it.

### The Evolution Cycle (Morphogen Agent)

Runs ONLY during sleep, ONLY when triggered by task completion or user-initiated sleep (not memory pressure).

```
MORPHOGEN receives sleep_report + connection_strengths + session_history
     │
     ▼
STEP 1: Snapshot current topology as INCUMBENT
     │  (the topology that was actually used during the session)
     │  Represented as: directed graph of agent→agent edges with weights
     │
     ▼
STEP 2: Generate CANDIDATE topologies (population_size = 10 default)
     │  Using NEAT operations:
     │  - Add node: insert new agent relay between two connected agents
     │  - Add connection: create new agent→agent pathway
     │  - Mutate weight: adjust existing connection strength ±δ
     │  - Remove connection: prune an underperforming pathway
     │  - Crossover: combine two parent topologies (if population > 1 generation)
     │
     │  Constraints (NEAT speciation preserves these):
     │  - MUST keep all 8 core agents (cannot remove a ganglion)
     │  - MUST keep orchestrator→agent edges (central brain → arms)
     │  - CAN add/remove agent→agent edges (inter-arm connections)
     │  - CAN adjust routing weights on any edge
     │  - CANNOT create cycles that bypass the Trinity gate
     │
     ▼
STEP 3: Evaluate ALL candidates against HISTORICAL DATA
     │  (this is the key safety mechanism — no live queries during evolution)
     │
     │  For each candidate topology:
     │    Replay the last N sessions (N = 10 default) through the candidate:
     │    - Simulate routing: given query Q, which agent would this topology select?
     │    - Compare to actual outcome: did the ACTUAL agent that handled Q succeed?
     │    - Compute fitness(candidate) using the composite function above
     │
     │  This is RETROSPECTIVE evaluation. The morphogen asks:
     │  "If this topology had been in charge during the last 10 sessions,
     │   would routing have been better or worse?"
     │
     ▼
STEP 4: Select WINNER
     │  - If best candidate fitness > incumbent fitness + threshold (0.05):
     │      → PROPOSE candidate as new topology
     │      → Route proposal through Trinity (dream → check → act)
     │      → Ethos: "Is this change consistent with our character?"
     │      → Logos: "Does the fitness improvement justify the change?"
     │      → Pathos: "Does this open new capabilities?"
     │      → If Trinity VERIFIED: promote candidate to active topology
     │      → If Trinity BLOCKED: log reason, keep incumbent
     │  - If no candidate beats incumbent + threshold:
     │      → Keep incumbent, log "no improvement found"
     │      → Increase mutation rate slightly for next cycle (exploration pressure)
     │
     ▼
STEP 5: Record evolution artifacts (stigmergy)
     │  - Write `memory/evolution_log.json`:
     │      { generation, incumbent_fitness, best_candidate_fitness,
     │        promoted: bool, topology_diff, timestamp }
     │  - Update `memory/connection_strengths.json` if topology changed
     │  - Write trail pheromone: `research/evolution_report_YYYYMMDD.md`
     │
     ▼
DONE — morphogen terminates (episodic runtime)
```

### Implementation (for coding agent)

```python
# morphogen.py — the evolution cycle
import neat  # neat-python, BSD-3, zero deps

class MorphogenAgent:

    def execute(self, context: dict) -> EvolutionResult:
        """Run during sleep. Propose topology improvements. Never act without Trinity."""

        incumbent = self.load_current_topology()
        session_history = context["session_history"]
        strengths = context["connection_strengths"]

        # === STEP 1: Configure NEAT ===
        config = neat.Config(
            neat.DefaultGenome,
            neat.DefaultReproduction,
            neat.DefaultSpeciesSet,
            neat.DefaultStagnation,
            config_file="openbrainlm/evolution/neat_config.ini"
        )

        # === STEP 2: Generate population ===
        population = neat.Population(config)

        # Seed population with incumbent + mutations
        # (neat-python handles this via its reproduction methods)

        # === STEP 3: Evaluate fitness retrospectively ===
        def evaluate_genome(genome_id, genome, config):
            topology = self.genome_to_topology(genome)
            fitness = self.compute_fitness(topology, session_history, strengths)
            genome.fitness = fitness

        # Run for 1 generation (we don't need convergence, just candidates)
        winner = population.run(evaluate_genome, n=1)

        # === STEP 4: Compare to incumbent ===
        incumbent_fitness = self.compute_fitness(incumbent, session_history, strengths)
        winner_fitness = winner.fitness
        improvement = winner_fitness - incumbent_fitness

        if improvement > self.improvement_threshold:  # default 0.05
            # Route through Trinity before promoting
            proposal = EvolutionProposal(
                current=incumbent,
                proposed=self.genome_to_topology(winner),
                fitness_improvement=improvement,
                rationale=self.explain_topology_diff(incumbent, winner),
            )
            trinity_result = self.submit_to_trinity(proposal)

            if trinity_result.status == "VERIFIED":
                self.promote_topology(winner)
                return EvolutionResult(promoted=True, improvement=improvement)
            else:
                return EvolutionResult(promoted=False, reason=trinity_result.reason)
        else:
            # Increase exploration for next cycle
            self.increase_mutation_rate()
            return EvolutionResult(promoted=False, reason="no_improvement")

    def compute_fitness(self, topology, session_history, strengths) -> float:
        """Composite fitness: prediction accuracy + handoff efficiency + dialectic efficiency."""
        alpha, beta, gamma = self.load_fitness_weights()

        pred_acc = self.evaluate_prediction_accuracy(topology, session_history)
        handoff_eff = self.evaluate_handoff_efficiency(topology, strengths)
        dialectic_eff = self.evaluate_dialectic_efficiency(topology, session_history)

        return alpha * pred_acc + beta * handoff_eff + gamma * dialectic_eff

    def evaluate_prediction_accuracy(self, topology, history) -> float:
        """Replay sessions: would this topology have routed queries correctly?"""
        errors = []
        for session in history[-self.replay_window:]:  # last N sessions
            for query in session.queries:
                predicted_agent = topology.route(query.embedding)
                actual_agent = query.handled_by
                actual_success = query.was_successful
                if predicted_agent == actual_agent and actual_success:
                    errors.append(0.0)
                elif predicted_agent == actual_agent and not actual_success:
                    errors.append(0.5)
                else:
                    errors.append(1.0)
        return 1.0 - (sum(errors) / max(len(errors), 1))

    def evaluate_handoff_efficiency(self, topology, strengths) -> float:
        """Mean success rate across topology's active edges."""
        scores = []
        for edge in topology.edges:
            key = f"{edge.source}→{edge.target}"
            if key in strengths:
                s = strengths[key]
                total = s["success"] + s["failure"]
                if total >= self.min_samples:
                    scores.append(s["weight"])
                else:
                    scores.append(0.5)
            else:
                scores.append(0.5)
        return sum(scores) / max(len(scores), 1)

    def evaluate_dialectic_efficiency(self, topology, history) -> float:
        """1 / mean dialectic rounds. Deadlocks (10 rounds) score 0."""
        rounds = []
        for session in history[-self.replay_window:]:
            for query in session.queries:
                if query.dialectic_rounds >= 10:
                    rounds.append(float('inf'))
                else:
                    rounds.append(query.dialectic_rounds)
        if not rounds:
            return 0.5
        finite_rounds = [r for r in rounds if r != float('inf')]
        if not finite_rounds:
            return 0.0
        return min(1.0, 1.0 / (sum(finite_rounds) / len(finite_rounds)))
```

### NEAT Configuration (for coding agent)

```ini
# openbrainlm/evolution/neat_config.ini
[NEAT]
fitness_criterion     = max
fitness_threshold     = 0.95
pop_size              = 10
reset_on_extinction   = False

[DefaultGenome]
# 8 input nodes = 8 agent salience scores
# 8 output nodes = 8 agent activation levels
num_inputs            = 8
num_hidden            = 0
num_outputs           = 8
initial_connection    = partial_direct 0.5
feed_forward          = True
compatibility_disjoint_coefficient = 1.0
compatibility_weight_coefficient   = 0.5

# Connection mutation rates
conn_add_prob         = 0.3
conn_delete_prob      = 0.1
node_add_prob         = 0.1
node_delete_prob      = 0.05

# Weight mutation
weight_init_mean      = 0.0
weight_init_stdev     = 1.0
weight_mutate_rate    = 0.8
weight_mutate_power   = 0.5
weight_replace_rate   = 0.1
weight_max_value      = 3.0
weight_min_value      = -3.0

# Activation
activation_default    = sigmoid
activation_mutate_rate = 0.0
activation_options    = sigmoid

[DefaultSpeciesSet]
compatibility_threshold = 3.0

[DefaultStagnation]
species_fitness_func = max
max_stagnation       = 5
species_elitism      = 1

[DefaultReproduction]
elitism              = 2
survival_threshold    = 0.2
```

### What Gets Evolved (and What Doesn't)

| Evolves | Does NOT Evolve |
|---|---|
| Agent→agent connection weights | The 8 core agents themselves |
| Which agents connect to which | The orchestrator's existence |
| Routing thresholds per agent | The Trinity gate requirement |
| Burst vs tonic mode thresholds | The sleep/wake cycle |
| Indirect pathway strengths | The L6 quorum requirements |
| New relay nodes between agents | The append-only memory rule |

The 8 core cognitive agents are the GENOME — fixed like the octopus's basic body plan. What evolves is how they WIRE together — like the octopus editing its RNA to change how neurons connect, not which neurons exist.

Future: the 10 additional agents (derived from neurology + Nicomachean Ethics taxonomy) will be BORN from evolution, not hand-designed. Morphogen proposes a new agent type → Trinity validates → immune challenges → if it survives, the brain has a 9th arm.

---

## 3. KNOWLEDGE PROMOTION — The Barrier Protocol

### Biology

The blood-brain barrier (BBB) is a selective permeability membrane that protects the brain from pathogens, toxins, and most large molecules in the bloodstream. Only molecules that the BBB specifically PERMITS can enter the brain. This is not filtering — it is active gatekeeping. The immune system's T-cells patrol the barrier, and anything that looks suspicious gets challenged.

### Principle

New knowledge enters the barrier (quarantine). It stays there until actively promoted. Promotion requires a quorum: the immune agent adversarially challenges, the domain agent checks relevance and consistency. Both must agree unanimously. No exceptions.

### The Promotion Protocol

```
New research artifact arrives in barrier/
     │  (e.g., research/basal_ganglia_findings.md)
     │
     ▼
CONSOLIDATOR identifies candidate during sleep Phase 1
     │  (quality gate check: was it verified by immune agent?)
     │
     ▼
CONSOLIDATOR requests PROMOTION QUORUM from orchestrator
     │  (recruitment pheromone: "quorum needed for barrier→region promotion")
     │
     ▼
ORCHESTRATOR dispatches L6 quorum subgraph:
     │
     ├── IMMUNE agent (adversarial challenge):
     │   - Are all claims cited? (trail pheromone check)
     │   - Do any claims contradict verified knowledge in the target brain region?
     │   - Is the source credible? (provenance check)
     │   - Can I find a counterexample or flaw? (red team)
     │   - Verdict: APPROVE / REJECT / NEEDS_MORE_EVIDENCE
     │
     ├── DOMAIN agent (relevance + consistency):
     │   - Which brain region does this belong in?
     │   - Is it consistent with existing entries in that region?
     │   - Does it add NEW information or duplicate what's already there?
     │   - Is the granularity appropriate? (too broad? too narrow?)
     │   - Verdict: APPROVE / REJECT / WRONG_REGION
     │
     ▼
QUORUM EVALUATION (L6 Stage 2):
     │
     │  Both APPROVE?
     │  ├── YES → PROMOTE: move artifact to target brain region
     │  │         Update region index. Log promotion. Trail pheromone.
     │  │         Update OPEN_BRAIN.md if the knowledge is significant enough.
     │  │
     │  ├── One REJECTS → BLOCK: artifact stays in barrier
     │  │         Log rejection reason. Alarm pheromone.
     │  │         If NEEDS_MORE_EVIDENCE: flag for explorer agent next session
     │  │
     │  ├── WRONG_REGION → REDIRECT: domain agent specifies correct region
     │  │         Re-run quorum with correct domain agent
     │  │
     │  └── CONFLICT detected → ESCALATE to prefrontal + owner
     │           (contradicts existing verified knowledge — needs human judgment)
     │
     ▼
POST-PROMOTION (if promoted):
     │
     ├── Update brain region index
     ├── Strengthen explorer→verifier→immune Hebbian pathway (STDP)
     ├── Update HippoRAG knowledge graph with new entities/relations
     └── Log to memory/promotion_log.json
```

### Domain Agent Mapping

Each brain region has a natural domain agent that evaluates relevance:

| Brain Region | Domain Agent | Why |
|---|---|---|
| neural_arc | explorer | Explorer acquired it, knows the neuroscience domain |
| agents_arcs | morphogen | Morphogen is the agent architecture expert |
| zero_trust | verifier | Verifier IS the prediction error / zero-trust agent |
| adversarial_security | immune | Immune IS the adversarial expert |
| evolutionary_ml | morphogen | Morphogen handles self-evolution |
| rag_vector_search | hippocampus | Hippocampus IS the memory routing expert |
| open_brain_memory | consolidator | Consolidator manages the brain's own memory |
| barrier | immune | Immune guards the barrier by definition |

### Implementation (for coding agent)

```python
# promotion.py — the barrier→region protocol
class PromotionQuorum:
    """L6 quorum subgraph for knowledge promotion. Unanimous 2/2 required."""

    def evaluate(self, artifact: ResearchArtifact) -> PromotionResult:
        # Determine target region and domain agent
        target_region = self.classify_region(artifact)
        domain_agent = REGION_TO_AGENT[target_region]

        # Dispatch both evaluators independently (no shared state during eval)
        immune_verdict = self.dispatch_immune(artifact, target_region)
        domain_verdict = self.dispatch_domain_agent(domain_agent, artifact, target_region)

        # Quorum evaluation
        if immune_verdict.approve and domain_verdict.approve:
            return self.promote(artifact, target_region)

        elif domain_verdict.status == "WRONG_REGION":
            # Redirect and retry with correct domain agent
            return self.evaluate_with_region(artifact, domain_verdict.correct_region)

        elif immune_verdict.status == "NEEDS_MORE_EVIDENCE":
            # Flag for explorer to investigate next session
            self.flag_for_exploration(artifact, immune_verdict.what_is_missing)
            return PromotionResult(promoted=False, reason="needs_evidence",
                                   action="explore_next_session")

        elif self.detects_conflict(immune_verdict, domain_verdict):
            # Escalate: contradicts existing verified knowledge
            return self.escalate_to_owner(artifact, immune_verdict, domain_verdict)

        else:
            # Simple rejection
            return PromotionResult(promoted=False,
                                   immune_reason=immune_verdict.reason,
                                   domain_reason=domain_verdict.reason)

    def promote(self, artifact: ResearchArtifact, region: str) -> PromotionResult:
        """Move artifact from barrier to brain region. Update all indexes."""
        # 1. Copy artifact to knowledge/{region}/
        target_path = f"knowledge/{region}/{artifact.filename}"
        shutil.copy(artifact.path, target_path)

        # 2. Update HippoRAG knowledge graph
        self.hipporag.index(docs=[artifact.content])

        # 3. Strengthen Hebbian pathway
        self.update_connection_strengths([
            ("explorer", "verifier", "success"),
            ("verifier", "immune", "success"),
            ("immune", "consolidator", "success"),
        ])

        # 4. Log promotion
        self.append_promotion_log({
            "artifact": artifact.filename,
            "region": region,
            "timestamp": datetime.utcnow().isoformat(),
            "immune_confidence": immune_verdict.confidence,
            "domain_confidence": domain_verdict.confidence,
        })

        # 5. DO NOT delete from research/ (append-only ledger)
        # Mark as promoted instead
        artifact.metadata["promoted_to"] = region
        artifact.metadata["promoted_at"] = datetime.utcnow().isoformat()

        return PromotionResult(promoted=True, region=region)
```

---

## Complete Self-Evolution Loop — How It All Connects

```
AWAKE (active processing)
  │
  │  Queries arrive → L4 routes → agents work → results flow
  │  Every handoff is LOGGED (source agent, target agent, success/failure)
  │  Every prediction error is LOGGED (expected vs actual)
  │  Every dialectic resolution is LOGGED (rounds to VERIFIED)
  │  Every research artifact lands in barrier/
  │
  ▼
SLEEP TRIGGER fires (memory pressure | task complete | session end | user command)
  │
  ▼
PHASE 1: QUIET SLEEP (consolidator)
  │  Consolidate memory: promote verified knowledge, compress, sync
  │  Replay handoffs: update Hebbian connection strengths
  │  Update prediction baselines
  │
  ▼
PHASE 2: ACTIVE SLEEP (morphogen) — only if not memory-pressure-triggered
  │  Snapshot current routing topology
  │  Generate 10 candidate topologies via NEAT mutations
  │  Evaluate ALL candidates against last 10 sessions (retrospective)
  │  Compare best candidate to incumbent
  │  If improvement > threshold: submit to Trinity
  │  If Trinity VERIFIED: promote new topology
  │  If not: keep incumbent, increase exploration pressure
  │
  ▼
POST-SLEEP HEALTH CHECK (homeostasis)
  │  Memory pressure resolved?
  │  Connection strengths updated?
  │  Evolution log written?
  │  All brain regions have current OPEN_BRAIN.md?
  │
  ▼
WAKE — next session starts with improved routing, stronger connections,
       and new knowledge in the right brain regions.
       The brain that wakes up is better than the brain that fell asleep.
```

### The Feedback Loop (why it actually self-improves)

1. **Session N:** Query arrives → semantic-router picks agent → agent works → result is good/bad
2. **Sleep after N:** Consolidator logs success/failure → Morphogen evaluates: "if I had wired explorer directly to consolidator instead of going through verifier, would session N have been faster?" → NEAT generates that topology → fitness says yes → Trinity approves → new wiring is live
3. **Session N+1:** Same query type arrives → new routing is faster → prediction error is lower → Hebbian weight gets stronger → pymdp learns this is a reliable pathway
4. **Sleep after N+1:** Morphogen sees the improvement in session N+1 data → fitness for this topology increases → it's the new incumbent → NEAT explores FURTHER mutations from this better starting point
5. **Session N+2:** The brain is measurably better at this query type than it was at session N

This is the RNA editing cycle. The organism that emerges from sleep is permanently different from the one that went in. Not a preference change. Not a config change. A structural self-modification.

---

> Sources:
> - Wilson & McNaughton (1994), "Reactivation of hippocampal ensemble memories during sleep" — sharp-wave replay
> - Medeiros et al. (2021), "Cyclic alternation of quiet and active sleep states in the octopus" — two-phase sleep
> - Liscovitch-Brauer et al. (2017), "Trade-off between Transcriptome Plasticity and Genome Evolution in Cephalopods" — octopus RNA editing
> - Stanley & Miikkulainen (2002), "Evolving Neural Networks through Augmenting Topologies" — NEAT
> - Friston (2010), "The free-energy principle" — prediction error as fitness signal
> - Hebb (1949), "The Organization of Behavior" — "neurons that fire together wire together"
> - Seeley (2010), "Honeybee Democracy" — quorum sensing thresholds
> - WHITEPAPER.md §2.4 — sleep triggers (memory pressure, task completion, session end)
> - OPERATIONAL_LAYERS.md L6 — quorum table (barrier→region requires immune + domain agent, 2/2 unanimous)
>
> "The brain that wakes up is better than the brain that fell asleep."
