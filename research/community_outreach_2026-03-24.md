# Community Outreach Research — OpenClaw & OB1
**Date:** 2026-03-24
**Status:** Verified (live GitHub API + web search, same-day)

---

## 1. OpenClaw

### What is it?

OpenClaw (`github.com/openclaw/openclaw`) is a personal, open-source AI assistant you self-host and run on your own devices. It routes your AI through messaging channels you already use — WhatsApp, Telegram, Slack, Discord, Signal, iMessage, IRC, Teams, Matrix, and 15+ others. It is NOT a Discord/forum community in the sense of being a place to discuss AI research — it IS a community built around building and extending the OpenClaw agent runtime itself.

- **GitHub org:** https://github.com/openclaw (23 repositories)
- **Main repo:** https://github.com/openclaw/openclaw — MIT licensed, 250K+ stars as of March 2026 (most starred software project on GitHub by that point)
- **Website:** https://openclaw.ai
- **Docs:** https://docs.openclaw.ai
- **License:** MIT
- **Stack:** TypeScript, Node 24+

Key sub-projects:
- **ClawHub** — community skills registry with 5,700+ submitted skills: `github.com/openclaw` org repos
- **Lobster** — OpenClaw-native workflow shell / macro engine
- **openclaw/community** — policies and documentation for the Discord server

### How to join / post

**Discord server:**
- Invite link: `https://discord.gg/clawd`
- Server ID (from badge): `1456350064065904867`
- This is the PRIMARY community channel — real-time help, show-and-tell, contributor discussion
- Admin: Shadow (`@4shadowed` on X and Discord)
- Staff email (for staff applications): `shadow@openclaw.ai`
- Moderation appeals: `https://appeal.gg/clawd`

**GitHub (for project contributions):**
- Fork and PR against `openclaw/openclaw`
- Issues tracker is open: `github.com/openclaw/openclaw/issues`
- Skills submissions go to ClawHub registry
- Community policies repo: `github.com/openclaw/community` (open issues for policy feedback)

**Reddit:**
- Reddit moderators exist (listed in community org chart) but subreddit URL not directly found in sources

### Sharing open-source projects there

OpenClaw is focused on extending its OWN runtime (skills, channel integrations, workflows). To share an external open-source project like OpenBrainLM:
- **Discord `#show-and-tell` or equivalent channel** — the community README credits "every clawtributor who's shipped code, filed issues, joined our Discord, or just tried the project" — general show-and-tell is culturally expected
- **GitHub issues** — can reference related projects if there's an integration angle (e.g., OpenBrainLM as a memory backend for OpenClaw skills)
- **ClawHub** — if you build an OpenClaw skill that wraps OpenBrainLM MCP calls, you can submit it to the registry
- **Caveat:** OpenClaw is about its own ecosystem. A cold "here's my project" post without an OpenClaw integration angle may get ignored. Best angle: MCP skill or integration.

**Sources:**
- https://github.com/openclaw/openclaw (README, verified 2026-03-24)
- https://github.com/openclaw/community (README, verified 2026-03-24)
- https://similarlabs.com/blog/openclaw-ai-agent-trend-2026
- https://github.com/orgs/openclaw/repositories

---

## 2. OB1 (Open Brain by Nate B. Jones)

### What is it?

OB1 (`github.com/NateBJones-Projects/OB1`) is "the infrastructure layer for your thinking" — one Supabase database (PostgreSQL + pgvector), one AI gateway, one chat channel. Any AI plugs in. No middleware, no SaaS.

- **GitHub:** https://github.com/NateBJones-Projects/OB1
- **Stars:** 728 (created 2026-03-11 — less than 2 weeks old as of this research)
- **Forks:** 120
- **Language:** TypeScript
- **License:** FSL-1.1-MIT
- **Discussions:** DISABLED on the repo
- **Topics:** `ai-agents`, `mcp`, `memory-layer`, `supabase`, `personal-knowledge-management`
- **Creator:** Nate B. Jones — `natesnewsletter.substack.com`
- **Maintainer/admin:** Matt Hallett (`@matthallett1`) — first community admin and repo manager
- **PR review:** Automated agent (11-rule check) + human admin review

### How to join / post

**Discord (primary community):**
- Invite: `https://discord.gg/Cgh9WJEkeG`
- Purpose: real-time help, show-and-tell, contributor discussion
- Non-developer contributions channel: `#non-dev-contributions`

**Substack:**
- https://natesnewsletter.substack.com/ — updates, deep dives, story behind Open Brain — follow for updates and to engage with Nate directly

**GitHub Issues:**
- Discussions are disabled; use Issues for feature requests, bugs, non-technical ideas
- Non-technical contribution issue template: `github.com/NateBJones-Projects/OB1/issues/new?template=non-technical-contribution.yml`
- Extension proposal template: `github.com/NateBJones-Projects/OB1/issues/new?template=extension-submission.yml`

