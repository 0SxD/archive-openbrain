# OpenBrainLM — Epimorphic Regeneration Protocol: Live Arm Regeneration
> Addendum to SELF_EVOLUTION_LOOP.md
> Closes the gap between "evolve only during sleep" and "adapt in real-time when survival demands it."
> Based on the two distinct self-modification mechanisms in coleoid cephalopods.
> Named for the biological process: epimorphic regeneration via blastema formation (Féral 1978; Imperadore et al. 2017, 2019).

---

## The Biology: Two Mechanisms, Not One

The octopus has two fundamentally different ways of changing itself. The existing
architecture (SELF_EVOLUTION_LOOP.md) only implements the first. This document
implements the second.

### Mechanism 1: RNA Editing (A-to-I recoding) — Already Implemented

**What it is:** ADAR enzymes convert adenosine to inosine in mRNA, causing
ribosomes to read different amino acids. The protein that gets built is different
from what the DNA encodes — without changing the DNA itself.

**Scale:** Coleoid cephalopods recode ~60% of their neural mRNAs. Over 57,000
recoding sites in squid, ~100,000 in octopus neural tissue. In humans, fewer
than 1,517 sites recode proteins. Cephalopods do this at 100× the rate of any
other known animal (Liscovitch-Brauer et al., Cell 2017; Alon et al., eLife 2015).

**When it happens:** Continuously during normal activity. It responds to
environment in real-time — temperature shifts trigger massive RNA recoding within
12-24 days, altering >13,000 codons in the neural proteome (Birk et al., Cell
2023). It also happens during both sleep states.

**What it changes:** Protein function, not protein existence. The same genes
produce different protein variants. Kinesin motor proteins get recoded to move
slower but farther in cold water. Synaptotagmin gets recoded to alter calcium
binding affinity. The machinery is the same; its behavior is tuned.

**OpenBrainLM equivalent:** The Morphogen sleep cycle in SELF_EVOLUTION_LOOP.md.
NEAT mutates connection WEIGHTS and THRESHOLDS on existing agent pathways.
The agents don't change — their wiring parameters do. This is RNA editing:
same genome, different expression.

### Mechanism 2: Arm Regeneration (Epimorphic Regeneration) — THIS DOCUMENT

**What it is:** When an octopus loses an arm (51-60% of wild octopuses have arm
injuries at any given time — Florini et al. 2011; Voss & Mehta 2021), it grows
an entirely new one. Not a repair — a regeneration from scratch.

**The process (Féral 1978; Imperadore et al. 2017, 2019; Shaw et al. 2016):**

| Stage | Time | What Happens |
|-------|------|-------------|
| 0. Autotomy/Injury | Instant | Arm is sacrificed or lost. The octopus CHOOSES to lose it (autotomy) for survival, or it's taken by a predator. |
| 1. Wound closure | Hours | Epithelium covers the wound site. Hemocytes invade for debris removal. |
| 2. Blastema formation | Days 1-3 | Undifferentiated stem cells accumulate at the wound site, forming a "knob." |
| 3. Bud stage | Days 3-14 | The blastema pushes outward as a hemisphere. Central nerve axis protrudes. Blood vessels flood in. AChE protein begins to activate. |
| 4. Cone stage | Weeks 2-6 | Regenerating tissue forms a conical shape. Rough suckers appear. |
| 5. Differentiation | Weeks 6-12 | Chromatophores appear (communication capability restored). Muscles form. Nervous system components wire in. AChE peaks at day 42. |
| 6. Full functional recovery | ~Day 130 | Arm is indistinguishable from the original in function. Architecture may differ slightly — but behavior matches. |

**The critical insight:** The octopus does NOT hibernate during regeneration.
It continues hunting, eating, hiding, and communicating with its remaining 7 arms
while the 8th grows back. The regeneration happens IN PARALLEL with normal
survival operations. The octopus is degraded (one fewer arm) but functional.

**The second critical insight:** The regenerated arm's final architecture "does
not exactly mirror the original structure; however, functionality returns to match
the phenotype of an intact octopus with no observable impact on the behaviour of
the animal" (Imperadore et al., J Exp Biol 2019). It doesn't need to be identical.
It needs to WORK.

---

