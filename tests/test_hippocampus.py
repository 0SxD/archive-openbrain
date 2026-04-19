"""
Tests for Hippocampus — the memory routing agent (L5 Memory).

Hippocampus routes queries to brain regions like the biological hippocampus
routes memories to cortical areas. Tests cover:
    1. Query routing (salience, threshold, fan-out, burst mode)
    2. Hebbian connection tracking (potentiation, depression, influence on routing)
    3. Session management
    4. Freshness checking (pheromone decay, OPEN_BRAIN.md sync)
    5. Consolidation cycle (promote, quarantine, refresh, park, keep)
    6. Layer interface (process, describe, blocking)
"""

from datetime import datetime, timedelta

import pytest

from openbrainlm.agents.hippocampus import (
    BrainRegion,
    ConsolidationAction,
    Hippocampus,
    MemoryTier,
    PHEROMONE_DECAY_DAYS,
)
from openbrainlm.layers.base import LayerStatus


# ──────────────────────────────────────────────────────────────────────────────
# Fixtures
# ──────────────────────────────────────────────────────────────────────────────

@pytest.fixture
def lm():
    """Hippocampus with 3 brain regions registered."""
    agent = Hippocampus()
    agent.register_region(BrainRegion(
        region_id="neural_arc",
        name="Neural_ARC",
        topics=["neuroscience", "brain", "biomimicry", "cortex"],
        has_open_brain=True,
        last_accessed=datetime.now(),
    ))
    agent.register_region(BrainRegion(
        region_id="agents_arcs",
        name="Agents_Arcs",
        topics=["agents", "orchestration", "multi-agent", "architecture"],
        has_open_brain=True,
        last_accessed=datetime.now(),
    ))
    agent.register_region(BrainRegion(
        region_id="barrier",
        name="Barrier",
        topics=["quarantine", "unverified", "staging", "screening"],
        has_open_brain=False,
        last_accessed=datetime.now() - timedelta(days=60),  # Stale
    ))
    return agent


@pytest.fixture
def empty_lm():
    """Hippocampus with no brain regions."""
    return Hippocampus()


# ──────────────────────────────────────────────────────────────────────────────
# Query Routing
# ──────────────────────────────────────────────────────────────────────────────

class TestQueryRouting:
    def test_routes_to_matching_region(self, lm):
        """Query with neuroscience keywords routes to Neural_ARC."""
        decision = lm.route_query("research neuroscience brain cortex")
        assert "neural_arc" in decision.target_regions
        assert decision.salience_scores["neural_arc"] > 0

    def test_routes_to_best_match(self, lm):
        """Top region should be the highest-salience match."""
        decision = lm.route_query("agent orchestration multi-agent architecture")
        assert decision.target_regions[0] == "agents_arcs"

    def test_fan_out_when_multiple_match(self, lm):
        """Multiple regions above threshold → fan_out=True."""
        decision = lm.route_query("neuroscience brain agents architecture")
        assert decision.fan_out is True
        assert len(decision.target_regions) >= 2

    def test_burst_mode_on_no_match(self, lm):
        """No salience match → burst mode routes to ALL brain regions."""
        decision = lm.route_query("completely unrelated cooking recipe")
        assert decision.fan_out is True
        assert len(decision.target_regions) == 3  # All registered
        assert "Burst mode" in decision.routing_reason

    def test_no_routing_without_regions(self, empty_lm):
        """Must fail gracefully with no regions registered."""
        decision = empty_lm.route_query("anything")
        assert len(decision.target_regions) == 0
        assert "No brain regions" in decision.routing_reason

    def test_domain_hint_boosts_score(self, lm):
        """domain_hint should add extra salience to matching regions."""
        without_hint = lm.route_query("brain")
        with_hint = lm.route_query("brain", domain_hint="neuroscience")
        # With hint should have higher score for neural_arc
        score_without = without_hint.salience_scores.get("neural_arc", 0)
        score_with = with_hint.salience_scores.get("neural_arc", 0)
        assert score_with > score_without

    def test_threshold_filters_low_scores(self, lm):
        """Regions below 50% of max score should be filtered out."""
        # Query strongly targets neural_arc, weakly others
        decision = lm.route_query("neuroscience brain cortex biomimicry")
        # neural_arc should dominate, regions below 50% of max excluded
        if len(decision.target_regions) == 1:
            assert decision.target_regions[0] == "neural_arc"


