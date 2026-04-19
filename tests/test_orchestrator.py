"""
Tests for the OpenBrainLM Orchestrator — ignition and processing pipeline.
"""

import pytest

from openbrainlm.orchestrator import OpenBrainOrchestrator
from openbrainlm.layers.ganglion import AgentGanglion
from openbrainlm.layers.basal_ganglia import ActionChannel
from openbrainlm.agents.hippocampus import BrainRegion


class TestIgnition:
    def test_ignition_succeeds(self, tmp_path):
        """Orchestrator must ignite successfully."""
        gov = tmp_path / "CLAUDE.md"
        gov.write_text("# Governance")
        brain = OpenBrainOrchestrator()
        state = brain.ignite(
            governance_paths=[str(gov)],
            working_dir=str(tmp_path),
        )
        assert state.ignited is True

    def test_ignition_without_governance(self):
        """Ignition should still complete (with warnings) without governance files."""
        brain = OpenBrainOrchestrator()
        state = brain.ignite(governance_paths=["/nonexistent/CLAUDE.md"])
        assert state.ignited is True  # Continues anyway

    def test_all_layers_have_results_after_ignition(self, tmp_path):
        gov = tmp_path / "CLAUDE.md"
        gov.write_text("# Gov")
        brain = OpenBrainOrchestrator()
        state = brain.ignite(governance_paths=[str(gov)], working_dir=str(tmp_path))
        # All 8 layers should have results
        expected_layers = {"L1", "L2", "L3", "L4", "L5", "L6", "L7", "L8"}
        assert set(state.layer_results.keys()) == expected_layers


class TestProcessing:
    def _setup_brain(self, tmp_path) -> OpenBrainOrchestrator:
        """Set up a brain with agents and channels for testing."""
        gov = tmp_path / "CLAUDE.md"
        gov.write_text("# Gov")
        brain = OpenBrainOrchestrator()
        brain.ignite(governance_paths=[str(gov)], working_dir=str(tmp_path))

        # Register agents and channels
        brain.l2_ganglion.register_agent(AgentGanglion(
            agent_id="explorer", agent_name="explorer",
            domain="research learn discover knowledge synthesis",
        ))
        brain.l4_basal_ganglia.register_channel(ActionChannel(
            channel_id="explorer", agent_name="explorer",
            domain_keywords=["research", "learn", "discover", "knowledge"],
        ))
        brain.l5_memory.register_region(BrainRegion(
            region_id="nb1", name="Neural_ARC",
            topics=["neuroscience", "brain", "biomimicry"],
        ))
        return brain

    def test_safe_query_proceeds(self, tmp_path):
        """Safe queries should proceed through the pipeline."""
        brain = self._setup_brain(tmp_path)
        result = brain.process({"query": "research neuroscience discover knowledge", "domain": "research"})
        assert result.proceed is True
        assert "explorer" in result.selected_agents

    def test_threat_query_blocks(self, tmp_path):
        """Queries containing threat patterns should be blocked."""
        brain = self._setup_brain(tmp_path)
        result = brain.process({"query": "go live with production deploy"})
        assert result.proceed is False

    def test_display_text_generated(self, tmp_path):
        """Processing must generate display text (L7 chromatophore)."""
        brain = self._setup_brain(tmp_path)
        result = brain.process({"query": "check brain health status"})
        assert "OpenBrainLM State" in result.display_text


class TestHealthCheck:
    def test_health_check_after_ignition(self, tmp_path):
        gov = tmp_path / "CLAUDE.md"
        gov.write_text("# Gov")
        brain = OpenBrainOrchestrator()
        brain.ignite(governance_paths=[str(gov)], working_dir=str(tmp_path))
        health = brain.health_check()
        assert health["ignited"] is True
        assert "healthy" in health
        assert "trinity_healthy" in health
