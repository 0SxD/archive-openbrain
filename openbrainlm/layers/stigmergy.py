"""
L3 — Stigmergy + Swarm Layer (Insect Hive Mind).

Biology: Ants communicate through stigmergy — modifying the environment to
signal others. Pheromone trails, nest architecture, food caches. The SAME
mechanism that enables communication IS the mechanism that enables emergence.
Splitting them was artificial — an ant colony's emergent intelligence is
BECAUSE of pheromone communication.

Principle: Simple rules + artifact communication → emergent complex behavior.
           No central coordinator needed.

Source: Bhowmick (2021), Ch 6 — stigmergy communication strategies.
        Seeley (2010) — honeybee democracy, collective decision-making.
"""

from __future__ import annotations

import logging
from dataclasses import dataclass, field
from datetime import datetime, timedelta
from enum import Enum, auto
from pathlib import Path
from typing import Any

from openbrainlm.layers.base import Layer, LayerResult, LayerStatus

logger = logging.getLogger(__name__)


# ──────────────────────────────────────────────────────────────────────────────
# Pheromone taxonomy
# ──────────────────────────────────────────────────────────────────────────────

class PheromoneType(Enum):
    """Types of pheromone signals agents leave as artifacts."""
    TRAIL = auto()       # research/*.md — "I found something here"
    ALARM = auto()       # quarantine entries — "Danger, unverified"
    NEST = auto()        # memory/*.md — "This is home territory"
    QUEEN = auto()       # OPEN_BRAIN.md — "This is important for all"
    RECRUITMENT = auto() # task dispatch — "Help needed here"


@dataclass
class Pheromone:
    """A single pheromone signal left by an agent."""
    ptype: PheromoneType
    source_agent: str
    artifact_path: str
    message: str = ""
    deposited_at: datetime = field(default_factory=datetime.now)
    strength: float = 1.0  # Decays over time

    @property
    def decay_days(self) -> int:
        """How many days before this pheromone type decays."""
        return {
            PheromoneType.TRAIL: 30,
            PheromoneType.ALARM: 14,
            PheromoneType.NEST: 999999,    # Persistent
            PheromoneType.QUEEN: 999999,   # Persistent
            PheromoneType.RECRUITMENT: 1,  # Session-scoped
        }[self.ptype]

    def current_strength(self, now: datetime | None = None) -> float:
        """Compute current strength after decay."""
        if now is None:
            now = datetime.now()
        elapsed = (now - self.deposited_at).days
        if elapsed >= self.decay_days:
            return 0.0
        # Linear decay
        return self.strength * (1.0 - elapsed / self.decay_days)


@dataclass
class SwarmSignal:
    """Emergent signal from multiple pheromones reinforcing the same path."""
    path_key: str            # What trail/domain this represents
    contributing_agents: list[str] = field(default_factory=list)
    total_strength: float = 0.0
    pheromone_count: int = 0


# ──────────────────────────────────────────────────────────────────────────────
# L3 Layer
# ──────────────────────────────────────────────────────────────────────────────