# ──────────────────────────────────────────────────────────────────────────────
# Hebbian Connection Tracking
# ──────────────────────────────────────────────────────────────────────────────

class TestHebbianConnections:
    def test_strengthen_increases_weight(self, lm):
        """Potentiation must increase connection weight."""
        lm.strengthen_connection("neural_arc", amount=0.5)
        assert lm._connection_strengths["neural_arc"] == 1.5

    def test_weaken_decreases_weight(self, lm):
        """Depression must decrease connection weight."""
        lm.weaken_connection("neural_arc", amount=0.3)
        assert lm._connection_strengths["neural_arc"] == pytest.approx(0.7)

    def test_weight_capped_at_3(self, lm):
        """Weight must never exceed 3.0."""
        for _ in range(50):
            lm.strengthen_connection("neural_arc", amount=1.0)
        assert lm._connection_strengths["neural_arc"] == 3.0

    def test_weight_floored_at_01(self, lm):
        """Weight must never go below 0.1."""
        for _ in range(50):
            lm.weaken_connection("neural_arc", amount=1.0)
        assert lm._connection_strengths["neural_arc"] == 0.1

    def test_hebbian_boost_affects_routing(self, lm):
        """Strengthened regions should score higher in routing."""
        # Route before boost
        before = lm.route_query("neuroscience brain")
        score_before = before.salience_scores.get("neural_arc", 0)

        # Boost neural_arc
        lm.strengthen_connection("neural_arc", amount=1.0)

        # Route after boost
        after = lm.route_query("neuroscience brain")
        score_after = after.salience_scores.get("neural_arc", 0)

        assert score_after > score_before


# ──────────────────────────────────────────────────────────────────────────────
# Session Management
# ──────────────────────────────────────────────────────────────────────────────

class TestSessionManagement:
    def test_start_session(self, lm):
        session = lm.start_session("neural_arc", "s1")
        assert session.session_id == "s1"
        assert session.region_id == "neural_arc"
        assert session.messages == 0

    def test_record_query_increments(self, lm):
        lm.start_session("neural_arc", "s1")
        lm.record_query("s1")
        lm.record_query("s1")
        assert lm.get_session("s1").messages == 2

    def test_get_nonexistent_session(self, lm):
        assert lm.get_session("nonexistent") is None


# ──────────────────────────────────────────────────────────────────────────────
# Freshness Checking
# ──────────────────────────────────────────────────────────────────────────────

class TestFreshness:
    def test_stale_region_flagged(self, lm):
        """Regions last accessed >30 days ago must be flagged stale."""
        report = lm.check_freshness()
        assert "barrier" in report.stale_regions

    def test_fresh_region_not_flagged(self, lm):
        """Recently accessed regions should be fresh."""
        report = lm.check_freshness()
        assert "neural_arc" in report.fresh_regions

    def test_open_brain_sync_missing(self, lm):
        """Regions without OPEN_BRAIN.md must be flagged for sync."""
        report = lm.check_freshness()
        assert "barrier" in report.needs_open_brain_sync

    def test_open_brain_sync_present(self, lm):
        """Regions WITH OPEN_BRAIN.md should NOT be in sync list."""
        report = lm.check_freshness()
        assert "neural_arc" not in report.needs_open_brain_sync

    def test_custom_time_for_freshness(self, lm):
        """Passing custom 'now' should shift the decay window."""
        far_future = datetime.now() + timedelta(days=365)
        report = lm.check_freshness(now=far_future)
        # All regions should be stale 365 days from now
        assert len(report.stale_regions) == 3


# ──────────────────────────────────────────────────────────────────────────────
# Consolidation Cycle
# ──────────────────────────────────────────────────────────────────────────────

