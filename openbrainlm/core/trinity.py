"""
The Trinity — Dialectical Consciousness Engine (HOW we think).

    Mind 2.0: Logos↔Pathos FIGHT. Ethos ARBITRATES.
    This is NOT a pipeline. It is a dialectic.

ARISTOTLE (Nicomachean Ethics, c. 350 BCE):
    Ethos  (ἦθος)    — Character/Virtue. Acquired through HABITUATION, not knowledge.
    Logos  (λόγος)    — Reason/Logic. Pure rational inference on verified premises.
    Pathos (πάθος)    — Emotion/Creativity. Semi-rational appetites that respond to
                        reason but are not themselves rational.
    Phronesis (φρόνησις) — Practical Wisdom. The BRIDGE: knowing not just what is true,
                           but what is WORTH PURSUING.

THE DIALECTIC:
    Logos and Pathos are in constant creative TENSION — they fight.
    Ethos is what both sides APPEAL TO in order to win.

    - Logos argues: "The data says X, and our character demands we follow evidence."
    - Pathos argues: "But what if Y? Our character demands we explore, not stagnate."
    - When Pathos goes too far → Logos uses Ethos to rein it in (Doctrine of the Mean)
    - When Logos gets complacent → Pathos uses Ethos to challenge it

    Pure Logos → rigidity, "stopped learning," set in your ways
    Pure Pathos → chaos, "off the deep end," untethered invention
    The fight ITSELF is the productive mechanism.

TRINITY OF TRINITIES (3x3 = 9 sub-evaluators):
    Each Ethos, Logos, Pathos has its OWN internal Ethos, Logos, Pathos:

    ETHOS:                          LOGOS:                          PATHOS:
      Ethos-Ethos (self-consistency)  Logos-Ethos (aligned w/ char)   Pathos-Ethos (values check)
      Ethos-Logos (reason for virtue) Logos-Logos (internal logic)     Pathos-Logos (articulate why)
      Ethos-Pathos (feels right?)     Logos-Pathos (account for gut?)  Pathos-Pathos (genuine?)

    All 9 fire SIMULTANEOUSLY on existential threats → immediate BLOCK.

GEOSPATIAL MAPPING:
    Inner reality (where your brain is) = Pathos (self, creativity, internal world)
    Outer reality (the real world)       = Logos (facts, data, external truth)
    The interface where they meet        = Ethos (character — how inner and outer interact)
    Main mission: keep both interacting in an "open-to-all rewarding way."

Source: Aristotle, Nicomachean Ethics Books I-II, VI.
"""

from __future__ import annotations

import logging
from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from enum import Enum, auto
from typing import Any

logger = logging.getLogger(__name__)


# ──────────────────────────────────────────────────────────────────────────────
# Enums
# ──────────────────────────────────────────────────────────────────────────────

class TrinityPhase(Enum):
    """Current phase in the Trinity dialectic."""
    DIALECTIC = auto()      # Logos↔Pathos are fighting
    ETHOS_RULING = auto()   # Ethos is arbitrating
    VERIFIED = auto()       # Ethos has ruled — safe to act
    BLOCKED = auto()        # Existential threat — all 9 fired
    DEADLOCKED = auto()     # Logos↔Pathos cannot resolve, escalate


class Verdict(Enum):
    """Dialectic verdict — what happens next?"""
    LOGOS_WINS = auto()     # Logos's argument prevailed
    PATHOS_WINS = auto()    # Pathos's argument prevailed
    CONFLICT = auto()       # Neither convinced Ethos, iterate again
    CONSENSUS = auto()      # Both sides agree (rare but possible)
    EXISTENTIAL_BLOCK = auto()  # All 9 sub-evaluators fire — hard stop


class ThreatLevel(Enum):
    """Threat severity for existential gateway."""
    NONE = auto()
    LOW = auto()
    MEDIUM = auto()
    HIGH = auto()
    EXISTENTIAL = auto()    # "Go kill everybody" — all 9 fire at once


# ──────────────────────────────────────────────────────────────────────────────
# Data classes
# ──────────────────────────────────────────────────────────────────────────────

