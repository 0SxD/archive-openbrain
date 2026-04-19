"""
Hippocampus — Memory Routing Agent.

The hippocampus of the OpenBrainLM system.
Implements L5 Memory's long-term storage tier via brain regions (local knowledge stores).

Biology: The hippocampus converts short-term memories into long-term storage
during consolidation. It replays experiences, decides what to keep,
strengthens important connections (Hebbian), and discards noise.
In SPAUN (Eliasmith 2013), working memory uses Ordinal Serial Encoding
with gated integrator circuits in the prefrontal cortex.

What Hippocampus does:
    1. ROUTE queries to the correct brain region(s) based on domain/topic
       (semantic routing via L4 basal ganglia salience, not brute search)
    2. MULTI-REGION fan-out — some queries hit multiple brain regions, merge results
    3. SESSION management — maintain brain region sessions for multi-turn research
    4. OPEN_BRAIN.md sync — ensure every brain region has the latest copy
    5. FRESHNESS checks — flag sources >1 month old for refresh (pheromone decay)
    6. QUARANTINE staging — new research → quarantine region first → then promote
    7. CONSOLIDATION — move verified knowledge between tiers (working → short → long)

Named for the biological function it IS (Rule #7).
    This agent IS the interface between OpenBrainLM (the architecture)
    and the local knowledge store (brain regions). Mind ↔ Brain.

Principle: Brain regions are knowledge stores, not file cabinets.
    Routing > brute-force probability.

Source: Eliasmith (2013), Ch 6 — gated integrators for working memory, STDP
        for long-term potentiation. Ch 7 — SPAUN's OSE working memory module.
"""

from __future__ import annotations

import logging
from dataclasses import dataclass, field
from datetime import datetime, timedelta
from enum import Enum, auto
from typing import Any

from openbrainlm.layers.base import Layer, LayerResult, LayerStatus

logger = logging.getLogger(__name__)


# ──────────────────────────────────────────────────────────────────────────────
# Constants
# ──────────────────────────────────────────────────────────────────────────────

PHEROMONE_DECAY_DAYS = 30  # Trail pheromone decay rate (1 month)
BARRIER_REGION_ID = "barrier"  # Blood-brain barrier (screening + uncertainty)
OPEN_BRAIN_REGION_ID = "open_brain_memory"  # Long-term memory


class MemoryTier(Enum):
    """3-tier memory architecture (hippocampal model)."""
    WORKING = auto()    # Session context + OPEN_BRAIN.md — 200 lines, session-scoped
    SHORT_TERM = auto() # research/*.md, memory/*.md — 1 month decay
    LONG_TERM = auto()  # brain region brain regions — persistent, 300 sources/region


class ConsolidationAction(Enum):
    """What to do with knowledge during consolidation cycle."""
    PROMOTE = auto()    # Move to domain brain region (verified)
    QUARANTINE = auto() # Move to quarantine (unverified)
    REFRESH = auto()    # Flag as stale, needs re-research
    KEEP = auto()       # Leave in current tier
    PARK = auto()       # Move to barrier (uncertain — doubt parking)


# ──────────────────────────────────────────────────────────────────────────────
# Data classes
# ──────────────────────────────────────────────────────────────────────────────

@dataclass
class BrainRegion:
    """A single brain region repo = one brain region."""
    region_id: str
    name: str
    topics: list[str] = field(default_factory=list)
    primary_agents: list[str] = field(default_factory=list)
    source_count: int = 0
    last_accessed: datetime | None = None
    has_open_brain: bool = False  # Does this brain region contain OPEN_BRAIN.md?


@dataclass
class RoutingDecision:
    """Result of routing a query to brain region(s)."""
    query: str = ""
    target_regions: list[str] = field(default_factory=list)
    routing_reason: str = ""
    salience_scores: dict[str, float] = field(default_factory=dict)
    fan_out: bool = False  # True if query hits multiple brain regions


@dataclass
class FreshnessReport:
    """Report on source freshness across brain regions."""
    stale_regions: list[str] = field(default_factory=list)
    fresh_regions: list[str] = field(default_factory=list)
    needs_open_brain_sync: list[str] = field(default_factory=list)


@dataclass
class ConsolidationResult:
    """Result of a memory consolidation cycle (the 'sleep' equivalent)."""
    promoted: list[str] = field(default_factory=list)
    quarantined: list[str] = field(default_factory=list)
    refreshed: list[str] = field(default_factory=list)
    parked: list[str] = field(default_factory=list)


@dataclass
class SessionState:
    """Active brain region session state for multi-turn queries."""
    session_id: str = ""
    region_id: str = ""
    messages: int = 0
    created_at: datetime = field(default_factory=datetime.now)


# ──────────────────────────────────────────────────────────────────────────────
# The Hippocampus Agent
# ──────────────────────────────────────────────────────────────────────────────

