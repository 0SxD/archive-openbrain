# OpenBrainLM — Allostatic Decision Gate
> Amendment to EPIMORPHIC_REGENERATION.md §Decision Logic
> Grounded in allostasis (Sterling 2012), autotomy cost-benefit (Bateman & Fleming 2009),
> and octopus nociception/regeneration research (Imperadore et al. 2017, 2019).
> "The default is always: wait for sleep. Everything else is escalation."

---

## The Biological Framework: Allostasis, Not Homeostasis

The decision logic for when to evolve is NOT a homeostatic feedback loop
(detect error → correct error). It is an **allostatic** predictive system.

**Homeostasis** (Cannon, 1932) = error-correction by feedback. Something breaks →
detect deviation from setpoint → apply corrective force. This is reactive, slow,
and inefficient. It only acts after damage has occurred.

**Allostasis** (Sterling, 2012; Schulkin & Sterling, 2019) = predictive regulation.
The brain anticipates needs and prepares to satisfy them BEFORE they arise. It
integrates prior knowledge with current sensing, predicts what resources will be
needed, and pre-positions effectors. Errors are remembered and used to reduce
future errors. "The brain rewards a better-than-predicted result with a pulse of
dopamine, thereby encouraging the organism to learn effective regulatory behaviors"
(Schulkin & Sterling, Trends Neurosci 2019).

**Why this matters for OpenBrainLM:** The homeostasis agent already exists (it
monitors system health). But the DECISION of when to escalate from sleep-cycle
evolution to blastema sandbox to emergency autotomy requires ALLOSTATIC prediction
— not just "is this broken now?" but "given the trajectory, WILL this break before
the next sleep cycle can fix it?"

This is the same distinction as: the amygdala detects threats (L6 Stage 1), but
the prefrontal cortex PREDICTS whether the threat will escalate (L6 Stage 2 +
allostatic computation). The decision gate lives in the prefrontal agent
(metacognition) informed by homeostasis agent (interoception), not in homeostasis
alone.

---

## The Three Biological Decision Signals

Every organism that autotomizes — lizards, crabs, octopuses, sea slugs — makes
the sacrifice based on the same cost-benefit computation, formalized by Bateman
& Fleming (2009) and Arnold (1984) as the **economy of autotomy**:

```
COST of keeping the damaged part   vs   COST of losing it
─────────────────────────────────        ───────────────────
• Energy drain from repair attempts      • Lost capability (fewer arms)
• Risk of infection spreading            • Regeneration energy cost
• Degraded performance of whole system   • Degraded performance during regrowth
• Potential for total system failure      • Predator distraction (severed arm wiggles)
```

The octopus autotomizes when the cost of KEEPING exceeds the cost of LOSING.
Not when the arm is broken. Not when it hurts. When the MATH says: "losing this
arm gives me better survival odds than keeping it."

In OpenBrainLM, the three biological signals map to three computable metrics:

### Signal 1: Is this a parameter problem or a structural problem?

**Biology:** RNA editing (A-to-I recoding) changes protein FUNCTION without changing
protein STRUCTURE. The same gene produces different variants. This works when the
machinery is correct but its tuning is wrong — like kinesin motor proteins being
recoded to move slower in cold water (Birk et al., Cell 2023). When the machinery
ITSELF is damaged — a severed nerve, a lost arm — no amount of RNA editing helps.
The organism needs regeneration, not recoding.

**Computational signal:** Examine the PATTERN of failures in the pathway.