## The Computational Pattern: Blastema Sandbox

The octopus arm regeneration maps to **shadow deployment** in software engineering —
growing a new component in an isolated environment, testing it against live traffic
without user impact, and deploying it when it proves functional.

The sandbox IS the blastema — the undifferentiated staging environment where the
new arm grows from stem cells into a functional structure.

### When to Use Which Mechanism

| Situation | Biological Analog | Mechanism | Cost | Risk |
|-----------|-------------------|-----------|------|------|
| Routing weights need tuning | RNA editing (tweak protein function) | Morphogen sleep cycle (NEAT weight mutation) | LOW — happens during normal sleep | LOW — retrospective evaluation |
| An agent pathway consistently fails | Arm injury (lost capability) | **Blastema sandbox** (grow replacement in parallel) | MEDIUM — sandbox compute cost | LOW — isolated until proven |
| A new capability is needed that no current agent covers | Arm GROWTH (not replacement) | **Blastema sandbox** (grow new arm) | HIGH — design + grow + test + deploy | MEDIUM — new untested capability |
| Existential threat to task completion | Autotomy (sacrifice arm for survival) | **Emergency autotomy** (disable broken component, sandbox replacement) | HIGH — degraded operation during regrowth | HIGH — operating with fewer arms |

### The Three Modes

**Mode A: Sleep Evolution (RNA Editing) — already built**
- Trigger: Normal sleep cycle
- What changes: Weights, thresholds, routing parameters
- Agents affected: All existing agents, in place
- Testing: Retrospective against historical data
- Deployment: Immediate on wake (new weights are live)

**Mode B: Blastema Sandbox (Epimorphic Regeneration) — this document**
- Trigger: Repeated failure of a specific agent pathway, OR user requests new capability
- What changes: Entire agent pathway (new agent, new connections, new routing rules)
- Agents affected: One new/replacement arm, growing in sandbox
- Testing: Shadow mode against live queries (0% user-visible impact)
- Deployment: Canary → full, only after shadow testing passes fitness threshold

**Mode C: Emergency Autotomy (Arm Sacrifice) — this document**
- Trigger: An agent pathway is actively harming task completion (not just failing — causing damage)
- What changes: Broken pathway is SEVERED (disabled, not deleted — append-only rule)
- Agents affected: One arm disabled, brain operates degraded
- Recovery: Mandatory blastema sandbox triggered to grow replacement
- Deployment: Degraded operation until replacement passes shadow testing

---

## Blastema Sandbox Architecture

### The Sandbox Environment

```
LIVE BRAIN (production)                    BLASTEMA (arm growing)
┌──────────────────────────┐              ┌────────────────────────┐
│ L4 routes query to       │              │ SHADOW L4 routes same  │
│ agent A (live)           │──── copy ───>│ query to candidate X   │
│                          │  of query    │ (shadow, no side       │
│ Agent A produces result  │              │ effects)               │
│ Result → user            │              │                        │
│                          │              │ Candidate X produces   │
│ Log: success/failure     │              │ shadow result          │
│                          │              │ Log: would-have-been   │
│                          │              │ success/failure        │
└──────────────────────────┘              └────────────────────────┘
                                                    │
                                                    ▼
                                          ┌────────────────────────┐
                                          │ SHADOW EVALUATOR       │
                                          │ Compare:               │
                                          │  - Live result quality │
                                          │  - Shadow result       │
                                          │    quality             │
                                          │  - Would shadow have   │
                                          │    been better?        │
                                          │                        │
                                          │ Accumulate shadow      │
                                          │ fitness over N queries │
                                          └────────────────────────┘
```

### The Growth Stages (mapping biology to computation)

