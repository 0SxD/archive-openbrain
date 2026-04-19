# SANDBOX_RULES.md — Sandbox Governance
> Every agent working inside `sandbox/` reads this at boot.
> Inherits all rules from `CLAUDE.md` and `OPEN_BRAIN.md`.
> Sandbox-specific overrides and extensions are defined here.

---

## What the Sandbox Is

An isolated execution zone for integration work, prototyping, and pipeline wiring.
Code here is NOT production. It does NOT affect the core `openbrainlm/` package.

Three sandbox directories currently active:

| Directory | Purpose |
|---|---|
| `sandbox/NoteBookLM_Research_IT/` | NotebookLM research loop CLI — AntiGravity integration |
| `sandbox/NT_Bin_Sandbox/` | NautilusTrader pipeline sandbox |
| `sandbox/OpenBrain_Upgrades/` | Staged architectural upgrades before promotion |

---

## Sandbox-Specific Rules

### Rule SB-01 — Source Verification Gate (No Presumptions)
**Every tool, library, or pattern used inside the sandbox must have a cited source.**
Acceptable sources, in order of authority:

1. **arXiv** — preprints from accredited institutions (MIT, Stanford, DeepMind, etc.)
2. **GitHub** — open-source repositories with a recognized OSI license (MIT, Apache-2.0, BSD)
3. **Professional documentation** — official library docs (e.g., PyPI, npmjs.com)
4. **NotebookLM corridors** — once connected, becomes the primary gate (see SB-05)

**Unacceptable sources:** blog posts, Reddit, personal sites, undocumented private forks,
any repo without a clear license. If the source is unclear — DO NOT USE IT.

### Rule SB-02 — No Custom Code Without Approval
Sandbox agents do NOT write novel algorithms or custom logic without explicit approval.
The only acceptable code is:
- **Glue code** — wiring together verified open-source components via their public API
- **Config files** — Dockerfile, docker-compose, YAML, TOML
- **CLI wrappers** — minimal stdin/stdout/subprocess calls to invoke open-source binaries

Any deviation from an open-source component's documented API requires a citation
and explicit approval before merge. No creative reimplementations.

### Rule SB-03 — Stdlib-First for Python Glue Code
Python glue scripts inside sandbox use **Python stdlib only** unless:
- The non-stdlib package is listed as a direct dependency of an approved open-source tool
- OR explicit approval is given with a cited source

Example: `subprocess`, `json`, `argparse`, `pathlib` — ✓ always allowed.
Example: `mcp` (PyPI) — ✗ not stdlib. Use subprocess + JSON-RPC stdio instead.

### Rule SB-04 — Isolation Boundary
Sandbox code **cannot import from** `openbrainlm/` (the core package).
Sandbox code **can read from** `memory/` and **write to** `handoffs/` (the blackboard).
No sandbox process should modify `memory/long_term.md` directly — write to `handoffs/`
and let the orchestrator promote it.

### Rule SB-05 — NotebookLM as the Research Gate (Pending Auth)
Once the NotebookLM connection is authenticated and operational, it becomes
the **mandatory first stop** before any new tool or pattern is introduced into the sandbox.

Until then: arXiv + GitHub open-source repos serve as the verification fallback.

**Current status:** NotebookLM MCP = `authenticated: false` (2026-03-25).
Auth must be resolved before this gate is active.
See `memory/notebooklm_brain.md` for full status log.

### Rule SB-06 — Promotion Path
Code cannot move from `sandbox/` to production without passing the 5-Gate Airlock:

| Gate | Check |
|---|---|
| 1. Syntax | `python -m py_compile` or equivalent |
| 2. Zero-Context | Can a fresh agent understand this file alone? |
| 3. Architecture | Does it respect split-brain? No core imports? |
| 4. Security | No secrets, no PII, no shell injection surface |
| 5. Source Audit | Every dep cited? License confirmed open-source? |

---

## What Is NOT Allowed in the Sandbox

- No hardcoded secrets, tokens, credentials, or API keys in any file
- No biological naming (no pheromone, no hippocampal, no basal ganglia)
- No private/closed-source libraries without owner approval
- No network egress other than to verified endpoints (GitHub, arXiv, npmjs, PyPI)
- No modifying sibling sandboxes without orchestrator coordination

---

> Source: Inherits from `OPEN_BRAIN.md`, `CLAUDE.md`, `AGENT_RULES.md`.
> Author: Gemini AntiGravity session 2026-03-30. Rule SB-05 pending NotebookLM auth resolution.