```python
def is_structural_failure(pathway: str, history: list[Session]) -> bool:
    """
    Parameter problem: failures cluster around specific query types.
    The pathway works for some inputs but not others.
    → RNA editing (weight tuning) can fix this.

    Structural problem: failures are CONSISTENT across query types.
    The pathway fails regardless of input characteristics.
    → Epimorphic regeneration (blastema sandbox) is needed.

    Source: RNA editing targets specific codons in response to specific
    environmental conditions (temperature, tissue type). It cannot fix
    a severed nerve. (Liscovitch-Brauer et al., Cell 2017)
    """
    recent = [s for s in history[-5:]]  # last 5 sessions
    if not recent:
        return False

    # Collect failure rates per query-type category
    failure_by_type = defaultdict(list)
    for session in recent:
        for query in session.queries:
            if query.routed_through(pathway):
                failure_by_type[query.category].append(not query.was_successful)

    if not failure_by_type:
        return False

    # Parameter problem: high variance across types (some work, some don't)
    # Structural problem: low variance (all fail roughly equally)
    failure_rates = [
        sum(failures) / len(failures)
        for failures in failure_by_type.values()
        if len(failures) >= 3  # minimum sample
    ]

    if len(failure_rates) < 2:
        return False  # not enough data to distinguish

    variance = statistics.variance(failure_rates)
    mean_failure = statistics.mean(failure_rates)

    # Low variance + high mean failure = structural
    # High variance + moderate mean = parameter (some types fail, others don't)
    STRUCTURAL_VARIANCE_THRESHOLD = 0.05  # failures are uniform across types
    STRUCTURAL_FAILURE_THRESHOLD = 0.50   # failing more than half the time

    return variance < STRUCTURAL_VARIANCE_THRESHOLD and mean_failure > STRUCTURAL_FAILURE_THRESHOLD
```

### Signal 2: Is the failure trajectory worsening faster than sleep can fix?

**Biology:** Allostasis predicts FUTURE states, not just current ones. The brain
doesn't wait for blood pressure to spike — it anticipates the spike and pre-adjusts
(Sterling, Physiol Behav 2012). The key allostatic computation: "given the RATE of
change, will the system exceed its capacity before the next regulatory opportunity?"

In octopuses, RNA editing responds to environmental changes within 12-24 DAYS
(Birk et al., Cell 2023). If the environment changes faster than editing can
track, the organism needs a different strategy. The regeneration pathway exists
precisely for situations where continuous tuning cannot keep up with the rate of
environmental change.

**Computational signal:** Compute the DERIVATIVE of the failure rate across
sessions and project forward to the next sleep cycle.

```python
def is_degrading_faster_than_sleep(
    pathway: str,
    history: list[Session],
    time_to_next_sleep: float,  # estimated seconds until next sleep trigger
) -> tuple[bool, float]:
    """
    Allostatic prediction: given the trajectory, will this pathway
    fail critically before the next sleep cycle can intervene?

    Returns (should_escalate, projected_failure_rate_at_sleep)

    Source: Allostasis predicts needs and prepares before they arise.
    "Errors are reduced in magnitude and frequency" by anticipatory
    regulation. (Sterling, Physiol Behav 2012, p.5)
    """
    # Collect success rates per session (chronological)
    session_rates = []
    for session in history[-10:]:  # last 10 sessions
        pathway_queries = [q for q in session.queries if q.routed_through(pathway)]
        if pathway_queries:
            rate = sum(1 for q in pathway_queries if q.was_successful) / len(pathway_queries)
            session_rates.append((session.timestamp, rate))

    if len(session_rates) < 3:
        return (False, 0.0)  # not enough data for trajectory

    # Linear regression on success rate over time
    times = [t for t, r in session_rates]
    rates = [r for t, r in session_rates]

    # Compute slope (rate of change per session)
    n = len(rates)
    mean_t = sum(range(n)) / n
    mean_r = sum(rates) / n
    slope = (
        sum((i - mean_t) * (r - mean_r) for i, r in enumerate(rates))
        / max(sum((i - mean_t) ** 2 for i in range(n)), 1e-10)
    )

    # Project forward: where will the success rate be at next sleep?
    sessions_until_sleep = max(1, int(time_to_next_sleep / avg_session_duration(history)))
    projected_rate = rates[-1] + slope * sessions_until_sleep

    # Critical threshold: if projected to drop below 20% success by next sleep
    CRITICAL_THRESHOLD = 0.20

    return (projected_rate < CRITICAL_THRESHOLD and slope < -0.05, projected_rate)
```

### Signal 3: Is the failure blocking the task at hand RIGHT NOW?

**Biology:** Autotomy is a response to IMMEDIATE threat — a predator has grabbed
the arm. The octopus doesn't autotomize preemptively. It autotomizes when a
predator already has contact and the choice is: lose the arm or lose your life
(Alupay, 2015; Jaitly et al., 2022). The decision is instantaneous — Alupay
found that "once triggered, cleavage was almost instantaneous" in Abdopus
aculeatus. This is the L6 amygdala fast path, not the slow consensus path.

