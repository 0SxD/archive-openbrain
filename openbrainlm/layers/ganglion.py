"""
L2 — Ganglion Layer (Octopus).

Biology: 2/3 of an octopus's ~500M neurons are in the arms. Each arm has its
own ganglion that processes sensory input and executes motor commands locally.
Central brain sets goals; arms figure out HOW.

Principle: Push intelligence to the edge. Center says WHAT, periphery decides HOW.
"""

from __future__ import annotations

import logging
from dataclasses import dataclass, field
from typing import Any

from openbrainlm.layers.base import Layer, LayerResult, LayerStatus

logger = logging.getLogger(__name__)


@dataclass
class AgentGanglion:
    """An agent's local brain — its capabilities and domain."""
    agent_id: str
    agent_name: str
    domain: str
    region_ids: list[str] = field(default_factory=list)
    tools: list[str] = field(default_factory=list)
    can_write: bool = False
    can_execute: bool = False


class GanglionLayer(Layer):
    """L2: Agent autonomy — each agent is a self-contained arm."""

    def __init__(self):
        super().__init__(
            name="Ganglion",
            layer_number=2,
            biological_source="Octopus"
        )
        self._registry: dict[str, AgentGanglion] = {}

    def register_agent(self, ganglion: AgentGanglion) -> None:
        """Register an agent's ganglion (capabilities, domain, tools)."""
        self._registry[ganglion.agent_id] = ganglion
        logger.info("L2: Registered ganglion: %s (%s)", ganglion.agent_name, ganglion.domain)

    def get_agent(self, agent_id: str) -> AgentGanglion | None:
        return self._registry.get(agent_id)

    def list_agents(self) -> list[AgentGanglion]:
        return list(self._registry.values())

    def find_by_domain(self, domain_keyword: str) -> list[AgentGanglion]:
        """Find agents whose domain matches a keyword."""
        return [
            g for g in self._registry.values()
            if domain_keyword.lower() in g.domain.lower()
        ]

    def process(self, context: dict[str, Any]) -> LayerResult:
        """
        Identify which agent(s) should handle this task.
        Returns BLOCKED if no candidates found — inhibition-by-default (basal ganglia).
        """
        task_domain = context.get("domain", "")
        candidates = self.find_by_domain(task_domain) if task_domain else []

        if not candidates:
            return LayerResult(
                layer_name=self.name,
                status=LayerStatus.BLOCKED,
                data={
                    "total_agents": len(self._registry),
                    "candidates": [],
                },
                blocked_reason=(
                    f"No agents registered for domain: '{task_domain}'. "
                    "Default = suppress all — actions require explicit release."
                ),
            )

        return LayerResult(
            layer_name=self.name,
            status=LayerStatus.READY,
            data={
                "total_agents": len(self._registry),
                "candidates": [g.agent_name for g in candidates],
            },
        )

    def describe(self) -> str:
        return (
            "Octopus ganglia: 2/3 of neurons in arms, not central brain. "
            "Each agent has its own local brain with domain expertise."
        )
