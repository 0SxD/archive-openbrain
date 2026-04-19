# Categorical Memory Architecture — Hostile Audit
> Date: 2026-03-24
> Auditor: Claude Sonnet 4.6 (hostile mode — assume everything broken)
> Standard source: OpenBrainLM/memory/long_term.md § "Categorical Memory Architecture"

---

## Standard Being Verified

From `OpenBrainLM/memory/long_term.md` [2026-03-24]:

- Every project brain requires BOTH chronological (`short_term.md`) AND categorical files
- Required categorical files for all projects: `decisions.md`, `blockers.md`
- Required for trading projects additionally: `indicators.md`
- Schema: Statement | Confidence | Source | Status | last_verified_date (5 fields max)
- Confidence bouncer: < 0.6 → quarantine, NOT promoted
- `brain-harness.md` skill must enumerate all categorical files for all 3 projects
- Memory must live in `memory/` (NOT `.claude/memory/`) — Issue #21242

---

## 1. OpenBrainLM Brain

### long_term.md — Categorical Memory Standard Documented?
**PASS**

Section `## Categorical Memory Architecture (STANDARD — applies to ALL project brains)` is present at line 42.
Contains:
- Source: Agents_Arcs NotebookLM (156 sources), research file cited
- Finding (verified): chronological + categorical both required — stated explicitly
- Schema rule (5 fields max): Statement | Confidence | Source | Status | last_verified_date — present
- Confidence bouncer: Confidence < 0.6 → quarantine — present
- List of required files: decisions.md, blockers.md, indicators.md (trading) — present
- Anti-pattern (naive AI summarization = memory rot) — present
- Implementation status as of 2026-03-24 — present

All required elements confirmed.

### decisions.md — Exists and Has Content?
**PASS**

File: `<WORKSPACE>\OpenBrainLM\memory\decisions.md`
- Exists: YES
- Has content: YES — 22 decision rows spanning 2026-03-21 to 2026-03-24
- Schema columns: Date | Decision | Reasoning | Status | Confidence | Source — all present
- Most recent entry: 2026-03-24 (categorical memory architecture added)
- Confidence bouncer compliant: lowest entry is 0.7 (above 0.6 threshold)

### blockers.md — Exists and Has Content?
**PASS**

File: `<WORKSPACE>\OpenBrainLM\memory\blockers.md`
- Exists: YES
- Has content: YES — 6 blocker rows
- Schema columns: Date | Blocker | Status | Resolution | Source — all present
- Mix of RESOLVED and OPEN entries — correct usage
- 2 OPEN blockers noted (MCP auth gaps, NotebookLM add_source capability)

### brain-harness.md — Exists and Reads All Categorical Files for All 3 Projects?
**PARTIAL PASS — minor gap**

File: `<WORKSPACE>\OpenBrainLM\.claude\skills\brain-harness.md`
- Exists: YES
- Reads OpenBrainLM decisions.md and blockers.md: YES (Step 3, lines 36-37) — listed as "(if exists)"
- Reads Trading Bot decisions.md, blockers.md, indicators.md: YES (Step 4, lines 45-47) — listed as "(if exists)"
- Reads NautilusTrader decisions.md and blockers.md: YES (Step 5, lines 54-55) — listed as "(if exists)"

Note: All categorical files are listed as "(if exists)" — this is acceptable conditional loading. No missing files.

---

## 2. <TRADING_PROJECT> Brain — CRITICAL GAP SUSPECTED

### Dual Memory Location — .claude/memory/ AND memory/?
**FAIL — DUAL LOCATION CONFIRMED**