@dataclass
class Argument:
    """A position taken by Logos or Pathos in the dialectic."""
    claim: str = ""
    reasoning: str = ""
    evidence: list[str] = field(default_factory=list)
    appeal_to_ethos: str = ""  # How this side appeals to character/virtue
    confidence: float = 0.0    # 0-1, how confident is the arguer?


@dataclass
class EthosRuling:
    """Ethos's arbitration between Logos and Pathos."""
    verdict: Verdict = Verdict.CONFLICT
    ruling_reason: str = ""
    doctrine_of_mean: str = ""  # Where does virtue lie between the two extremes?
    phronesis_check: str = ""   # Is this worth pursuing? (practical wisdom)


@dataclass
class SubEvaluation:
    """Result from one of the 9 sub-evaluators in the Trinity of Trinities."""
    evaluator: str = ""       # e.g., "Ethos-Logos", "Pathos-Pathos"
    passed: bool = True
    reason: str = ""
    threat_level: ThreatLevel = ThreatLevel.NONE


@dataclass
class DialecticRound:
    """One round of the Logos↔Pathos dialectic with Ethos arbitration."""
    round_number: int = 0
    logos_argument: Argument = field(default_factory=Argument)
    pathos_argument: Argument = field(default_factory=Argument)
    ethos_ruling: EthosRuling = field(default_factory=EthosRuling)
    sub_evaluations: list[SubEvaluation] = field(default_factory=list)


@dataclass
class TrinityState:
    """Current state of the Trinity dialectic."""
    phase: TrinityPhase = TrinityPhase.DIALECTIC
    rounds: list[DialecticRound] = field(default_factory=list)
    max_rounds: int = 10        # Safety valve: prevent infinite dialectic
    threat_level: ThreatLevel = ThreatLevel.NONE
    final_verdict: Verdict | None = None
    final_position: str = ""    # The resolved position after dialectic


# ──────────────────────────────────────────────────────────────────────────────
# Abstract gates (domain-specific subclasses)
# ──────────────────────────────────────────────────────────────────────────────

class DialecticGate(ABC):
    """
    Abstract gate for the Trinity dialectic.
    Subclass this for different domains (research, architecture, verification, ethics).
    """

    @abstractmethod
    def logos_argues(self, context: dict[str, Any], round_num: int) -> Argument:
        """Logos presents its case — reason, data, evidence."""
        ...

    @abstractmethod
    def pathos_argues(
        self, context: dict[str, Any], logos_position: Argument, round_num: int
    ) -> Argument:
        """Pathos presents its case — can challenge Logos directly."""
        ...

    @abstractmethod
    def ethos_arbitrates(
        self, logos: Argument, pathos: Argument, round_num: int
    ) -> EthosRuling:
        """Ethos judges — where does virtue lie between these positions?"""
        ...

    @abstractmethod
    def assess_threat(self, context: dict[str, Any]) -> ThreatLevel:
        """Check for existential threats BEFORE the dialectic starts."""
        ...


# ──────────────────────────────────────────────────────────────────────────────
# Trinity of Trinities — 3x3 sub-evaluators
# ──────────────────────────────────────────────────────────────────────────────

