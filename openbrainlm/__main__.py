"""
OpenBrainLM — CLI Entry Point.

Usage:
    python -m openbrainlm                         # Interactive mode
    python -m openbrainlm "train markov model"     # Single query
    python -m openbrainlm --health                 # Health check
    python -m openbrainlm --describe               # Describe all layers

Boots the brain (ignition protocol), processes queries through the full
8-layer pipeline, and displays results via the chromatophore (L7).
"""

from __future__ import annotations

import argparse
import io
import logging
import sys
from pathlib import Path

# Force UTF-8 stdout on Windows to handle Unicode in layer descriptions
if sys.stdout.encoding != "utf-8":
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")

from openbrainlm import __version__
from openbrainlm.orchestrator import OpenBrainOrchestrator
from openbrainlm.registry import AGENT_REGISTRY, REGION_REGISTRY, build_action_channels
from openbrainlm.bridge import SpinalCord, LocalMarkdownStore, ConsoleNotifier, StubAgentBackend
from openbrainlm.layers.ganglion import AgentGanglion
from openbrainlm.layers.basal_ganglia import ActionChannel
from openbrainlm.agents.hippocampus import BrainRegion


# ──────────────────────────────────────────────────────────────────────────────
# Boot
# ──────────────────────────────────────────────────────────────────────────────

def populate_brain(brain: OpenBrainOrchestrator) -> None:
    """Load all 8 core cognitive agents and 8 brain regions into the brain."""
    # L2: Register agent ganglia
    for agent in AGENT_REGISTRY:
        brain.l2_ganglion.register_agent(agent)

    # L4: Register action channels (one per agent)
    for channel in build_action_channels():
        brain.l4_basal_ganglia.register_channel(channel)

    # L5: Register brain regions
    for region in REGION_REGISTRY:
        brain.l5_memory.register_region(region)


def boot_brain(
    governance_paths: list[str] | None = None,
    working_dir: str = "",
    verbose: bool = False,
    bridge: SpinalCord | None = None,
) -> OpenBrainOrchestrator:
    """Full boot sequence: create brain, populate, ignite."""
    brain = OpenBrainOrchestrator(bridge=bridge)

    # Populate with real registry data
    populate_brain(brain)

    # Ignition protocol
    brain.ignite(
        governance_paths=governance_paths or [],
        working_dir=working_dir,
    )

    return brain


# ──────────────────────────────────────────────────────────────────────────────
# Display helpers
# ──────────────────────────────────────────────────────────────────────────────

def print_header() -> None:
    print(f"""
 +==================================================+
 |            OpenBrainLM v{__version__}                   |
 |  Biomimicry (Insect+Octopus+Human)              |
 |  + Trinity Dialectic (Pathos v Logos / Ethos)    |
 |  8 layers | 8 agents  | 8 brain regions         |
 +==================================================+
""")


def print_result(result) -> None:
    """Print a ProcessingResult in a readable format."""
    print("\n" + "=" * 60)

    if result.proceed:
        print("  RESULT: PROCEED")
    else:
        print("  RESULT: BLOCKED")
        if result.state.blocked_reason:
            print(f"  Reason: {result.state.blocked_reason}")

    if result.selected_agents:
        print(f"  Agents: {', '.join(result.selected_agents)}")

    if result.target_regions:
        print(f"  Brain Regions: {', '.join(result.target_regions)}")

    # Layer-by-layer status
    print("\n  Layer Status:")
    for layer_key in sorted(result.state.layer_results.keys()):
        lr = result.state.layer_results[layer_key]
        status = lr.status.name
        marker = "[X]" if status == "BLOCKED" else "[+]" if status == "READY" else "[ ]"
        line = f"    {marker} {layer_key} {lr.layer_name}: {status}"
        if lr.blocked_reason:
            line += f" -- {lr.blocked_reason[:60]}"
        if lr.warnings:
            line += f" (warnings: {len(lr.warnings)})"
        print(line)

    # Chromatophore display
    print("\n" + result.display_text)
    print("=" * 60)


def print_health(health: dict) -> None:
    """Print health check results."""
    print("\n  Health Check:")
    print(f"    Ignited:        {'YES' if health['ignited'] else 'NO'}")
    print(f"    Healthy:        {'YES' if health['healthy'] else 'NO'}")
    print(f"    Trinity:        {'YES' if health['trinity_healthy'] else 'NO'}")

    if health.get("warnings"):
        print(f"    Warnings:       {health['warnings']}")
    if health.get("critical"):
        print(f"    CRITICAL:       {health['critical']}")
    if health.get("metrics"):
        print("    Metrics:")
        for name, value in health["metrics"].items():
            print(f"      {name}: {value}")
    print()


def print_layers(brain: OpenBrainOrchestrator) -> None:
    """Print all layer descriptions."""
    layers = [
        brain.l1_sensing,
        brain.l2_ganglion,
        brain.l3_stigmergy,
        brain.l4_basal_ganglia,
        brain.l5_memory,
        brain.l6_relevance,
        brain.l7_chromatophore,
        brain.l8_pathos,
    ]
    print("\n  8 Operational Layers:")
    for layer in layers:
        print(f"\n    L{layer.layer_number} {layer.name} ({layer.biological_source})")
        # Word-wrap the description
        desc = layer.describe()
        words = desc.split()
        line = "      "
        for word in words:
            if len(line) + len(word) + 1 > 72:
                print(line)
                line = "      " + word
            else:
                line += " " + word if line.strip() else "      " + word
        if line.strip():
            print(line)
    print()


