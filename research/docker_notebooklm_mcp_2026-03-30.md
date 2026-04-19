# Docker Deployment Research: NotebookLM MCP Server
**Date:** 2026-03-30
**Researcher:** Claude Sonnet (orchestrated by Opus)
**Status:** RESEARCH COMPLETE — awaiting orchestrator review before implementation

---

## Executive Summary

A production-verified Docker deployment for a Playwright-based NotebookLM MCP server exists and is actively maintained. The `roomi-fields/notebooklm-mcp` fork (MIT, v1.5.3) ships a complete Dockerfile + docker-compose.yml with noVNC for headless auth, HTTP REST API for multi-agent access, and a volume-mounted `/data` directory for cookie persistence. The `YassKhazzan/notebooklm-mcp-nodejs` repo (currently running on the host via npx) appears to be private or deleted (404 via GitHub API). The recommended path is to migrate to `roomi-fields/notebooklm-mcp` rather than containerize the YassKhazzan version.

---

## 1. Current State: How NotebookLM MCP Runs Now

### Architecture (verified from `SKILL.md`, `~/.claude/rules/10_notebooklm_orchestrator_only.md`)

```
Gemini AntiGravity session
  └── mcp_notebooklm_* tools (native to AntiGravity toolchain)
        └── notebooklm-mcp-nodejs (Node.js, npx, runs headless Chromium)
              └── logs into notebooklm.google.com via Playwright browser automation
```

- **Server:** `YassKhazzan/notebooklm-mcp-nodejs` (MIT) — runs via `npx` on the Windows host
- **Auth storage:** `~/.config/notebooklm-mcp/` or `%LOCALAPPDATA%\notebooklm-mcp\Data\` (Windows)
- **Access:** Gemini AntiGravity session only — NOT wired to Claude Code or Codex
- **Protocol:** stdio MCP only — no HTTP REST API
- **Limitation:** Single-client only; Google bot-detection risk; re-auth every few days to weeks
- **Source repo status:** `YassKhazzan/notebooklm-mcp-nodejs` returns 404 via GitHub API as of 2026-03-30 (private or deleted)

### Why "npx on host" is fragile

1. Node/npx version drift across OS updates
2. Chrome profile lock prevents running more than one MCP client simultaneously
3. No health check — silent failure is possible
4. Auth cookies stored in Windows user profile, not portable
5. Only Gemini AntiGravity can reach it (no Claude Code, no Codex)

---

## 2. Recommended Replacement: `roomi-fields/notebooklm-mcp`

### Repository

- **URL:** https://github.com/roomi-fields/notebooklm-mcp
- **License:** MIT
- **Latest version:** v1.5.3 (as of 2026-03-30)
- **Lineage:** Forked from `PleasePrompto/notebooklm-mcp` → extended with Docker, HTTP API, multi-account, noVNC
- **Actively maintained:** CI badges present, CHANGELOG active, 76 E2E tests

### Key difference from current setup

`roomi-fields/notebooklm-mcp` ships **two transport modes**:

| Mode | Protocol | Use case |
|---|---|---|
| Stdio MCP | stdin/stdout | Direct MCP client (Claude Code, Cursor, Codex) |
| HTTP REST API | HTTP on port 3000 | Any agent, any language, any tool (n8n, curl, Python) |

In Docker, only the **HTTP REST API mode** runs (`dist/http-wrapper.js`). Stdio MCP clients connect via a lightweight **stdio-HTTP proxy** (`dist/stdio-http-proxy.js`) that forwards calls to the HTTP server. This solves the Chrome profile locking problem: one Chrome instance, multiple clients.

---

## 3. Docker Approach: Exact Configuration

All content below is sourced directly from `roomi-fields/notebooklm-mcp` (verified via GitHub API, 2026-03-30).

### 3.1 Dockerfile (production-verified, v1.5.3)

Source: `github.com/roomi-fields/notebooklm-mcp/blob/main/Dockerfile`

```dockerfile
FROM node:20-bookworm-slim