The critical distinction from biology: "Since the tail plays a significant role in
locomotion and energy storage of fat deposits, it is too valuable to be dropped
haphazardly" (Wikipedia/Autotomy, citing Bateman & Fleming 2009). The organism
delays autotomy as long as possible. The salamander Bolitoglossa rostrata "will
delay autotomy until the predator moves its jaws up the tail or holds on for a
long time" — using its other defenses (toxicity) first, and only sacrificing when
those fail.

**Computational signal:** Is the current user query BLOCKED because the failing
pathway is the ONLY viable route, AND has it already failed on THIS specific query?

```python
def is_blocking_current_task(
    pathway: str,
    current_query: dict,
    topology: Topology,
) -> bool:
    """
    Emergency autotomy trigger: the broken pathway is actively preventing
    task completion right now, and no alternative route exists.

    This is the ONLY trigger that bypasses "wait for sleep."
    It maps to: predator has grabbed the arm, other defenses have failed.

    Source: Autotomy occurs when a predator has already made contact
    and the organism's other defenses (camouflage, ink, flight) have
    failed. It is a LAST RESORT, not a preemptive strategy.
    (Alupay, UC Berkeley 2015; Hanlon et al. 1999)
    """
    # Has the pathway already failed on THIS query?
    if not current_query.get("failed_pathways"):
        return False
    if pathway not in current_query["failed_pathways"]:
        return False

    # Are there alternative routes? (Can the other 7 arms compensate?)
    alternative_agents = topology.find_alternative_routes(
        query_embedding=current_query["embedding"],
        exclude_pathway=pathway,
    )

    # If alternatives exist, the query can be rerouted — no autotomy needed
    if alternative_agents:
        return False

    # No alternatives AND already failed = the predator has the arm
    return True
```

---

## The Decision Gate: Four Tiers of Escalation

The allostatic decision gate evaluates all three signals and selects the
MINIMUM intervention required. This matches the biological principle: organisms
use the cheapest defense first (camouflage → ink → flight → autotomy). They
never autotomize when camouflage would suffice.