class StigmergyLayer(Layer):
    """
    L3: Stigmergy + Swarm — agents communicate through artifacts.

    Agents don't message each other directly. They leave pheromones:
      - Research reports = trail pheromone
      - Memory entries = nest pheromone
      - Knowledge entries = food caches
      - Log entries = scent marks
      - Audit reports = alarm pheromone
      - OPEN_BRAIN.md entries = queen pheromone

    Stronger trails attract more agent attention.
    Trails DECAY: research >1 month old triggers refresh.
    """

    def __init__(self, persistence_path: str | None = None):
        super().__init__(
            name="Stigmergy+Swarm",
            layer_number=3,
            biological_source="Insect Hive Mind"
        )
        self._pheromones: list[Pheromone] = []
        self._persistence_path = Path(persistence_path) if persistence_path else None
        if self._persistence_path:
            self._load_pheromones()

    def deposit(self, pheromone: Pheromone) -> None:
        """An agent deposits a pheromone (creates an artifact)."""
        self._pheromones.append(pheromone)
        self._save_pheromones()
        logger.info(
            "L3: %s deposited %s pheromone at '%s' (strength=%.2f)",
            pheromone.source_agent, pheromone.ptype.name,
            pheromone.artifact_path, pheromone.strength,
        )

    def read_trail(self, path_key: str, now: datetime | None = None) -> SwarmSignal:
        """
        Read the combined pheromone trail for a given path/domain.
        Multiple agents reinforcing the same trail → stronger signal (emergence).
        """
        if now is None:
            now = datetime.now()

        relevant = [
            p for p in self._pheromones
            if path_key.lower() in p.artifact_path.lower()
            and p.current_strength(now) > 0
        ]

        agents = list({p.source_agent for p in relevant})
        total = sum(p.current_strength(now) for p in relevant)

        return SwarmSignal(
            path_key=path_key,
            contributing_agents=agents,
            total_strength=total,
            pheromone_count=len(relevant),
        )

    def get_active_alarms(self, now: datetime | None = None) -> list[Pheromone]:
        """Get all active alarm pheromones (quarantine signals)."""
        if now is None:
            now = datetime.now()
        return [
            p for p in self._pheromones
            if p.ptype == PheromoneType.ALARM
            and p.current_strength(now) > 0
        ]

    def get_stale_trails(self, now: datetime | None = None) -> list[Pheromone]:
        """Find trails that have fully decayed — need refresh."""
        if now is None:
            now = datetime.now()
        return [
            p for p in self._pheromones
            if p.ptype == PheromoneType.TRAIL
            and p.current_strength(now) <= 0
        ]

    def scan_artifacts(self, directory: str) -> list[Pheromone]:
        """
        Scan a directory for artifacts and auto-register as pheromones.
        Each .md file in research/ = trail pheromone.
        Each .md file in memory/ = nest pheromone.
        """
        path = Path(directory)
        discovered = []

        if not path.is_dir():
            return discovered

        for f in path.rglob("*.md"):
            rel = str(f.relative_to(path))
            # Classify by location
            if "research" in rel.lower():
                ptype = PheromoneType.TRAIL
            elif "memory" in rel.lower():
                ptype = PheromoneType.NEST
            elif "open_brain" in f.name.lower():
                ptype = PheromoneType.QUEEN
            else:
                ptype = PheromoneType.TRAIL  # Default

            stat = f.stat()
            mtime = datetime.fromtimestamp(stat.st_mtime)

            pheromone = Pheromone(
                ptype=ptype,
                source_agent="filesystem_scan",
                artifact_path=str(f),
                message=f"Auto-discovered: {f.name}",
                deposited_at=mtime,
            )
            discovered.append(pheromone)
            self._pheromones.append(pheromone)

        logger.info("L3: Scanned '%s' — discovered %d artifacts", directory, len(discovered))
        return discovered

    def process(self, context: dict[str, Any]) -> LayerResult:
        """
        L3 processing: scan for pheromones, report swarm state.

        Checks:
        1. Are there active alarms? (something unverified)
        2. Are there stale trails? (something needs refresh)
        3. What's the strongest trail? (where should attention go)
        """
        now = datetime.now()
        alarms = self.get_active_alarms(now)
        stale = self.get_stale_trails(now)

        warnings = []
        if alarms:
            warnings.append(f"{len(alarms)} active alarm pheromone(s) — unverified content exists")
        if stale:
            warnings.append(f"{len(stale)} stale trail(s) — research needs refresh")

        # If there are critical alarms, block
        critical_alarms = [a for a in alarms if a.strength >= 2.0]
        if critical_alarms:
            return LayerResult(
                layer_name=self.name,
                status=LayerStatus.BLOCKED,
                data={
                    "active_alarms": len(alarms),
                    "stale_trails": len(stale),
                    "total_pheromones": len(self._pheromones),
                    "critical_alarms": [a.message for a in critical_alarms],
                },
                warnings=warnings,
                blocked_reason=(
                    f"{len(critical_alarms)} critical alarm(s) active. "
                    "Cannot proceed until quarantine is resolved."
                ),
            )

        return LayerResult(
            layer_name=self.name,
            status=LayerStatus.READY,
            data={
                "active_alarms": len(alarms),
                "stale_trails": len(stale),
                "total_pheromones": len(self._pheromones),
            },
            warnings=warnings,
        )

    # ── Persistence ────────────────────────────────────────────────────

    def _save_pheromones(self) -> None:
        """Persist pheromones to disk (JSON)."""
        if not self._persistence_path:
            return
        import json
        data = []
        for p in self._pheromones:
            data.append({
                "ptype": p.ptype.name,
                "source_agent": p.source_agent,
                "artifact_path": p.artifact_path,
                "message": p.message,
                "deposited_at": p.deposited_at.isoformat(),
                "strength": p.strength,
            })
        self._persistence_path.parent.mkdir(parents=True, exist_ok=True)
        self._persistence_path.write_text(
            json.dumps(data, indent=2), encoding="utf-8"
        )

    def _load_pheromones(self) -> None:
        """Load pheromones from disk."""
        if not self._persistence_path or not self._persistence_path.exists():
            return
        import json
        try:
            data = json.loads(self._persistence_path.read_text(encoding="utf-8"))
            for entry in data:
                p = Pheromone(
                    ptype=PheromoneType[entry["ptype"]],
                    source_agent=entry["source_agent"],
                    artifact_path=entry["artifact_path"],
                    message=entry.get("message", ""),
                    deposited_at=datetime.fromisoformat(entry["deposited_at"]),
                    strength=entry.get("strength", 1.0),
                )
                self._pheromones.append(p)
            logger.info("L3: Loaded %d pheromones from disk", len(data))
        except Exception as e:
            logger.warning("L3: Failed to load pheromones: %s", e)

    def describe(self) -> str:
        return (
            "Insect stigmergy: ants communicate by modifying the environment. "
            "Agents leave artifacts (research reports, memory entries, logs) as "
            "pheromone trails. Stronger trails attract more attention. "
            "Trails decay — research >1 month old triggers refresh. "
            "Simple rules + artifact communication → emergent complex behavior."
        )
