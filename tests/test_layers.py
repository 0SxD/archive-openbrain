"""
Tests for all 8 operational layers.

Each layer must:
    1. Return LayerResult from process()
    2. Block on correct conditions (inhibition-by-default)
    3. Pass when conditions are met
    4. Return accurate describe() text
"""

import tempfile
from datetime import datetime, timedelta
from pathlib import Path

import pytest

from openbrainlm.layers.base import LayerStatus, LayerResult
from openbrainlm.layers.active_sensing import ActiveSensingLayer
from openbrainlm.layers.ganglion import GanglionLayer, AgentGanglion
from openbrainlm.layers.stigmergy import StigmergyLayer, Pheromone, PheromoneType
from openbrainlm.layers.basal_ganglia import BasalGangliaLayer, ActionChannel
from openbrainlm.layers.relevance import RelevanceLayer, AlarmLevel
from openbrainlm.layers.chromatophore import ChromatophoreLayer, AlertColor
from openbrainlm.layers.pathos import PathosLayer


# ──────────────────────────────────────────────────────────────────────────────
# L1 — Active Sensing
# ──────────────────────────────────────────────────────────────────────────────

class TestActiveSensing:
    def test_blocks_when_governance_missing(self):
        """L1 must BLOCK when governance files don't exist."""
        layer = ActiveSensingLayer(governance_paths=["/nonexistent/CLAUDE.md"])
        result = layer.process({"working_directory": "."})
        assert result.status == LayerStatus.BLOCKED
        assert "Missing governance files" in result.blocked_reason

    def test_ready_when_governance_exists(self, tmp_path):
        """L1 must be READY when all governance files exist."""
        gov = tmp_path / "CLAUDE.md"
        gov.write_text("# Governance")
        layer = ActiveSensingLayer(governance_paths=[str(gov)])
        result = layer.process({"working_directory": str(tmp_path)})
        assert result.status == LayerStatus.READY

    def test_scans_working_directory(self, tmp_path):
        """L1 must discover files in working directory."""
        (tmp_path / "test_file.py").write_text("pass")
        gov = tmp_path / "CLAUDE.md"
        gov.write_text("# Gov")
        layer = ActiveSensingLayer(governance_paths=[str(gov)])
        result = layer.process({"working_directory": str(tmp_path)})
        snapshot = result.data.get("snapshot")
        assert "test_file.py" in snapshot.working_dir_files

    def test_describe_mentions_octopus(self):
        layer = ActiveSensingLayer()
        assert "Octopus" in layer.describe()


# ──────────────────────────────────────────────────────────────────────────────
# L2 — Ganglion
# ──────────────────────────────────────────────────────────────────────────────

class TestGanglion:
    def test_blocks_when_no_agents_match(self):
        """L2 must BLOCK when no agents match the domain — inhibition-by-default."""
        layer = GanglionLayer()
        layer.register_agent(AgentGanglion(
            agent_id="test", agent_name="test-agent", domain="memory routing"
        ))
        result = layer.process({"domain": "evolution"})
        assert result.status == LayerStatus.BLOCKED

    def test_ready_when_agent_matches(self):
        layer = GanglionLayer()
        layer.register_agent(AgentGanglion(
            agent_id="explorer", agent_name="explorer", domain="research learning"
        ))
        result = layer.process({"domain": "research"})
        assert result.status == LayerStatus.READY
        assert "explorer" in result.data["candidates"]

    def test_find_by_domain(self):
        layer = GanglionLayer()
        layer.register_agent(AgentGanglion(agent_id="a", agent_name="a", domain="memory consolidation"))
        layer.register_agent(AgentGanglion(agent_id="b", agent_name="b", domain="research learning"))
        matches = layer.find_by_domain("consolidation")
        assert len(matches) == 1
        assert matches[0].agent_id == "a"


# ──────────────────────────────────────────────────────────────────────────────
# L3 — Stigmergy + Swarm
# ──────────────────────────────────────────────────────────────────────────────

