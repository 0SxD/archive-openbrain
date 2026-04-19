"""
OpenBrainLM Bridge — The Spinal Cord.

LM-AGNOSTIC interface between the brain's decision engine and external systems.

Biology: The spinal cord doesn't make decisions — it relays them.
The brain (basal ganglia, cortex) decides WHAT to do.
The spinal cord (bridge) executes HOW.
An octopus brain works with 8 arms. A human brain works with 2.
Same decision-making architecture, different execution layer.

The bridge has THREE pluggable backends:
    1. KnowledgeBackend  — where the brain stores/retrieves knowledge
    2. AgentBackend      — how the brain dispatches agents
    3. NotifyBackend     — how the brain communicates with the owner

Each backend has multiple implementations:
    KnowledgeBackend:
        - LocalMarkdownStore    (open source, works offline, default)
        - VectorStore           (any vector DB / RAG — Pinecone, Chroma, etc.)
        - (future: any knowledge system via Protocol)

    AgentBackend:
        - StubAgentBackend      (standalone, no LLM required — default)
        - LLMDispatcher         (any LLM API — provider-agnostic)
        - GraphDispatcher       (LangGraph, CrewAI, AutoGen, etc.)
        - (future: any agent framework via Protocol)

    NotifyBackend:
        - ConsoleNotifier       (print to stdout — default)
        - TelegramNotifier      (mobile push via bot)
        - (future: Slack, Discord, email)

The brain doesn't know or care which backends are active.
It sends decisions through the bridge. The bridge adapts.
"""

from __future__ import annotations

import json
import logging
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Protocol, runtime_checkable

logger = logging.getLogger(__name__)


# ──────────────────────────────────────────────────────────────────────────────
# Result types — LM-agnostic, no vendor references
# ──────────────────────────────────────────────────────────────────────────────

@dataclass
class KnowledgeResult:
    """Result of querying a knowledge region (brain region, vector DB, file store)."""
    region_id: str
    answer: str = ""
    sources_used: list[str] = field(default_factory=list)
    confidence: float = 0.0
    backend: str = ""  # Which backend answered (e.g., "local_markdown")


@dataclass
class AgentDispatchResult:
    """Result of dispatching an agent to perform a task."""
    agent_name: str
    task: str = ""
    status: str = "pending"  # pending, running, completed, failed
    output: str = ""
    backend: str = ""  # Which backend dispatched (e.g., "claude_code", "langraph")


@dataclass
class NotifyResult:
    """Result of sending a notification."""
    delivered: bool = False
    channel: str = ""  # "console", "telegram", etc.


# ──────────────────────────────────────────────────────────────────────────────
# Backend Protocols — what the brain expects from its spinal cord
# ──────────────────────────────────────────────────────────────────────────────

@runtime_checkable
class KnowledgeBackend(Protocol):
    """Where the brain stores and retrieves knowledge."""

    def query(self, region_id: str, query: str) -> KnowledgeResult:
        """Query a knowledge region by ID."""
        ...

    def store(self, region_id: str, content: str, metadata: dict[str, Any] | None = None) -> bool:
        """Store content in a knowledge region."""
        ...

    def list_regions(self) -> list[str]:
        """List available region IDs."""
        ...

    def is_available(self) -> bool:
        """Check if this backend is reachable."""
        ...


@runtime_checkable
class AgentBackend(Protocol):
    """How the brain dispatches agents."""

    def dispatch(
        self, agent_name: str, task: str, context: dict[str, Any] | None = None
    ) -> AgentDispatchResult:
        """Dispatch an agent to perform a task."""
        ...

    def is_available(self) -> bool:
        """Check if this backend can dispatch agents."""
        ...


@runtime_checkable
class NotifyBackend(Protocol):
    """How the brain communicates with the owner."""

    def notify(self, message: str, severity: str = "INFO") -> NotifyResult:
        """Send a notification."""
        ...


# ──────────────────────────────────────────────────────────────────────────────
# The Bridge — assembles backends into a unified spinal cord
# ──────────────────────────────────────────────────────────────────────────────