### Contribution / submission guidelines

Full spec: `github.com/NateBJones-Projects/OB1/blob/main/CONTRIBUTING.md`

**Four contribution categories (open vs curated):**

| Category | Path | Open? |
|---|---|---|
| Extensions | `extensions/` | CURATED — discuss with maintainers first via issue |
| Primitives | `primitives/` | CURATED — must be referenced by 2+ extensions |
| Recipes | `recipes/` | OPEN — standalone capability builds |
| Schemas | `schemas/` | OPEN |
| Dashboards | `dashboards/` | OPEN |
| Integrations | `integrations/` | OPEN — MCP extensions, new capture sources |

**Required files for any contribution:**
- `README.md` — what it does, prerequisites, step-by-step, expected outcome, troubleshooting
- `metadata.json` — name, description, category, author, version, requires fields
- Actual code — SQL, edge functions, frontend, config
- NO credentials or API keys (automated review will reject)

**README must-have sections:**
1. What it does (1-2 sentences)
2. Prerequisites
3. Step-by-step instructions (numbered, copy-paste ready)
4. Expected outcome (specific)
5. Troubleshooting (2-3 common issues minimum)

**Visual formatting requirements:**
- shields.io step badges for extensions
- Verification checkpoints (`Done when:` lines)
- Collapsible SQL blocks (`<details>`)
- GitHub alert callouts (`[!CAUTION]`, `[!WARNING]`, `[!TIP]`, `[!NOTE]`)

**Non-developer path:**
- Open a Non-Technical Contribution issue — a community mentor will shape it into code
- Full credit given in `metadata.json` and `CONTRIBUTORS.md`
- Or post in `#non-dev-contributions` Discord channel

**Automated review agent:** Checks 11 rules (file structure, no secrets, SQL safety, primitive dependencies, etc.). Must pass before human admin review.

### How to share OpenBrainLM here

Best angles for OB1 community:
1. **Integration** — OpenBrainLM as an alternative or complementary memory layer. OB1 uses Supabase/pgvector; OpenBrainLM's 8-layer biomimetic architecture is conceptually adjacent. A recipe showing how to sync OB1 thoughts to OpenBrainLM or vice versa would be a strong submission.
2. **MCP integration** — OB1 exposes MCP tools. If OpenBrainLM has MCP-compatible interfaces, an `integrations/` PR is the path.
3. **Discord show-and-tell** — `discord.gg/Cgh9WJEkeG` — post in the community and get feedback. The repo is 13 days old; the community is actively building.
4. **GitHub issue** — Propose a cross-system recipe (non-curated, so open for community contributions).

**Sources:**
- https://github.com/NateBJones-Projects/OB1 (README + CONTRIBUTING.md, verified via GitHub API 2026-03-24)
- GitHub API: repo metadata, issues list (verified 2026-03-24)

---

## Summary Table

| | OpenClaw | OB1 |
|---|---|---|
| Type | Personal AI assistant runtime | Persistent memory infrastructure |
| GitHub | github.com/openclaw/openclaw | github.com/NateBJones-Projects/OB1 |
| Stars | 250K+ | 728 |
| Age | ~Jan 2026 | Created 2026-03-11 |
| License | MIT | FSL-1.1-MIT |
| Discord | discord.gg/clawd | discord.gg/Cgh9WJEkeG |
| Discussions | Discord + GitHub issues | Discord + GitHub issues (Discussions disabled) |
| Best angle for OpenBrainLM | MCP skill or integration PR | Recipe or integration PR |
| Non-dev path | Show-and-tell in Discord | `#non-dev-contributions` + issue template |

---

## Confidence Assessment

| Claim | Confidence | Source | Status |
|---|---|---|---|
| OpenClaw Discord invite: discord.gg/clawd | 0.97 | openclaw/openclaw README badge, verified 2026-03-24 | verified |
| OpenClaw 250K+ stars | 0.85 | Web search (SimilarLabs blog, not primary) | needs_review |
| OB1 Discord: discord.gg/Cgh9WJEkeG | 0.99 | OB1 README, GitHub API, verified 2026-03-24 | verified |
| OB1 stars: 728 | 0.99 | GitHub API direct call, 2026-03-24 | verified |
| OB1 discussions disabled | 0.99 | GitHub API 410 response, 2026-03-24 | verified |
| CONTRIBUTING.md contribution categories | 0.99 | File read directly from GitHub raw, 2026-03-24 | verified |
| OpenClaw ClawHub 5,700+ skills | 0.75 | Web search summary (boilerplatehub.com), not primary | needs_review |
| OpenClaw moved to open-source foundation (Feb 2026) | 0.70 | Web search summary only | needs_review |
