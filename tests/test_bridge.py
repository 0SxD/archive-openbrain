"""
Tests for SpinalCord — the Spinal Cord.

The bridge is LM-agnostic. It relays decisions to pluggable backends.
Tests cover:
    1. Knowledge backends (fan-out queries, store to multiple, fallback)
    2. Agent dispatch (with/without backend, error handling)
    3. Notifications (with/without backend, console fallback)
    4. Status and connectivity checks
    5. Error resilience (backend failures don't crash the bridge)
"""

from typing import Any

import pytest

from openbrainlm.bridge import (
    AgentBackend,
    AgentDispatchResult,
    SpinalCord,
    ConsoleNotifier,
    KnowledgeBackend,
    KnowledgeResult,
    LocalMarkdownStore,
    NotifyBackend,
    NotifyResult,
    StubAgentBackend,
)


# ──────────────────────────────────────────────────────────────────────────────
# Test backends (mock implementations satisfying Protocol)
# ──────────────────────────────────────────────────────────────────────────────

class MockKnowledgeBackend:
    """Test knowledge backend that returns canned results."""

    def __init__(self, name: str = "mock", available: bool = True):
        self._name = name
        self._available = available
        self._stored: list[tuple[str, str]] = []

    def query(self, region_id: str, query: str) -> KnowledgeResult:
        return KnowledgeResult(
            region_id=region_id,
            answer=f"Answer from {self._name}: {query}",
            sources_used=[f"{self._name}_source"],
            confidence=0.8,
        )

    def store(self, region_id: str, content: str, metadata: dict[str, Any] | None = None) -> bool:
        self._stored.append((region_id, content))
        return True

    def list_regions(self) -> list[str]:
        return ["test_region"]

    def is_available(self) -> bool:
        return self._available


class FailingKnowledgeBackend:
    """Backend that throws on query."""

    def query(self, region_id: str, query: str) -> KnowledgeResult:
        raise RuntimeError("Backend exploded")

    def store(self, region_id: str, content: str, metadata: dict[str, Any] | None = None) -> bool:
        raise RuntimeError("Store exploded")

    def list_regions(self) -> list[str]:
        return []

    def is_available(self) -> bool:
        return True


class MockAgentBackend:
    def __init__(self, available: bool = True):
        self._available = available

    def dispatch(self, agent_name: str, task: str, context: dict[str, Any] | None = None) -> AgentDispatchResult:
        return AgentDispatchResult(
            agent_name=agent_name,
            task=task,
            status="completed",
            output=f"Agent {agent_name} done",
            backend="mock",
        )

    def is_available(self) -> bool:
        return self._available


class FailingAgentBackend:
    def dispatch(self, agent_name: str, task: str, context: dict[str, Any] | None = None) -> AgentDispatchResult:
        raise RuntimeError("Dispatch exploded")

    def is_available(self) -> bool:
        return True


# ──────────────────────────────────────────────────────────────────────────────
# Fixtures
# ──────────────────────────────────────────────────────────────────────────────

@pytest.fixture
def bridge():
    """Bridge with one mock knowledge backend and stub agent backend."""
    b = SpinalCord()
    b.add_knowledge_backend("mock", MockKnowledgeBackend("mock"))
    b.set_agent_backend(StubAgentBackend())
    b.set_notify_backend(ConsoleNotifier())
    return b


@pytest.fixture
def empty_bridge():
    """Bridge with no backends configured."""
    return SpinalCord()


# ──────────────────────────────────────────────────────────────────────────────
# Knowledge Queries
# ──────────────────────────────────────────────────────────────────────────────