# ──────────────────────────────────────────────────────────────────────────────
# Interactive mode
# ──────────────────────────────────────────────────────────────────────────────

def interactive(brain: OpenBrainOrchestrator, bridge: SpinalCord) -> None:
    """Interactive REPL — type queries, see the brain process them."""
    print("  Interactive mode. Type a query, or:")
    print("    :health    — run health check")
    print("    :layers    — describe all layers")
    print("    :agents    — list registered agents")
    print("    :regions   — list brain regions")
    print("    :quit      — exit")
    print()

    while True:
        try:
            query = input("  brain> ").strip()
        except (EOFError, KeyboardInterrupt):
            print("\n  Shutting down.")
            break

        if not query:
            continue

        if query == ":quit" or query == ":q":
            print("  Shutting down.")
            break

        if query == ":health":
            print_health(brain.health_check())
            continue

        if query == ":layers":
            print_layers(brain)
            continue

        if query == ":agents":
            agents = brain.l2_ganglion.list_agents()
            print(f"\n  {len(agents)} registered agents:")
            for a in agents:
                print(f"    - {a.agent_name} ({a.domain[:40]}...)")
            print()
            continue

        if query in (":notebooks", ":regions"):
            regions = brain.l5_memory.list_regions()
            print(f"\n  {len(regions)} brain regions:")
            for r in regions:
                agents = ", ".join(r.primary_agents) if r.primary_agents else "none"
                print(f"    - {r.name} [{r.region_id}] (agents: {agents})")
            print()
            continue

        # Process query through full pipeline
        result = brain.process({"query": query})
        print_result(result)

        # If agents were selected, show what the bridge would do
        if result.selected_agents:
            for agent_name in result.selected_agents:
                dispatch = bridge.dispatch_agent(agent_name, query)
                print(f"  >> {dispatch.output}")

        if result.target_regions:
            for nb_id in result.target_regions[:3]:  # Top 3
                kb_results = bridge.query_knowledge(nb_id, query)
                for kb in kb_results:
                    print(f"  >> [{kb.region_id}] {kb.answer[:200]}")

        print()


# ──────────────────────────────────────────────────────────────────────────────
# Main
# ──────────────────────────────────────────────────────────────────────────────

def main() -> None:
    parser = argparse.ArgumentParser(
        description="OpenBrainLM — Biomimicry brain engine",
    )
    parser.add_argument("query", nargs="?", help="Single query to process")
    parser.add_argument("--health", action="store_true", help="Run health check")
    parser.add_argument("--describe", action="store_true", help="Describe all layers")
    parser.add_argument("--json", action="store_true", help="Output as JSON (for LLM runtime integration)")
    parser.add_argument("--verbose", "-v", action="store_true", help="Enable debug logging")
    parser.add_argument(
        "--governance", "-g", nargs="*", default=[], help="Governance file paths"
    )
    parser.add_argument(
        "--working-dir", "-w", default="", help="Working directory to scan"
    )
    args = parser.parse_args()

    # Logging
    level = logging.DEBUG if args.verbose else logging.WARNING
    logging.basicConfig(
        level=level,
        format="%(name)s [%(levelname)s] %(message)s",
    )

    if not args.json:
        print_header()
        print("  Igniting...")

    # Build bridge with available backends
    bridge = SpinalCord()

    # Local markdown knowledge store (always available, open source default)
    knowledge_dir = Path(args.working_dir) / "knowledge" if args.working_dir else Path("./knowledge")
    bridge.add_knowledge_backend("local", LocalMarkdownStore(knowledge_dir))
    bridge.set_agent_backend(StubAgentBackend())
    bridge.set_notify_backend(ConsoleNotifier())

    brain = boot_brain(
        governance_paths=args.governance,
        working_dir=args.working_dir,
        verbose=args.verbose,
        bridge=bridge,
    )

    agent_count = len(brain.l2_ganglion.list_agents())
    region_count = len(brain.l5_memory.list_regions())

    # JSON output mode — for LLM runtime integration (any LLM, not just Claude)
    if args.json and args.query:
        import json as json_mod
        result = brain.process({"query": args.query})
        output = {
            "version": __version__,
            "query": args.query,
            "proceed": result.proceed,
            "blocked": result.state.blocked,
            "blocked_by": result.state.blocked_by,
            "blocked_reason": result.state.blocked_reason,
            "selected_agents": result.selected_agents,
            "target_regions": result.target_regions,
            "layers": {
                k: {
                    "status": lr.status.name,
                    "blocked_reason": lr.blocked_reason,
                    "warnings": lr.warnings,
                    "data": {
                        dk: dv for dk, dv in lr.data.items()
                        if isinstance(dv, (str, int, float, bool, list))
                    },
                }
                for k, lr in result.state.layer_results.items()
            },
            "bridge_status": bridge.status(),
        }
        print(json_mod.dumps(output, indent=2, default=str))
        return

    print(f"  Ignited: {agent_count} agents, {region_count} brain regions loaded.")
    print(f"  Bridge: {'CONNECTED' if bridge.is_connected() else 'STANDALONE (local backends only)'}")
    print()

    if args.health:
        print_health(brain.health_check())
        return

    if args.describe:
        print_layers(brain)
        return

    if args.query:
        # Single query mode
        result = brain.process({"query": args.query})
        print_result(result)
        return

    # Interactive mode
    interactive(brain, bridge)


if __name__ == "__main__":
    main()
