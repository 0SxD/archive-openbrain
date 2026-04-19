"""
OpenBrainLM Operational Layers — 8-Layer Biomimicry Architecture (v2).

L1  Active Sensing (Octopus + Rat Whiskers) — Active probe, don't assume
L2  Ganglion (Octopus)                      — Agent autonomy, edge intelligence
L3  Stigmergy + Swarm (Insect)              — Artifact communication + emergence
L4  Action Selection (Basal Ganglia + Thalamus) — Inhibition-based routing
L5  Memory (Hippocampus + Prefrontal)       — 3-tier consolidation
L6  Relevance Detection (Amygdala + Quorum) — 2-stage: fast alarm → slow consensus
L7  Chromatophore (Octopus)                 — Real-time state visualization
L8  Pathos (Human DMN)                      — Background invention (dreams but cannot act)

Cross-cutting: Prediction Error, Hebbian Plasticity, Interoception, Cerebellum Timing.

Corrected from 10 → 8 layers (Eliasmith 2013, Aristotle, adversarial audit).
Merges: L3+L5 → Stigmergy+Swarm, L7+L8 → Relevance Detection.
"""

from openbrainlm.layers.base import Layer, LayerResult, LayerStatus
from openbrainlm.layers.active_sensing import ActiveSensingLayer
from openbrainlm.layers.ganglion import GanglionLayer
from openbrainlm.layers.stigmergy import StigmergyLayer
from openbrainlm.layers.basal_ganglia import BasalGangliaLayer
from openbrainlm.layers.relevance import RelevanceLayer
from openbrainlm.layers.chromatophore import ChromatophoreLayer
from openbrainlm.layers.pathos import PathosLayer

__all__ = [
    "Layer", "LayerResult", "LayerStatus",
    "ActiveSensingLayer",
    "GanglionLayer",
    "StigmergyLayer",
    "BasalGangliaLayer",
    "RelevanceLayer",
    "ChromatophoreLayer",
    "PathosLayer",
]