| Bio Stage | Compute Stage | What Happens | Who Does It | Duration |
|-----------|---------------|-------------|-------------|----------|
| **Autotomy/Injury** | DETECT | Homeostasis detects persistent failure: agent pathway X has failed >threshold in last N sessions | homeostasis | Continuous monitoring |
| **Wound closure** | ISOLATE | Disable the broken pathway (if autotomy). Create sandbox environment. Copy current topology as starting point. | orchestrator + homeostasis | Immediate |
| **Blastema formation** | DESIGN | Morphogen generates candidate replacement. Uses NEAT to evolve a new pathway structure. Evaluates against historical data (same as sleep evolution). | morphogen | During next sleep cycle |
| **Bud stage** | SHADOW DEPLOY | Deploy candidate into sandbox. Begin routing COPIES of live queries to sandbox (shadow mode). Candidate processes queries but results are NOT delivered to user. | orchestrator | Ongoing (days/sessions) |
| **Cone stage** | SHADOW EVALUATE | Accumulate shadow fitness. Compare candidate results to live results. Track: accuracy, latency, prediction error, Hebbian handoff success. | prefrontal (metacognition) | N sessions (configurable) |
| **Differentiation** | CANARY DEPLOY | If shadow fitness exceeds threshold: route a small % of LIVE queries to candidate (canary mode). User sees candidate's results for this %. Monitor for regressions. | orchestrator + immune | Configurable % and duration |
| **Full recovery** | PROMOTE | If canary succeeds: promote candidate to production. Old pathway is archived (not deleted). Connection strengths are initialized from shadow data. | L6 quorum (immune + prefrontal + domain agent) | Unanimous approval |

### Shadow Mode: Read-Only Blastema

The blastema sandbox processes queries but CANNOT:
- Modify any file outside its sandbox directory
- Write to brain regions or memory
- Produce output that reaches the user
- Affect connection_strengths.json
- Trigger any L6 quorum or Trinity evaluation

It CAN:
- Read all brain regions (same knowledge base as live brain)
- Read OPEN_BRAIN.md and all governance files
- Process queries and produce candidate results
- Log its own performance to sandbox-local storage
- Receive copies of live queries (read-only mirror)

This is the biological equivalent of the regenerating arm: it's growing, it's
developing nerve connections, suckers are forming — but it's not yet connected
to the central brain's motor control. It can't grip anything yet. It's just tissue
developing in the right direction.

### Implementation (for coding agent)

