# Memory Architecture Research — Categorical vs Chronological
**Date:** 2026-03-24
**Source:** Agents_Arcs NotebookLM (1a7bcc9d), session 2c64e831
**Queried by:** Opus directly (Sonnet subagent blocked — MCP permissions don't propagate to subagents)

---

## Q1: Categorical vs Chronological Structure

Research says: use BOTH. Not a choice.

- **Chronological (Session Event Logs)** — "Sessions" tier. Tracks trajectory: what did we do last time? Required for procedural continuity across sessions. Cannot be replaced by categorical files.
- **Categorical (Domain Memory)** — "Memory" tier. Durable, searchable, topic-organized. Holds verified findings extracted across multiple sessions. Prevents re-deriving project understanding every session start.
- **Fatal flaw**: Treating memory as a single monolithic bucket → "memory wall" — context jammed with unsorted noise.
- **Bridge**: Schema-driven compaction. Chronological logs → extract → categorical markdown files. NOT naive summarization.

Source citation: Google, Anthropic, production AI systems (grounded in Agents_Arcs 156 sources)

---

## Q2: Required Schema Fields for Long-Term Promotion

Minimum viable schema (keep "painfully small" — max 5 fields):

| Field | Purpose |
|---|---|
| Statement | The actual claim, fact, or decision |
| Confidence | 0-1 score of certainty |
| Source | Exact provenance (paper, file, URL, notebook) |
| Status | verified / pending / disputed |
| last_verified_date | Tracks memory decay |

**Critical design rules:**
- **Avoid "glossy soup"**: Naive AI summarization strips decision structures → memory rot. Must use schema-driven compaction, not free-text summarization.
- **Keep fields painfully small**: Richness creates friction → agent drift and hallucination. Max 5 fields. Add sophistication later.
- **Confidence bouncer (hard gate)**: Confidence < 0.6 → route to pending log, NOT long-term. Ask human for clarification. This prevents long-term memory becoming a "junk drawer."

---

## Key Takeaways

1. short_term.md (chronological) + categorical topic files = both required, not either/or
2. Schema-driven compaction is the bridge — structured extraction, not summarization
3. 5 fields max: Statement, Confidence, Source, Status, last_verified_date
4. Confidence bouncer < 0.6 → quarantine/pending (validates rule 07 already in place)
5. Categorical files should be topic-scoped: "verified findings", "decisions", "blockers", "corrections" — NOT one big long_term.md

## Implication for Trading Brain

Current structure has:
- short_term.md (chronological) ✓ — keep
- long_term.md (semi-categorical but one file) — split into topic files
- connections.md ✓ — keep

Proposed additions:
- `memory/indicators.md` — indicator inventory (names, library/custom status, verification status)
- `memory/decisions.md` — architecture decisions with reasoning
- `memory/blockers.md` — active blockers with status
- `memory/verified_findings.md` — schema-driven entries only (5 fields)
- short_term.md stays as chronological session log → compacts into above files
