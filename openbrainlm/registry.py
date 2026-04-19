"""
OpenBrainLM Agent & Brain Region Registry — The Brain's Anatomy.

Pre-populates 8 core cognitive agents and 8 brain regions.
Called during ignition to wire the brain's ganglia (L2), action channels (L4),
and memory regions (L5).

Every agent is named for the biological/cognitive function it IS — not
a tech domain it serves. The brain starts from these 8 primitives (derived
from SPAUN 2.0 + biomimicry foundations) and self-evolves from there.

10 additional agents will be derived from the symbiosis of neurology and
Nicomachean Ethics heuristic taxonomy — added as the brain matures.
"""

from __future__ import annotations

from openbrainlm.layers.ganglion import AgentGanglion
from openbrainlm.layers.basal_ganglia import ActionChannel
from openbrainlm.agents.hippocampus import BrainRegion


# ──────────────────────────────────────────────────────────────────────────────
# 8 Core Cognitive Agents — the bare minimum for a brain to be a brain
#
# These are cognitive primitives, not tech tools. Named for what they ARE
# biologically. The brain self-evolves from this starting set.
#
# Future: 10 more agents derived from neurology + Nicomachean Ethics taxonomy
# ──────────────────────────────────────────────────────────────────────────────

AGENT_REGISTRY: list[AgentGanglion] = [
    # 1. Hippocampus — memory routing (L5)
    #    Routes queries to brain regions by semantic salience.
    #    Hebbian learning: regions that produce results get stronger connections.
    AgentGanglion(
        agent_id="hippocampus",
        agent_name="hippocampus",
        domain="memory routing brain region consolidation hebbian recall episodic semantic",
        region_ids=["open_brain_memory"],
        tools=["read"],
        can_write=False, can_execute=False,
    ),
    # 2. Explorer — learning, knowledge acquisition
    #    The brain's ability to discover and learn new things.
    #    Dispatches research, finds sources, synthesizes knowledge.
    AgentGanglion(
        agent_id="explorer",
        agent_name="explorer",
        domain="research literature learn discover knowledge synthesis paper arxiv source",
        region_ids=["neural_arc", "rag_vector_search"],
        tools=["read", "write", "web_search", "web_fetch"],
        can_write=True, can_execute=False,
    ),
    # 3. Verifier — error detection, claim validation
    #    Prediction error circuit. Checks if what the brain believes is true.
    #    Zero-trust: nothing accepted without evidence.
    AgentGanglion(
        agent_id="verifier",
        agent_name="verifier",
        domain="verify error detection claim validation evidence proof zero trust audit",
        region_ids=["zero_trust"],
        tools=["read", "grep", "glob"],
        can_write=True, can_execute=False,
    ),
    # 4. Immune — adversarial challenge, threat detection
    #    The brain's immune system. Red team. Hostile twin.
    #    Challenges every claim, attacks every plan, finds weaknesses.
    AgentGanglion(
        agent_id="immune",
        agent_name="immune",
        domain="adversarial challenge threat attack defense falsify red team hostile immune",
        region_ids=["adversarial_security", "barrier"],
        tools=["read", "grep"],
        can_write=True, can_execute=False,
    ),
    # 5. Prefrontal — metacognition, thinking about thinking
    #    Who watches the watchers? Audits the verifier. Audits the immune system.
    #    Recursive self-reflection. Prevents blind spots.
    AgentGanglion(
        agent_id="prefrontal",
        agent_name="prefrontal",
        domain="metacognition recursive review oversight self-reflection audit quality",
        region_ids=["zero_trust"],
        tools=["read", "grep"],
        can_write=True, can_execute=False,
    ),
    # 6. Morphogen — self-modification, neuroplasticity
    #    The octopus RNA editing equivalent. Grows new capabilities.
    #    Builds new agents, modifies architecture, evolves the brain.
    AgentGanglion(
        agent_id="morphogen",
        agent_name="morphogen",
        domain="self-modification neuroplasticity evolve grow adapt build agent architecture",
        region_ids=["agents_arcs", "evolutionary_ml"],
        tools=["read", "write"],
        can_write=True, can_execute=False,
    ),
    # 7. Consolidator — memory consolidation, knowledge store management
    #    Glial cell analogue. Manages long-term storage.
    #    Promotes verified knowledge, compresses, handles sleep cycle.
    AgentGanglion(
        agent_id="consolidator",
        agent_name="consolidator",
        domain="memory consolidation storage promote compress sleep knowledge manage organize",
        region_ids=["open_brain_memory"],
        tools=["read", "write"],
        can_write=True, can_execute=False,
    ),
    # 8. Homeostasis — self-maintenance, internal regulation
    #    Keeps the brain healthy. Cleanup, deduplication, integrity checks.
    #    The brain's autonomic nervous system equivalent.
    AgentGanglion(
        agent_id="homeostasis",
        agent_name="homeostasis",
        domain="self-maintenance cleanup organize integrity health regulate autonomic",
        region_ids=[],
        tools=["read", "write", "glob"],
        can_write=True, can_execute=False,
    ),
]


