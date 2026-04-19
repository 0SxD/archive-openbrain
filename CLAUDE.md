# OpenBrainLM — Subproject Governance
> Auto-loaded by Claude Code when working in this directory.
> Parent governance: `<WORKSPACE>\CLAUDE.md` (inherits all global rules).

---

## What Is This

A harness for large language models. Three parts: Trinity (dialectic reasoning),
Memory (persistence across sessions), Self-Learning Loop (research + verification).

The harness is MD files, rules, skills, hooks, memory, and agent dispatch.
LM-agnostic — works with any backend.

## Owner

See parent `<WORKSPACE>\CLAUDE.md` for owner profile.

## The Harness (What's Operational)

### Trinity Mode
- **Ethos** — evidence corridors + rules + evaluation criteria (set per task)
- **Pathos** — the mission (Opus doing work, managing agents and memory)
- **Logos** — the gates (Sonnet agent checking work against Ethos)
- Trinity is a DIALECTIC, not a pipeline. The structured disagreement IS the reasoning.
- **Spec:** `memory/trinity_mode_spec.md` — AUTHORITATIVE

### Memory
- `memory/short_term.md` — session activity ledger
- `memory/long_term.md` — verified findings (consolidated from short_term)
- `memory/todos.md` — persistent task list
- `memory/connections.md` — what works/doesn't, cross-refs
- Auto-consolidation at session breakpoints and end

### Self-Learning Loop
- corridor → verify → cite → save → explore/learn
- Corridors: NotebookLM (1-2 assigned), arXiv, GitHub, Context7
- Source hierarchy: arXiv → top-tier academics → open source GitHub
- Loop count and depth set per task

### Rules
1. **No public actions without explicit approval.** (rule 00)
2. **Trinity is a DIALECTIC, not a pipeline.** Logos and Pathos fight. Ethos provides the corridors and criteria.
3. **Always cite.** No claims without third-party sources.
4. **Append-only memory.** Never delete from long-term. Overflow to archival.
5. **ASK before expanding scope.** Corridors, notebooks, research direction — ASK if not specified.

## Key Files

| File | Purpose |
|---|---|
| `OPEN_BRAIN.md` | Core principles (append-only) |
| `memory/trinity_mode_spec.md` | Trinity Mode operational spec |
| `memory/short_term.md` | Session activity |
| `memory/long_term.md` | Verified findings |
| `memory/todos.md` | Persistent tasks |
| `memory/connections.md` | Cross-refs, what works/doesn't |

## Archived Vision (concept papers — NOT operational)

The repo also contains concept papers and a Python CLI for the full vision:
- 8-layer architecture, biological naming, cognitive agents — concept papers only
- Python CLI (`python -m openbrainlm`) — standalone demo, 135 tests pass, agents are stubs
- Concept papers: `docs/concept_papers/01-04`
- Architecture specs: `ARCHITECTURE.md`, `OPERATIONAL_LAYERS.md`
- These are PUBLIC in the repo but are NOT the operational harness

**Do NOT mix vision language into operational work.** No biological naming,
no "queen pheromone", no "hippocampal", no "basal ganglia" in operational context.

## Source of Truth Hierarchy

1. `memory/trinity_mode_spec.md` (how the harness works)
2. `OPEN_BRAIN.md` (core principles)
3. Rules (`~/.claude/rules/`)
4. Memory files (accumulated findings)

## Dependencies

- Python 3.10+ (stdlib only for core)
- Claude Code (hooks, rules, skills, agent dispatch)
- NotebookLM MCP (evidence corridors)
- No additional infrastructure required for the harness

## Sandbox Governance

Work inside `sandbox/` is governed by `sandbox/SANDBOX_RULES.md`.
Key sandbox constraints: open-source only (MIT/Apache/BSD), every dep cited,
stdlib-first Python, outputs to `handoffs/` only, never to `memory/long_term.md`.
See `SANDBOX_RULES.md` Rule SB-01 through SB-06.

## Append Log

| Date | Change | Author |
|---|---|---|
| 2026-03-30 | Added sandbox governance pointer + `sandbox/SANDBOX_RULES.md` | Gemini AntiGravity |