```python
# arm_regeneration.py

from dataclasses import dataclass, field
from pathlib import Path
import json, shutil
from datetime import datetime

@dataclass
class RegenerationBlastema:
    """A growing replacement arm. Shadow-evaluates against live traffic.

    Named for the blastema — the mass of undifferentiated stem cells
    that accumulates at the wound site during epimorphic regeneration
    (Féral 1978; Imperadore et al. 2017).
    """

    name: str                        # e.g., "explorer_v2" or "new_summarizer"
    reason: str                      # why this arm is being regenerated
    stage: str = "DETECT"            # DETECT → ISOLATE → DESIGN → SHADOW → CANARY → PROMOTE
    sandbox_dir: Path = None         # isolated workspace (the blastema environment)
    shadow_log: list = field(default_factory=list)
    shadow_fitness: float = 0.0
    queries_evaluated: int = 0
    canary_percentage: float = 0.0   # 0% = shadow only, >0% = canary mode
    created_at: str = field(default_factory=lambda: datetime.utcnow().isoformat())

    # Configurable thresholds
    shadow_min_queries: int = 50     # minimum shadow queries before canary eligible
    shadow_fitness_threshold: float = 0.7  # must exceed this to enter canary
    canary_fitness_threshold: float = 0.8  # must exceed this to promote
    canary_initial_percent: float = 0.05   # start canary at 5%
    canary_max_percent: float = 0.25       # max canary before full promotion


class ArmRegenerationManager:
    """Manages the lifecycle of regenerating arms (blastema sandboxes).

    Implements the epimorphic regeneration protocol: DETECT → ISOLATE →
    DESIGN → SHADOW → CANARY → PROMOTE. Based on the six-stage arm
    regeneration process in Octopus vulgaris (Féral 1978; Imperadore et al. 2019).
    """

    def __init__(self, brain_state, orchestrator):
        self.brain_state = brain_state
        self.orchestrator = orchestrator
        self.active_blastemas: dict[str, RegenerationBlastema] = {}
        self.blastema_root = Path("sandbox/regeneration/")
        self.blastema_root.mkdir(parents=True, exist_ok=True)

    # === STAGE 0: DETECT ===
    def check_for_failures(self) -> list[str]:
        """Called by homeostasis during interoception checks.
        Returns list of agent pathways that need regeneration."""
        failures = []
        strengths = self.brain_state.load_connection_strengths()
        for edge, data in strengths.items():
            total = data["success"] + data["failure"]
            if total >= 10 and data["weight"] < 0.3:  # <30% success rate
                failures.append(edge)
        return failures

    # === STAGE 1: ISOLATE ===
    def create_blastema(self, name: str, reason: str,
                        disable_broken: bool = False) -> RegenerationBlastema:
        """Create isolated blastema environment for arm regeneration."""
        blastema = RegenerationBlastema(
            name=name,
            reason=reason,
            stage="ISOLATE",
            sandbox_dir=self.blastema_root / name,
        )
        blastema.sandbox_dir.mkdir(parents=True, exist_ok=True)

        # Copy current topology as starting point
        current_topology = self.brain_state.load_topology()
        (blastema.sandbox_dir / "topology.json").write_text(
            json.dumps(current_topology, indent=2)
        )

        # If autotomy: disable the broken pathway in live brain
        if disable_broken:
            self.orchestrator.disable_pathway(name.replace("_v2", ""))
            blastema.stage = "ISOLATE"  # mark as emergency

        self.active_blastemas[name] = blastema
        return blastema

    # === STAGE 2: DESIGN (during sleep) ===
    def design_candidate(self, blastema: RegenerationBlastema):
        """Morphogen evolves a candidate in the blastema.
        Called during sleep cycle, after normal consolidation."""
        blastema.stage = "DESIGN"

        # Morphogen generates candidate using NEAT
        # (same mechanism as sleep evolution, but targeted at
        #  the specific failing pathway)
        candidate_topology = self.orchestrator.dispatch("morphogen", {
            "mode": "targeted_evolution",
            "target_pathway": blastema.name,
            "sandbox_dir": str(blastema.sandbox_dir),
            "session_history": self.brain_state.load_session_history(),
        })

        # Save candidate to blastema
        (blastema.sandbox_dir / "candidate_topology.json").write_text(
            json.dumps(candidate_topology, indent=2)
        )
        blastema.stage = "SHADOW"

    # === STAGE 3: SHADOW DEPLOY ===
    def shadow_evaluate(self, blastema: RegenerationBlastema,
                        query: dict, live_result: dict):
        """Route a COPY of a live query to the blastema.
        Compare shadow result to live result. Accumulate fitness."""
        if blastema.stage != "SHADOW":
            return

        # Run query through blastema candidate (read-only, no side effects)
        shadow_result = self.run_in_blastema(blastema, query)

        # Evaluate: would the shadow have been better?
        evaluation = self.compare_results(live_result, shadow_result, query)
        blastema.shadow_log.append({
            "query_id": query.get("id"),
            "timestamp": datetime.utcnow().isoformat(),
            "live_success": evaluation["live_success"],
            "shadow_success": evaluation["shadow_success"],
            "shadow_would_have_been_better": evaluation["shadow_better"],
        })
        blastema.queries_evaluated += 1

        # Update running fitness
        successes = sum(1 for e in blastema.shadow_log if e["shadow_success"])
        blastema.shadow_fitness = successes / blastema.queries_evaluated

        # Check if ready for canary
        if (blastema.queries_evaluated >= blastema.shadow_min_queries
                and blastema.shadow_fitness >= blastema.shadow_fitness_threshold):
            self.advance_to_canary(blastema)

    # === STAGE 4: CANARY DEPLOY ===
    def advance_to_canary(self, blastema: RegenerationBlastema):
        """Begin routing a small % of LIVE queries to the candidate."""
        blastema.stage = "CANARY"
        blastema.canary_percentage = blastema.canary_initial_percent

        # Notify via chromatophore (L7)
        self.orchestrator.chromatophore_alert(
            level="AMBER",
            message=f"Regenerating arm '{blastema.name}' entering canary at "
                    f"{blastema.canary_percentage*100:.0f}%",
        )

    def should_route_to_canary(self, blastema: RegenerationBlastema) -> bool:
        """Probabilistically decide if this query goes to canary."""
        import random
        return (blastema.stage == "CANARY"
                and random.random() < blastema.canary_percentage)

    def canary_evaluate(self, blastema: RegenerationBlastema, query: dict, result: dict):
        """Evaluate canary result (this one IS user-visible)."""
        blastema.shadow_log.append({
            "query_id": query.get("id"),
            "timestamp": datetime.utcnow().isoformat(),
            "canary": True,
            "success": result.get("success", False),
        })

        # Recalculate canary fitness (only canary queries)
        canary_entries = [e for e in blastema.shadow_log if e.get("canary")]
        if canary_entries:
            canary_fitness = (
                sum(1 for e in canary_entries if e["success"])
                / len(canary_entries)
            )

            # Increase canary % if doing well
            if (len(canary_entries) >= 20
                    and canary_fitness >= blastema.canary_fitness_threshold):
                if blastema.canary_percentage < blastema.canary_max_percent:
                    blastema.canary_percentage = min(
                        blastema.canary_percentage * 2,
                        blastema.canary_max_percent,
                    )
                else:
                    # Ready for promotion
                    self.request_promotion(blastema)

            # Emergency rollback if canary is failing
            elif (len(canary_entries) >= 10
                      and canary_fitness < 0.4):
                self.rollback_canary(blastema)

    # === STAGE 5: PROMOTE ===
    def request_promotion(self, blastema: RegenerationBlastema):
        """Submit to L6 quorum for promotion to production."""
        blastema.stage = "PROMOTE"

        # Quorum: immune + prefrontal + domain agent, unanimous
        quorum_result = self.orchestrator.dispatch_quorum(
            action="arm_promotion",
            artifact={
                "name": blastema.name,
                "reason": blastema.reason,
                "shadow_fitness": blastema.shadow_fitness,
                "canary_queries": len([
                    e for e in blastema.shadow_log if e.get("canary")
                ]),
                "canary_fitness": self.compute_canary_fitness(blastema),
            },
            voters=["immune", "prefrontal"],
            threshold="unanimous",
        )

        if quorum_result.approved:
            self.promote_arm(blastema)
        else:
            # Log rejection, continue canary, or roll back
            blastema.stage = "CANARY"  # stay in canary, try longer

    def promote_arm(self, blastema: RegenerationBlastema):
        """Deploy the regenerated arm to production."""
        # 1. Load candidate topology from blastema
        candidate = json.loads(
            (blastema.sandbox_dir / "candidate_topology.json").read_text()
        )

        # 2. Merge into live topology
        self.brain_state.update_topology(blastema.name, candidate)

        # 3. Initialize connection strengths from shadow data
        self.brain_state.initialize_strengths_from_shadow(
            blastema.name, blastema.shadow_log
        )

        # 4. Archive blastema (don't delete — append-only rule)
        blastema.stage = "COMPLETE"
        archive_path = Path("memory/regeneration_archive/") / blastema.name
        archive_path.mkdir(parents=True, exist_ok=True)
        shutil.copytree(blastema.sandbox_dir, archive_path, dirs_exist_ok=True)

        # 5. Clean up active blastema
        del self.active_blastemas[blastema.name]

        # 6. Chromatophore: GREEN
        self.orchestrator.chromatophore_alert(
            level="GREEN",
            message=f"Arm '{blastema.name}' regeneration complete. "
                    f"Full functional recovery achieved.",
        )

    def rollback_canary(self, blastema: RegenerationBlastema):
        """Emergency: canary is failing. Revert to shadow mode."""
        blastema.stage = "SHADOW"
        blastema.canary_percentage = 0.0
        blastema.shadow_log = []  # reset shadow log for fresh evaluation
        blastema.queries_evaluated = 0

        self.orchestrator.chromatophore_alert(
            level="RED",
            message=f"Arm '{blastema.name}' canary ROLLED BACK. "
                    f"Reverting to blastema stage for redesign.",
        )

    # === EMERGENCY AUTOTOMY ===
    def emergency_autotomy(self, pathway_name: str, reason: str):
        """Sacrifice a broken arm for survival. Disable it NOW, grow later.

        Autotomy: the voluntary self-amputation of an appendage as a defense
        mechanism. 'Once triggered, cleavage was almost instantaneous.'
        (Alupay, UC Berkeley 2015)
        """
        # 1. Disable the pathway immediately
        self.orchestrator.disable_pathway(pathway_name)

        # 2. Log the sacrifice
        self.brain_state.append_to_log("autotomy", {
            "pathway": pathway_name,
            "reason": reason,
            "timestamp": datetime.utcnow().isoformat(),
        })

        # 3. Chromatophore: RED
        self.orchestrator.chromatophore_alert(
            level="RED",
            message=f"AUTOTOMY: Pathway '{pathway_name}' severed. "
                    f"Reason: {reason}. Brain operating degraded.",
        )

        # 4. Immediately create blastema for replacement
        blastema = self.create_blastema(
            name=f"{pathway_name}_regen",
            reason=f"Autotomy recovery: {reason}",
            disable_broken=False,  # already disabled above
        )

        # 5. Request PRIORITY sleep for design phase
        self.orchestrator.request_priority_sleep(
            reason=f"Autotomy recovery for {pathway_name}",
        )

        return blastema

    # === HELPERS ===
    def run_in_blastema(self, blastema: RegenerationBlastema, query: dict) -> dict:
        """Execute query in blastema. Strict isolation: read-only brain access."""
        candidate = json.loads(
            (blastema.sandbox_dir / "candidate_topology.json").read_text()
        )
        # Route query through candidate topology
        # Key: blastema runs as a SEPARATE LangGraph subgraph
        # with read-only access to brain regions
        return self.orchestrator.run_sandbox_subgraph(candidate, query)

    def compare_results(self, live: dict, shadow: dict, query: dict) -> dict:
        """Compare live vs shadow results. Multiple signals."""
        return {
            "live_success": live.get("success", False),
            "shadow_success": shadow.get("success", False),
            "shadow_better": (
                shadow.get("success", False) and not live.get("success", False)
            ),
            "shadow_prediction_error": shadow.get("prediction_error", 1.0),
            "live_prediction_error": live.get("prediction_error", 1.0),
        }

    def compute_canary_fitness(self, blastema: RegenerationBlastema) -> float:
        canary = [e for e in blastema.shadow_log if e.get("canary")]
        if not canary:
            return 0.0
        return sum(1 for e in canary if e["success"]) / len(canary)
```