class TestKnowledgeQueries:
    def test_query_returns_results(self, bridge):
        """Knowledge query must return results from registered backend."""
        results = bridge.query_knowledge("test_region", "what is X?")
        assert len(results) == 1
        assert "mock" in results[0].answer
        assert results[0].backend == "mock"

    def test_fan_out_to_multiple_backends(self):
        """Query must fan out to ALL available backends."""
        b = SpinalCord()
        b.add_knowledge_backend("a", MockKnowledgeBackend("backend_a"))
        b.add_knowledge_backend("b", MockKnowledgeBackend("backend_b"))
        results = b.query_knowledge("reg", "test")
        assert len(results) == 2
        backends = {r.backend for r in results}
        assert backends == {"a", "b"}

    def test_no_backends_returns_fallback(self, empty_bridge):
        """No backends → returns NO BACKEND message."""
        results = empty_bridge.query_knowledge("any", "any")
        assert len(results) == 1
        assert "NO BACKEND" in results[0].answer

    def test_unavailable_backend_skipped(self):
        """Unavailable backends must be skipped."""
        b = SpinalCord()
        b.add_knowledge_backend("up", MockKnowledgeBackend("up", available=True))
        b.add_knowledge_backend("down", MockKnowledgeBackend("down", available=False))
        results = b.query_knowledge("reg", "test")
        assert len(results) == 1
        assert results[0].backend == "up"

    def test_failing_backend_returns_error(self):
        """Backend that throws must return error result, not crash."""
        b = SpinalCord()
        b.add_knowledge_backend("bad", FailingKnowledgeBackend())
        results = b.query_knowledge("reg", "test")
        assert len(results) == 1
        assert "ERROR" in results[0].answer

    def test_all_backends_down_returns_unavailable(self):
        """All backends unavailable → UNAVAILABLE message."""
        b = SpinalCord()
        b.add_knowledge_backend("down", MockKnowledgeBackend("down", available=False))
        results = b.query_knowledge("reg", "test")
        assert len(results) == 1
        assert "UNAVAILABLE" in results[0].answer


# ──────────────────────────────────────────────────────────────────────────────
# Knowledge Storage
# ──────────────────────────────────────────────────────────────────────────────

class TestKnowledgeStorage:
    def test_store_to_backend(self, bridge):
        results = bridge.store_knowledge("test_region", "content here")
        assert results["mock"] is True

    def test_store_to_multiple_backends(self):
        b = SpinalCord()
        a = MockKnowledgeBackend("a")
        c = MockKnowledgeBackend("c")
        b.add_knowledge_backend("a", a)
        b.add_knowledge_backend("c", c)
        results = b.store_knowledge("reg", "data")
        assert results == {"a": True, "c": True}

    def test_store_with_failing_backend(self):
        b = SpinalCord()
        b.add_knowledge_backend("bad", FailingKnowledgeBackend())
        results = b.store_knowledge("reg", "data")
        assert results["bad"] is False


# ──────────────────────────────────────────────────────────────────────────────
# Agent Dispatch
# ──────────────────────────────────────────────────────────────────────────────

class TestAgentDispatch:
    def test_dispatch_with_backend(self):
        b = SpinalCord()
        b.set_agent_backend(MockAgentBackend())
        result = b.dispatch_agent("explorer", "research brain")
        assert result.status == "completed"
        assert result.backend == "mock"

    def test_dispatch_without_backend(self, empty_bridge):
        """No agent backend → unavailable result."""
        result = empty_bridge.dispatch_agent("explorer", "task")
        assert result.status == "unavailable"
        assert "NO BACKEND" in result.output

    def test_dispatch_with_unavailable_backend(self):
        b = SpinalCord()
        b.set_agent_backend(MockAgentBackend(available=False))
        result = b.dispatch_agent("explorer", "task")
        assert result.status == "unavailable"

    def test_dispatch_with_failing_backend(self):
        """Backend that throws must return error result."""
        b = SpinalCord()
        b.set_agent_backend(FailingAgentBackend())
        result = b.dispatch_agent("explorer", "task")
        assert result.status == "failed"
        assert "ERROR" in result.output

    def test_stub_backend_returns_stub_status(self):
        b = SpinalCord()
        b.set_agent_backend(StubAgentBackend())
        result = b.dispatch_agent("immune", "check threat")
        assert result.status == "stub"
        assert result.backend == "stub"


