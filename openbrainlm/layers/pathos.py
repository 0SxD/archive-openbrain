"""
L8 — Pathos Layer (Default Mode Network — Human).

Biology: The Default Mode Network (DMN) activates when the brain is NOT focused
on external tasks — daydreaming, mind-wandering, future planning. It's where
creativity happens: connecting unrelated memories, seeing patterns across
domains, imagining possibilities. The DMN is suppressed during focused work
and activates during rest.

The Aristotle Connection (Nicomachean Ethics):
    Pathos (πάθος) = the "semi-rational appetites." They respond to reason
    but are not themselves rational. They generate proposals that MUST pass
    through Ethos before becoming actionable.

Principle: Invention happens in the background, not on demand. But invention
           CANNOT act — it can only propose.

Source: Raichle (2001) — DMN discovery.
        Aristotle, Nicomachean Ethics Books I-II, VI.
        Eliasmith (2013), Ch 7 — SPAUN transform computation module.
"""

from __future__ import annotations

import logging
from dataclasses import dataclass, field
from datetime import datetime
from typing import Any

from openbrainlm.layers.base import Layer, LayerResult, LayerStatus

logger = logging.getLogger(__name__)


# ──────────────────────────────────────────────────────────────────────────────
# Data classes
# ──────────────────────────────────────────────────────────────────────────────

@dataclass
class DreamProposal:
    """
    A creative proposal from the DMN (Pathos).
    Dreams cannot act — they can only propose.
    Must pass through Trinity dialectic (Ethos arbitration) before becoming actionable.
    """
    idea: str
    reasoning: str = ""
    source_regions: list[str] = field(default_factory=list)
    cross_domain_links: list[str] = field(default_factory=list)
    confidence: float = 0.5
    created_at: datetime = field(default_factory=datetime.now)
    verified: bool = False      # Must be set by Trinity/Ethos, not self
    acted_upon: bool = False    # Track if this dream became action


@dataclass
class ConnectionProposal:
    """A proposed link between two brain regions/domains that aren't explicitly connected."""
    region_a: str
    region_b: str
    connection_type: str = ""   # e.g., "shared concept", "complementary methods"
    evidence: str = ""
    strength: float = 0.0       # 0-1, how strong is the proposed link


@dataclass
class ResearchDirection:
    """A proposed research direction from background processing."""
    topic: str
    motivation: str = ""
    relevant_regions: list[str] = field(default_factory=list)
    priority: float = 0.5       # 0-1


@dataclass
class DreamCycleResult:
    """Output from one cycle of the DMN / Pathos layer."""
    proposals: list[DreamProposal] = field(default_factory=list)
    connections: list[ConnectionProposal] = field(default_factory=list)
    research_directions: list[ResearchDirection] = field(default_factory=list)
    cycle_number: int = 0


# ──────────────────────────────────────────────────────────────────────────────
# L8 Layer
# ──────────────────────────────────────────────────────────────────────────────

