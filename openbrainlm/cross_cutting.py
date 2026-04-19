"""
Cross-Cutting Mechanisms — not layers, they permeate everything.

These four mechanisms operate ACROSS all 8 layers simultaneously.
They are NOT in the layer stack — they influence all layers.

1. Prediction Error Filter (Friston) — route based on surprise
2. Hebbian Plasticity (STDP) — connection strengths adapt over time
3. Interoception — system health monitoring
4. Cerebellum Timing — predictive scheduling

Source: Friston (2010), free-energy principle.
        Eliasmith (2013), Ch 6 — STDP learning.
        Craig (2002) — interoceptive awareness.
        Ito (2008) — cerebellum as prediction machine.
"""

from __future__ import annotations

import json
import logging
from dataclasses import dataclass, field
from datetime import datetime
from pathlib import Path
from typing import Any

logger = logging.getLogger(__name__)


# ──────────────────────────────────────────────────────────────────────────────
# 1. Prediction Error Filter (Friston)
# ──────────────────────────────────────────────────────────────────────────────

@dataclass
class PredictionError:
    """
    When actual observation diverges from prediction.
    Low error → routine (tonic). High error → investigate (hyperdirect).
    """
    source: str
    predicted: Any = None
    actual: Any = None
    magnitude: float = 0.0   # 0-1 normalized surprise
    timestamp: datetime = field(default_factory=datetime.now)

    @property
    def is_surprising(self) -> bool:
        return self.magnitude > 0.5

    @property
    def is_alarming(self) -> bool:
        return self.magnitude > 0.8


class PredictionErrorFilter:
    """
    Every layer generates PREDICTIONS about what it expects.
    When observations diverge → error signal routed by magnitude:
        Low  → routine (tonic mode)
        Med  → flag for attention (L6 amygdala)
        High → suppress action, investigate (L4 hyperdirect)
    """

    def __init__(self):
        self._predictions: dict[str, Any] = {}
        self._errors: list[PredictionError] = []

    def set_prediction(self, key: str, value: Any) -> None:
        """Record what we expect to observe."""
        self._predictions[key] = value

    def observe(self, key: str, actual: Any) -> PredictionError | None:
        """
        Compare observation to prediction.
        Returns PredictionError if there was a prediction, None if no prediction existed.
        """
        if key not in self._predictions:
            return None

        predicted = self._predictions[key]

        # Compute magnitude (simple: 0 if match, 1 if complete mismatch)
        if predicted == actual:
            magnitude = 0.0
        elif isinstance(predicted, (int, float)) and isinstance(actual, (int, float)):
            # Numeric: relative difference
            denom = max(abs(predicted), abs(actual), 1)
            magnitude = min(abs(predicted - actual) / denom, 1.0)
        else:
            # Non-numeric: binary mismatch
            magnitude = 1.0

        error = PredictionError(
            source=key,
            predicted=predicted,
            actual=actual,
            magnitude=magnitude,
        )

        if error.magnitude > 0:
            self._errors.append(error)
            if error.is_alarming:
                logger.warning(
                    "PREDICTION ERROR [%.2f]: %s — expected %s, got %s",
                    magnitude, key, predicted, actual,
                )
            elif error.is_surprising:
                logger.info(
                    "Prediction surprise [%.2f]: %s — expected %s, got %s",
                    magnitude, key, predicted, actual,
                )

        return error

    def get_recent_errors(self, count: int = 10) -> list[PredictionError]:
        return self._errors[-count:]

    def clear_predictions(self) -> None:
        self._predictions.clear()


# ──────────────────────────────────────────────────────────────────────────────
# 2. Hebbian Plasticity (STDP) — Connection Strengths
# ──────────────────────────────────────────────────────────────────────────────

@dataclass
class ConnectionStrength:
    """Hebbian weight between two components (agents, brain regions, layers)."""
    source: str
    target: str
    weight: float = 1.0
    last_updated: datetime = field(default_factory=datetime.now)
    update_count: int = 0


