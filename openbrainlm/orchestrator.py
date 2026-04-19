"""
OpenBrainLM Orchestrator — Ignition Protocol + Layer Stack.

The orchestrator wires all 8 layers + 4 cross-cutting mechanisms together.
It IS the nervous system: receives input, runs it through the layer stack,
and produces a coordinated response.

Ignition sequence (boot):
    1. L1 Active Sensing — probe environment, read governance files
    2. L2 Ganglion — load agent registry
    3. L3 Stigmergy — scan for existing pheromones/artifacts
    4. L4 Basal Ganglia — register action channels (all suppressed)
    5. L5 Hippocampus — register brain regions
    6. L6 Relevance — arm threat detection (amygdala ready)
    7. L7 Chromatophore — initialize display
    8. L8 Pathos — activate DMN if no focused task

Processing pipeline (per query):
    L1 → L6 (threat check) → L4 (select action) → L2 (find agent)
    → L5 (route to brain region) → L3 (check pheromones) → L7 (display)
    → L8 (dream if idle)

Cross-cutting mechanisms fire at every stage:
    - Prediction error: compare expected vs actual at each layer
    - STDP: update connection weights after handoffs
    - Interoception: monitor system health continuously
    - Cerebellum: predict timing for preemptive scheduling
"""

from __future__ import annotations

import logging
from dataclasses import dataclass, field
from typing import Any

from openbrainlm.layers.base import LayerResult, LayerStatus
from openbrainlm.layers.active_sensing import ActiveSensingLayer
from openbrainlm.layers.ganglion import GanglionLayer
from openbrainlm.layers.stigmergy import StigmergyLayer
from openbrainlm.layers.basal_ganglia import BasalGangliaLayer
from openbrainlm.agents.hippocampus import Hippocampus
from openbrainlm.layers.relevance import RelevanceLayer, AlarmLevel
from openbrainlm.layers.chromatophore import ChromatophoreLayer, AlertColor
from openbrainlm.layers.pathos import PathosLayer
from openbrainlm.core.trinity import TrinityEngine, TrinityPhase
from openbrainlm.bridge import SpinalCord
from openbrainlm.cross_cutting import (
    PredictionErrorFilter,
    HebbianPlasticity,
    InteroceptionMonitor,
    CerebellumTiming,
)

logger = logging.getLogger(__name__)


# ──────────────────────────────────────────────────────────────────────────────
# Orchestrator state
# ──────────────────────────────────────────────────────────────────────────────

@dataclass
class OrchestratorState:
    """Current state of the full OpenBrainLM system."""
    ignited: bool = False
    layer_results: dict[str, LayerResult] = field(default_factory=dict)
    blocked: bool = False
    blocked_by: str = ""
    blocked_reason: str = ""


@dataclass
class ProcessingResult:
    """Result of processing a query through the full layer stack."""
    query: str = ""
    state: OrchestratorState = field(default_factory=OrchestratorState)
    selected_agents: list[str] = field(default_factory=list)
    target_regions: list[str] = field(default_factory=list)
    proceed: bool = False
    display_text: str = ""


# ──────────────────────────────────────────────────────────────────────────────
# The Orchestrator
# ──────────────────────────────────────────────────────────────────────────────

