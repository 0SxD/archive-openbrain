"""
L4 — Action Selection Layer (Basal Ganglia + Thalamus — Human).

Biology: The basal ganglia selects actions through INHIBITION, not excitation.
Default state: GPi (Globus Pallidus internal) INHIBITS all actions via tonic
firing. An action is selected when the direct pathway RELEASES inhibition.

Three pathways:
    1. Direct (Go): Striatum → GPi inhibition released → action proceeds
    2. Hyperdirect (Global Stop): STN → GPi excites ALL → everything suppressed
    3. Indirect (No-Go): Striatum → GPe → STN → GPi → selective suppression

The thalamus then GATES information flow: once released, thalamus routes
signals between cortical areas.

Principle: Default = everything suppressed. Actions are RELEASED from
           inhibition, not activated. Fundamentally safer than activation.

Source: Eliasmith (2013), Ch 5 — basal ganglia action selection in SPAUN.
        Stewart, Choo, & Eliasmith (2010) — spiking neuron BG implementation.
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

class RoutingMode(Enum):
    """Thalamic gating mode — how broadly to route."""
    TONIC = auto()   # Familiar input → precise single-agent routing
    BURST = auto()   # Novel input → broad multi-agent routing


class Pathway(Enum):
    """Basal ganglia pathways."""
    DIRECT = auto()      # Go — release inhibition on winner
    INDIRECT = auto()    # No-Go — selective suppression
    HYPERDIRECT = auto() # Global Stop — suppress ALL, escalate


@dataclass
class ActionChannel:
    """
    A single action channel in the basal ganglia.
    Each agent/action has a channel. Default = SUPPRESSED.
    """
    channel_id: str
    agent_name: str
    domain_keywords: list[str] = field(default_factory=list)
    salience: float = 0.0       # Computed per query
    suppressed: bool = True     # Default: GPi tonic inhibition
    hebbian_weight: float = 1.0 # Learned from connection_strengths


@dataclass
class SelectionResult:
    """Result of the basal ganglia action selection process."""
    pathway_used: Pathway
    mode: RoutingMode
    released_channels: list[str] = field(default_factory=list)
    suppressed_channels: list[str] = field(default_factory=list)
    salience_scores: dict[str, float] = field(default_factory=dict)
    escalated: bool = False  # True if hyperdirect fired


# ──────────────────────────────────────────────────────────────────────────────
# L4 Layer
# ──────────────────────────────────────────────────────────────────────────────

class BasalGangliaLayer(Layer):
    """
    L4: Inhibition-based action selection.

    Default: ALL channels suppressed (GPi tonic inhibition).
    Query arrives → compute salience per channel → release winner(s).
    Threat detected → hyperdirect pathway → ALL re-suppressed → escalate to L6.
    """

    # Threshold: channel must have salience >= this fraction of max to be released
    RELEASE_THRESHOLD = 0.5
    # Minimum absolute salience to be considered at all
    MIN_SALIENCE = 0.1

    def __init__(self):
        super().__init__(
            name="ActionSelection",
            layer_number=4,
            biological_source="Basal Ganglia + Thalamus (Human)"
        )
        self._channels: dict[str, ActionChannel] = {}

    def register_channel(self, channel: ActionChannel) -> None:
        """Register an action channel (one per agent)."""
        channel.suppressed = True  # Always start suppressed
        self._channels[channel.channel_id] = channel
        logger.info(
            "L4: Registered channel '%s' (%s) — SUPPRESSED by default",
            channel.agent_name, channel.channel_id,
        )

    def compute_salience(self, query: str, domain_hint: str = "") -> dict[str, float]:
        """
        Compute salience score for each channel given a query.
        Phase 1: keyword matching + Hebbian weight.
        Future: semantic-router embeddings (Phase 2), PyMDP (Phase 3).
        """
        scores = {}
        query_lower = query.lower()
        domain_lower = domain_hint.lower()

        for cid, channel in self._channels.items():
            score = 0.0
            for keyword in channel.domain_keywords:
                kw_lower = keyword.lower()
                if kw_lower in query_lower:
                    score += 1.0
                if domain_lower and kw_lower in domain_lower:
                    score += 0.5
                # Partial word matching
                for word in kw_lower.split():
                    if len(word) > 3 and word in query_lower:
                        score += 0.3

            # Apply Hebbian weight (learned connection strength)
            score *= channel.hebbian_weight
            scores[cid] = score

        return scores

    def select_action(
        self, query: str, domain_hint: str = "", threat_detected: bool = False
    ) -> SelectionResult:
        """
        Run the basal ganglia selection process.

        1. If threat: hyperdirect pathway → suppress ALL → escalate
        2. Compute salience for each channel
        3. Release channels above threshold (direct pathway)
        4. Determine routing mode (tonic vs burst)
        """
        # ── Hyperdirect pathway: threat → global stop ────────────────────
        if threat_detected:
            logger.warning("L4: HYPERDIRECT — threat detected, ALL channels suppressed.")
            for channel in self._channels.values():
                channel.suppressed = True
            return SelectionResult(
                pathway_used=Pathway.HYPERDIRECT,
                mode=RoutingMode.TONIC,
                suppressed_channels=list(self._channels.keys()),
                escalated=True,
            )

        # ── Compute salience ─────────────────────────────────────────────
        scores = self.compute_salience(query, domain_hint)
        positive_scores = {k: v for k, v in scores.items() if v > self.MIN_SALIENCE}

        if not positive_scores:
            # No match — burst mode (broad routing)
            logger.info("L4: No salience match — BURST mode, releasing all channels.")
            released = list(self._channels.keys())
            for cid in released:
                self._channels[cid].suppressed = False
                self._channels[cid].salience = 0.0
            return SelectionResult(
                pathway_used=Pathway.DIRECT,
                mode=RoutingMode.BURST,
                released_channels=released,
                salience_scores=scores,
            )

        # ── Direct pathway: release winners above threshold ──────────────
        max_score = max(positive_scores.values())
        threshold = max_score * self.RELEASE_THRESHOLD

        released = []
        suppressed = []
        for cid, score in scores.items():
            channel = self._channels[cid]
            if score >= threshold:
                channel.suppressed = False
                channel.salience = score
                released.append(cid)
            else:
                channel.suppressed = True
                channel.salience = score
                suppressed.append(cid)

        # Determine mode: 1 winner = tonic, multiple = burst
        mode = RoutingMode.TONIC if len(released) == 1 else RoutingMode.BURST

        logger.info(
            "L4: DIRECT pathway — released %d channel(s) [%s], mode=%s, max_salience=%.2f",
            len(released),
            ", ".join(self._channels[c].agent_name for c in released),
            mode.name, max_score,
        )

        return SelectionResult(
            pathway_used=Pathway.DIRECT,
            mode=mode,
            released_channels=released,
            suppressed_channels=suppressed,
            salience_scores=scores,
        )

    def update_hebbian(self, channel_id: str, success: bool, amount: float = 0.1) -> None:
        """
        Update Hebbian weight for a channel after use.
        Success → strengthen (potentiate). Failure → weaken (depress).
        """
        if channel_id not in self._channels:
            return
        channel = self._channels[channel_id]
        if success:
            channel.hebbian_weight = min(channel.hebbian_weight + amount, 3.0)
        else:
            channel.hebbian_weight = max(channel.hebbian_weight - amount, 0.1)
        logger.info(
            "L4: Hebbian update '%s': %s → weight=%.2f",
            channel.agent_name,
            "POTENTIATE" if success else "DEPRESS",
            channel.hebbian_weight,
        )

    def suppress_all(self) -> None:
        """Emergency: re-suppress all channels (hyperdirect equivalent)."""
        for channel in self._channels.values():
            channel.suppressed = True
        logger.warning("L4: ALL channels re-suppressed (hyperdirect emergency).")

    def process(self, context: dict[str, Any]) -> LayerResult:
        """
        L4 processing: select action channel(s) for the given query.
        Returns BLOCKED if no channels registered or threat escalation.
        """
        query = context.get("query", "")
        domain = context.get("domain", "")
        threat = context.get("threat_detected", False)

        if not self._channels:
            return LayerResult(
                layer_name=self.name,
                status=LayerStatus.BLOCKED,
                blocked_reason="No action channels registered in basal ganglia.",
            )

        result = self.select_action(query, domain_hint=domain, threat_detected=threat)

        if result.escalated:
            return LayerResult(
                layer_name=self.name,
                status=LayerStatus.BLOCKED,
                data={
                    "pathway": result.pathway_used.name,
                    "mode": result.mode.name,
                    "escalated": True,
                },
                blocked_reason="HYPERDIRECT: threat detected — all channels suppressed, escalating to L6.",
            )

        if not result.released_channels:
            return LayerResult(
                layer_name=self.name,
                status=LayerStatus.BLOCKED,
                data={
                    "pathway": result.pathway_used.name,
                    "salience_scores": result.salience_scores,
                },
                blocked_reason="No channels released — inhibition-by-default holds.",
            )

        return LayerResult(
            layer_name=self.name,
            status=LayerStatus.READY,
            data={
                "pathway": result.pathway_used.name,
                "mode": result.mode.name,
                "released": result.released_channels,
                "released_agents": [
                    self._channels[c].agent_name for c in result.released_channels
                ],
                "salience_scores": result.salience_scores,
            },
        )

    def describe(self) -> str:
        return (
            "Basal ganglia action selection: GPi tonic inhibition suppresses ALL "
            "actions by default. The direct pathway RELEASES inhibition on the "
            "winning channel. Hyperdirect pathway re-suppresses everything on "
            "threat detection. Actions are RELEASED, not activated — fundamentally "
            "safer than an activation model."
        )