# ──────────────────────────────────────────────────────────────────────────────
# Notifications
# ──────────────────────────────────────────────────────────────────────────────

class TestNotifications:
    def test_notify_with_backend(self, bridge, capsys):
        result = bridge.notify("test message", "WARNING")
        assert result.delivered is True
        assert result.channel == "console"
        captured = capsys.readouterr()
        assert "WARNING" in captured.out

    def test_notify_without_backend(self, empty_bridge, capsys):
        """No notify backend → console fallback."""
        result = empty_bridge.notify("fallback message", "INFO")
        assert result.delivered is True
        assert result.channel == "console_fallback"
        captured = capsys.readouterr()
        assert "fallback message" in captured.out


# ──────────────────────────────────────────────────────────────────────────────
# Status and Connectivity
# ──────────────────────────────────────────────────────────────────────────────

class TestStatus:
    def test_status_reports_backends(self, bridge):
        status = bridge.status()
        assert status["knowledge_backends"]["mock"] is True
        assert status["agent_backend"] is True
        assert status["notify_backend"] is True

    def test_status_empty_bridge(self, empty_bridge):
        status = empty_bridge.status()
        assert status["knowledge_backends"] == {}
        assert status["agent_backend"] is False
        assert status["notify_backend"] is False

    def test_is_connected_with_both(self, bridge):
        assert bridge.is_connected() is True

    def test_not_connected_without_knowledge(self):
        b = SpinalCord()
        b.set_agent_backend(StubAgentBackend())
        assert b.is_connected() is False

    def test_not_connected_without_agents(self):
        b = SpinalCord()
        b.add_knowledge_backend("k", MockKnowledgeBackend())
        assert b.is_connected() is False

    def test_not_connected_empty(self, empty_bridge):
        assert empty_bridge.is_connected() is False


# ──────────────────────────────────────────────────────────────────────────────
# LocalMarkdownStore
# ──────────────────────────────────────────────────────────────────────────────

class TestLocalMarkdownStore:
    def test_query_finds_matching_content(self, tmp_path):
        region_dir = tmp_path / "neural_arc"
        region_dir.mkdir()
        (region_dir / "finding.md").write_text("# Neuroscience\nThe brain has neurons.")

        store = LocalMarkdownStore(str(tmp_path))
        result = store.query("neural_arc", "neurons brain")
        assert result.confidence > 0
        assert "finding.md" in result.sources_used

    def test_query_no_match(self, tmp_path):
        region_dir = tmp_path / "neural_arc"
        region_dir.mkdir()
        (region_dir / "finding.md").write_text("# Cooking\nPasta recipes.")

        store = LocalMarkdownStore(str(tmp_path))
        result = store.query("neural_arc", "quantum physics")
        assert result.confidence == 0
        assert len(result.sources_used) == 0

    def test_query_nonexistent_region(self, tmp_path):
        store = LocalMarkdownStore(str(tmp_path))
        result = store.query("nonexistent", "anything")
        assert "not found" in result.answer

    def test_store_creates_file(self, tmp_path):
        store = LocalMarkdownStore(str(tmp_path))
        success = store.store("neural_arc", "# New Finding", {"name": "discovery"})
        assert success is True
        files = list((tmp_path / "neural_arc").glob("*.md"))
        assert len(files) == 1
        assert "discovery" in files[0].name

    def test_list_regions(self, tmp_path):
        (tmp_path / "region_a").mkdir()
        (tmp_path / "region_b").mkdir()
        store = LocalMarkdownStore(str(tmp_path))
        regions = store.list_regions()
        assert set(regions) == {"region_a", "region_b"}

    def test_is_available(self, tmp_path):
        store = LocalMarkdownStore(str(tmp_path))
        assert store.is_available() is True