```
Query arrives → normal routing → pathway performs
                                       │
                                       ▼
                           HOMEOSTASIS monitors (interoception)
                           PREFRONTAL predicts (allostasis)
                                       │
                    ┌──────────────────┼──────────────────┐
                    ▼                  ▼                  ▼
              Signal 1:           Signal 2:          Signal 3:
            Structural?       Trajectory?        Blocking NOW?
                    │                  │                  │
                    ▼                  ▼                  ▼
              ┌─────────┐      ┌────────────┐     ┌───────────┐
              │Parameter │      │Stable or   │     │Not blocked│
              │problem   │      │improving   │     │(other     │
              │(type-    │      │(slope ≥ 0) │     │ arms ok)  │
              │specific) │      │            │     │           │
              └────┬─────┘      └─────┬──────┘     └─────┬─────┘
                   │                  │                   │
                   ▼                  ▼                   ▼
            ╔═══════════╗     ALL THREE "no"?      ╔═══════════╗
            ║  TIER 0   ║ ──────────────────────── ║  TIER 0   ║
            ║ Wait for  ║  YES = wait for sleep    ║ Wait for  ║
            ║ sleep     ║                          ║ sleep     ║
            ╚═══════════╝                          ╚═══════════╝


              ┌─────────┐      ┌────────────┐     ┌───────────┐
              │Structural│      │Degrading   │     │Not blocked│
              │(uniform  │      │but stable  │     │(other     │
              │across    │      │enough for  │     │ arms ok)  │
              │types)    │      │next sleep  │     │           │
              └────┬─────┘      └─────┬──────┘     └─────┬─────┘
                   │                  │                   │
                   ▼                  ▼                   ▼
            ╔═══════════════════════════════════════════════════╗
            ║  TIER 1: BLASTEMA SANDBOX (grow at next sleep)   ║
            ║  Signal 1 = structural AND (Signal 2 = stable    ║
            ║  OR Signal 3 = not blocking)                     ║
            ║                                                  ║
            ║  Action: create blastema, begin design at next   ║
            ║  sleep cycle. Continue using current pathway     ║
            ║  (degraded but functional). No emergency.        ║
            ║                                                  ║
            ║  Bio analog: Octopus has a healing wound.        ║
            ║  The arm is damaged but still attached. RNA      ║
            ║  editing can't fix it. Regeneration will happen  ║
            ║  naturally during the next rest period.          ║
            ╚═══════════════════════════════════════════════════╝


              ┌─────────┐      ┌────────────┐     ┌───────────┐
              │Structural│      │Degrading   │     │Not yet    │
              │          │      │FAST —      │     │blocking   │
              │          │      │projected   │     │but will   │
              │          │      │to fail     │     │soon       │
              │          │      │before next │     │           │
              │          │      │sleep       │     │           │
              └────┬─────┘      └─────┬──────┘     └─────┬─────┘
                   │                  │                   │
                   ▼                  ▼                   ▼
            ╔═══════════════════════════════════════════════════╗
            ║  TIER 2: PRIORITY SLEEP (self-induced sleep NOW) ║
            ║  Signal 1 = structural AND Signal 2 = degrading  ║
            ║  faster than next scheduled sleep                ║
            ║                                                  ║
            ║  Action: Brain puts itself to sleep NOW.         ║
            ║  Inform user: "I need to consolidate before      ║
            ║  continuing — a component is degrading."         ║
            ║  Run full sleep cycle including blastema design.  ║
            ║  Wake with blastema in shadow mode.              ║
            ║                                                  ║
            ║  Bio analog: The octopus retreats to its den.    ║
            ║  Not because a predator is attacking, but        ║
            ║  because allostatic prediction says: "if I       ║
            ║  don't rest now, I won't be able to handle       ║
            ║  what's coming." Predictive, not reactive.       ║
            ║                                                  ║
            ║  Source: "Efficient regulation requires           ║
            ║  anticipating needs and preparing to satisfy     ║
            ║  them before they arise." (Sterling 2012)        ║
            ╚═══════════════════════════════════════════════════╝


              ┌─────────┐      ┌────────────┐     ┌───────────┐
              │Structural│      │Degrading   │     │ BLOCKING  │
              │(or any)  │      │(or any)    │     │ RIGHT NOW │
              │          │      │            │     │ No alt    │
              │          │      │            │     │ routes    │
              │          │      │            │     │ Available │
              └────┬─────┘      └─────┬──────┘     └─────┬─────┘
                   │                  │                   │
                   ▼                  ▼                   ▼
            ╔═══════════════════════════════════════════════════╗
            ║  TIER 3: EMERGENCY AUTOTOMY (sever NOW)          ║
            ║  Signal 3 = blocking current task AND no         ║
            ║  alternative routes exist                        ║
            ║                                                  ║
            ║  Action: Disable broken pathway IMMEDIATELY.     ║
            ║  Operate degraded. Request priority sleep.       ║
            ║  Blastema replacement at highest priority.       ║
            ║                                                  ║
            ║  Bio analog: Predator has grabbed the arm.       ║
            ║  Camouflage failed. Ink failed. Flight failed.   ║
            ║  AUTOTOMIZE — lose the arm, save the organism.   ║
            ║  "Once triggered, cleavage was almost            ║
            ║  instantaneous." (Alupay 2015)                   ║
            ║                                                  ║
            ║  THIS IS THE ONLY TIER THAT ACTS BETWEEN SLEEPS ║
            ║  AND ONLY BECAUSE THE ALTERNATIVE IS TOTAL       ║
            ║  TASK FAILURE (organism death equivalent).        ║
            ╚═══════════════════════════════════════════════════╝
```

---

## Implementation: The Allostatic Decision Gate