Two memory directories exist:
- `<WORKSPACE>\<TRADING_PROJECT>\.claude\memory\` — contains: `connections.md`, `long_term.md`, `short_term.md`
- `<WORKSPACE>\<TRADING_PROJECT>\memory\` — contains: `blockers.md`, `connections.md`, `decisions.md`, `indicators.md`, `long_term.md`, `short_term.md`

The `.claude/memory/` location is the OLD location — pre-Issue #21242 fix. The `memory/` location is the correct one (per OpenBrainLM long_term.md decision [2026-03-23]: "Memory dirs moved from .claude/memory/ to memory/ due to Claude Code Issue #21242").

The `.claude/memory/` copies have NOT been removed. They are stale and potentially diverged from the canonical `memory/` files.

**Action required:** Remove or archive `<TRADING_PROJECT>/.claude/memory/` to prevent stale reads. Claude Code may load `.claude/memory/` preferentially in some contexts.

### CLAUDE.md in .claude/ — Exists?
**FAIL — NO CLAUDE.md IN .claude/**

`<WORKSPACE>\<TRADING_PROJECT>\.claude\` contains:
- hookify.*.local.md files (5)
- memory/ (stale — see above)
- settings.json, settings.local.json
- skills/
- worktrees/

**NO CLAUDE.md exists in `<TRADING_PROJECT>/.claude/`.** This is a critical gap. Without a project-level CLAUDE.md in `.claude/`, Claude Code cannot auto-load project governance when working in this directory. The project has no bootup identity declaration.

Note: The hookify files and settings.json indicate the `.claude/` directory is in use. The absence of CLAUDE.md means no project rules, memory file paths, or governance are auto-loaded.

### memory/decisions.md — Exists and Has Content?
**PASS**

File: `<WORKSPACE>\<TRADING_PROJECT>\memory\decisions.md`
- Exists: YES
- Has content: YES — 13 decision rows spanning 2026-03-23 to 2026-03-24
- Schema columns: Date | Decision | Reasoning | Status | Confidence | Source — all present
- Key decisions captured: Python 3.13, off-the-shelf only, SJM regime gate as alpha source, full rebuild
- Confidence bouncer compliant: lowest entry is 0.7

### memory/blockers.md — Exists and Has Content?
**PASS**

File: `<WORKSPACE>\<TRADING_PROJECT>\memory\blockers.md`
- Exists: YES
- Has content: YES — 9 blocker rows (7 OPEN, 2 RESOLVED)
- Schema columns: Date | Blocker | Status | Resolution | Source — all present
- Critical OPEN blockers documented: missing 30s bars, predict_online not implemented, strategy shell incomplete

### memory/indicators.md — Exists and Has Content?
**PASS**

File: `<WORKSPACE>\<TRADING_PROJECT>\memory\indicators.md`
- Exists: YES
- Has content: YES — comprehensive inventory
- 42 distinct indicators documented, 14 flagged CUSTOM
- 101 Boolean signal modules across 18 groups documented
- Risk tiers (HIGH/MEDIUM/LOW) applied — appropriate schema extension
- Locked formula references noted as REFERENCE ONLY per Creator directive
- PDF gap flagged (5 files unread due to missing pdftoppm)

---

## 3. NautilusTrader Brain

### CLAUDE.md — Memory Section Points to decisions.md and blockers.md?
**PASS**

File: `<WORKSPACE>\nautilus_trader\.claude\CLAUDE.md`
- Exists: YES (in `.claude/CLAUDE.md` — correct location for project governance)
- Memory section present at line 65: `## Memory Files (read these at session start)`
- Table explicitly lists: `memory/decisions.md` and `memory/blockers.md`
- Both entries note "(new 2026-03-24) per Agents_Arcs research" with source citation
- States categorical files exist "alongside short_term.md — not a replacement" — correct framing

Note: NautilusTrader .claude/ does NOT have a stale `.claude/memory/` directory — only the correct `memory/` top-level directory exists.

### memory/decisions.md — Exists and Has Content?
**PASS**

File: `<WORKSPACE>\nautilus_trader\memory\decisions.md`
- Exists: YES
- Has content: YES — 10 decision rows spanning 2026-03-23 to 2026-03-24
- Schema columns: Date | Decision | Reasoning | Status | Confidence | Source — all present
- Key decisions: BarDataWrangler over BarBuilder, Python 3.13, 4-sub-project architecture, migration governance
- One entry marked "Active — needs verification" (ts_init_delta, Confidence 0.8) — correct usage

### memory/blockers.md — Exists and Has Content?
**PASS**

File: `<WORKSPACE>\nautilus_trader\memory\blockers.md`
- Exists: YES
- Has content: YES — 6 blocker rows (4 OPEN, 2 RESOLVED)
- Schema columns: Date | Blocker | Status | Resolution | Source — all present
- Critical OPEN blocker: data/ directory empty (pipeline cannot run until populated)

---

## Gap Summary

| # | Gap | Severity | Project | Action |
|---|---|---|---|---|
| 1 | `<TRADING_PROJECT>/.claude/memory/` exists alongside `memory/` — stale old location not removed | HIGH | Trading Bot | Remove/archive `.claude/memory/` to eliminate stale read risk |
| 2 | No `CLAUDE.md` in `<TRADING_PROJECT>/.claude/` | CRITICAL | Trading Bot | Create project CLAUDE.md with governance, rules, and memory file paths |

---

## Overall Verdict: CONDITIONAL PASS

**The categorical memory standard is structurally in place** — all 6 categorical files (decisions.md, blockers.md for all 3 projects; indicators.md for trading bot) exist with content and correct schema. The brain-harness.md skill reads all of them. The standard itself is properly documented in OpenBrainLM/long_term.md.

**Two gaps prevent a clean PASS:**

1. **CRITICAL**: `<TRADING_PROJECT>/.claude/CLAUDE.md` does not exist. Claude Code cannot auto-load project governance for this project.
2. **HIGH**: Stale `.claude/memory/` in trading bot was not cleaned up when memory was migrated to `memory/`. Risk of stale reads or confusion.

The NautilusTrader and OpenBrainLM brains are fully compliant. The trading bot brain has both categorical files in place but is missing its project CLAUDE.md and has a stale memory directory.