class HebbianPlasticity:
    """
    Connection strengths adapt over time.
    "Neurons that fire together wire together."

    SPIKE-TIMING-DEPENDENT: the ORDER matters.
    A must fire BEFORE B for potentiation (A→B strengthens).
    If B fires before A → depression (A→B weakens).
    """

    WEIGHT_MIN = 0.1
    WEIGHT_MAX = 3.0

    def __init__(self, persistence_path: str | None = None):
        self._connections: dict[str, ConnectionStrength] = {}
        self._persistence_path = Path(persistence_path) if persistence_path else None
        if self._persistence_path and self._persistence_path.exists():
            self._load()

    def _key(self, source: str, target: str) -> str:
        return f"{source}→{target}"

    def get_weight(self, source: str, target: str) -> float:
        key = self._key(source, target)
        conn = self._connections.get(key)
        return conn.weight if conn else 1.0

    def potentiate(self, source: str, target: str, amount: float = 0.1) -> float:
        """Strengthen connection (successful handoff)."""
        key = self._key(source, target)
        conn = self._connections.get(key)
        if conn is None:
            conn = ConnectionStrength(source=source, target=target)
            self._connections[key] = conn

        old = conn.weight
        conn.weight = min(conn.weight + amount, self.WEIGHT_MAX)
        conn.last_updated = datetime.now()
        conn.update_count += 1

        logger.info("STDP POTENTIATE: %s → %.2f (was %.2f)", key, conn.weight, old)
        self._save()
        return conn.weight

    def depress(self, source: str, target: str, amount: float = 0.1) -> float:
        """Weaken connection (rejected/failed handoff)."""
        key = self._key(source, target)
        conn = self._connections.get(key)
        if conn is None:
            conn = ConnectionStrength(source=source, target=target)
            self._connections[key] = conn

        old = conn.weight
        conn.weight = max(conn.weight - amount, self.WEIGHT_MIN)
        conn.last_updated = datetime.now()
        conn.update_count += 1

        logger.info("STDP DEPRESS: %s → %.2f (was %.2f)", key, conn.weight, old)
        self._save()
        return conn.weight

    def get_all_connections(self) -> list[ConnectionStrength]:
        return list(self._connections.values())

    def _save(self) -> None:
        if not self._persistence_path:
            return
        data = {
            k: {
                "source": c.source,
                "target": c.target,
                "weight": c.weight,
                "last_updated": c.last_updated.isoformat(),
                "update_count": c.update_count,
            }
            for k, c in self._connections.items()
        }
        self._persistence_path.parent.mkdir(parents=True, exist_ok=True)
        self._persistence_path.write_text(json.dumps(data, indent=2))

    def _load(self) -> None:
        if not self._persistence_path or not self._persistence_path.exists():
            return
        try:
            data = json.loads(self._persistence_path.read_text())
            for k, v in data.items():
                self._connections[k] = ConnectionStrength(
                    source=v["source"],
                    target=v["target"],
                    weight=v["weight"],
                    last_updated=datetime.fromisoformat(v["last_updated"]),
                    update_count=v.get("update_count", 0),
                )
            logger.info("STDP: Loaded %d connections from %s", len(self._connections), self._persistence_path)
        except (json.JSONDecodeError, KeyError) as e:
            logger.warning("STDP: Failed to load connections: %s", e)


# ──────────────────────────────────────────────────────────────────────────────
# 3. Interoception — System Health Monitoring
# ──────────────────────────────────────────────────────────────────────────────

@dataclass
class HealthMetric:
    """A single health metric reading."""
    name: str
    value: float
    threshold_warn: float = 0.7
    threshold_critical: float = 0.9
    timestamp: datetime = field(default_factory=datetime.now)

    @property
    def is_warning(self) -> bool:
        return self.value >= self.threshold_warn

    @property
    def is_critical(self) -> bool:
        return self.value >= self.threshold_critical


