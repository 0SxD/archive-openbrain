"""
L7 — Chromatophore Layer (Octopus Skin Display).

Biology: Octopus chromatophores are pigment cells controlled by muscles that
expand or contract in milliseconds. The display IS the state — you don't need
to ask the octopus how it feels; you can see it. Multi-timescale:
    - Chromatophores (ms): instant color changes
    - Iridophores (seconds): structural color shifts
    - Leucophores (minutes): white reflectors for contrast

Principle: State should be visible, not hidden. Multiple timescales:
           instant alerts, session summaries, trend lines.

Source: Eliasmith (2013) — SPAUN's motor output module.
        Octopus chromatophore biology — direct neural control, no hormones.
"""

from __future__ import annotations

import logging
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum, auto
from typing import Any

from openbrainlm.layers.base import Layer, LayerResult, LayerStatus

logger = logging.getLogger(__name__)


# ──────────────────────────────────────────────────────────────────────────────
# Display types
# ──────────────────────────────────────────────────────────────────────────────

class DisplayTimescale(Enum):
    """Multi-timescale state display (biological chromatophore model)."""
    INSTANT = auto()   # Chromatophore — ms response, alert flashes
    SESSION = auto()   # Iridophore — minutes, current session state
    TREND = auto()     # Leucophore — hours/days, patterns over time


class AlertColor(Enum):
    """Chromatophore flash colors — instant state display."""
    GREEN = auto()    # PASS — all clear
    AMBER = auto()    # WARNING — quarantine or uncertainty
    RED = auto()      # BLOCKED — action suppressed or threat
    BLUE = auto()     # INFO — routine status update
    PURPLE = auto()   # RESEARCH — active investigation underway


@dataclass
class ChromatophoreFlash:
    """Instant alert — the fastest display timescale."""
    color: AlertColor
    message: str
    source_layer: str = ""
    timestamp: datetime = field(default_factory=datetime.now)


@dataclass
class IridophoreState:
    """Session-level state display — active agents, current task, memory activity."""
    active_agents: list[str] = field(default_factory=list)
    current_task: str = ""
    memory_tier_activity: dict[str, int] = field(default_factory=dict)
    quarantine_occupancy: int = 0
    audit_status: str = "IDLE"


@dataclass
class LeucophorePattern:
    """Trend-level display — patterns over hours/days."""
    agent_handoff_count: dict[str, int] = field(default_factory=dict)
    research_pipeline_throughput: int = 0
    connection_strength_changes: dict[str, float] = field(default_factory=dict)
    stale_region_count: int = 0


@dataclass
class SystemDisplay:
    """Complete multi-timescale state display."""
    flashes: list[ChromatophoreFlash] = field(default_factory=list)
    session: IridophoreState = field(default_factory=IridophoreState)
    trends: LeucophorePattern = field(default_factory=LeucophorePattern)
    timestamp: datetime = field(default_factory=datetime.now)


# ──────────────────────────────────────────────────────────────────────────────
# L7 Layer
# ──────────────────────────────────────────────────────────────────────────────