class OpenBrainOrchestrator:
    """
    Wires all 8 layers and 4 cross-cutting mechanisms together.

    Usage:
        brain = OpenBrainOrchestrator()
        brain.ignite(governance_paths=[...], working_dir="...")
        result = brain.process({"query": "...", "domain": "..."})
    """

    def __init__(
        self,
        connection_strengths_path: str | None = None,
        bridge: SpinalCord | None = None,
    ):
        # 8 Layers
        self.l1_sensing = ActiveSensingLayer()
        self.l2_ganglion = GanglionLayer()
        self.l3_stigmergy = StigmergyLayer()
        self.l4_basal_ganglia = BasalGangliaLayer()
        self.l5_memory = Hippocampus()
        self.l6_relevance = RelevanceLayer()
        self.l7_chromatophore = ChromatophoreLayer()
        self.l8_pathos = PathosLayer()

        # Core engine
        self.trinity = TrinityEngine()

        # Bridge (spinal cord — pluggable backends for knowledge, agents, notify)
        self.bridge = bridge or SpinalCord()

        # Cross-cutting mechanisms
        self.prediction_error = PredictionErrorFilter()
        self.hebbian = HebbianPlasticity(persistence_path=connection_strengths_path)
        self.interoception = InteroceptionMonitor()
        self.cerebellum = CerebellumTiming()

        # State
        self._state = OrchestratorState()

    @property
    def is_ignited(self) -> bool:
        return self._state.ignited

    # ── Ignition Protocol ─────────────────────────────────────────────────

    def ignite(
        self,
        governance_paths: list[str] | None = None,
        region_ids: list[str] | None = None,
        working_dir: str = "",
    ) -> OrchestratorState:
        """
        Boot sequence — fire up all 8 layers in order.

        1. L1: Probe environment (governance files, working directory)
        2. L2-L8: Initialize all layers
        3. Cross-cutting: Arm all mechanisms
        4. L7: Flash GREEN if all clear, RED if blocked
        """
        logger.info("=== OpenBrainLM IGNITION ===")

        # ── L1: Active Sensing (probe environment) ───────────────────────
        self.l1_sensing = ActiveSensingLayer(
            governance_paths=governance_paths or [],
            region_ids=region_ids or [],
        )
        l1_result = self.l1_sensing.process({"working_directory": working_dir})
        self._state.layer_results["L1"] = l1_result
        self.l7_chromatophore.flash_from_layer_result(l1_result)

        if l1_result.status == LayerStatus.BLOCKED:
            logger.warning("IGNITION: L1 BLOCKED — %s", l1_result.blocked_reason)
            # Continue anyway (governance files may not exist yet during initial setup)
            self.l7_chromatophore.flash(
                AlertColor.AMBER,
                f"L1 governance warning: {l1_result.blocked_reason}",
                "L1",
            )

        # ── L2: Ganglion (agent registry ready) ──────────────────────────
        l2_result = self.l2_ganglion.process({"domain": ""})
        self._state.layer_results["L2"] = l2_result

        # ── L3: Stigmergy (scan existing artifacts) ──────────────────────
        if working_dir:
            self.l3_stigmergy.scan_artifacts(working_dir)
        l3_result = self.l3_stigmergy.process({})
        self._state.layer_results["L3"] = l3_result

        # ── L4: Basal Ganglia (channels registered, all suppressed) ──────
        l4_result = self.l4_basal_ganglia.process({"query": ""})
        self._state.layer_results["L4"] = l4_result

        # ── L5: Hippocampus (brain regions ready for routing) ─────────────────
        l5_result = self.l5_memory.process({"query": ""})
        self._state.layer_results["L5"] = l5_result

        # ── L6: Relevance Detection (amygdala armed) ────────────────────
        l6_result = self.l6_relevance.process({})
        self._state.layer_results["L6"] = l6_result

        # ── L7: Chromatophore (display initialized) ──────────────────────
        l7_result = self.l7_chromatophore.process({})
        self._state.layer_results["L7"] = l7_result

        # ── L8: Pathos (DMN ready, will activate when idle) ──────────────
        l8_result = self.l8_pathos.process({})
        self._state.layer_results["L8"] = l8_result

        # ── Interoception baseline ───────────────────────────────────────
        # Track missing layers (fires when count goes UP = layers failing)
        blocked_layers = sum(
            1 for r in self._state.layer_results.values()
            if r.status == LayerStatus.BLOCKED
        )
        self.interoception.record("blocked_layers_ignition", float(blocked_layers), warn=1.0, critical=3.0)
        snapshot = l1_result.data.get("snapshot")
        gov_count = float(len(snapshot.governance_files)) if hasattr(snapshot, "governance_files") else 0.0
        # Thresholds: alarm when governance count drops BELOW expected
        # HealthMetric fires when value >= threshold, so invert: track MISSING count
        gov_missing = float(len(snapshot.governance_missing)) if hasattr(snapshot, "governance_missing") else 0.0
        self.interoception.record("governance_missing", gov_missing, warn=1.0, critical=2.0)

        self._state.ignited = True

        # Final flash
        self.l7_chromatophore.flash(AlertColor.GREEN, "IGNITION COMPLETE", "orchestrator")
        logger.info("=== OpenBrainLM IGNITED ===")

        return self._state

    # ── Main Processing Pipeline ──────────────────────────────────────────

    def process(self, context: dict[str, Any]) -> ProcessingResult:
        """
        Process a query through the full layer stack.

        Pipeline:
            L6 (threat check) → L4 (select action) → L2 (find agent)
            → L5 (route to brain region) → L3 (check pheromones)
            → L7 (display) → L8 (dream if idle)
        """
        query = context.get("query", "")
        domain = context.get("domain", "")
        action = context.get("action", query)

        result = ProcessingResult(query=query)

        # ── L6: Threat check (amygdala fast scan) ────────────────────────
        l6_result = self.l6_relevance.process({"action": action, **context})
        result.state.layer_results["L6"] = l6_result
        self.l7_chromatophore.flash_from_layer_result(l6_result)

        if l6_result.status == LayerStatus.BLOCKED:
            result.state.blocked = True
            result.state.blocked_by = "L6"
            result.state.blocked_reason = l6_result.blocked_reason or "Threat detected"
            self.l7_chromatophore.flash(AlertColor.RED, f"BLOCKED by L6: {l6_result.blocked_reason}", "L6")

            # Hyperdirect: suppress all L4 channels
            self.l4_basal_ganglia.suppress_all()

            result.display_text = self.l7_chromatophore.render_text()
            return result

        # ── L4: Action selection (basal ganglia) ─────────────────────────
        threat_in_context = l6_result.data.get("alarm_level", "NONE") in ("HIGH", "CRITICAL")
        l4_context = {"query": query, "domain": domain, "threat_detected": threat_in_context}
        l4_result = self.l4_basal_ganglia.process(l4_context)
        result.state.layer_results["L4"] = l4_result
        self.l7_chromatophore.flash_from_layer_result(l4_result)

        if l4_result.status == LayerStatus.BLOCKED:
            result.state.blocked = True
            result.state.blocked_by = "L4"
            result.state.blocked_reason = l4_result.blocked_reason or "No action channels released"
            result.display_text = self.l7_chromatophore.render_text()
            return result

        # Extract released agents
        released_agents = l4_result.data.get("released_agents", [])
        result.selected_agents = released_agents

        # ── L5: Memory routing (brain region lookup) ────────────────────
        l5_result = self.l5_memory.process({"query": query, "domain": domain})
        result.state.layer_results["L5"] = l5_result

        if l5_result.status == LayerStatus.READY:
            routing = l5_result.data.get("routing")
            if hasattr(routing, "target_regions"):
                result.target_regions = routing.target_regions
            elif isinstance(routing, dict):
                result.target_regions = routing.get("target_regions", [])

            # Query knowledge backends for each routed region
            knowledge_answers = []
            for region_id in result.target_regions[:3]:
                kb_results = self.bridge.query_knowledge(region_id, query)
                knowledge_answers.extend(kb_results)
            if knowledge_answers:
                l5_result.data["knowledge_results"] = [
                    {"region": kr.region_id, "answer": kr.answer[:500],
                     "sources": kr.sources_used, "confidence": kr.confidence}
                    for kr in knowledge_answers
                ]

        # ── L3: Check pheromone state ────────────────────────────────────
        l3_result = self.l3_stigmergy.process({})
        result.state.layer_results["L3"] = l3_result

        # ── L7: Update display ───────────────────────────────────────────
        self.l7_chromatophore.update_session(
            active_agents=released_agents,
            current_task=query[:100],
        )
        l7_result = self.l7_chromatophore.process({})
        result.state.layer_results["L7"] = l7_result

        # ── L8: Dream check (suppress if focused task active) ────────────
        l8_context = {"active_task": query} if query else {}
        l8_result = self.l8_pathos.process(l8_context)
        result.state.layer_results["L8"] = l8_result

        # ── Interoception update ─────────────────────────────────────────
        blocked_count = sum(
            1 for r in result.state.layer_results.values()
            if r.status == LayerStatus.BLOCKED
        )
        self.interoception.record("blocked_layers", float(blocked_count), warn=1.0, critical=3.0)

        # ── Final ────────────────────────────────────────────────────────
        result.proceed = not result.state.blocked
        result.display_text = self.l7_chromatophore.render_text()

        self.l7_chromatophore.flash(
            AlertColor.GREEN if result.proceed else AlertColor.RED,
            f"Processing complete: {'PROCEED' if result.proceed else 'BLOCKED'}",
            "orchestrator",
        )

        logger.info(
            "OpenBrain processed: query='%s' → agents=%s, proceed=%s",
            query[:50], released_agents, result.proceed,
        )

        return result

    # ── Convenience ───────────────────────────────────────────────────────

    def get_display(self) -> str:
        """Get current system state as text."""
        return self.l7_chromatophore.render_text()

    def health_check(self) -> dict[str, Any]:
        """Run interoception health check."""
        report = self.interoception.check_health()
        trinity_healthy = self.trinity.is_healthy()

        return {
            "ignited": self._state.ignited,
            "healthy": report.healthy and trinity_healthy,
            "trinity_healthy": trinity_healthy,
            "warnings": report.warnings,
            "critical": report.critical,
            "metrics": {m.name: m.value for m in report.metrics},
        }
