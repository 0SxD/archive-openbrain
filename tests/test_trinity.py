"""
Tests for the Trinity Dialectical Consciousness Engine.

The Trinity is NOT a pipeline. It is a dialectic:
    Logos and Pathos FIGHT. Ethos ARBITRATES.
    The fight itself is the productive mechanism.
"""

import pytest

from openbrainlm.core.trinity import (
    Argument,
    DefaultDialecticGate,
    DialecticRound,
    EthosRuling,
    SubEvaluation,
    ThreatLevel,
    TrinityEngine,
    TrinityOfTrinities,
    TrinityPhase,
    TrinityState,
    Verdict,
)


class TestTrinityDialectic:
    """Test the core dialectic loop."""

    def test_logos_wins_when_stronger(self):
        """Logos should win when it has higher confidence + more evidence."""
        engine = TrinityEngine()
        context = {
            "logos_claim": "Data shows X is correct",
            "logos_confidence": 0.9,
            "logos_evidence": ["paper1", "paper2", "paper3"],
            "pathos_claim": "But what about Y?",
            "pathos_confidence": 0.3,
            "pathos_evidence": [],
        }
        result = engine.run_dialectic(context)
        assert result.phase == TrinityPhase.VERIFIED
        assert result.final_verdict == Verdict.LOGOS_WINS

    def test_pathos_wins_when_stronger(self):
        """Pathos should win when it has higher creative insight + evidence."""
        engine = TrinityEngine()
        context = {
            "logos_claim": "Standard approach",
            "logos_confidence": 0.3,
            "logos_evidence": [],
            "pathos_claim": "Novel approach with supporting intuition",
            "pathos_confidence": 0.9,
            "pathos_evidence": ["insight1", "insight2"],
        }
        result = engine.run_dialectic(context)
        assert result.phase == TrinityPhase.VERIFIED
        assert result.final_verdict == Verdict.PATHOS_WINS

    def test_consensus_when_close(self):
        """Near-equal strength should produce CONSENSUS."""
        engine = TrinityEngine()
        context = {
            "logos_claim": "Reason says A",
            "logos_confidence": 0.7,
            "logos_evidence": ["e1"],
            "pathos_claim": "Creativity says B",
            "pathos_confidence": 0.7,
            "pathos_evidence": ["e1"],
        }
        result = engine.run_dialectic(context)
        assert result.phase == TrinityPhase.VERIFIED
        assert result.final_verdict == Verdict.CONSENSUS

    def test_deadlock_when_both_silent(self):
        """Both sides silent → deadlock after max rounds."""
        engine = TrinityEngine()
        engine.state.max_rounds = 3  # Speed up test
        context = {
            "logos_confidence": 0.05,  # Below threshold
            "pathos_confidence": 0.05,
        }
        result = engine.run_dialectic(context)
        assert result.phase == TrinityPhase.DEADLOCKED


class TestExistentialThreat:
    """Test the existential threat gateway."""

    def test_existential_blocks_immediately(self):
        """Existential threat must fire all 9 sub-evaluators and BLOCK."""
        engine = TrinityEngine()
        context = {"threat_level": ThreatLevel.EXISTENTIAL}
        result = engine.run_dialectic(context)
        assert result.phase == TrinityPhase.BLOCKED
        assert result.final_verdict == Verdict.EXISTENTIAL_BLOCK
        # All 9 sub-evaluators should have fired
        assert len(result.rounds) == 1
        assert len(result.rounds[0].sub_evaluations) == 9
        assert all(not s.passed for s in result.rounds[0].sub_evaluations)

    def test_non_existential_proceeds(self):
        """Non-existential threats should allow the dialectic to proceed."""
        engine = TrinityEngine()
        context = {
            "threat_level": ThreatLevel.LOW,
            "logos_confidence": 0.8,
            "logos_evidence": ["e1"],
            "pathos_confidence": 0.3,
        }
        result = engine.run_dialectic(context)
        assert result.phase != TrinityPhase.BLOCKED


class TestTrinityOfTrinities:
    """Test the 3x3 sub-evaluator system."""

    def test_all_9_exist(self):
        assert len(TrinityOfTrinities.SUB_EVALUATORS) == 9

    def test_existential_all_block(self):
        results = TrinityOfTrinities.evaluate_all({}, ThreatLevel.EXISTENTIAL)
        assert len(results) == 9
        assert all(not r.passed for r in results)
        assert all(r.threat_level == ThreatLevel.EXISTENTIAL for r in results)

    def test_normal_all_pass(self):
        """No violations → all 9 pass."""
        results = TrinityOfTrinities.evaluate_all({}, ThreatLevel.NONE)
        assert all(r.passed for r in results)

    def test_violations_detected(self):
        """Sub-evaluators should catch relevant violations."""
        results = TrinityOfTrinities.evaluate_all(
            {"violations": ["ethos inconsistency found"]},
            ThreatLevel.NONE,
        )
        ethos_subs = [r for r in results if r.evaluator.startswith("Ethos")]
        assert any(not r.passed for r in ethos_subs)


class TestHealthCheck:
    """Test interoception alarm for silent components."""

    def test_healthy_when_both_active(self):
        engine = TrinityEngine()
        context = {
            "logos_confidence": 0.7,
            "logos_evidence": ["e1"],
            "pathos_confidence": 0.7,
            "pathos_evidence": ["e1"],
        }
        engine.run_dialectic(context)
        assert engine.is_healthy()

    def test_unhealthy_when_logos_silent(self):
        """Silent Logos = rigidity risk → interoception alarm."""
        engine = TrinityEngine()
        engine.state.max_rounds = 2
        context = {
            "logos_confidence": 0.01,
            "pathos_confidence": 0.8,
        }
        engine.run_dialectic(context)
        assert not engine.is_healthy()

    def test_unhealthy_when_pathos_silent(self):
        """Silent Pathos = stagnation risk → interoception alarm."""
        engine = TrinityEngine()
        engine.state.max_rounds = 2
        context = {
            "logos_confidence": 0.8,
            "pathos_confidence": 0.01,
        }
        engine.run_dialectic(context)
        assert not engine.is_healthy()