class SpinalCord:
    """
    Assembles pluggable backends into a unified interface.

    Usage:
        bridge = SpinalCord()
        bridge.add_knowledge_backend("local", LocalMarkdownStore("./knowledge"))
        bridge.add_knowledge_backend("vectors", VectorStore(...))
        bridge.set_agent_backend(LLMDispatcher(api_key="..."))
        bridge.set_notify_backend(ConsoleNotifier())

    The brain calls bridge methods. The bridge routes to available backends.
    If a backend isn't available, it falls back gracefully.
    """

    def __init__(self):
        self._knowledge_backends: dict[str, KnowledgeBackend] = {}
        self._agent_backend: AgentBackend | None = None
        self._notify_backend: NotifyBackend | None = None

    # ── Configuration ────────────────────────────────────────────────────

    def add_knowledge_backend(self, name: str, backend: KnowledgeBackend) -> None:
        """Register a knowledge backend. Multiple can coexist (fan-out queries)."""
        self._knowledge_backends[name] = backend
        logger.info("Bridge: registered knowledge backend '%s'", name)

    def set_agent_backend(self, backend: AgentBackend) -> None:
        """Set the agent dispatch backend (only one active at a time)."""
        self._agent_backend = backend
        logger.info("Bridge: agent backend set")

    def set_notify_backend(self, backend: NotifyBackend) -> None:
        """Set the notification backend."""
        self._notify_backend = backend
        logger.info("Bridge: notify backend set")

    # ── Knowledge queries ────────────────────────────────────────────────

    def query_knowledge(self, region_id: str, query: str) -> list[KnowledgeResult]:
        """
        Query knowledge backends. Returns results from ALL available backends.
        The brain's L5 routing already decided WHICH region — the bridge asks HOW.
        """
        if not self._knowledge_backends:
            logger.warning("Bridge: no knowledge backends registered")
            return [KnowledgeResult(
                region_id=region_id,
                answer="[NO BACKEND] No knowledge backends registered.",
                backend="none",
            )]

        results = []
        for name, backend in self._knowledge_backends.items():
            if backend.is_available():
                try:
                    result = backend.query(region_id, query)
                    result.backend = name
                    results.append(result)
                except Exception as e:
                    logger.error("Bridge: knowledge backend '%s' failed: %s", name, e)
                    results.append(KnowledgeResult(
                        region_id=region_id,
                        answer=f"[ERROR] Backend '{name}' failed: {e}",
                        backend=name,
                    ))

        return results or [KnowledgeResult(
            region_id=region_id,
            answer="[UNAVAILABLE] All knowledge backends offline.",
            backend="none",
        )]

    def store_knowledge(
        self, region_id: str, content: str, metadata: dict[str, Any] | None = None
    ) -> dict[str, bool]:
        """Store content in all available knowledge backends. Returns {backend: success}."""
        results = {}
        for name, backend in self._knowledge_backends.items():
            if backend.is_available():
                try:
                    results[name] = backend.store(region_id, content, metadata)
                except Exception as e:
                    logger.error("Bridge: store to '%s' failed: %s", name, e)
                    results[name] = False
        return results

    # ── Agent dispatch ───────────────────────────────────────────────────

    def dispatch_agent(
        self, agent_name: str, task: str, context: dict[str, Any] | None = None
    ) -> AgentDispatchResult:
        """Dispatch an agent via the active backend."""
        if not self._agent_backend or not self._agent_backend.is_available():
            logger.warning("Bridge: no agent backend available")
            return AgentDispatchResult(
                agent_name=agent_name,
                task=task,
                status="unavailable",
                output="[NO BACKEND] No agent dispatch backend available.",
                backend="none",
            )
        try:
            return self._agent_backend.dispatch(agent_name, task, context)
        except Exception as e:
            logger.error("Bridge: agent dispatch failed: %s", e)
            return AgentDispatchResult(
                agent_name=agent_name, task=task, status="failed",
                output=f"[ERROR] Dispatch failed: {e}", backend="error",
            )

    # ── Notifications ────────────────────────────────────────────────────

    def notify(self, message: str, severity: str = "INFO") -> NotifyResult:
        """Send a notification via the active backend."""
        if not self._notify_backend:
            # Fallback: print to console
            print(f"  >> [{severity}] {message}")
            return NotifyResult(delivered=True, channel="console_fallback")
        return self._notify_backend.notify(message, severity)

    # ── Status ───────────────────────────────────────────────────────────

    def status(self) -> dict[str, Any]:
        """Report which backends are connected and available."""
        return {
            "knowledge_backends": {
                name: backend.is_available()
                for name, backend in self._knowledge_backends.items()
            },
            "agent_backend": (
                self._agent_backend.is_available() if self._agent_backend else False
            ),
            "notify_backend": self._notify_backend is not None,
        }

    def is_connected(self) -> bool:
        """True if at least one knowledge backend and agent backend are available."""
        has_knowledge = any(
            b.is_available() for b in self._knowledge_backends.values()
        )
        has_agents = (
            self._agent_backend is not None and self._agent_backend.is_available()
        )
        return has_knowledge and has_agents


