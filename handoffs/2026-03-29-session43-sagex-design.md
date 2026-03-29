# Handoff — Session 43: SageX Plugin Design + System Reset
> Date: 2026-03-29
> From: Claude Code (Sonnet 4.6, session 43)
> For: Any model (Claude/Gemini/Codex) picking up this work
> Project: OpenBrainLM → SageX plugin build

---

## CURRENT SYSTEM STATUS

### What Works ✓
- **Audit gate** (`audit_gate_check.sh`): blocks `git commit` without valid receipt — TESTED 3/3
- **Research gate** (`validate_research.py` v2): blocks `.py` writes without fresh approved-domain citations — WORKING
  - Cross-cwd fix: resolves project root from target file (not shell cwd)
  - Citation quality: URL must be from `approved_sources.json` domains AND resolve
  - Citation log: `.claude/research_citations.log` (TSV, append-only)
- **ZCR** (zero-context reviewer): WORKING — spawns Sonnet cold, read-only
- **Semgrep**: WORKING — 0 findings on all hook files
- **Opus write guard** (`opus_write_guard.sh`): enforces Opus→Sonnet delegation
- **Audit read blocker**: prevents Opus reading unaudited code
- **Session save/restore**: `precompact_save.sh` → `session_savepoint_inject.sh`
- **Brainstem inject**: re-broadcasts core principles on every matched tool call
- **Destructive command guard**: blocks rm -rf, force push, file-write bypasses
- **5 project skills**: audit-loop, brain-harness, coding-harness, notebooklm-research, worktree-isolation

### What Doesn't Work ✗
- **NotebookLM MCP**: auth failing — Playwright browser scraper, not an official API. Requires manual browser login (`npx notebooklm-mcp cleanup --preserve-library` then re-auth)
- **CodeRabbit**: CLI never installed, was a fake Sonnet fallback — UNINSTALLED
- **GitHub MCP**: needs `GITHUB_PERSONAL_ACCESS_TOKEN` env var
- **Greptile MCP**: needs API key

### What's Pending
- **3rd auditor slot**: CodeRabbit replacement TBD — will be adapted from one of the installed plugins
- **Notebook access**: ALL 24 notebooks zeroed out — Sage re-assigns as needed
- **Approved sources**: arXiv + github.com only until Sage adds more via `/sagex:approve-source`

---

## SESSION 43 MAJOR DECISIONS

### 1. Architecture: SageX + OpenBrain — Coupled, Separate Versioning
- **SageX** = enforcement layer: hooks, rules, skills, agents, gates, commands
  - Installed as Claude Code plugin: `~/.claude/plugins/sagex/`
  - Carries its own `config/approved_sources.json` and `config/notebook_assignments.json`
  - The mechanical brain — nothing runs without it
- **OpenBrain** = memory layer: `short_term.md`, `long_term.md`, session state, project brains
  - Lives at `C:/apps_ai/OpenBrainLM/` (or whatever machine/path)
  - The persistent brain — context across sessions
- **Interface**: SageX reads OpenBrain config files. OpenBrain uses SageX skills.
- **Neither works without the other by design.**

### 2. Two-Session Architecture
```
Session 1 (OB terminal, port/cwd: OpenBrainLM)
  - General work, new projects, plugin development
  - Own context window, own short_term.md

Session 2 (NT terminal, port/cwd: nautilus_trader)
  - Trading bot, NT-specific work
  - Own context window, own short_term.md

Shared (central):
  - ~/.claude/plugins/sagex/config/approved_sources.json
  - ~/.claude/plugins/sagex/config/notebook_assignments.json
  - ~/.claude/hooks/ (all enforcement hooks)
  - OpenBrainLM/memory/ (long_term.md, connections.md — archival)
```
Sessions are INDEPENDENT. Same enforcement. Separate memory. No cross-contamination.

### 3. Notebook Access — Zero Trust
- ALL 24 registered notebooks: NO ACCESS until Sage assigns
- Assignment via `/sagex:approve-source notebook "Name" for project`
- Orchestrator (Opus/main session) queries NotebookLM only — no sub-agents
- Gemini handles NotebookLM queries as fallback (native Google auth, faster)

### 4. Edit Mode
- `/sagex:edit-mode` — unlocks config files, rules, skills for modification
- `/sagex:lock` — re-engages, validates JSON integrity, logs changes
- Hooks still fire during edit mode — only the files hooks READ become editable
- Fail-safe: if session ends without lock, next session starts locked

### 5. GitHub as Airlock + Handoff Layer
- **Not a cloud drive**: code + process only, no personal files, no large artifacts
- **Large files** → Google Drive (link from repo, not stored in Git)
- **Handoffs**: every session commits `handoffs/YYYY-MM-DD-session-N.md` — cross-model readable
- **Branches**: feature work in worktrees, merge to main only after audit gate PASS
- **GitHub agent** (to build): manages repo hygiene, handoff commits, PR gating, airlock enforcement

---

## SAGEX SCAFFOLD REVIEW

Scaffold from `sagex-plugin-scaffold.tar.gz` (built by another model — reviewed session 43):