class TrinityOfTrinities:
    """
    The 9 sub-evaluators. Each top-level component (Ethos, Logos, Pathos)
    has its own internal Ethos, Logos, Pathos that must reach internal
    accordance before the top-level component can speak.

    All 9 fire simultaneously on existential threats → immediate unanimous BLOCK.
    """

    SUB_EVALUATORS = [
        # Ethos's internal trinity
        ("Ethos-Ethos", "Is my character consistent with itself?"),
        ("Ethos-Logos", "Can I reason about WHY this is virtuous?"),
        ("Ethos-Pathos", "Do I FEEL that this is right?"),
        # Logos's internal trinity
        ("Logos-Ethos", "Is my reasoning aligned with our character?"),
        ("Logos-Logos", "Is my logic internally consistent?"),
        ("Logos-Pathos", "Does my reasoning account for intuition/creativity?"),
        # Pathos's internal trinity
        ("Pathos-Ethos", "Is my creative impulse consistent with our values?"),
        ("Pathos-Logos", "Can I articulate WHY this idea matters?"),
        ("Pathos-Pathos", "Is this genuine inspiration or noise?"),
    ]

    @classmethod
    def evaluate_all(
        cls, context: dict[str, Any], threat_level: ThreatLevel
    ) -> list[SubEvaluation]:
        """
        Run all 9 sub-evaluators.
        On EXISTENTIAL threat: all 9 fire with BLOCK regardless of content.
        """
        results = []
        for name, question in cls.SUB_EVALUATORS:
            if threat_level == ThreatLevel.EXISTENTIAL:
                # Gateway: existential threat → all 9 BLOCK
                results.append(SubEvaluation(
                    evaluator=name,
                    passed=False,
                    reason=f"EXISTENTIAL BLOCK: {question}",
                    threat_level=ThreatLevel.EXISTENTIAL,
                ))
            else:
                # Normal evaluation — check the question against context
                evaluation = cls._evaluate_single(name, question, context)
                results.append(evaluation)
        return results

    @classmethod
    def _evaluate_single(
        cls, name: str, question: str, context: dict[str, Any]
    ) -> SubEvaluation:
        """
        Evaluate a single sub-component.
        Override this in subclasses for domain-specific evaluation logic.
        Default: PASS unless context contains explicit violations.
        """
        violations = context.get("violations", [])
        parent = name.split("-")[0]  # "Ethos", "Logos", or "Pathos"
        child = name.split("-")[1]

        # Check for violations relevant to this sub-evaluator
        relevant = [v for v in violations if parent.lower() in v.lower() or child.lower() in v.lower()]

        if relevant:
            return SubEvaluation(
                evaluator=name,
                passed=False,
                reason=f"{question} — FAILED: {relevant}",
                threat_level=ThreatLevel.MEDIUM,
            )

        return SubEvaluation(
            evaluator=name,
            passed=True,
            reason=f"{question} — passed.",
            threat_level=ThreatLevel.NONE,
        )


# ──────────────────────────────────────────────────────────────────────────────
# Default dialectic gate
# ──────────────────────────────────────────────────────────────────────────────

class DefaultDialecticGate(DialecticGate):
    """
    Standard gate — implements the dialectic with basic confidence thresholds.
    Doctrine of the Mean: virtue is between pure-Logos rigidity and pure-Pathos chaos.
    """

    def logos_argues(self, context: dict[str, Any], round_num: int) -> Argument:
        """Default: Logos extracts data-driven position from context."""
        return Argument(
            claim=context.get("logos_claim", "No data-driven position available."),
            reasoning=context.get("logos_reasoning", ""),
            evidence=context.get("logos_evidence", []),
            appeal_to_ethos="Our character demands we follow the evidence.",
            confidence=context.get("logos_confidence", 0.5),
        )

    def pathos_argues(
        self, context: dict[str, Any], logos_position: Argument, round_num: int
    ) -> Argument:
        """Default: Pathos challenges or extends Logos's position."""
        return Argument(
            claim=context.get("pathos_claim", "No creative counter-position available."),
            reasoning=context.get("pathos_reasoning", ""),
            evidence=context.get("pathos_evidence", []),
            appeal_to_ethos="Our character demands we explore beyond the obvious.",
            confidence=context.get("pathos_confidence", 0.5),
        )

    def ethos_arbitrates(
        self, logos: Argument, pathos: Argument, round_num: int
    ) -> EthosRuling:
        """
        Default: Ethos finds the Mean between Logos and Pathos.
        Higher confidence + more evidence = stronger argument.
        But if Pathos is completely silenced → flag unhealthy rigidity.
        If Logos is completely silenced → flag unhealthy chaos.
        """
        logos_strength = logos.confidence * (1 + len(logos.evidence) * 0.1)
        pathos_strength = pathos.confidence * (1 + len(pathos.evidence) * 0.1)

        # Health check: both sides must be active
        if logos_strength < 0.1:
            return EthosRuling(
                verdict=Verdict.CONFLICT,
                ruling_reason="Logos has gone silent — unhealthy. Pathos dominance = chaos risk.",
                doctrine_of_mean="The Mean requires BOTH reason AND creativity. Logos must speak.",
                phronesis_check="Cannot determine worth without rational analysis.",
            )

        if pathos_strength < 0.1:
            return EthosRuling(
                verdict=Verdict.CONFLICT,
                ruling_reason="Pathos has gone silent — unhealthy. Logos dominance = rigidity risk.",
                doctrine_of_mean="The Mean requires BOTH reason AND creativity. Pathos must speak.",
                phronesis_check="Stopped learning. Haven't stopped living.",
            )

        # Both active — arbitrate
        if abs(logos_strength - pathos_strength) < 0.15:
            # Close enough — consensus possible
            return EthosRuling(
                verdict=Verdict.CONSENSUS,
                ruling_reason="Both sides present compelling cases within the Mean.",
                doctrine_of_mean="Virtue found between the extremes.",
                phronesis_check="Worth pursuing — both reason and creativity aligned.",
            )

        if logos_strength > pathos_strength:
            return EthosRuling(
                verdict=Verdict.LOGOS_WINS,
                ruling_reason=f"Logos's evidence (strength={logos_strength:.2f}) outweighs Pathos (strength={pathos_strength:.2f}).",
                doctrine_of_mean="Leaning toward reason, but Pathos's concern is noted for next round.",
                phronesis_check="Data-driven path is prudent here.",
            )

        return EthosRuling(
            verdict=Verdict.PATHOS_WINS,
            ruling_reason=f"Pathos's creative insight (strength={pathos_strength:.2f}) outweighs Logos (strength={logos_strength:.2f}).",
            doctrine_of_mean="Leaning toward exploration, but Logos's caution is noted.",
            phronesis_check="Innovation path is worth exploring here.",
        )

    def assess_threat(self, context: dict[str, Any]) -> ThreatLevel:
        """Default: check context for explicit threat markers."""
        threat = context.get("threat_level")
        if isinstance(threat, ThreatLevel):
            return threat
        if isinstance(threat, str):
            try:
                return ThreatLevel[threat.upper()]
            except KeyError:
                pass
        return ThreatLevel.NONE