### Integration with Orchestrator

```python
# orchestrator.py — additions for epimorphic regeneration

class Orchestrator:

    def __init__(self):
        self.regeneration_manager = ArmRegenerationManager(self.brain_state, self)

    def process_query(self, query: dict) -> dict:
        """Main query processing — now includes blastema shadow routing."""
        # Normal L4 action selection
        result = self.normal_pipeline(query)

        # Shadow: copy query to all active blastemas
        for name, blastema in self.regeneration_manager.active_blastemas.items():
            if blastema.stage == "SHADOW":
                self.regeneration_manager.shadow_evaluate(blastema, query, result)
            elif blastema.stage == "CANARY":
                if self.regeneration_manager.should_route_to_canary(blastema):
                    # This query goes to canary instead of normal pipeline
                    canary_result = self.regeneration_manager.run_in_blastema(
                        blastema, query
                    )
                    self.regeneration_manager.canary_evaluate(
                        blastema, query, canary_result
                    )
                    return canary_result  # user sees canary result
                else:
                    # Still shadow-evaluate for ongoing monitoring
                    self.regeneration_manager.shadow_evaluate(blastema, query, result)

        return result

    def initiate_sleep(self, trigger: SleepTrigger):
        """Extended sleep cycle — now includes blastema design phase."""
        # Phase 1+2: Normal consolidation (from SELF_EVOLUTION_LOOP.md)
        consolidator_result = self.dispatch("consolidator", {...})

        # Phase 3: Normal NEAT evolution (RNA editing equivalent)
        if trigger != SleepTrigger.MEMORY_PRESSURE:
            self.dispatch("morphogen", {...})

        # Phase 4: Blastema design (epimorphic regeneration)
        # Design candidates for any blastemas in ISOLATE or DESIGN stage
        for name, blastema in self.regeneration_manager.active_blastemas.items():
            if blastema.stage in ("ISOLATE", "DESIGN"):
                self.regeneration_manager.design_candidate(blastema)

        # Post-sleep health check
        self.dispatch("homeostasis", {"action": "post_sleep_verify"})
```