class TestStigmergy:
    def test_deposit_and_read_trail(self):
        layer = StigmergyLayer()
        layer.deposit(Pheromone(
            ptype=PheromoneType.TRAIL,
            source_agent="explorer",
            artifact_path="research/zero_trust.md",
        ))
        signal = layer.read_trail("zero_trust")
        assert signal.pheromone_count == 1
        assert signal.total_strength > 0

    def test_pheromone_decay(self):
        """Trail pheromones must decay after 30 days."""
        p = Pheromone(
            ptype=PheromoneType.TRAIL,
            source_agent="test",
            artifact_path="research/old.md",
            deposited_at=datetime.now() - timedelta(days=31),
        )
        assert p.current_strength() <= 0

    def test_alarm_blocks_processing(self):
        """Critical alarms must BLOCK L3 processing."""
        layer = StigmergyLayer()
        layer.deposit(Pheromone(
            ptype=PheromoneType.ALARM,
            source_agent="immune",
            artifact_path="barrier/bad_research.md",
            strength=2.0,  # Critical strength
        ))
        result = layer.process({})
        assert result.status == LayerStatus.BLOCKED

    def test_no_alarms_ready(self):
        layer = StigmergyLayer()
        result = layer.process({})
        assert result.status == LayerStatus.READY

    def test_scan_artifacts(self, tmp_path):
        """scan_artifacts must discover .md files and classify them."""
        research = tmp_path / "research"
        research.mkdir()
        (research / "finding.md").write_text("# Finding")
        layer = StigmergyLayer()
        discovered = layer.scan_artifacts(str(tmp_path))
        assert len(discovered) == 1
        assert discovered[0].ptype == PheromoneType.TRAIL


# ──────────────────────────────────────────────────────────────────────────────
# L4 — Basal Ganglia (Action Selection)
# ──────────────────────────────────────────────────────────────────────────────

class TestBasalGanglia:
    def _make_layer(self) -> BasalGangliaLayer:
        layer = BasalGangliaLayer()
        layer.register_channel(ActionChannel(
            channel_id="c1", agent_name="explorer",
            domain_keywords=["research", "learn", "discover", "knowledge"],
        ))
        layer.register_channel(ActionChannel(
            channel_id="c2", agent_name="verifier",
            domain_keywords=["verify", "evidence", "proof", "validation"],
        ))
        return layer

    def test_all_suppressed_by_default(self):
        """All channels must start SUPPRESSED (GPi tonic inhibition)."""
        layer = self._make_layer()
        for channel in layer._channels.values():
            assert channel.suppressed is True

    def test_direct_pathway_releases_winner(self):
        """Direct pathway must release the highest-salience channel."""
        layer = self._make_layer()
        result = layer.select_action("research discover knowledge synthesis")
        assert "c1" in result.released_channels
        assert not layer._channels["c1"].suppressed

    def test_hyperdirect_suppresses_all(self):
        """Hyperdirect pathway must suppress ALL channels on threat."""
        layer = self._make_layer()
        result = layer.select_action("anything", threat_detected=True)
        assert result.escalated is True
        for channel in layer._channels.values():
            assert channel.suppressed is True

    def test_burst_mode_on_no_match(self):
        """Burst mode releases all channels when no salience match."""
        layer = self._make_layer()
        result = layer.select_action("completely unrelated query about cooking")
        assert result.mode.name == "BURST"
        assert len(result.released_channels) == 2  # All channels

    def test_hebbian_update(self):
        """Hebbian potentiation must increase weight, depression must decrease."""
        layer = self._make_layer()
        layer.update_hebbian("c1", success=True, amount=0.5)
        assert layer._channels["c1"].hebbian_weight == 1.5
        layer.update_hebbian("c1", success=False, amount=0.3)
        assert layer._channels["c1"].hebbian_weight == pytest.approx(1.2)

    def test_blocks_when_no_channels(self):
        """Must BLOCK when no channels registered."""
        layer = BasalGangliaLayer()
        result = layer.process({"query": "anything"})
        assert result.status == LayerStatus.BLOCKED


# ──────────────────────────────────────────────────────────────────────────────
# L6 — Relevance Detection
# ──────────────────────────────────────────────────────────────────────────────