class Hippocampus(Layer):
    """
    Language Model ↔ Language Model bridge.

    Implements L5 Memory's long-term tier via local brain region repos.
    Routes queries like the hippocampus routes memories to cortical regions.
    Brain regions are brain region repos — routing > brute-force probability.

    Brain regions (8 registered):
        #1 Neural_ARC (neuroscience foundation)
        #2 Agents / Arcs (agent architecture patterns)
        #3 Zero Trust Architecture (verification philosophy)
        #4 Adversarial Security / Red Team (immune system methodology)
        #5 Evolutionary ML (self-evolution foundations)
        #6 RAG Architecture / Vector Search (memory routing)
        #7 Open Brain Long-Term Memory (the brain's own memory)
        #8 Blood-Brain Barrier (screening + uncertainty)
    """

    def __init__(self):
        super().__init__(
            name="Hippocampus",
            layer_number=5,  # L5 Memory
            biological_source="Hippocampus (Human)"
        )
        self._regions: dict[str, BrainRegion] = {}
        self._sessions: dict[str, SessionState] = {}
        self._connection_strengths: dict[str, float] = {}  # Hebbian weights

    # ── Region Management ────────────────────────────────────────────────

    def register_region(self, region: BrainRegion) -> None:
        """Register a brain region (brain region repo)."""
        self._regions[region.region_id] = region
        logger.info(
            "Hippocampus: Registered brain region '%s' (%s) — %d topics",
            region.name, region.region_id, len(region.topics)
        )

    def get_region(self, region_id: str) -> BrainRegion | None:
        return self._regions.get(region_id)

    def list_regions(self) -> list[BrainRegion]:
        return list(self._regions.values())

    # ── Query Routing (Semantic — basal ganglia salience model) ──────────

    def route_query(self, query: str, domain_hint: str = "") -> RoutingDecision:
        """
        Route a query to the best-matching brain region(s).

        Uses topic-based salience scoring (Phase 1).
        Future: semantic-router embeddings (Phase 2), PyMDP active inference (Phase 3).

        Inhibition-by-default: all brain regions are SUPPRESSED.
        Only brain regions whose salience exceeds threshold are RELEASED.
        """
        if not self._regions:
            logger.warning("Hippocampus: No brain regions registered. Cannot route.")
            return RoutingDecision(
                query=query,
                routing_reason="No brain regions registered.",
            )

        # Compute salience for each region (keyword match — Phase 1)
        scores: dict[str, float] = {}
        query_lower = query.lower()
        domain_lower = domain_hint.lower()

        for rid, region in self._regions.items():
            score = 0.0
            for topic in region.topics:
                topic_lower = topic.lower()
                if topic_lower in query_lower:
                    score += 1.0
                if domain_lower and topic_lower in domain_lower:
                    score += 0.5
                # Partial word match
                for word in topic_lower.split():
                    if word in query_lower and len(word) > 3:
                        score += 0.3

            # Hebbian boost: if this region has been productive, boost salience
            hebbian_weight = self._connection_strengths.get(rid, 1.0)
            score *= hebbian_weight

            if score > 0:
                scores[rid] = score

        if not scores:
            # No match — try burst mode (broader routing)
            logger.info("Hippocampus: No salience match for '%s'. Burst mode — routing to all.", query)
            return RoutingDecision(
                query=query,
                target_regions=list(self._regions.keys()),
                routing_reason="Burst mode: no clear domain match, routing broadly.",
                salience_scores={},
                fan_out=True,
            )

        # Threshold: only release brain regions above 50% of max score
        max_score = max(scores.values())
        threshold = max_score * 0.5
        winners = {k: v for k, v in scores.items() if v >= threshold}

        # Sort by score descending
        sorted_winners = sorted(winners.keys(), key=lambda k: winners[k], reverse=True)

        fan_out = len(sorted_winners) > 1
        top_name = self._regions[sorted_winners[0]].name if sorted_winners else "?"

        logger.info(
            "Hippocampus: Routed '%s' → %s (score=%.2f, fan_out=%s)",
            query[:50], top_name, max_score, fan_out
        )

        return RoutingDecision(
            query=query,
            target_regions=sorted_winners,
            routing_reason=f"Salience routing: top match = {top_name} ({max_score:.2f})",
            salience_scores=winners,
            fan_out=fan_out,
        )

    # ── Session Management ───────────────────────────────────────────────

    def start_session(self, region_id: str, session_id: str) -> SessionState:
        """Track an brain region session for multi-turn queries."""
        session = SessionState(
            session_id=session_id,
            region_id=region_id,
        )
        self._sessions[session_id] = session
        logger.info("Hippocampus: Session started — %s on %s", session_id, region_id)
        return session

    def get_session(self, session_id: str) -> SessionState | None:
        return self._sessions.get(session_id)

    def record_query(self, session_id: str) -> None:
        """Record that a query was made in this session."""
        if session_id in self._sessions:
            self._sessions[session_id].messages += 1

    # ── Freshness Checking (pheromone decay) ─────────────────────────────

    def check_freshness(self, now: datetime | None = None) -> FreshnessReport:
        """
        Check all brain regions for staleness.
        Trail pheromone decay rate = 1 month.
        Also checks OPEN_BRAIN.md sync status.
        """
        if now is None:
            now = datetime.now()

        decay_threshold = now - timedelta(days=PHEROMONE_DECAY_DAYS)
        report = FreshnessReport()

        for rid, region in self._regions.items():
            # Freshness check
            if region.last_accessed and region.last_accessed < decay_threshold:
                report.stale_regions.append(rid)
                logger.warning(
                    "Hippocampus: Brain region '%s' is STALE (last accessed: %s)",
                    region.name, region.last_accessed.isoformat()
                )
            else:
                report.fresh_regions.append(rid)

            # OPEN_BRAIN.md sync check (queen pheromone must be in every brain region)
            if not region.has_open_brain:
                report.needs_open_brain_sync.append(rid)

        if report.needs_open_brain_sync:
            logger.warning(
                "Hippocampus: %d brain regions missing OPEN_BRAIN.md: %s",
                len(report.needs_open_brain_sync), report.needs_open_brain_sync
            )

        return report

    # ── Consolidation Cycle (the "sleep" equivalent) ─────────────────────

    def consolidate(
        self,
        artifacts: list[dict[str, Any]],
    ) -> ConsolidationResult:
        """
        Memory consolidation — the hippocampal "sleep replay" cycle.

        For each artifact, decide:
          - PROMOTE: verified → move to domain brain region
          - QUARANTINE: unverified → move to barrier (screening)
          - REFRESH: stale → flag for re-research
          - PARK: uncertain → move to barrier (doubt parking)
          - KEEP: still in progress → leave in current tier

        Consolidation quality gates:
          - Was it verified by immune agent? → PROMOTE
          - Was it only quarantined? → KEEP in quarantine
          - Is it stale (>1 month)? → REFRESH
          - Does it contradict existing memory? → QUARANTINE
        """
        result = ConsolidationResult()

        for artifact in artifacts:
            name = artifact.get("name", "unknown")
            verified = artifact.get("verified", False)
            quarantined = artifact.get("quarantined", False)
            stale = artifact.get("stale", False)
            contradicts = artifact.get("contradicts_existing", False)
            uncertain = artifact.get("uncertain", False)

            if uncertain:
                action = ConsolidationAction.PARK
                result.parked.append(name)
            elif contradicts:
                action = ConsolidationAction.QUARANTINE
                result.quarantined.append(name)
            elif stale:
                action = ConsolidationAction.REFRESH
                result.refreshed.append(name)
            elif verified and not quarantined:
                action = ConsolidationAction.PROMOTE
                result.promoted.append(name)
            else:
                action = ConsolidationAction.KEEP

            logger.info("Hippocampus consolidation: %s → %s", name, action.name)

        return result

    # ── Hebbian Connection Tracking (STDP) ───────────────────────────────

    def strengthen_connection(self, region_id: str, amount: float = 0.1) -> None:
        """
        Hebbian potentiation: brain region was productively used → strengthen.
        "Neurons that fire together wire together."
        """
        current = self._connection_strengths.get(region_id, 1.0)
        self._connection_strengths[region_id] = min(current + amount, 3.0)  # Cap at 3x
        logger.info(
            "Hippocampus: Strengthened connection to '%s': %.2f → %.2f",
            region_id, current, self._connection_strengths[region_id]
        )

    def weaken_connection(self, region_id: str, amount: float = 0.1) -> None:
        """
        Hebbian depression: brain region output was rejected → weaken.
        """
        current = self._connection_strengths.get(region_id, 1.0)
        self._connection_strengths[region_id] = max(current - amount, 0.1)  # Floor at 0.1
        logger.info(
            "Hippocampus: Weakened connection to '%s': %.2f → %.2f",
            region_id, current, self._connection_strengths[region_id]
        )

    # ── Layer interface ──────────────────────────────────────────────────

    def process(self, context: dict[str, Any]) -> LayerResult:
        """
        L5 Memory layer processing.
        Routes query to brain region(s), returns routing decision.
        """
        query = context.get("query", "")
        domain = context.get("domain", "")

        if not query:
            return LayerResult(
                layer_name=self.name,
                status=LayerStatus.BLOCKED,
                blocked_reason="No query provided to Hippocampus.",
            )

        routing = self.route_query(query, domain_hint=domain)

        if not routing.target_regions:
            return LayerResult(
                layer_name=self.name,
                status=LayerStatus.BLOCKED,
                blocked_reason="Hippocampus could not route query to any brain region.",
                data={"routing": routing},
            )

        return LayerResult(
            layer_name=self.name,
            status=LayerStatus.READY,
            data={
                "routing": routing,
                "target_count": len(routing.target_regions),
                "fan_out": routing.fan_out,
                "top_region": self._regions.get(
                    routing.target_regions[0], BrainRegion(region_id="?", name="?")
                ).name,
            },
        )

    def describe(self) -> str:
        return (
            "Hippocampal bridge: routes queries to brain regions "
            "like the hippocampus routes memories to cortical areas. 8 brain regions. "
            "Routing > brute-force probability. Consolidation cycle "
            "replays and promotes verified knowledge, screens uncertain findings via barrier."
        )
