"""
Tests for the 4 cross-cutting mechanisms.
These permeate all layers — they're not in the stack, they influence everything.
"""

from datetime import datetime, timedelta

import pytest

from openbrainlm.cross_cutting import (
    PredictionErrorFilter,
    HebbianPlasticity,
    InteroceptionMonitor,
    CerebellumTiming,
)


class TestPredictionError:
    """Friston free-energy principle: route based on surprise."""

    def test_no_error_when_match(self):
        pef = PredictionErrorFilter()
        pef.set_prediction("agent_count", 19)
        error = pef.observe("agent_count", 19)
        assert error.magnitude == 0.0
        assert not error.is_surprising

    def test_high_error_on_mismatch(self):
        pef = PredictionErrorFilter()
        pef.set_prediction("agent_count", 19)
        error = pef.observe("agent_count", 5)
        assert error.magnitude > 0.5
        assert error.is_surprising

    def test_alarming_on_extreme_mismatch(self):
        pef = PredictionErrorFilter()
        pef.set_prediction("status", "READY")
        error = pef.observe("status", "BLOCKED")
        assert error.magnitude == 1.0
        assert error.is_alarming

    def test_no_error_without_prediction(self):
        pef = PredictionErrorFilter()
        error = pef.observe("unknown_key", 42)
        assert error is None


class TestHebbianPlasticity:
    """STDP: neurons that fire together wire together."""

    def test_potentiation(self):
        h = HebbianPlasticity()
        w = h.potentiate("agent_a", "agent_b", amount=0.5)
        assert w == 1.5
        assert h.get_weight("agent_a", "agent_b") == 1.5

    def test_depression(self):
        h = HebbianPlasticity()
        w = h.depress("agent_a", "agent_b", amount=0.3)
        assert w == 0.7

    def test_weight_capped_at_max(self):
        h = HebbianPlasticity()
        for _ in range(50):
            h.potentiate("a", "b", amount=1.0)
        assert h.get_weight("a", "b") == 3.0

    def test_weight_floored_at_min(self):
        h = HebbianPlasticity()
        for _ in range(50):
            h.depress("a", "b", amount=1.0)
        assert h.get_weight("a", "b") == 0.1

    def test_directional(self):
        """A→B weight is independent of B→A."""
        h = HebbianPlasticity()
        h.potentiate("a", "b", amount=1.0)
        assert h.get_weight("a", "b") == 2.0
        assert h.get_weight("b", "a") == 1.0  # Default

    def test_persistence(self, tmp_path):
        """Weights should persist to disk and reload."""
        path = str(tmp_path / "strengths.json")
        h1 = HebbianPlasticity(persistence_path=path)
        h1.potentiate("x", "y", amount=0.5)

        h2 = HebbianPlasticity(persistence_path=path)
        assert h2.get_weight("x", "y") == pytest.approx(1.5)


class TestInteroception:
    """System health monitoring — the body's internal sense."""

    def test_healthy_by_default(self):
        monitor = InteroceptionMonitor()
        report = monitor.check_health()
        assert report.healthy is True

    def test_warning_detected(self):
        monitor = InteroceptionMonitor()
        monitor.record("memory_pressure", 0.75, warn=0.7, critical=0.9)
        report = monitor.check_health()
        assert len(report.warnings) == 1
        assert report.healthy is True  # Warning, not critical

    def test_critical_unhealthy(self):
        monitor = InteroceptionMonitor()
        monitor.record("context_window", 0.95, warn=0.7, critical=0.9)
        report = monitor.check_health()
        assert report.healthy is False
        assert len(report.critical) == 1


class TestCerebellumTiming:
    """Predictive scheduling — cerebellum as prediction machine."""

    def test_predict_with_no_data(self):
        ct = CerebellumTiming()
        assert ct.predict_duration("unknown_op") == 0.0

    def test_predict_from_samples(self):
        ct = CerebellumTiming()
        ct.record_duration("gcp_compute", 30.0)
        ct.record_duration("gcp_compute", 40.0)
        ct.record_duration("gcp_compute", 50.0)
        predicted = ct.predict_duration("gcp_compute")
        assert predicted == pytest.approx(40.0)

    def test_should_preempt(self):
        ct = CerebellumTiming()
        ct.record_duration("consolidation", 120.0)
        assert ct.should_preempt("consolidation", deadline_seconds=100.0) is True
        assert ct.should_preempt("consolidation", deadline_seconds=200.0) is False
