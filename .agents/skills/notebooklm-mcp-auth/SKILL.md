---
name: notebooklm-mcp-auth
description: How to authenticate and connect to NotebookLM via the notebooklm-mcp-nodejs MCP server inside an AntiGravity (Gemini) session. Exact steps that worked 2026-03-30.
---

# NotebookLM MCP — Authentication & Connection Skill

> Governance: `sandbox/SANDBOX_RULES.md` (Rule SB-01, SB-05)
> Status: VERIFIED WORKING — authenticated 2026-03-30, session f1b694cc

---

## What This Skill Covers

Exactly how to connect AntiGravity (Gemini) to NotebookLM via the
`notebooklm-mcp-nodejs` MCP server. This is NOT a generic guide —
it is the exact sequence that worked on 2026-03-30 in this workspace.

---

## How It Works (Architecture)

The MCP server (`notebooklm-mcp-nodejs`) is a **Playwright-based web scraper**
that automates the NotebookLM browser UI. There is no official Google API.

```
Gemini AntiGravity session
  └── mcp_notebooklm_* tools (native to AntiGravity toolchain)
        └── notebooklm-mcp-nodejs (Node.js, npx, runs headless Chromium)
              └── logs into notebooklm.google.com as your Google account
                    └── queries your notebooks via browser automation
```

**Key facts:**
- Auth cookies are saved locally (`~/.config/notebooklm-mcp/` or equivalent)
- Session persists until cookies expire or Google invalidates them
- headless = true by default (no visible browser during queries)
- stealth mode enabled by default (mimics human browsing to avoid bot detection)
- Re-auth takes ~53 seconds (opens browser window for manual Google login)

---

## Is This AntiGravity-Only?

**Currently yes — native tool calls (`mcp_notebooklm_*`) are wired into the
Gemini AntiGravity MCP toolchain only.**

Claude Code can also use this MCP server IF it is added to Claude's
`~/.claude/settings.json` mcpServers config. It is NOT there by default.

The `sandbox/NoteBookLM_Research_IT/query_notebook.py` CLI wrapper is
**model-agnostic** — any agent or orchestrator can invoke it via subprocess.

---

## Step-by-Step: How Authentication Was Done

### Step 1 — Verify the MCP server is running
```
Tool: mcp_notebooklm_get_health
Expected: { "authenticated": false, "status": "ok" }
```
If you get `authenticated: false`, proceed to Step 2.
If you get a connection error, the MCP server process is not loaded — restart AntiGravity.

### Step 2 — Trigger Google auth (opens browser window)
```
Tool: mcp_notebooklm_setup_auth
Parameters: { "show_browser": true }
```
- A Chromium browser window opens on your screen
- Log in to your Google account manually (the one with your NotebookLM notebooks)
- The tool waits up to 10 minutes for you to complete login
- When complete: `{ "authenticated": true, "duration_seconds": ~53 }`

### Step 3 — Verify auth saved
```
Tool: mcp_notebooklm_get_health
Expected: { "authenticated": true, "status": "ok" }
```

### Step 4 — List registered notebooks to confirm connection
```
Tool: mcp_notebooklm_list_notebooks
Expected: list of notebooks with IDs, names, topics
```

### Step 5 — Run a live query
```
Tool: mcp_notebooklm_ask_question
Parameters: {
  "question": "What is the core architecture described here?",
  "notebook_id": "<id-from-step-4>"
}
```

---

## Re-Authentication (when cookies expire)

Cookies typically expire after Google session timeout (days to weeks).
When `mcp_notebooklm_get_health` returns `authenticated: false` again:

```
Tool: mcp_notebooklm_re_auth
Parameters: { "show_browser": true }
```

If re_auth fails repeatedly, do a clean reset:
1. Close all Chrome/Chromium instances
2. `mcp_notebooklm_cleanup_data(confirm=true, preserve_library=true)`
3. `mcp_notebooklm_setup_auth(show_browser=true)`
4. Verify with `mcp_notebooklm_get_health`

---

## Registered Notebooks (as of 2026-03-30)

23 notebooks — key ones for OpenBrain research:

| ID | Name | Size | Primary Use |
|---|---|---|---|
| `strategic-implementation-of-ze` | Agents_Arcs | 156 sources | Agent architecture gate |
| `neural-arc-brain-architecture-` | Neural_ARC | 55 books | Brain implementation |
| `python-ai-finance-ml-library` | Python AI Finance ML | Massive | Code reference |
| `quarantine-layer` | Quarantine Layer | — | Unverified research staging |
| `forget-ram-check` | Forget RAM Check | — | End-of-session deferred items |

Full registry: `memory/notebooklm_brain.md`

---

## Source Citations (Rule SB-01)

| Component | Source | License |
|---|---|---|
| `notebooklm-mcp-nodejs` | [github.com/YassKhazzan/notebooklm-mcp-nodejs](https://github.com/YassKhazzan/notebooklm-mcp-nodejs) | MIT |
| Playwright (headless browser) | [github.com/microsoft/playwright](https://github.com/microsoft/playwright) | Apache-2.0 |
| MCP protocol spec | [modelcontextprotocol.io](https://modelcontextprotocol.io/specification) | Apache-2.0 |

---

## What Is NOT Documented Here

- Adding this MCP to Claude Code config (needs owner approval per Rule 00)
- The `query_notebook.py` stdlib CLI — see `notebooklm-research/SKILL.md`
- Notebook source management (what goes in each notebook) — see `memory/notebooklm_brain.md`