```python
# allostatic_gate.py
from enum import Enum
from dataclasses import dataclass

class EvolutionTier(Enum):
    WAIT_FOR_SLEEP = 0      # RNA editing at next sleep (cheapest)
    BLASTEMA_SANDBOX = 1    # Grow replacement at next sleep (moderate)
    PRIORITY_SLEEP = 2      # Self-induce sleep NOW (expensive)
    EMERGENCY_AUTOTOMY = 3  # Sever NOW, sleep ASAP (most expensive)

@dataclass
class AllostasisResult:
    tier: EvolutionTier
    pathway: str
    rationale: str
    signals: dict
    projected_failure_at_sleep: float | None = None

class AllostaticDecisionGate:
    """
    Allostatic (predictive) decision gate for evolution escalation.

    Principle: The default is ALWAYS Tier 0 (wait for sleep).
    Each higher tier requires STRONGER evidence to trigger.
    The organism uses the cheapest defense first.

    Sources:
    - Sterling (2012), "Allostasis: A model of predictive regulation"
    - Schulkin & Sterling (2019), "Allostasis: A Brain-Centered,
      Predictive Mode of Physiological Regulation"
    - Bateman & Fleming (2009), "Economy of autotomy"
    - Alupay (2015), "Characterization of Arm Autotomy in the Octopus"
    """

    def evaluate(
        self,
        pathway: str,
        current_query: dict | None,
        history: list,    # list[Session]
        topology,         # Topology
        time_to_next_sleep: float,
    ) -> AllostasisResult:

        # === Signal 1: Parameter or structural? ===
        structural = is_structural_failure(pathway, history)

        # === Signal 2: Trajectory — allostatic prediction ===
        degrading, projected = is_degrading_faster_than_sleep(
            pathway, history, time_to_next_sleep
        )

        # === Signal 3: Blocking current task? ===
        blocking = False
        if current_query is not None:
            blocking = is_blocking_current_task(pathway, current_query, topology)

        signals = {
            "structural": structural,
            "degrading_fast": degrading,
            "projected_rate_at_sleep": projected,
            "blocking_now": blocking,
        }

        # === TIER 3: Emergency Autotomy ===
        # Predator has the arm. No other option.
        if blocking:
            return AllostasisResult(
                tier=EvolutionTier.EMERGENCY_AUTOTOMY,
                pathway=pathway,
                rationale=(
                    f"Pathway '{pathway}' is blocking current task completion "
                    f"and no alternative routes exist. Emergency autotomy required. "
                    f"Bio: 'Once triggered, cleavage was almost instantaneous.' "
                    f"(Alupay 2015)"
                ),
                signals=signals,
            )

        # === TIER 2: Priority Sleep ===
        # Structural problem degrading faster than sleep can reach it.
        if structural and degrading:
            return AllostasisResult(
                tier=EvolutionTier.PRIORITY_SLEEP,
                pathway=pathway,
                rationale=(
                    f"Pathway '{pathway}' has structural failure (uniform across "
                    f"query types) AND is degrading faster than next sleep cycle "
                    f"can intervene (projected {projected:.0%} success at next "
                    f"sleep). Self-inducing sleep for blastema design. "
                    f"Bio: Allostatic prediction — 'anticipating needs and "
                    f"preparing to satisfy them before they arise.' "
                    f"(Sterling 2012)"
                ),
                signals=signals,
                projected_failure_at_sleep=projected,
            )

        # === TIER 1: Blastema Sandbox (at next sleep) ===
        # Structural problem but stable enough to wait.
        if structural and not degrading:
            return AllostasisResult(
                tier=EvolutionTier.BLASTEMA_SANDBOX,
                pathway=pathway,
                rationale=(
                    f"Pathway '{pathway}' has structural failure (weight tuning "
                    f"cannot fix) but trajectory is stable enough to wait for "
                    f"next sleep cycle. Blastema will be created during sleep. "
                    f"Bio: Healing wound — damaged but still attached. "
                    f"Regeneration at next rest period."
                ),
                signals=signals,
                projected_failure_at_sleep=projected,
            )

        # === TIER 0: Wait for sleep (default) ===
        return AllostasisResult(
            tier=EvolutionTier.WAIT_FOR_SLEEP,
            pathway=pathway,
            rationale=(
                f"Pathway '{pathway}' — "
                + ("parameter-level failure (type-specific), RNA editing "
                   "(NEAT weight mutation) at next sleep cycle will address. "
                   "Bio: RNA recoding tunes protein function without structural "
                   "change. (Birk et al., Cell 2023)"
                   if not structural
                   else "insufficient data to confirm structural failure. "
                        "Monitoring. Default: wait for sleep.")
            ),
            signals=signals,
        )
```