# Chromium system dependencies + virtual display stack + noVNC
RUN apt-get update && apt-get install -y \
    libnss3 libnspr4 libatk1.0-0 libatk-bridge2.0-0 libcups2 libdrm2 \
    libdbus-1-3 libxkbcommon0 libatspi2.0-0 libxcomposite1 libxdamage1 \
    libxfixes3 libxrandr2 libgbm1 libasound2 libpango-1.0-0 libcairo2 \
    xvfb x11vnc novnc websockify fluxbox \
    fonts-liberation fonts-noto-color-emoji wget ca-certificates procps \
    && rm -rf /var/lib/apt/lists/*

# Non-root user for security
RUN groupadd -r notebooklm && useradd -r -g notebooklm -d /home/notebooklm notebooklm \
    && mkdir -p /home/notebooklm /app /data \
    && chown -R notebooklm:notebooklm /home/notebooklm /app /data \
    && mkdir -p /tmp/.X11-unix \
    && chmod 1777 /tmp/.X11-unix

WORKDIR /app
COPY --chown=notebooklm:notebooklm package*.json ./
USER notebooklm

# Install ALL deps (including devDependencies for TypeScript build)
RUN npm ci --ignore-scripts

COPY --chown=notebooklm:notebooklm src/ ./src/
COPY --chown=notebooklm:notebooklm tsconfig*.json ./
RUN npm run build

COPY --chown=notebooklm:notebooklm scripts/ ./scripts/
RUN npm prune --omit=dev

# patchright (stealth Playwright fork) installs Chromium
RUN npx patchright install chromium

USER root
RUN chmod +x /app/scripts/*.sh
USER notebooklm

ENV NODE_ENV=production \
    HTTP_PORT=3000 \
    HTTP_HOST=0.0.0.0 \
    HEADLESS=true \
    NOTEBOOKLM_DATA_DIR=/data \
    PLAYWRIGHT_BROWSERS_PATH=/home/notebooklm/.cache/ms-playwright \
    DISPLAY=:99 \
    NOVNC_PORT=6080

EXPOSE 3000 6080

HEALTHCHECK --interval=30s --timeout=10s --start-period=10s --retries=3 \
    CMD wget --no-verbose --tries=1 --spider http://localhost:3000/health || exit 1

VOLUME ["/data"]

CMD ["/app/scripts/docker-entrypoint.sh"]
```

**Key design decisions in this Dockerfile:**

- **`node:20-bookworm-slim`** — Debian Bookworm base. Playwright requires glibc (Alpine/musl is incompatible). Source: [playwright.dev/docs/docker](https://playwright.dev/docs/docker)
- **`patchright` not standard `playwright`** — patchright is a stealth fork of Playwright that mimics human browsing patterns to reduce Google bot-detection. Source: [github.com/dylangroos/patchright-mcp-lite](https://github.com/dylangroos/patchright-mcp-lite)
- **Xvfb + x11vnc + noVNC** — Creates a virtual X11 display (`:99`) accessible via browser at port 6080. Required for initial Google auth on headless servers.
- **Non-root user** — `notebooklm` user. Standard security practice for containerized browsers.
- **`VOLUME ["/data"]`** — Declares `/data` as the persistence point for cookies, Chrome profile, and notebook library.

### 3.2 docker-compose.yml (production-verified)

Source: `github.com/roomi-fields/notebooklm-mcp/blob/main/docker-compose.yml`

```yaml
version: '3.8'

services:
  notebooklm-mcp:
    build:
      context: .
      dockerfile: Dockerfile
    image: notebooklm-mcp:latest
    container_name: notebooklm-mcp

    ports:
      - '${HTTP_PORT:-3000}:3000'   # HTTP REST API
      - '6080:6080'                  # noVNC (auth only — restrict in production)

    volumes:
      # Bind-mount a local data directory so cookies survive container restarts
      - ./deploy-package/data:/data

    environment:
      - NODE_ENV=production
      - HTTP_PORT=3000
      - HTTP_HOST=0.0.0.0
      - HEADLESS=true
      - STEALTH_ENABLED=true
      - DATA_DIR=/data
      - NOTEBOOKLM_UI_LOCALE=en   # Change to 'fr' if Google account is French

    deploy:
      resources:
        limits:
          memory: 2G           # Chromium is memory-hungry
        reservations:
          memory: 512M

    restart: unless-stopped

    healthcheck:
      test: ['CMD', 'wget', '--no-verbose', '--tries=1', '--spider', 'http://localhost:3000/health']
      interval: 30s
      timeout: 10s
      retries: 3
      start_period: 30s

    logging:
      driver: 'json-file'
      options:
        max-size: '10m'
        max-file: '3'

volumes:
  notebooklm-data:
    name: notebooklm-mcp-data
```

**Notes for this workspace:**
- Change `NOTEBOOKLM_UI_LOCALE` to `en` (the current setup uses English selectors per SKILL.md)
- The `./deploy-package/data` bind-mount should point to wherever auth data lives on the host
- Memory limit of 2G is the minimum for stable Chromium; 4G recommended for heavy use

### 3.3 Entrypoint (docker-entrypoint.sh)

Source: `github.com/roomi-fields/notebooklm-mcp/blob/main/scripts/docker-entrypoint.sh`

```bash
#!/bin/bash
set -e
ENABLE_VNC="${ENABLE_VNC:-true}"
if [ "$ENABLE_VNC" = "true" ]; then
    source /app/scripts/start-vnc.sh   # Starts Xvfb + x11vnc + noVNC on :6080
fi
export HTTP_PORT=${PORT:-${HTTP_PORT:-3000}}
exec node dist/http-wrapper.js          # HTTP REST API server (foreground)
```

The entrypoint starts VNC services then launches the HTTP server. `ENABLE_VNC=false` disables the VNC stack entirely once auth is established (reduces attack surface).

### 3.4 Critical Chromium Docker flags

Source: `DOCKER-FIXES.md` in the repo (verified fix log, timestamped 2025-01-05)

These flags MUST be passed to Chromium when running in Docker, or it will timeout:
```
--no-sandbox
--disable-setuid-sandbox
--disable-gpu
--disable-infobars
--log-level=3
```

The repo's auth code passes these automatically. If building a custom variant, they must be explicit in the `launchPersistentContext()` call.

---

## 4. Cookie Persistence Strategy

### What gets persisted (inside `/data`)

Source: `deployment/docs/08-DOCKER.md`

```
/data/
├── library.json              # Notebook registry (IDs, names, topics)
├── chrome_profile/           # Chrome profile (Google session cookies live here)
├── browser_state/            # Playwright browser state backup
├── accounts.json             # Account configuration
├── accounts/
│   └── account-xxx/
│       ├── credentials.enc.json   # Encrypted credentials
│       ├── quota.json
│       └── state.json
└── encryption.key            # Key for credentials.enc.json
```

### Volume strategy: bind-mount vs named volume

Two options in docker-compose.yml:

**Option A: Bind-mount (recommended for this workspace)**
```yaml
volumes:
  - /path/on/host/notebooklm-data:/data
```
- Data lives at a known host path — easy to back up, inspect, and migrate
- Survives `docker-compose down && docker-compose up`
- Survives image rebuilds

**Option B: Named Docker volume**
```yaml
volumes:
  - notebooklm-data:/data
```
- Docker manages the location
- Harder to inspect or migrate without Docker commands

For this workspace, bind-mount to a path like `<WORKSPACE>\OpenBrainLM\notebooklm-docker-data\` is recommended — keeps it under the project tree and gitignore-able.

### Migrating existing auth from host to container

Source: `deployment/docs/08-DOCKER.md`

If auth cookies already exist on the host (from the current npx-based setup):
```bash
# Windows host path → container /data
docker cp %LOCALAPPDATA%\notebooklm-mcp\Data\. notebooklm-mcp:/data/
docker restart notebooklm-mcp
```

Then verify with:
```bash
curl http://localhost:3000/health
# Expected: {"success":true,"data":{"authenticated":true,...}}
```

### Re-authentication workflow (headless server)

1. Open `http://localhost:6080/vnc.html` in browser
2. POST to setup-auth: `curl -X POST http://localhost:3000/setup-auth -d '{"show_browser":true}'`
3. Chromium appears in the noVNC window — log in to Google manually
4. Auth saved to `/data/chrome_profile/` automatically
5. After successful auth, `ENABLE_VNC=false` can be set to disable the VNC surface

---

## 5. Multi-Agent Access Pattern

### The core insight

Running in Docker exposes an **HTTP REST API** on port 3000. Any agent — Claude Code, Gemini, Codex, n8n, Python scripts — can call it via HTTP. This breaks the "orchestrator-only" constraint that currently exists because the npx/stdio server can only be accessed by one MCP client at a time.

### Architecture with Docker

```
┌─────────────────────────────────────────────────────────┐
│                Docker Container                          │
│  HTTP REST API (port 3000)                              │
│  ↓                                                      │
│  Node.js http-wrapper.js                                │
│  ↓                                                      │
│  Playwright/patchright → Chromium → notebooklm.google   │
│                                                         │
│  noVNC (port 6080) — auth only, disable after setup     │
└─────────────────────────────────────────────────────────┘
        ↑                    ↑                    ↑
  Claude Code           Gemini                 Codex
  (stdio proxy          (HTTP POST             (HTTP POST
   or HTTP)              to :3000)              to :3000)
```

### Client connection methods

**Method 1: HTTP REST API (model-agnostic, any agent)**

Direct HTTP call from any agent:
```bash
# Ask a question
curl -X POST http://localhost:3000/ask \
  -H "Content-Type: application/json" \
  -d '{"question": "What is the agent architecture pattern?", "notebook_id": "strategic-implementation-of-ze"}'

# Health check
curl http://localhost:3000/health
```

This works from Python (`requests.post`), from shell scripts, from n8n, from any HTTP client. No MCP protocol required.

**Method 2: stdio-HTTP proxy (Claude Code, Cursor, Codex as MCP clients)**

Source: `deployment/docs/09-MULTI-INTERFACE.md`

Each MCP client runs a lightweight proxy (`dist/stdio-http-proxy.js`) that translates MCP stdio ↔ HTTP calls to the container. The proxy has no Chrome dependency — it's just an HTTP forwarder.

Claude Code config (`~/.claude/settings.json`):
```json
{
  "mcpServers": {
    "notebooklm": {
      "command": "node",
      "args": ["/path/to/notebooklm-mcp/dist/stdio-http-proxy.js"],
      "env": {
        "MCP_HTTP_URL": "http://localhost:3000"
      }
    }
  }
}
```

Gemini AntiGravity can continue using the existing `mcp_notebooklm_*` tool calls — they would need to be pointed at the HTTP endpoint instead of npx. This is a config change, not a code change.

**Method 3: Python subprocess (existing `query_notebook.py`)**

The existing `sandbox/NoteBookLM_Research_IT/query_notebook.py` can be adapted to POST to `http://localhost:3000/ask` instead of invoking the npx server directly. Zero dependency on MCP protocol.

### Concurrency note

The HTTP server supports up to `MAX_SESSIONS=10` concurrent sessions (configurable). Chrome profile locking is solved because there is only one Chrome instance (in the container), and the HTTP server serializes requests through it. Multiple agents hitting the endpoint simultaneously are queued, not conflicted.

---

## 6. Health Check Endpoint

Source: Dockerfile HEALTHCHECK directive + `deployment/docs/08-DOCKER.md`

The container exposes `GET /health` on port 3000:

```json
{
  "success": true,
  "data": {
    "authenticated": true,
    "status": "ok",
    "version": "1.5.3",
    "uptime": 3600
  }
}
```

Docker runs this check every 30s. If it fails 3 times, the container is marked `unhealthy`. This can trigger auto-restart with appropriate orchestration (Docker Swarm, Kubernetes, or a simple `restart: unless-stopped` in compose).

A Claude Code hook or cron job can poll this endpoint to detect auth expiry before attempting queries.

---

## 7. Risks and Limitations

### Risk 1: Google bot detection (HIGH)

- **Issue:** Playwright automation is actively detected and blocked by Google. Re-auth required when detected.
- **Mitigation:** `patchright` stealth mode (used in roomi-fields) mimics human behavior. The repo notes "realistic typing speeds, natural delays, mouse movements." Not guaranteed.
- **Citation:** `roomi-fields/notebooklm-mcp` README disclaimer: "I can't guarantee Google won't detect or flag automated usage. Use a dedicated Google account for automation."
- **Recommendation:** Use a dedicated Google account for the automation account, separate from personal.

### Risk 2: Cookie expiry (MEDIUM)

- **Issue:** Google sessions expire. When they do, the container returns `authenticated: false` and all queries fail silently.
- **Mitigation:** Health check polling + automated alert. Re-auth requires human interaction (noVNC).
- **Frequency:** Days to weeks depending on Google session policy. Can't be fully automated without storing Google password (security risk).

### Risk 3: NoVNC port exposure (MEDIUM)

- **Issue:** Port 6080 (noVNC) gives anyone with access a full browser window on your Google account.
- **Mitigation:** Never expose 6080 publicly. Restrict to localhost (`127.0.0.1:6080:6080`) after initial auth. Use `ENABLE_VNC=false` env var once auth is established.
- **Citation:** `deployment/docs/08-DOCKER.md`: "Don't expose port 6080 publicly — noVNC gives browser access."

### Risk 4: Chromium memory usage (LOW-MEDIUM)

- **Issue:** Chromium consumes significant RAM. Under load, 2G may not be enough.
- **Mitigation:** Set memory limit to 4G for production. Monitor container stats.
- **Data:** `deployment/docs/08-DOCKER.md` resource table: Minimum 512MB, Recommended 2GB. For heavy multi-agent use, 4G.
- **Docker flag:** `/dev/shm` limited to 64MB by default in Docker; Chromium crashes if it runs out. The `--disable-dev-shm-usage` flag (already included via `--no-sandbox`) routes around this.
- **Citation:** Playwright Docker docs ([playwright.dev/docs/docker](https://playwright.dev/docs/docker)): "Use `--disable-dev-shm-usage` to avoid memory crashes."

### Risk 5: Single Chrome instance bottleneck (LOW)

- **Issue:** All queries funnel through one Chrome/Chromium instance. High concurrency could queue up.
- **Mitigation:** `MAX_SESSIONS=10` default. Queries to NotebookLM are inherently rate-limited by Google anyway (15-30s per query). Single Chrome is not the bottleneck.

### Risk 6: No official Google API (STRUCTURAL)

- **Issue:** This entire approach depends on browser automation against a private web UI. Google can change the DOM at any time and break the scraper.
- **Mitigation:** Pin to a known-working image version. Monitor the repo's issue tracker for breakage reports.
- **Citation:** `~/.claude/rules/10_notebooklm_orchestrator_only.md`: "All community MCP servers for NotebookLM are Playwright web scrapers — no public API exists."

### Risk 7: Windows host + Docker Desktop (OPERATIONAL)

- **Issue:** On Windows, Docker Desktop uses WSL2 as the backend. The container runs Linux fine, but port mapping to `localhost` requires Docker Desktop's host networking features.
- **Mitigation:** Standard `ports: - "3000:3000"` in docker-compose.yml works correctly with Docker Desktop. Confirmed in `deployment/docs/09-MULTI-INTERFACE.md` which explicitly calls out WSL/Windows port access patterns.

---

## 8. Migration Decision: YassKhazzan vs roomi-fields

| Factor | YassKhazzan/notebooklm-mcp-nodejs | roomi-fields/notebooklm-mcp |
|---|---|---|
| GitHub status | 404 (private/deleted) as of 2026-03-30 | Public, active |
| Docker support | None found | Full (Dockerfile + compose + docs) |
| HTTP REST API | No (stdio only) | Yes (port 3000) |
| Multi-agent access | No | Yes (proxy pattern) |
| noVNC auth | No | Yes |
| Stealth mode | Unknown | Yes (patchright) |
| Health endpoint | No | Yes (`/health`) |
| Multi-account | No | Yes (v1.4.0+) |
| License | MIT | MIT |
| Test coverage | Unknown | 76 E2E tests |

**Verdict:** Migrate to `roomi-fields/notebooklm-mcp`. The YassKhazzan repo is inaccessible and lacks every feature needed for Docker + multi-agent operation.

---

## 9. Recommended Implementation Sequence

This is research only. Implementation requires orchestrator review and explicit approval.

1. **Clone** `roomi-fields/notebooklm-mcp` to `<WORKSPACE>\OpenBrainLM\tools\notebooklm-mcp\`
2. **Create data directory** at `<WORKSPACE>\OpenBrainLM\notebooklm-docker-data\` (gitignored)
3. **Adjust docker-compose.yml**: change locale to `en`, bind-mount to the data directory above
4. **Build image**: `docker-compose build`
5. **First-run auth**: start container, open `localhost:6080/vnc.html`, trigger setup-auth, log in
6. **Verify**: `curl http://localhost:3000/health` → `authenticated: true`
7. **Disable VNC**: add `ENABLE_VNC=false` env var (or restrict port 6080 to localhost only)
8. **Wire Claude Code**: add stdio-HTTP proxy to `~/.claude/settings.json` mcpServers
9. **Wire Gemini**: update AntiGravity config to point `mcp_notebooklm_*` at `http://localhost:3000`
10. **Test**: run `ask_question` from both Claude and Gemini, confirm same notebook answers

---

## 10. Citations

| Claim | Source | Verified |
|---|---|---|
| roomi-fields Dockerfile contents | `github.com/roomi-fields/notebooklm-mcp/blob/main/Dockerfile` (GitHub API, 2026-03-30) | Yes |
| docker-compose.yml contents | `github.com/roomi-fields/notebooklm-mcp/blob/main/docker-compose.yml` (GitHub API, 2026-03-30) | Yes |
| DOCKER-FIXES.md (Chromium flags) | `github.com/roomi-fields/notebooklm-mcp/blob/main/DOCKER-FIXES.md` (GitHub API, 2026-03-30) | Yes |
| Docker deployment guide | `github.com/roomi-fields/notebooklm-mcp/blob/main/deployment/docs/08-DOCKER.md` (GitHub API, 2026-03-30) | Yes |
| Multi-interface proxy pattern | `github.com/roomi-fields/notebooklm-mcp/blob/main/deployment/docs/09-MULTI-INTERFACE.md` (GitHub API, 2026-03-30) | Yes |
| Chrome profile locking limitation | `github.com/roomi-fields/notebooklm-mcp/blob/main/docs/CHROME_PROFILE_LIMITATION.md` (GitHub API, 2026-03-30) | Yes |
| Playwright Docker best practices | [playwright.dev/docs/docker](https://playwright.dev/docs/docker) (web search, 2026-03-30) | Yes |
| Playwright Docker base image (bookworm) | Web search result: "avoid Alpine; use Debian/Ubuntu" (2026-03-30) | Yes |
| /dev/shm 64MB limit + `--disable-dev-shm-usage` | Web search: Thomas Bourimech, playwright.dev/docs/docker (2026-03-30) | Yes |
| patchright stealth mode | [github.com/dylangroos/patchright-mcp-lite](https://github.com/dylangroos/patchright-mcp-lite) (web search, 2026-03-30) | Yes |
| No official Google NotebookLM API | `~/.claude/rules/10_notebooklm_orchestrator_only.md` (workspace rule) | Yes |
| Current auth cookie path | `SKILL.md` in `.agents/skills/notebooklm-mcp-auth/` (local read, 2026-03-30) | Yes |
| YassKhazzan repo 404 | GitHub API `repos/YassKhazzan/notebooklm-mcp-nodejs` → 404 (2026-03-30) | Yes |
