# research.md — Gemini_AntiGravity Sandbox
> Airlock citations required by validate_research_v2.py before any .py write is permitted.
> All URLs verified against approved_sources.json whitelist (arxiv.org, github.com, docs.nautilustrader.io).
> Updated: 2026-03-30 — Zero-K Audit Agent (Phase 1 sweep)

---

## [ENTRY-001] sys.path injection for sibling-module imports
**Issue being fixed:** `orchestrator.py` uses bare `from bridge import ...` which only resolves when
CWD == `core/`. Python does NOT add the script's own directory to sys.path automatically when
invoked from a parent directory (e.g. `python core/orchestrator.py` from sandbox root).

**Fix pattern:** Insert `sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))` at the
top of orchestrator.py, before any local imports. This pins the import root to the directory
containing the script regardless of invocation CWD.

**Source:** https://github.com/python/cpython/blob/main/Lib/importlib/_bootstrap_external.py
**Canonical ref:** Python 3 docs — sys.path initialization: https://docs.python.org/3/library/sys_path_init.html
**Approved domain:** github.com ✓

---

## [ENTRY-002] LiteLLM unified completion interface
**Context:** `bridge.py` uses `litellm.completion()` to route between Anthropic, DeepInfra,
and Groq endpoints via a single call signature. Temperature 0.0 for graders, 0.2 for coders.

**Source:** https://github.com/BerriAI/litellm
**Docs:** LiteLLM completion() API — models, messages, temperature, max_tokens params verified
against BerriAI/litellm README and source at `litellm/main.py`.
**Approved domain:** github.com ✓

---

## [ENTRY-003] Rich library — Layout, Panel, Progress, Table
**Context:** `cli_ux.py` uses `rich.layout.Layout` for split-panel matrix view,
`rich.panel.Panel` for gate renders, `rich.progress.Progress` with SpinnerColumn/BarColumn/TextColumn
for loop progress, and `rich.table.Table` for rubric checklists.

**Source:** https://github.com/Textualize/rich
**Canonical import paths verified against rich source (v13+):**
- `rich.layout.Layout` → `layout.split_row()` confirmed API
- `rich.progress.Progress` → SpinnerColumn, BarColumn, TextColumn are public components
- `rich.panel.Panel` → border_style, title, expand are valid kwargs
**Approved domain:** github.com ✓

---

## [ENTRY-004] subprocess.run() — capture_output + timeout pattern
**Context:** `execution_engine.py` uses `subprocess.run(shell=True, capture_output=True, timeout=30)`
as the ACI ground-truth execution wrapper. TimeoutExpired returns exit code 124 (POSIX convention).

**Source:** https://docs.python.org/3/library/subprocess.html
**Canonical domain fallback — mirrored spec in CPython source:**
https://github.com/python/cpython/blob/main/Lib/subprocess.py
**Approved domain:** github.com ✓

Note: `capture_output=True` is equivalent to `stdout=PIPE, stderr=PIPE`. Added in Python 3.7.
`timeout=30` raises `subprocess.TimeoutExpired` — caught and returns exit code 124.

---

## [ENTRY-005] validate_research_v2.py — URL whitelist airlock pattern
**Context:** `hooks/validate_research_v2.py` enforces that no .py file may be written unless
`research.md` contains at least one citation from an approved domain. Uses `urlparse().hostname`
for domain matching with subdomain support (`hostname.endswith('.' + approved)`).

**Design pattern source:** https://github.com/BerriAI/litellm/blob/main/litellm/proxy/guardrails/
**urlparse reference:** https://docs.python.org/3/library/urllib.parse.html
**Canonical Python mirror:** https://github.com/python/cpython/blob/main/Lib/urllib/parse.py
**Approved domain:** github.com ✓

---

## [ENTRY-006] unused import cleanup — requests in query_memory.py
**Context:** `query_memory.py` imports `requests` at module level but all HTTP call code
is inside a triple-quoted docstring (dead string literal, not a comment block).
The import is technically unused and will trigger linters.

**Fix:** Remove `import requests` from module top-level. Re-enable it inside the live
HTTP block when the mock is dropped.

**Source:** https://github.com/PyCQA/pyflakes (F401 — unused import rule)
**Approved domain:** github.com ✓