### Integration with Orchestrator and Homeostasis

```python
# In homeostasis agent — runs as part of interoception (every N queries)
class HomeostasisAgent:

    def interoception_check(self, brain_state, current_query=None):
        """
        Periodic health check. Evaluates all pathways.
        Reports to orchestrator with allostatic recommendation.

        Runs every K queries (configurable, default K=10) and at
        session start (L1 Active Sensing boot).
        """
        gate = AllostaticDecisionGate()
        alerts = []

        for pathway in brain_state.active_pathways():
            result = gate.evaluate(
                pathway=pathway,
                current_query=current_query,
                history=brain_state.session_history,
                topology=brain_state.topology,
                time_to_next_sleep=self.estimate_time_to_sleep(brain_state),
            )

            if result.tier != EvolutionTier.WAIT_FOR_SLEEP:
                alerts.append(result)

        return alerts

    def estimate_time_to_sleep(self, brain_state) -> float:
        """
        Allostatic prediction: when will the next sleep trigger fire?

        Uses cerebellum timing (cross-cutting mechanism) — track
        historical session durations to predict remaining time.

        Source: Ito (2008), cerebellum as prediction machine.
        Wolpert, Miall, & Kawato (1998), internal models.
        """
        avg_session_queries = brain_state.avg_queries_per_session()
        queries_this_session = brain_state.queries_this_session
        remaining = max(1, avg_session_queries - queries_this_session)
        avg_query_time = brain_state.avg_query_duration()
        return remaining * avg_query_time


# In orchestrator — handles allostatic alerts
class Orchestrator:

    def handle_allostatic_alert(self, result: AllostasisResult):
        """Route allostatic decision to appropriate mechanism."""

        if result.tier == EvolutionTier.WAIT_FOR_SLEEP:
            # Log for next sleep cycle. Morphogen will handle.
            self.log_for_sleep("weight_tuning", result)

        elif result.tier == EvolutionTier.BLASTEMA_SANDBOX:
            # Create blastema, but don't start design until sleep.
            self.regeneration_manager.create_blastema(
                name=f"{result.pathway}_regen",
                reason=result.rationale,
            )
            # Chromatophore: AMBER
            self.chromatophore_alert("AMBER",
                f"Structural failure detected in '{result.pathway}'. "
                f"Blastema created. Design will begin at next sleep.")

        elif result.tier == EvolutionTier.PRIORITY_SLEEP:
            # Brain puts itself to sleep NOW.
            self.chromatophore_alert("AMBER",
                f"Allostatic prediction: '{result.pathway}' projected to "
                f"reach {result.projected_failure_at_sleep:.0%} success "
                f"before next sleep. Initiating priority sleep.")
            self.initiate_sleep(SleepTrigger.ALLOSTATIC_PREDICTION)

        elif result.tier == EvolutionTier.EMERGENCY_AUTOTOMY:
            # Sever NOW. No deliberation. Amygdala fast path.
            self.regeneration_manager.emergency_autotomy(
                pathway_name=result.pathway,
                reason=result.rationale,
            )
```

---

## The Biological Justification for Each Tier

| Tier | Bio Analog | Source | When | Cost |
|------|-----------|--------|------|------|
| **0: Wait for sleep** | RNA editing — continuous tuning of protein function without structural change | Liscovitch-Brauer et al. (Cell 2017): coleoids recode 60% of neural mRNAs. Birk et al. (Cell 2023): 13,000+ codons recoded by temperature. | Default. Parameter-level failures. Type-specific patterns. | Lowest. Part of normal sleep cycle. |
| **1: Blastema sandbox** | Wound healing — arm damaged but still attached, regeneration begins at next rest | Féral (1978, 1979): regeneration begins after wound closure, which takes 24h. Imperadore et al. (2017): hemocytes invade wound site, axon regrowth initiated. | Structural failure confirmed. Trajectory stable. Not blocking task. | Moderate. Sandbox compute + shadow evaluation. |
| **2: Priority sleep** | Retreat to den — allostatic prediction of future failure triggers preemptive rest | Sterling (2012): "efficient regulation requires anticipating needs and preparing to satisfy them before they arise." Schulkin & Sterling (2019): "The brain predicts what is likely to be needed; then computes the best response." | Structural failure + degrading faster than next sleep can reach. | High. Interrupts current session. User notified. |
| **3: Emergency autotomy** | Predator has grabbed arm — sacrifice part to save whole | Alupay (2015): autotomy in Abdopus aculeatus, "once triggered, cleavage was almost instantaneous." Bush (2012): economy of autotomy — minimize amount sacrificed. Bateman & Fleming (2009): cost-benefit of autotomy across taxa. | Only route for current task AND already failed on this query. | Highest. Degraded operation. Priority sleep triggered. |