### Keep As-Is
| Component | Status |
|---|---|
| `plugin.json` | Good structure, correct fields |
| `config/approved_sources.json` | Perfect — global + per-project, `_edit_mode_required` |
| `config/notebook_assignments.json` | Perfect — zero access default |
| `/sagex:edit-mode` command | Exactly right |
| `/sagex:lock` command | Good — validates JSON integrity |
| `/sagex:approve-source` command | Correct protocol |
| `/sagex:build-loop` command | Solid — coder→ZCR→Semgrep→retry, max 3 rounds |
| `skills/audit-loop/SKILL.md` | Well written |
| `skills/research-gate/SKILL.md` | Well written — per-project sources, URL resolution |
| `agents/zero-context-reviewer.md` | Clean, Sonnet, read-only |

### Missing / Needs Building
| Component | Priority | Notes |
|---|---|---|
| `hooks/` directory | CRITICAL | Empty — needs validate_research.py + audit_gate_check.sh + all current hooks |
| `rules/` directory | CRITICAL | Empty — needs all sagex rules written |
| `skills/brain-harness/SKILL.md` | HIGH | Dir exists, no content |
| `skills/coding-harness/SKILL.md` | HIGH | Dir exists, no content |
| `skills/edit-mode/SKILL.md` | HIGH | Dir exists, no content |
| GitHub agent + skill | HIGH | Not in scaffold — needs full design |
| NotebookLM research skill | HIGH | Not in scaffold |
| Multi-session / worktree skill | MED | Not in scaffold |
| Sandbox mode | MED | Not in scaffold |
| Cross-model handoff skill | MED | This handoff pattern — needs to be automated |

---

## REPOS BEING CONSIDERED

### For SageX Plugin Base (fork or adapt)
| Repo | URL | What to Take | Action |
|---|---|---|---|
| superpowers | github.com/obra/superpowers | Skills structure, brainstorming/planning patterns | Adapt skills pattern |
| dev-process-toolkit | github.com/nesquikm/dev-process-toolkit | Gate-check, spec-driven development | Already installed, study structure |
| autoresearch | github.com/uditgoenka/autoresearch | Autonomous loop protocol, iteration patterns | Already installed, study loop design |
| hookify | (Anthropic plugin) | Rule-from-conversation pattern, hook generation | Adapt for sagex rule management |
| deep-plan | github.com/piercelamb/plugins | Multi-LLM plan review, section-based planning | Already installed |

### Fork vs Link Decision
- **Fork** if we need to modify internals (superpowers skills → sagex skills)
- **Link** (install as dependency) if using as-is (dev-process-toolkit, autoresearch)
- **Adapt** (copy patterns, don't fork) for conceptual borrowing

### For NT Work (load when needed, NOT NOW)
| Repo | URL | Purpose |
|---|---|---|
| OPRO | github.com/google-deepmind/opro | LLM optimization loop for indicator selection |
| ReEvo | github.com/ai4co/reevo | Evolutionary code optimization |
| OpenEvolve | github.com/codelion/openevolve | Full AlphaEvolve implementation |

---

## GITHUB AGENT — NOTES FOR FUTURE BUILD

**Purpose**: Manage repos as code + process infrastructure, not cloud storage.

**Key behaviors needed**:
1. Auto-commit handoffs: every session end → commit `handoffs/YYYY-MM-DD-session-N.md`
2. Repo hygiene: flag non-code files, personal info, large binaries
3. Large file routing: artifacts >10MB → Google Drive link, not Git
4. Branch discipline: feature in worktree, audit gate required for merge to main
5. Airlock enforcement: no push without audit receipt
6. Cross-model readable: handoffs must be structured for Gemini/Codex/Claude to parse
7. Sandbox management: `0SxD/sjm-sandbox` needs cleanup (personal files, unnecessary output)

**Note**: GitHub is a source of truth and audit trail for code changes — NOT a sync drive.

---

## WHAT'S NEXT (for whoever picks this up)

### Immediate (before NT work resumes)
1. Fix NotebookLM auth (run cleanup + re-auth manually in terminal)
2. Build SageX plugin from scaffold — fill missing components
3. Write rules/ for sagex
4. Port existing hooks into sagex/hooks/
5. Write brain-harness, coding-harness, edit-mode skills
6. Design GitHub agent + skill

### Then
7. Research gate: add URL resolution check (verify link works, not just domain)
8. Approved sources: move to `sagex/config/approved_sources.json` — Sage re-approves all
9. NT resume: NT sandbox + indicator visualization + SJM re-run

### Carry-Forward Sage Directives
- OpenBrainLM is umbrella overseer for ALL projects
- NT = `C:/apps_ai/nautilus_trader/` ONLY — subproject under OB governance
- Only open source with 1K+ GitHub stars
- trading_bot_build_2026 is OLD — DO NOT TOUCH
- Step-by-step with Sage at every piece — no autonomous deployment
- Research gate must enforce approved sources — never guess or google
- Agents are defined and locked — only change in edit mode

---

## KEY FILE LOCATIONS

| File | Purpose |
|---|---|
| `~/.claude/hooks/validate_research.py` | Research gate v2 |
| `~/.claude/hooks/audit_gate_check.sh` | Commit gate |
| `~/.claude/hooks/auto_reviewer_trigger.sh` | Post-write audit trigger |
| `~/.claude/hooks/opus_write_guard.sh` | Opus→Sonnet enforcement |
| `.claude/skills/audit-loop.md` | Coder-auditor loop skill |
| `memory/short_term.md` | Session 41-43 activity |
| `memory/handoff_session42_guardrails_fix.md` | Previous handoff |
| `memory/repos_to_evaluate.md` | ML repos + plugins list |
| `Downloads/sagex-plugin-scaffold.tar.gz` | SageX scaffold (reviewed session 43) |