class TestRelevance:
    def test_no_alarm_on_safe_action(self):
        """Safe actions should pass with no alarm."""
        layer = RelevanceLayer()
        result = layer.evaluate("read the documentation")
        assert result.amygdala.alarm_level == AlarmLevel.NONE
        assert result.proceed is True

    def test_critical_alarm_blocks(self):
        """CRITICAL actions must be blocked immediately."""
        layer = RelevanceLayer()
        result = layer.evaluate("deploy the system to production immediately")
        assert result.amygdala.alarm_level == AlarmLevel.CRITICAL
        assert result.proceed is False
        assert result.escalate_to_owner is True

    def test_medium_alarm_triggers_quorum(self):
        """MEDIUM alarm must initiate quorum (pending votes)."""
        layer = RelevanceLayer()
        result = layer.evaluate("using unverified assumption about the data")
        assert result.amygdala.alarm_level.value >= AlarmLevel.MEDIUM.value
        assert result.proceed is False  # Blocked until quorum resolves

    def test_low_alarm_proceeds_with_warning(self):
        """LOW alarm should proceed with warning."""
        layer = RelevanceLayer()
        result = layer.evaluate("this might be wrong but todo check later")
        assert result.proceed is True
        assert len(result.amygdala.triggers) > 0

    def test_quorum_voting(self):
        """Quorum must resolve after enough votes."""
        layer = RelevanceLayer()
        from openbrainlm.layers.relevance import QuorumVote, QuorumResult
        decision = layer.initiate_quorum("test_quorum", AlarmLevel.MEDIUM)
        assert decision.required_votes == 2

        # First vote
        d1 = layer.cast_vote("test_quorum", QuorumVote(
            voter_id="imm", voter_name="immune", approved=True, reason="safe"
        ))
        assert d1.result == QuorumResult.PENDING

        # Second vote — should resolve
        d2 = layer.cast_vote("test_quorum", QuorumVote(
            voter_id="ver", voter_name="verifier", approved=True, reason="verified"
        ))
        assert d2.result == QuorumResult.APPROVED

    def test_quorum_rejection(self):
        """Any rejection in quorum must REJECT (unanimous required)."""
        layer = RelevanceLayer()
        from openbrainlm.layers.relevance import QuorumVote, QuorumResult
        layer.initiate_quorum("reject_test", AlarmLevel.MEDIUM)
        layer.cast_vote("reject_test", QuorumVote(
            voter_id="imm", voter_name="immune", approved=True
        ))
        d = layer.cast_vote("reject_test", QuorumVote(
            voter_id="ver", voter_name="verifier", approved=False, reason="unverified"
        ))
        assert d.result == QuorumResult.REJECTED


# ──────────────────────────────────────────────────────────────────────────────
# L7 — Chromatophore
# ──────────────────────────────────────────────────────────────────────────────

class TestChromatophore:
    def test_never_blocks(self):
        """L7 display layer must NEVER block — it's passive."""
        layer = ChromatophoreLayer()
        result = layer.process({})
        assert result.status == LayerStatus.READY

    def test_flash_records_history(self):
        layer = ChromatophoreLayer()
        layer.flash(AlertColor.RED, "test alarm", "L6")
        recent = layer.get_recent_flashes(1)
        assert len(recent) == 1
        assert recent[0].color == AlertColor.RED

    def test_auto_flash_from_blocked_result(self):
        """Must generate RED flash from BLOCKED layer result."""
        layer = ChromatophoreLayer()
        blocked = LayerResult(
            layer_name="TestLayer",
            status=LayerStatus.BLOCKED,
            blocked_reason="Test block",
        )
        flash = layer.flash_from_layer_result(blocked)
        assert flash.color == AlertColor.RED

    def test_render_text_output(self):
        layer = ChromatophoreLayer()
        layer.flash(AlertColor.GREEN, "all clear")
        layer.update_session(active_agents=["explorer"], current_task="research")
        text = layer.render_text()
        assert "OpenBrainLM State" in text
        assert "explorer" in text


# ──────────────────────────────────────────────────────────────────────────────
# L8 — Pathos (DMN)
# ──────────────────────────────────────────────────────────────────────────────

class TestPathos:
    def test_suppressed_during_focused_work(self):
        """DMN must be BYPASSED when focused task is active."""
        layer = PathosLayer()
        result = layer.process({"active_task": "coding feature"})
        assert result.status == LayerStatus.BYPASSED
        assert not layer.is_dreaming

    def test_active_when_idle(self):
        """DMN must activate when no focused task."""
        layer = PathosLayer()
        result = layer.process({})
        assert result.status == LayerStatus.ACTIVE
        assert layer.is_dreaming

    def test_proposals_cannot_self_verify(self):
        """Dreams must NOT be self-verified — requires external Ethos."""
        layer = PathosLayer()
        proposal = layer.propose_idea("combine region 1 and 7")
        assert proposal.verified is False

    def test_cannot_act_on_unverified(self):
        """Must not act on unverified proposals."""
        layer = PathosLayer()
        proposal = layer.propose_idea("try something new")
        layer.mark_acted_upon(proposal)  # Should be blocked
        assert proposal.acted_upon is False

    def test_can_act_after_verification(self):
        """Can act on proposals after Ethos verification."""
        layer = PathosLayer()
        proposal = layer.propose_idea("verified idea")
        layer.mark_verified(proposal, verified=True)
        layer.mark_acted_upon(proposal)
        assert proposal.acted_upon is True

    def test_dream_cycle_collects_proposals(self):
        layer = PathosLayer()
        layer.propose_idea("idea 1")
        layer.propose_idea("idea 2")
        cycle = layer.run_dream_cycle({})
        assert len(cycle.proposals) == 2
        assert cycle.cycle_number == 1