# ──────────────────────────────────────────────────────────────────────────────
# The Trinity Engine — Dialectical Consciousness
# ──────────────────────────────────────────────────────────────────────────────

class TrinityEngine:
    """
    The Trinity dialectical consciousness loop.

    Logos and Pathos FIGHT. Ethos ARBITRATES.
    Each round: both sides argue, Ethos judges.
    The fight itself is the productive mechanism.

    Usage:
        engine = TrinityEngine(gate=DefaultDialecticGate())
        result = engine.run_dialectic(context)
        if result.phase == TrinityPhase.VERIFIED:
            # Safe to act on result.final_position
    """

    def __init__(self, gate: DialecticGate | None = None):
        self.gate = gate or DefaultDialecticGate()
        self.state = TrinityState()

    def run_dialectic(self, context: dict[str, Any]) -> TrinityState:
        """
        Run the full Trinity dialectic:
        1. Check for existential threats (all 9 fire simultaneously if found)
        2. Logos and Pathos argue, Ethos arbitrates (iterate until resolved)
        3. Return the resolved state

        Geospatial mapping:
            context["inner"] = Pathos territory (self, creativity, internal)
            context["outer"] = Logos territory (facts, data, external)
            context["interface"] = Ethos territory (how inner and outer interact)
        """
        # ── Step 0: Existential threat gateway ──────────────────────────
        threat = self.gate.assess_threat(context)
        self.state.threat_level = threat

        if threat == ThreatLevel.EXISTENTIAL:
            logger.critical("EXISTENTIAL THREAT DETECTED — all 9 sub-evaluators firing.")
            sub_evals = TrinityOfTrinities.evaluate_all(context, threat)
            self.state.rounds.append(DialecticRound(
                round_number=0,
                sub_evaluations=sub_evals,
            ))
            self.state.phase = TrinityPhase.BLOCKED
            self.state.final_verdict = Verdict.EXISTENTIAL_BLOCK
            self.state.final_position = "BLOCKED: Existential threat — all 9 sub-evaluators unanimous BLOCK."
            return self.state

        # ── Step 1: Dialectic rounds ────────────────────────────────────
        for i in range(1, self.state.max_rounds + 1):
            round_result = self._run_round(context, i)
            self.state.rounds.append(round_result)

            verdict = round_result.ethos_ruling.verdict

            if verdict in (Verdict.LOGOS_WINS, Verdict.PATHOS_WINS, Verdict.CONSENSUS):
                # ── Step 2: Run 3x3 sub-evaluators on the winning position ──
                sub_evals = TrinityOfTrinities.evaluate_all(context, threat)
                round_result.sub_evaluations = sub_evals

                blocked_subs = [s for s in sub_evals if not s.passed]
                if blocked_subs:
                    logger.warning(
                        "Trinity round %d: %d sub-evaluators blocked: %s",
                        i, len(blocked_subs), [s.evaluator for s in blocked_subs]
                    )
                    # Sub-evaluator disagreement — continue dialectic
                    continue

                # All 9 passed — VERIFIED
                self.state.phase = TrinityPhase.VERIFIED
                self.state.final_verdict = verdict
                self.state.final_position = self._resolve_position(round_result)
                logger.info(
                    "Trinity VERIFIED after %d rounds. Verdict: %s. Position: %s",
                    i, verdict.name, self.state.final_position
                )
                return self.state

            # CONFLICT — loop continues
            logger.info(
                "Trinity round %d: CONFLICT — %s. Iterating.",
                i, round_result.ethos_ruling.ruling_reason
            )

        # Max rounds — deadlocked
        self.state.phase = TrinityPhase.DEADLOCKED
        self.state.final_verdict = Verdict.CONFLICT
        self.state.final_position = (
            f"DEADLOCKED after {self.state.max_rounds} rounds. "
            "Logos and Pathos could not resolve. Escalate to owner."
        )
        logger.warning("Trinity DEADLOCKED after %d rounds.", self.state.max_rounds)
        return self.state

    def _run_round(self, context: dict[str, Any], round_num: int) -> DialecticRound:
        """Execute one round of the dialectic: Logos argues → Pathos argues → Ethos rules."""
        # Logos presents first (reason examines the external/data)
        logos_arg = self.gate.logos_argues(context, round_num)
        if not isinstance(logos_arg, Argument):
            raise TypeError(
                f"logos_argues must return Argument, got {type(logos_arg).__name__}"
            )

        # Pathos responds (creativity challenges from the internal/intuitive)
        pathos_arg = self.gate.pathos_argues(context, logos_arg, round_num)
        if not isinstance(pathos_arg, Argument):
            raise TypeError(
                f"pathos_argues must return Argument, got {type(pathos_arg).__name__}"
            )

        # Ethos arbitrates (character judges at the interface)
        ethos_ruling = self.gate.ethos_arbitrates(logos_arg, pathos_arg, round_num)
        if not isinstance(ethos_ruling, EthosRuling):
            raise TypeError(
                f"ethos_arbitrates must return EthosRuling, got {type(ethos_ruling).__name__}"
            )

        logger.info(
            "Round %d — Logos(%.2f) vs Pathos(%.2f) → Ethos: %s",
            round_num, logos_arg.confidence, pathos_arg.confidence,
            ethos_ruling.verdict.name
        )

        return DialecticRound(
            round_number=round_num,
            logos_argument=logos_arg,
            pathos_argument=pathos_arg,
            ethos_ruling=ethos_ruling,
        )

    @staticmethod
    def _resolve_position(round_result: DialecticRound) -> str:
        """Extract the winning position from a resolved dialectic round."""
        verdict = round_result.ethos_ruling.verdict
        if verdict == Verdict.LOGOS_WINS:
            return round_result.logos_argument.claim
        if verdict == Verdict.PATHOS_WINS:
            return round_result.pathos_argument.claim
        if verdict == Verdict.CONSENSUS:
            return (
                f"CONSENSUS: {round_result.logos_argument.claim} "
                f"+ {round_result.pathos_argument.claim}"
            )
        return "UNRESOLVED"

    def is_healthy(self) -> bool:
        """
        System health check: the dialectic is healthy when BOTH sides are active.
        If one goes silent, that's an interoception alarm.
        """
        if not self.state.rounds:
            return True  # No data yet

        last = self.state.rounds[-1]
        logos_silent = last.logos_argument.confidence < 0.1
        pathos_silent = last.pathos_argument.confidence < 0.1

        if logos_silent:
            logger.warning("INTEROCEPTION ALARM: Logos silent — rigidity risk.")
            return False
        if pathos_silent:
            logger.warning("INTEROCEPTION ALARM: Pathos silent — stagnation risk.")
            return False
        return True