class TestConsolidation:
    def test_verified_promotes(self, lm):
        """Verified, non-quarantined artifact → PROMOTE."""
        result = lm.consolidate([{"name": "paper1", "verified": True}])
        assert "paper1" in result.promoted

    def test_unverified_keeps(self, lm):
        """Unverified artifact with no flags → KEEP (not in any list)."""
        result = lm.consolidate([{"name": "draft1", "verified": False}])
        assert "draft1" not in result.promoted
        assert "draft1" not in result.quarantined
        assert "draft1" not in result.refreshed
        assert "draft1" not in result.parked

    def test_contradicting_quarantines(self, lm):
        """Artifact that contradicts existing memory → QUARANTINE."""
        result = lm.consolidate([{"name": "conflict1", "contradicts_existing": True}])
        assert "conflict1" in result.quarantined

    def test_stale_refreshes(self, lm):
        """Stale artifact → REFRESH."""
        result = lm.consolidate([{"name": "old1", "stale": True}])
        assert "old1" in result.refreshed

    def test_uncertain_parks(self, lm):
        """Uncertain artifact → PARK (doubt parking lot)."""
        result = lm.consolidate([{"name": "maybe1", "uncertain": True}])
        assert "maybe1" in result.parked

    def test_uncertain_takes_priority(self, lm):
        """Uncertain flag should take priority over verified."""
        result = lm.consolidate([{
            "name": "confused",
            "uncertain": True,
            "verified": True,
        }])
        assert "confused" in result.parked
        assert "confused" not in result.promoted

    def test_mixed_artifacts(self, lm):
        """Multiple artifacts with different dispositions."""
        result = lm.consolidate([
            {"name": "good", "verified": True},
            {"name": "bad", "contradicts_existing": True},
            {"name": "old", "stale": True},
            {"name": "doubt", "uncertain": True},
            {"name": "wip", "verified": False},
        ])
        assert "good" in result.promoted
        assert "bad" in result.quarantined
        assert "old" in result.refreshed
        assert "doubt" in result.parked


# ──────────────────────────────────────────────────────────────────────────────
# Layer Interface
# ──────────────────────────────────────────────────────────────────────────────

class TestLayerInterface:
    def test_blocks_without_query(self, lm):
        """L5 must BLOCK when no query is provided."""
        result = lm.process({})
        assert result.status == LayerStatus.BLOCKED
        assert "No query" in result.blocked_reason

    def test_blocks_without_regions(self, empty_lm):
        """L5 must BLOCK when no regions can handle the query."""
        result = empty_lm.process({"query": "anything"})
        assert result.status == LayerStatus.BLOCKED

    def test_ready_with_matching_query(self, lm):
        """L5 must be READY when query routes successfully."""
        result = lm.process({"query": "neuroscience brain research"})
        assert result.status == LayerStatus.READY
        assert "routing" in result.data

    def test_process_includes_region_count(self, lm):
        """Process result must include target_count."""
        result = lm.process({"query": "neuroscience brain"})
        assert result.data["target_count"] >= 1

    def test_describe_mentions_hippocampal(self, lm):
        """Describe must reference biological analogue."""
        assert "Hippocampal" in lm.describe()

    def test_layer_number_is_5(self, lm):
        """Hippocampus must be layer 5."""
        assert lm.layer_number == 5

    def test_burst_mode_via_process(self, lm):
        """Process with unrelated query → burst mode fan-out."""
        result = lm.process({"query": "cooking pasta recipes"})
        assert result.status == LayerStatus.READY
        assert result.data["fan_out"] is True


# ──────────────────────────────────────────────────────────────────────────────
# Region Management
# ──────────────────────────────────────────────────────────────────────────────

class TestRegionManagement:
    def test_register_and_retrieve(self, lm):
        region = lm.get_region("neural_arc")
        assert region is not None
        assert region.name == "Neural_ARC"

    def test_list_regions(self, lm):
        regions = lm.list_regions()
        assert len(regions) == 3

    def test_get_nonexistent_region(self, lm):
        assert lm.get_region("nonexistent") is None