# ──────────────────────────────────────────────────────────────────────────────
# 8 Brain Regions (LM-LTM repos)
#
# These are the brain's knowledge domains — curated research that ships
# with the project. Each region is a directory under knowledge/ containing
# markdown files searchable by the LocalMarkdownStore backend.
# ──────────────────────────────────────────────────────────────────────────────

REGION_REGISTRY: list[BrainRegion] = [
    # 1. Neural_ARC — neuroscience foundation
    BrainRegion(
        region_id="neural_arc",
        name="Neural_ARC",
        topics=["neural", "brain", "neuroscience", "biomimicry", "consciousness",
                "spaun", "eliasmith", "octopus", "insect", "basal ganglia",
                "amygdala", "hippocampus", "chromatophore", "free energy"],
        primary_agents=["explorer", "hippocampus"],
        source_count=42,
    ),
    # 2. Agents/Arcs — agent architecture patterns
    BrainRegion(
        region_id="agents_arcs",
        name="Agents / Arcs",
        topics=["agent", "architecture", "multi-agent", "orchestration", "ganglion",
                "context engineering", "initializer", "worker", "judge",
                "self-modification", "neuroplasticity"],
        primary_agents=["morphogen", "prefrontal"],
        source_count=156,
    ),
    # 3. Zero Trust — verification philosophy
    BrainRegion(
        region_id="zero_trust",
        name="Zero Trust Architecture",
        topics=["zero trust", "security", "verification", "trust", "audit",
                "claim validation", "proof", "evidence", "prediction error"],
        primary_agents=["verifier", "prefrontal"],
    ),
    # 4. Adversarial Security — immune system methodology
    BrainRegion(
        region_id="adversarial_security",
        name="Adversarial Security / Immune System",
        topics=["adversarial", "security", "red team", "vulnerability",
                "hostile", "attack", "defense", "threat model", "immune"],
        primary_agents=["immune", "verifier"],
    ),
    # 5. Evolutionary ML — self-evolution foundations
    BrainRegion(
        region_id="evolutionary_ml",
        name="Evolutionary ML",
        topics=["evolutionary", "genetic algorithm", "neat", "neuroevolution",
                "mutation", "crossover", "fitness", "population", "rna editing"],
        primary_agents=["explorer", "morphogen"],
    ),
    # 6. RAG / Vector Search — knowledge retrieval architecture
    BrainRegion(
        region_id="rag_vector_search",
        name="RAG Architecture / Vector Search",
        topics=["rag", "retrieval", "vector", "embedding", "search", "semantic",
                "knowledge graph", "similarity", "routing"],
        primary_agents=["explorer"],
    ),
    # 7. Open Brain Memory — the brain's own persistent memory
    BrainRegion(
        region_id="open_brain_memory",
        name="Open Brain Long-Term Memory",
        topics=["open brain", "long-term memory", "consolidation", "knowledge base",
                "brain region", "hippocampus", "episodic", "semantic", "sleep"],
        primary_agents=["consolidator", "hippocampus"],
    ),
    # 8. Blood-Brain Barrier — screening and uncertainty staging
    #    Combines quarantine (unverified input) and doubt parking (uncertainty).
    #    The biological blood-brain barrier controls what enters the brain.
    #    Nothing passes into brain regions without screening here first.
    BrainRegion(
        region_id="barrier",
        name="Blood-Brain Barrier",
        topics=["quarantine", "staging", "unverified", "pending", "zero trust",
                "immune", "verification", "provisional", "doubt", "uncertain",
                "screening", "barrier", "uncertainty"],
        primary_agents=["immune"],
    ),
]


# ──────────────────────────────────────────────────────────────────────────────
# Helper: generate ActionChannels from AgentGanglion registry
# ──────────────────────────────────────────────────────────────────────────────

def build_action_channels() -> list[ActionChannel]:
    """Convert agent ganglia into L4 action channels (one per agent)."""
    channels = []
    for agent in AGENT_REGISTRY:
        channels.append(ActionChannel(
            channel_id=agent.agent_id,
            agent_name=agent.agent_name,
            domain_keywords=agent.domain.split(),
        ))
    return channels