class ChromatophoreLayer(Layer):
    """
    L7: Real-time state visualization.

    The display IS the state. You don't ask the system how it feels — you see it.
    Multi-timescale: instant alerts, session summaries, trend lines.

    Consumers:
        - Dashboard agent → web UI
        - Telegram integration → mobile notifications
        - Log system → persistent record
    """

    MAX_FLASH_HISTORY = 100

    def __init__(self):
        super().__init__(
            name="Chromatophore",
            layer_number=7,
            biological_source="Octopus (Chromatophore + Iridophore + Leucophore)"
        )
        self._flash_history: list[ChromatophoreFlash] = []
        self._current_session = IridophoreState()
        self._trends = LeucophorePattern()

    # ── Instant display (chromatophore) ───────────────────────────────────

    def flash(self, color: AlertColor, message: str, source_layer: str = "") -> ChromatophoreFlash:
        """
        Fire a chromatophore flash — instant state change.
        Like the octopus: the display IS the state, no delay.
        """
        f = ChromatophoreFlash(
            color=color,
            message=message,
            source_layer=source_layer,
        )
        self._flash_history.append(f)
        # Trim history
        if len(self._flash_history) > self.MAX_FLASH_HISTORY:
            self._flash_history = self._flash_history[-self.MAX_FLASH_HISTORY:]

        logger.info("L7 FLASH [%s]: %s (from %s)", color.name, message, source_layer or "system")
        return f

    def flash_from_layer_result(self, result: LayerResult) -> ChromatophoreFlash:
        """Auto-generate a flash from any layer's result."""
        if result.status == LayerStatus.BLOCKED:
            color = AlertColor.RED
        elif result.warnings:
            color = AlertColor.AMBER
        else:
            color = AlertColor.GREEN

        return self.flash(
            color=color,
            message=f"{result.layer_name}: {result.status.name}"
                    + (f" — {result.blocked_reason}" if result.blocked_reason else ""),
            source_layer=result.layer_name,
        )

    # ── Session display (iridophore) ──────────────────────────────────────

    def update_session(
        self,
        active_agents: list[str] | None = None,
        current_task: str | None = None,
        quarantine_occupancy: int | None = None,
        audit_status: str | None = None,
    ) -> IridophoreState:
        """Update session-level state display."""
        if active_agents is not None:
            self._current_session.active_agents = active_agents
        if current_task is not None:
            self._current_session.current_task = current_task
        if quarantine_occupancy is not None:
            self._current_session.quarantine_occupancy = quarantine_occupancy
        if audit_status is not None:
            self._current_session.audit_status = audit_status
        return self._current_session

    # ── Trend display (leucophore) ────────────────────────────────────────

    def record_handoff(self, agent_name: str) -> None:
        """Record an agent handoff for trend tracking."""
        count = self._trends.agent_handoff_count.get(agent_name, 0)
        self._trends.agent_handoff_count[agent_name] = count + 1

    def record_connection_change(self, region_id: str, delta: float) -> None:
        """Record a Hebbian connection strength change."""
        current = self._trends.connection_strength_changes.get(region_id, 0.0)
        self._trends.connection_strength_changes[region_id] = current + delta

    # ── Full state snapshot ───────────────────────────────────────────────

    def get_display(self) -> SystemDisplay:
        """Get the complete multi-timescale state display."""
        return SystemDisplay(
            flashes=list(self._flash_history),
            session=self._current_session,
            trends=self._trends,
        )

    def get_recent_flashes(self, count: int = 10) -> list[ChromatophoreFlash]:
        """Get the N most recent flashes."""
        return self._flash_history[-count:]

    # ── Render (text output for console/logs) ─────────────────────────────

    def render_text(self) -> str:
        """Render current state as text (for console/log output)."""
        lines = ["=== OpenBrainLM State ==="]

        # Recent flashes
        recent = self.get_recent_flashes(5)
        if recent:
            lines.append("-- Alerts --")
            for f in recent:
                lines.append(f"  [{f.color.name}] {f.message}")

        # Session
        s = self._current_session
        lines.append("-- Session --")
        lines.append(f"  Task: {s.current_task or 'IDLE'}")
        lines.append(f"  Active agents: {', '.join(s.active_agents) or 'none'}")
        lines.append(f"  Quarantine: {s.quarantine_occupancy} item(s)")
        lines.append(f"  Audit: {s.audit_status}")

        # Trends
        t = self._trends
        if t.agent_handoff_count:
            lines.append("-- Trends --")
            top_agents = sorted(t.agent_handoff_count.items(), key=lambda x: x[1], reverse=True)[:5]
            for agent, count in top_agents:
                lines.append(f"  {agent}: {count} handoff(s)")

        lines.append("=" * 25)
        return "\n".join(lines)

    def process(self, context: dict[str, Any]) -> LayerResult:
        """
        L7 processing: render current state display.
        Always READY — the display layer never blocks.
        """
        display = self.get_display()

        return LayerResult(
            layer_name=self.name,
            status=LayerStatus.READY,
            data={
                "recent_flashes": len(display.flashes),
                "active_agents": display.session.active_agents,
                "current_task": display.session.current_task,
                "quarantine_occupancy": display.session.quarantine_occupancy,
                "text_display": self.render_text(),
            },
        )

    def describe(self) -> str:
        return (
            "Octopus chromatophores: the display IS the state. Multi-timescale: "
            "chromatophores (instant alerts), iridophores (session state), "
            "leucophores (trend patterns). You don't ask the system how it "
            "feels — you SEE it."
        )
