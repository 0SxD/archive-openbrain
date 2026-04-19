---
name: notebooklm-research
description: Native AntiGravity integration for querying NotebookLM notebooks programmatically from the OpenBrain sandbox. Enables the Orchestrator to trigger headless research loops without human intervention.
---

# NotebookLM Research — Skill

> Governance: `sandbox/SANDBOX_RULES.md` (Rule SB-01, SB-02, SB-03, SB-05)
> Inherits: `CLAUDE.md` → `OPEN_BRAIN.md` → `AGENT_RULES.md`
> Status: ACTIVE — auth pending (see `memory/notebooklm_brain.md`)

---

## What This Skill Does

Provides a verified, open-source CLI pipeline for querying a NotebookLM notebook
programmatically from within the OpenBrain sandbox. The Orchestrator invokes this
as a subprocess command. Results are written to `handoffs/` for memory consolidation.

---

## Source Citations (Rule SB-01 — No Presumptions)

Every component used here must be traced to an open-source or professional source:

| Component | Source | License |
|---|---|---|
| `notebooklm-mcp-nodejs` | [github.com/YassKhazzan/notebooklm-mcp-nodejs](https://github.com/YassKhazzan/notebooklm-mcp-nodejs) | MIT |
| MCP JSON-RPC stdio protocol | [modelcontextprotocol.io/specification](https://modelcontextprotocol.io/specification) | Apache-2.0 |
| `npx` / Node.js | [nodejs.org](https://nodejs.org) | MIT |
| Python stdlib (`subprocess`, `json`, `argparse`, `pathlib`) | [docs.python.org](https://docs.python.org/3/library/) | PSF |

No custom algorithms. No private code. No unapproved pip packages.

---

## Prerequisites

1. **Node.js + npx installed** and available in `PATH`
2. **NotebookLM auth** completed via `mcp_notebooklm_setup_auth`
   - Current status: `authenticated: false` — see `memory/notebooklm_brain.md`
   - Until resolved, this skill cannot execute live queries
3. **Target notebook** must have ≥ 50 sources loaded (per user directive)

---

## CLI Interface

```bash
# Basic query (active notebook)
python sandbox/NoteBookLM_Research_IT/query_notebook.py \
  --query "What is the architecture described across these sources?"

# Targeted query with output to handoffs/ for Orchestrator consumption
python sandbox/NoteBookLM_Research_IT/query_notebook.py \
  --notebook_id <google-notebooklm-id> \
  --query "Provide exact implementation logic for ..." \
  --output handoffs/notebook_research_output.md
```

**Script:** `sandbox/NoteBookLM_Research_IT/query_notebook.py`
**Deps:** Python stdlib only (Rule SB-03). Zero pip installs.
**Protocol:** MCP JSON-RPC 2.0 over stdio — spawns `npx -y notebooklm-mcp-nodejs`

---

## Research Loop Pattern (Split-Brain Law)

```
Orchestrator dispatches CLI →
  query_notebook.py runs →
    MCP stdio → notebooklm-mcp-nodejs → NotebookLM →
  response written to handoffs/notebook_research_output.md →
Orchestrator reads handoffs/ →
  promotes verified findings → memory/long_term.md
```

**Rule:** Sandbox NEVER writes directly to `memory/long_term.md`.
Outputs go to `handoffs/` only. Orchestrator promotes after review.

---

## Source Hierarchy for Research (Rule SB-01)

When NotebookLM returns findings, the Orchestrator validates against:

1. arXiv papers (institutional, peer-reviewed)
2. Open-source GitHub repos (MIT / Apache-2.0 / BSD)
3. Official library documentation (PyPI, npmjs, readthedocs)

Findings not traceable to one of these tiers → **quarantine** (do not promote to long-term).

---

## When to Use This Skill

- Before introducing any new pattern, tool, or library into the sandbox
- When the Orchestrator needs deep research on an architectural decision
- As the **Research Gate** (Rule SB-05) — once auth is active, this is the mandatory first stop

---

## What Is NOT Done Here

- No live queries until `authenticated: true` in `memory/notebooklm_brain.md`
- No promotion to `memory/long_term.md` — handoffs/ only
- No custom algorithmic logic — glue code only (Rule SB-02)
- No querying across all notebooks — always specify which notebook (per `trinity_mode_spec.md`)