# ──────────────────────────────────────────────────────────────────────────────
# Built-in backends (stdlib only — no external dependencies)
# ──────────────────────────────────────────────────────────────────────────────

class LocalMarkdownStore:
    """
    Knowledge backend using local markdown files.
    Open source, works offline, no vendor lock-in.

    Structure:
        knowledge_dir/
            region_id/
                source_1.md
                source_2.md
                ...

    Query = keyword search across files in the region directory.
    Store = write a new .md file to the region directory.
    """

    def __init__(self, knowledge_dir: str | Path):
        self._dir = Path(knowledge_dir)

    def query(self, region_id: str, query: str) -> KnowledgeResult:
        region_dir = self._dir / region_id
        if not region_dir.exists():
            return KnowledgeResult(
                region_id=region_id,
                answer=f"Region '{region_id}' not found in local store.",
            )

        # Simple keyword search across all .md files in the region
        query_words = set(query.lower().split())
        matches = []
        for md_file in region_dir.glob("*.md"):
            try:
                content = md_file.read_text(encoding="utf-8", errors="replace")
                content_lower = content.lower()
                score = sum(1 for w in query_words if w in content_lower)
                if score > 0:
                    matches.append((score, md_file.name, content[:500]))
            except Exception:
                continue

        matches.sort(reverse=True, key=lambda x: x[0])

        if not matches:
            return KnowledgeResult(
                region_id=region_id,
                answer=f"No matches for '{query}' in region '{region_id}'.",
                sources_used=[],
            )

        # Return top 3 matches
        top = matches[:3]
        answer_parts = []
        sources = []
        for score, name, preview in top:
            answer_parts.append(f"[{name}] {preview}...")
            sources.append(name)

        return KnowledgeResult(
            region_id=region_id,
            answer="\n\n".join(answer_parts),
            sources_used=sources,
            confidence=min(1.0, top[0][0] / max(len(query_words), 1)),
        )

    def store(self, region_id: str, content: str, metadata: dict[str, Any] | None = None) -> bool:
        region_dir = self._dir / region_id
        region_dir.mkdir(parents=True, exist_ok=True)

        # Generate filename from metadata or content
        name = "entry"
        if metadata and "name" in metadata:
            name = metadata["name"].replace(" ", "_").lower()

        from datetime import datetime
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"{name}_{timestamp}.md"

        filepath = region_dir / filename
        filepath.write_text(content, encoding="utf-8")
        logger.info("LocalMarkdownStore: stored %s in %s", filename, region_id)
        return True

    def list_regions(self) -> list[str]:
        if not self._dir.exists():
            return []
        return [d.name for d in self._dir.iterdir() if d.is_dir()]

    def is_available(self) -> bool:
        return True  # Local files are always available


class ConsoleNotifier:
    """Notification backend that prints to console. Always available."""

    def notify(self, message: str, severity: str = "INFO") -> NotifyResult:
        print(f"  >> [{severity}] {message}")
        return NotifyResult(delivered=True, channel="console")


class StubAgentBackend:
    """Agent backend that logs dispatch intent but doesn't execute. For testing."""

    def dispatch(
        self, agent_name: str, task: str, context: dict[str, Any] | None = None
    ) -> AgentDispatchResult:
        logger.info("STUB: would dispatch '%s' for: %s", agent_name, task[:50])
        return AgentDispatchResult(
            agent_name=agent_name, task=task, status="stub",
            output=f"[STUB] Agent '{agent_name}' would handle: {task[:50]}",
            backend="stub",
        )

    def is_available(self) -> bool:
        return True
