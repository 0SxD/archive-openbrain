"""
L1 — Active Sensing Layer (Octopus + Rat Whiskers).

Biology: Octopuses LACK proprioception — they have no internal map of where
their arms are. Each arm discovers itself and its environment through touch
and chemoreception every time. Rats use active whisking at 5-15 Hz — they
MOVE their whiskers to probe, not passively receive. Both strategies:
active probe, not passive receive.

Principle: Don't assume you know. Actively probe. The environment is the
ground truth, not your memory of it.

Source: Eliasmith (2013), Ch 7 — SPAUN visual input hierarchy actively
processes, not passively receives.

Implementation: Mandatory 3-step boot for every agent session:
    1. Read governance files (CLAUDE.md, AGENT_RULES.md, OPEN_BRAIN.md)
    2. Read assigned brain region(s) — actively query, don't assume
    3. Scan working directory for current state
"""

from __future__ import annotations

import logging
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

from openbrainlm.layers.base import Layer, LayerResult, LayerStatus

logger = logging.getLogger(__name__)


@dataclass
class EnvironmentSnapshot:
    """What the agent discovered about its environment."""
    governance_files: list[str] = field(default_factory=list)
    governance_missing: list[str] = field(default_factory=list)
    regions_read: list[str] = field(default_factory=list)
    working_dir_files: list[str] = field(default_factory=list)
    stale_assumptions: list[str] = field(default_factory=list)


class ActiveSensingLayer(Layer):
    """L1: Active environment discovery — probe before acting, always."""

    def __init__(
        self,
        governance_paths: list[str] | None = None,
        region_ids: list[str] | None = None,
    ):
        super().__init__(
            name="ActiveSensing",
            layer_number=1,
            biological_source="Octopus + Rat Whiskers"
        )
        self.governance_paths = governance_paths or []
        self.region_ids = region_ids or []

    def process(self, context: dict[str, Any]) -> LayerResult:
        """
        Boot sequence: discover environment before any action.
        Returns BLOCKED if governance files are missing — no governance = no action.
        """
        snapshot = EnvironmentSnapshot()

        # Step 1: Read governance files (mandatory)
        for path_str in self.governance_paths:
            path = Path(path_str)
            if path.exists():
                snapshot.governance_files.append(str(path))
                logger.info("L1: Read governance file: %s", path.name)
            else:
                snapshot.governance_missing.append(path_str)
                snapshot.stale_assumptions.append(
                    f"Expected governance file missing: {path_str}"
                )

        # Step 2: Brain region IDs to read (actual query happens in orchestrator)
        snapshot.regions_read = list(self.region_ids)

        # Step 3: Scan working directory
        work_dir = context.get("working_directory")
        if work_dir and Path(work_dir).is_dir():
            snapshot.working_dir_files = [
                f.name for f in Path(work_dir).iterdir()
                if not f.name.startswith(".")
            ]

        # BLOCKED if governance files missing — default-suppress (basal ganglia model)
        if snapshot.governance_missing:
            logger.warning(
                "L1 BLOCKED: governance files missing: %s", snapshot.governance_missing
            )
            return LayerResult(
                layer_name=self.name,
                status=LayerStatus.BLOCKED,
                data={"snapshot": snapshot},
                warnings=snapshot.stale_assumptions,
                blocked_reason=(
                    f"Missing governance files: {snapshot.governance_missing}. "
                    "Cannot proceed without governance — inhibition-by-default."
                ),
            )

        return LayerResult(
            layer_name=self.name,
            status=LayerStatus.READY,
            data={"snapshot": snapshot},
            warnings=snapshot.stale_assumptions if snapshot.stale_assumptions else [],
        )

    def describe(self) -> str:
        return (
            "Octopus active sensing + rat whisking: arms discover environment "
            "through active touch, not internal maps. Agents probe current state "
            "before every action — the codebase IS the ground truth."
        )
