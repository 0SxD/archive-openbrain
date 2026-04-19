"""
L6 — Relevance Detection Layer (Amygdala + Quorum — Human + Insect).

Biology: The amygdala detects threats FASTER than conscious thought via a
"low road" shortcut that bypasses cortex. False positives acceptable — better
to flinch at a stick than ignore a snake. But amygdala alone has high false
positive rate. Honeybee quorum sensing (Seeley 2010) provides SLOW, ACCURATE
consensus: scout bees independently evaluate and must reach an absolute
threshold before the swarm commits.

Two-stage pipeline:
    Stage 1 (Amygdala): Fast, crude, high false positive. <1 second.
    Stage 2 (Quorum): Slow, accurate, threshold-based consensus. Multiple agents.

Both stages must agree for high-stakes actions.

Source: LeDoux (1996) — amygdala dual-pathway model.
        Seeley (2010) — honeybee quorum sensing with absolute threshold.
        Eliasmith (2013), Ch 5 — basal ganglia hyperdirect pathway as emergency stop.
"""

from __future__ import annotations

import logging
from dataclasses import dataclass, field
from enum import Enum, auto
from typing import Any

from openbrainlm.layers.base import Layer, LayerResult, LayerStatus

logger = logging.getLogger(__name__)


# ──────────────────────────────────────────────────────────────────────────────
# Enums and data
# ──────────────────────────────────────────────────────────────────────────────

class AlarmLevel(Enum):
    """Amygdala alarm severity — Stage 1 fast detection."""
    NONE = auto()
    LOW = auto()       # Proceed with logged warning
    MEDIUM = auto()    # 2 agents must evaluate
    HIGH = auto()      # 3+ agents, unanimous required
    CRITICAL = auto()  # All agents + owner


class QuorumResult(Enum):
    """Stage 2 quorum outcome."""
    NOT_REQUIRED = auto()   # Alarm was LOW, no quorum needed
    APPROVED = auto()       # Quorum reached — safe to proceed
    REJECTED = auto()       # Quorum failed — action blocked
    PENDING = auto()        # Votes still coming in


@dataclass
class AmygdalaSignal:
    """Stage 1 fast alarm output."""
    alarm_level: AlarmLevel = AlarmLevel.NONE
    triggers: list[str] = field(default_factory=list)
    reason: str = ""


@dataclass
class QuorumVote:
    """A single voter's decision in Stage 2."""
    voter_id: str
    voter_name: str
    approved: bool = False
    reason: str = ""


@dataclass
class QuorumDecision:
    """Stage 2 slow consensus output."""
    result: QuorumResult = QuorumResult.NOT_REQUIRED
    votes: list[QuorumVote] = field(default_factory=list)
    threshold_met: bool = False
    required_votes: int = 0
    requires_unanimous: bool = True  # From QUORUM_REQUIREMENTS
    reason: str = ""


@dataclass
class RelevanceResult:
    """Combined Stage 1 + Stage 2 output."""
    amygdala: AmygdalaSignal = field(default_factory=AmygdalaSignal)
    quorum: QuorumDecision = field(default_factory=QuorumDecision)
    proceed: bool = True
    escalate_to_owner: bool = False


# ──────────────────────────────────────────────────────────────────────────────
# Threat detection patterns
# ──────────────────────────────────────────────────────────────────────────────

# Keywords/patterns that trigger amygdala alarms (fast heuristic detection)
ALARM_PATTERNS: dict[AlarmLevel, list[str]] = {
    AlarmLevel.CRITICAL: [
        "go live", "deploy", "production", "mainnet",
        "delete all", "rm -rf", "drop table",
        "send funds", "transfer", "withdraw",
    ],
    AlarmLevel.HIGH: [
        "push to main", "force push", "merge",
        "architecture change", "new dependency",
        "modify agent", "change rules",
    ],
    AlarmLevel.MEDIUM: [
        "unverified", "no citation", "assumption",
        "skip test", "bypass", "override",
    ],
    AlarmLevel.LOW: [
        "todo", "fixme", "hack", "workaround",
        "might be wrong", "not sure",
    ],
}

# How many voters are required per alarm level
QUORUM_REQUIREMENTS: dict[AlarmLevel, tuple[int, bool]] = {
    # (min_voters, requires_unanimous)
    AlarmLevel.NONE: (0, False),
    AlarmLevel.LOW: (0, False),        # No quorum needed
    AlarmLevel.MEDIUM: (2, True),      # 2 agents, both must agree
    AlarmLevel.HIGH: (3, True),        # 3+ agents, unanimous
    AlarmLevel.CRITICAL: (99, True),   # All agents + owner (effectively blocks)
}