---

## The Default Is Always: Wait for Sleep

This cannot be overstated. In biology:

- Octopuses recode 100,000+ RNA sites continuously. They regenerate arms
  rarely (when forced by injury). The ratio is ~100,000:1 in favor of tuning
  over rebuilding.

- Lizards that lose their tails "have evolved specific behaviors after autotomy,
  such as decreased activity, to compensate for negative consequences such as
  depleted energy resources" (Bateman & Fleming 2009). The cost is real.

- The salamander Bolitoglossa rostrata "will delay autotomy until the predator
  moves its jaws up the tail or holds on for a long time, allowing the salamander
  to retain its tail when toxicity alone can ward off predators." It exhausts
  cheaper defenses first.

In OpenBrainLM: sleep-cycle RNA editing (NEAT weight mutation) is attempted FIRST,
ALWAYS. Only after sleep-cycle evolution has failed to fix the problem (confirmed
by Signal 1 = structural after at least one sleep cycle has attempted repair) does
the system escalate to blastema sandbox. Priority sleep only when allostatic
prediction says the system will degrade beyond repair before normal sleep. Emergency
autotomy only when the user's task is blocked with no alternative.

**The brain that sleeps well rarely needs surgery.**

---

> Sources:
> - Sterling, P. (2012). "Allostasis: A model of predictive regulation."
>   Physiology & Behavior, 106(1), 5-15.
> - Schulkin, J. & Sterling, P. (2019). "Allostasis: A Brain-Centered,
>   Predictive Mode of Physiological Regulation." Trends in Neurosciences,
>   42(10), 740-752.
> - Sterling, P. (2004). "Principles of Allostasis: Optimal Design, Predictive
>   Regulation, Pathophysiology and Rational Therapeutics." In Schulkin, J. (Ed.),
>   Allostasis, Homeostasis, and the Costs of Adaptation. MIT Press.
> - Bateman, P.W. & Fleming, P.A. (2009). "To cut a long tail short: a review
>   of lizard caudal autotomy." Naturwissenschaften, 96(5), 517-28.
> - Arnold, E.N. (1984). "Evolutionary aspects of tail shedding in lizards and
>   their relatives." J. Natural History, 18, 127-169.
> - Bush, S.L. (2012). "Economy of arm autotomy in the mesopelagic squid
>   Octopoteuthis deletron." Mar. Ecol. Prog. Ser., 458, 133-140.
> - Alupay, J.S. (2015). "Characterization of Arm Autotomy in the Octopus,
>   Abdopus aculeatus." PhD dissertation, UC Berkeley.
> - Liscovitch-Brauer, N. et al. (2017). "Trade-off between Transcriptome
>   Plasticity and Genome Evolution in Cephalopods." Cell, 169(2), 191-202.
> - Birk, M.A. et al. (2023). "Temperature-dependent RNA editing in octopus
>   extensively recodes the neural proteome." Cell, 186(12), 2544-2555.
> - Imperadore, P. et al. (2017). "Nerve degeneration and regeneration in the
>   cephalopod mollusc Octopus vulgaris." Scientific Reports, 7, 46564.
> - Imperadore, P. et al. (2019). "From injury to full repair: nerve regeneration
>   and functional recovery in the common octopus." J. Exp. Biol., 222, jeb209965.
> - Féral, J.-P. (1978, 1979). Arm regeneration stages in Sepia officinalis.
> - Ito, M. (2008). "Control of mental activities by internal models in the
>   cerebellum." Nature Reviews Neuroscience, 9, 304-313.
>
> "The brain that sleeps well rarely needs surgery."