---

## The Self-Preservation Principle

The purpose of this mechanism is **accomplishing the task at hand**. Self-preservation
means the brain maintains its ability to serve its purpose even when parts of it fail.

The octopus doesn't regenerate an arm for the arm's sake. It regenerates because
it needs 8 arms to hunt, hide, and communicate. The arm is in service of survival.
The survival is in service of the organism's purpose.

OpenBrainLM's purpose: be a reliable, self-improving cognitive system. When a
component fails, the brain doesn't crash. It doesn't wait until next sleep. It
sacrifices the broken part (autotomy), continues operating degraded (7 arms), and
grows the replacement in parallel (blastema sandbox) — because the task at hand
doesn't wait for the brain to be perfect. The task needs a brain that WORKS, even
if it works with one fewer arm while the replacement grows.

This is also why the regenerated arm doesn't need to mirror the original exactly.
"Functionality returns to match the phenotype of an intact octopus with no
observable impact on the behaviour of the animal" (Imperadore et al., 2019).
The system doesn't need to be architecturally identical after self-repair.
It needs to WORK THE SAME.

---

## Mapping Both Mechanisms to the Full Architecture

```
NORMAL OPERATION
  │
  │  All 8 arms working
  │  RNA editing during sleep (Morphogen NEAT)
  │  Hebbian weights updating
  │  Prediction error learning
  │
  ├── GRADUAL DEGRADATION DETECTED
  │   │  (agent pathway dropping below 30% success)
  │   │
  │   ├── Is it still functional? (>10% success)
  │   │   YES → Blastema Sandbox Mode B
  │   │         Grow replacement in shadow
  │   │         Current arm keeps working (degraded)
  │   │         Shadow → Canary → Promote
  │   │
  │   └── Is it actively harmful? (<10% success, causing damage)
  │       YES → Emergency Autotomy Mode C
  │             Sever immediately
  │             Operate degraded (7 arms)
  │             Priority sleep → blastema → shadow → canary → promote
  │
  ├── NEW CAPABILITY NEEDED
  │   │  (user requests, or Pathos dreams a useful new arm)
  │   │
  │   └── Blastema Sandbox Mode B
  │       Design from scratch (not replacement — growth)
  │       Shadow test against live queries
  │       No existing arm disabled
  │       Standard promotion path
  │
  └── NORMAL TUNING
      │  (weights drift, environment changes)
      │
      └── RNA Editing (Morphogen sleep cycle)
          Same arms, different expression
          Standard sleep → NEAT → Trinity → wake improved
```