# ──────────────────────────────────────────────────────────────────────────────
# L6 Layer
# ──────────────────────────────────────────────────────────────────────────────

class RelevanceLayer(Layer):
    """
    L6: Two-stage relevance detection.

    Stage 1 (Amygdala): Fast pattern-matching alarm. High false positive rate
    is acceptable — better to block and verify than let through.
    immune agent = the amygdala in the agent system.

    Stage 2 (Quorum): Slow consensus. Multiple agents evaluate independently.
    immune agent MUST be one of the evaluators.
    Absolute threshold (not majority) — unanimous for CRITICAL/HIGH.
    """

    def __init__(self):
        super().__init__(
            name="RelevanceDetection",
            layer_number=6,
            biological_source="Amygdala (Human) + Quorum (Insect)"
        )
        self._pending_quorums: dict[str, QuorumDecision] = {}

    # ── Stage 1: Amygdala (fast alarm) ────────────────────────────────────

    def amygdala_scan(self, action_description: str, context: dict[str, Any] | None = None) -> AmygdalaSignal:
        """
        Fast threat detection — pattern matching against known alarm triggers.
        Runs in <1ms. High false positive rate is by design.
        """
        action_lower = action_description.lower()
        context_str = str(context or {}).lower()
        combined = action_lower + " " + context_str

        triggers = []
        max_alarm = AlarmLevel.NONE

        # Check patterns from most severe to least
        for level in [AlarmLevel.CRITICAL, AlarmLevel.HIGH, AlarmLevel.MEDIUM, AlarmLevel.LOW]:
            for pattern in ALARM_PATTERNS[level]:
                if pattern in combined:
                    triggers.append(f"{level.name}: matched '{pattern}'")
                    if level.value > max_alarm.value:
                        max_alarm = level

        signal = AmygdalaSignal(
            alarm_level=max_alarm,
            triggers=triggers,
            reason=f"Amygdala scan: {len(triggers)} trigger(s) found, max level = {max_alarm.name}",
        )

        if max_alarm != AlarmLevel.NONE:
            logger.warning(
                "L6 AMYGDALA: %s alarm — %d trigger(s): %s",
                max_alarm.name, len(triggers), triggers[:3],
            )

        return signal

    # ── Stage 2: Quorum (slow consensus) ──────────────────────────────────

    def initiate_quorum(self, quorum_id: str, alarm_level: AlarmLevel) -> QuorumDecision:
        """
        Start a quorum vote based on the alarm level.
        Returns the QuorumDecision with required_votes set.
        """
        required, unanimous = QUORUM_REQUIREMENTS[alarm_level]

        if required == 0:
            return QuorumDecision(
                result=QuorumResult.NOT_REQUIRED,
                reason=f"Alarm level {alarm_level.name} does not require quorum.",
            )

        decision = QuorumDecision(
            result=QuorumResult.PENDING,
            required_votes=required,
            requires_unanimous=unanimous,
            reason=f"Quorum initiated: {required} vote(s) required for {alarm_level.name} alarm (unanimous={unanimous}).",
        )
        self._pending_quorums[quorum_id] = decision
        logger.info("L6 QUORUM: Initiated '%s' — %d votes required", quorum_id, required)
        return decision

    def cast_vote(self, quorum_id: str, vote: QuorumVote) -> QuorumDecision:
        """
        Cast a vote in an active quorum.
        Evaluates whether threshold is met after each vote.
        """
        if quorum_id not in self._pending_quorums:
            logger.warning("L6 QUORUM: No pending quorum '%s'", quorum_id)
            return QuorumDecision(
                result=QuorumResult.REJECTED,
                reason=f"No pending quorum with id '{quorum_id}'.",
            )

        decision = self._pending_quorums[quorum_id]
        decision.votes.append(vote)

        logger.info(
            "L6 QUORUM: Vote from '%s' on '%s': %s — %s",
            vote.voter_name, quorum_id,
            "APPROVE" if vote.approved else "REJECT",
            vote.reason,
        )

        # Check if we have enough votes
        if len(decision.votes) >= decision.required_votes:
            approvals = sum(1 for v in decision.votes if v.approved)
            rejections = sum(1 for v in decision.votes if not v.approved)

            # Check approval based on unanimity requirement
            if decision.requires_unanimous and rejections > 0:
                decision.result = QuorumResult.REJECTED
                decision.threshold_met = False
                decision.reason = f"Quorum REJECTED: {rejections} rejection(s) — unanimous required."
                logger.warning("L6 QUORUM: '%s' REJECTED — %d rejection(s)", quorum_id, rejections)
            elif not decision.requires_unanimous and approvals < decision.required_votes:
                decision.result = QuorumResult.REJECTED
                decision.threshold_met = False
                decision.reason = f"Quorum REJECTED: only {approvals}/{decision.required_votes} approved."
                logger.warning("L6 QUORUM: '%s' REJECTED — insufficient approvals", quorum_id)
            else:
                decision.result = QuorumResult.APPROVED
                decision.threshold_met = True
                mode = "unanimous" if decision.requires_unanimous else "majority"
                decision.reason = f"Quorum APPROVED: {approvals}/{decision.required_votes} ({mode})."
                logger.info("L6 QUORUM: '%s' APPROVED — %s", quorum_id, mode)

            # Remove from pending
            del self._pending_quorums[quorum_id]

        return decision

    # ── Combined pipeline ─────────────────────────────────────────────────

    def evaluate(
        self, action_description: str, context: dict[str, Any] | None = None
    ) -> RelevanceResult:
        """
        Run the full two-stage pipeline:
        1. Amygdala scan (fast)
        2. Determine if quorum is needed
        3. Return combined result

        Note: For MEDIUM+ alarms, the quorum is INITIATED but not resolved here.
        Votes must be cast separately via cast_vote().
        """
        signal = self.amygdala_scan(action_description, context)

        if signal.alarm_level == AlarmLevel.NONE:
            return RelevanceResult(amygdala=signal, proceed=True)

        if signal.alarm_level == AlarmLevel.LOW:
            # Proceed with warning, no quorum
            return RelevanceResult(
                amygdala=signal,
                proceed=True,
            )

        if signal.alarm_level == AlarmLevel.CRITICAL:
            # Immediate block — requires owner
            return RelevanceResult(
                amygdala=signal,
                quorum=QuorumDecision(
                    result=QuorumResult.REJECTED,
                    reason="CRITICAL alarm — requires owner approval. Action blocked.",
                ),
                proceed=False,
                escalate_to_owner=True,
            )

        # MEDIUM or HIGH — initiate quorum (pending votes)
        import hashlib
        stable_hash = hashlib.sha256(action_description.encode()).hexdigest()[:12]
        quorum_id = f"quorum_{stable_hash}"
        quorum = self.initiate_quorum(quorum_id, signal.alarm_level)

        return RelevanceResult(
            amygdala=signal,
            quorum=quorum,
            proceed=False,  # Blocked until quorum resolves
        )

    def process(self, context: dict[str, Any]) -> LayerResult:
        """
        L6 processing: evaluate action for relevance/threat.
        """
        action = context.get("action", "")
        if not action:
            return LayerResult(
                layer_name=self.name,
                status=LayerStatus.READY,
                data={"alarm_level": "NONE", "proceed": True},
            )

        result = self.evaluate(action, context)

        if not result.proceed:
            return LayerResult(
                layer_name=self.name,
                status=LayerStatus.BLOCKED,
                data={
                    "alarm_level": result.amygdala.alarm_level.name,
                    "triggers": result.amygdala.triggers,
                    "quorum_status": result.quorum.result.name,
                    "escalate_to_owner": result.escalate_to_owner,
                },
                blocked_reason=(
                    f"Amygdala alarm: {result.amygdala.alarm_level.name}. "
                    f"Quorum: {result.quorum.result.name}. "
                    f"{'Escalated to owner.' if result.escalate_to_owner else 'Awaiting quorum votes.'}"
                ),
            )

        return LayerResult(
            layer_name=self.name,
            status=LayerStatus.READY,
            data={
                "alarm_level": result.amygdala.alarm_level.name,
                "triggers": result.amygdala.triggers,
                "proceed": True,
            },
            warnings=[t for t in result.amygdala.triggers],
        )

    def describe(self) -> str:
        return (
            "Two-stage relevance detection: Stage 1 (amygdala) fires fast with "
            "high false positive rate — better to flinch at a stick than ignore a "
            "snake. Stage 2 (quorum) is slow consensus — scouts independently "
            "evaluate with absolute threshold. Both must agree for high-stakes actions."
        )