@dataclass
class InteroceptionReport:
    """System health report — the body's internal sense."""
    metrics: list[HealthMetric] = field(default_factory=list)
    healthy: bool = True
    warnings: list[str] = field(default_factory=list)
    critical: list[str] = field(default_factory=list)


class InteroceptionMonitor:
    """
    Continuous monitoring of system health metrics.
    Like the body's interoceptive sense — awareness of internal state.

    Monitors:
    - Context window utilization
    - Token budget remaining
    - Agent availability
    - Memory pressure (region fullness, MEMORY.md line count)
    - Research staleness (age of freshest artifact per domain)
    """

    def __init__(self):
        self._metrics: dict[str, HealthMetric] = {}

    def record(self, name: str, value: float, warn: float = 0.7, critical: float = 0.9) -> HealthMetric:
        """Record a health metric."""
        metric = HealthMetric(
            name=name,
            value=value,
            threshold_warn=warn,
            threshold_critical=critical,
        )
        self._metrics[name] = metric

        if metric.is_critical:
            logger.warning("INTEROCEPTION CRITICAL: %s = %.2f (threshold: %.2f)", name, value, critical)
        elif metric.is_warning:
            logger.info("INTEROCEPTION WARNING: %s = %.2f (threshold: %.2f)", name, value, warn)

        return metric

    def check_health(self) -> InteroceptionReport:
        """Run full health check across all recorded metrics."""
        report = InteroceptionReport()

        for name, metric in self._metrics.items():
            report.metrics.append(metric)
            if metric.is_critical:
                report.critical.append(f"{name}: {metric.value:.2f} (critical threshold: {metric.threshold_critical:.2f})")
                report.healthy = False
            elif metric.is_warning:
                report.warnings.append(f"{name}: {metric.value:.2f} (warn threshold: {metric.threshold_warn:.2f})")

        return report

    def get_metric(self, name: str) -> HealthMetric | None:
        return self._metrics.get(name)


# ──────────────────────────────────────────────────────────────────────────────
# 4. Cerebellum Timing — Predictive Scheduling
# ──────────────────────────────────────────────────────────────────────────────

@dataclass
class TimingModel:
    """Simple timing model for an agent/operation."""
    operation: str
    samples: list[float] = field(default_factory=list)  # Duration in seconds

    @property
    def mean_duration(self) -> float:
        if not self.samples:
            return 0.0
        return sum(self.samples) / len(self.samples)

    @property
    def max_duration(self) -> float:
        return max(self.samples) if self.samples else 0.0


class CerebellumTiming:
    """
    Predictive scheduling based on learned timing models.
    Like the cerebellum: prediction machine for motor timing.

    Track agent execution times → build simple models → preemptive action.
    """

    MAX_SAMPLES = 50

    def __init__(self):
        self._models: dict[str, TimingModel] = {}

    def record_duration(self, operation: str, duration_seconds: float) -> None:
        """Record how long an operation took."""
        if operation not in self._models:
            self._models[operation] = TimingModel(operation=operation)
        model = self._models[operation]
        model.samples.append(duration_seconds)
        if len(model.samples) > self.MAX_SAMPLES:
            model.samples = model.samples[-self.MAX_SAMPLES:]

    def predict_duration(self, operation: str) -> float:
        """Predict how long an operation will take based on history."""
        model = self._models.get(operation)
        if model is None:
            return 0.0
        return model.mean_duration

    def should_preempt(self, operation: str, deadline_seconds: float) -> bool:
        """
        Should we start this operation now to finish by the deadline?
        Returns True if predicted duration is close to or exceeds deadline.
        """
        predicted = self.predict_duration(operation)
        if predicted <= 0:
            return False
        # Start if we need >80% of remaining time
        return predicted >= deadline_seconds * 0.8

    def get_all_models(self) -> dict[str, TimingModel]:
        return dict(self._models)