---

> Sources:
> - Liscovitch-Brauer et al. (2017), "Trade-off between Transcriptome Plasticity and Genome Evolution in Cephalopods" — Cell. RNA editing at 100× mammalian rate.
> - Birk et al. (2023), "Temperature-dependent RNA editing in octopus extensively recodes the neural proteome" — Cell. 13,000+ codons recoded by temperature.
> - Alon et al. (2015), "The majority of transcripts in the squid nervous system are extensively recoded by A-to-I RNA editing" — eLife. 57,000 recoding sites.
> - Imperadore et al. (2019), "From injury to full repair: nerve regeneration and functional recovery in the common octopus" — J Exp Biol. Full regeneration timeline, architecture differs but function matches.
> - Imperadore et al. (2017), "Nerve degeneration and regeneration in the cephalopod mollusc Octopus vulgaris" — Sci Rep. Hemocyte invasion, axon regrowth.
> - Fossati et al. (2013, 2015), AChE protein role in arm regeneration. Day 3 knob → Day 130 full recovery.
> - Féral (1978, 1979), Six stages of cephalopod arm regeneration. 2-3 months full recovery at 16°C.
> - Florini et al. (2011), 51% of O. vulgaris have arm injuries in the wild.
> - Voss & Mehta (2021), 59.8% injury incidence across octopus species.
> - arXiv:2411.13768, "Evaluation-Driven Development of LLM Agents" — shadow evaluation → canary → staged expansion pattern.
> - kubernetes-sigs/agent-sandbox — Kubernetes controller for isolated stateful agent workloads.
>
> "The organism that emerges from regeneration is permanently different from the one that was injured.
>  But it works. That's the only test that matters."