class PathosLayer(Layer):
    """
    L8: Background invention — the Default Mode Network.

    Pathos = the DMN. It runs when no active task is assigned.

    Pathos CAN:
        - Notice connections between brain regions that aren't explicitly linked
        - Propose new research directions
        - Suggest architectural improvements
        - Cross-pollinate findings across domains
        - Run multiple probes simultaneously

    Pathos CANNOT:
        - Modify any file
        - Execute any action
        - Bypass Ethos/Logos verification
        - Push to any external system

    The dream cycle (Trinity in action):
        1. Pathos proposes: "What if we combined X from region #1 with Y?"
        2. Ethos gathers: "Does X actually work? What does the literature say?"
        3. Logos connects: "If X and Y, then Z follows. Here's the proof."
        4. Only after Ethos ↔ Logos iterate does the proposal become actionable
        5. Phronesis decides: "Is Z worth pursuing?"
    """

    MAX_PROPOSALS = 50

    def __init__(self):
        super().__init__(
            name="Pathos",
            layer_number=8,
            biological_source="Default Mode Network (Human)"
        )
        self._proposals: list[DreamProposal] = []
        self._connections: list[ConnectionProposal] = []
        self._research_directions: list[ResearchDirection] = []
        self._cycle_count: int = 0
        self._active: bool = False  # DMN suppressed during focused work

    @property
    def is_dreaming(self) -> bool:
        """DMN is active when no focused task is running."""
        return self._active

    def activate(self) -> None:
        """Activate DMN — typically when no focused task is assigned."""
        self._active = True
        logger.info("L8: DMN activated — entering dream mode.")

    def suppress(self) -> None:
        """Suppress DMN — focused work takes over."""
        self._active = False
        logger.info("L8: DMN suppressed — entering focused mode.")

    # ── Dream generation ──────────────────────────────────────────────────

    def propose_idea(
        self,
        idea: str,
        reasoning: str = "",
        source_regions: list[str] | None = None,
    ) -> DreamProposal:
        """
        Generate a creative proposal.
        This does NOT execute anything — it only records the idea.
        """
        proposal = DreamProposal(
            idea=idea,
            reasoning=reasoning,
            source_regions=source_regions or [],
        )
        self._proposals.append(proposal)

        # Trim old proposals
        if len(self._proposals) > self.MAX_PROPOSALS:
            self._proposals = self._proposals[-self.MAX_PROPOSALS:]

        logger.info("L8 DREAM: '%s' (from regions: %s)", idea[:80], source_regions or [])
        return proposal

    def propose_connection(
        self,
        region_a: str,
        region_b: str,
        connection_type: str = "",
        evidence: str = "",
    ) -> ConnectionProposal:
        """
        Propose a link between two brain regions/domains.
        Cross-pollination discovery — seeing patterns across domains.
        """
        connection = ConnectionProposal(
            region_a=region_a,
            region_b=region_b,
            connection_type=connection_type,
            evidence=evidence,
        )
        self._connections.append(connection)
        logger.info(
            "L8 CONNECTION: %s ↔ %s (%s)", region_a, region_b, connection_type
        )
        return connection

    def propose_research(
        self,
        topic: str,
        motivation: str = "",
        relevant_regions: list[str] | None = None,
    ) -> ResearchDirection:
        """Propose a new research direction."""
        direction = ResearchDirection(
            topic=topic,
            motivation=motivation,
            relevant_regions=relevant_regions or [],
        )
        self._research_directions.append(direction)
        logger.info("L8 RESEARCH DIRECTION: '%s'", topic[:80])
        return direction

    # ── Dream cycle ───────────────────────────────────────────────────────

    def run_dream_cycle(self, context: dict[str, Any]) -> DreamCycleResult:
        """
        Run one cycle of the DMN.

        In the current implementation (Phase 1), this collects and returns
        all pending proposals. In Phase 2+, this will actively scan brain regions
        and generate cross-domain connection proposals.
        """
        self._cycle_count += 1

        # Collect unverified proposals
        unverified = [p for p in self._proposals if not p.verified and not p.acted_upon]
        recent_connections = self._connections[-10:]  # Last 10
        recent_research = self._research_directions[-5:]  # Last 5

        result = DreamCycleResult(
            proposals=unverified,
            connections=recent_connections,
            research_directions=recent_research,
            cycle_number=self._cycle_count,
        )

        logger.info(
            "L8 DREAM CYCLE #%d: %d proposals, %d connections, %d research directions",
            self._cycle_count, len(unverified), len(recent_connections), len(recent_research),
        )

        return result

    def get_unverified_proposals(self) -> list[DreamProposal]:
        """Get proposals that haven't been verified by Trinity/Ethos yet."""
        return [p for p in self._proposals if not p.verified]

    def mark_verified(self, proposal: DreamProposal, verified: bool = True) -> None:
        """Mark a proposal as verified (or rejected) by Ethos."""
        proposal.verified = verified
        logger.info(
            "L8: Proposal '%s' marked as %s by Ethos",
            proposal.idea[:50], "VERIFIED" if verified else "REJECTED",
        )

    def mark_acted_upon(self, proposal: DreamProposal) -> None:
        """Mark a verified proposal as acted upon."""
        if not proposal.verified:
            logger.warning("L8: Cannot act on unverified proposal '%s'", proposal.idea[:50])
            return
        proposal.acted_upon = True
        logger.info("L8: Proposal '%s' acted upon.", proposal.idea[:50])

    # ── Layer interface ───────────────────────────────────────────────────

    def process(self, context: dict[str, Any]) -> LayerResult:
        """
        L8 processing: run dream cycle if DMN is active.
        Always READY — the DMN never blocks (it can't act, only propose).

        But it DOES suppress itself during focused work — check context for
        active_task to determine whether to dream or stay quiet.
        """
        active_task = context.get("active_task", "")

        if active_task:
            # Focused work — suppress DMN
            if self._active:
                self.suppress()
            return LayerResult(
                layer_name=self.name,
                status=LayerStatus.BYPASSED,
                data={
                    "dreaming": False,
                    "reason": f"Suppressed during focused task: {active_task}",
                    "pending_proposals": len(self.get_unverified_proposals()),
                },
            )

        # No focused task — activate DMN
        if not self._active:
            self.activate()

        cycle = self.run_dream_cycle(context)

        return LayerResult(
            layer_name=self.name,
            status=LayerStatus.ACTIVE,
            data={
                "dreaming": True,
                "cycle_number": cycle.cycle_number,
                "proposals": len(cycle.proposals),
                "connections": len(cycle.connections),
                "research_directions": len(cycle.research_directions),
            },
        )

    def describe(self) -> str:
        return (
            "Default Mode Network: activates when no focused task is running. "
            "Generates creative proposals, cross-domain connections, and research "
            "directions. Dreams but CANNOT act — all proposals must pass through "
            "Trinity dialectic (Ethos arbitration) before becoming actionable. "
            "Pure Pathos = chaos. The fight with Logos IS the productive mechanism."
        )
