"""Base layer interface — all 8 operational layers implement this."""

from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from enum import Enum, auto
from typing import Any


class LayerStatus(Enum):
    READY = auto()
    ACTIVE = auto()
    BLOCKED = auto()
    BYPASSED = auto()


@dataclass
class LayerResult:
    """Standard output from any layer."""
    layer_name: str
    status: LayerStatus
    data: dict[str, Any] = field(default_factory=dict)
    warnings: list[str] = field(default_factory=list)
    blocked_reason: str | None = None


class Layer(ABC):
    """
    Abstract base for all operational layers.
    Each layer processes input and produces a LayerResult.
    Layers can block downstream processing (amygdala, quorum).
    """

    def __init__(self, name: str, layer_number: int, biological_source: str):
        self.name = name
        self.layer_number = layer_number
        self.biological_source = biological_source
        self.status = LayerStatus.READY

    @abstractmethod
    def process(self, context: dict[str, Any]) -> LayerResult:
        """Process input and return result. May block if necessary."""
        ...

    @abstractmethod
    def describe(self) -> str:
        """Biomimicry description — what biological mechanism this implements."""
        ...

    def __repr__(self) -> str:
        return f"L{self.layer_number}:{self.name}({self.biological_source})"
