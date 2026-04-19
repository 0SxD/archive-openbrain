# Session 38–44 Full Inventory
> Research agent report. Compiled 2026-03-29.
> Sources: short_term.md, long_term.md, progress.txt, connections.md, todos.md,
>          handoffs 38–42, session43 sagex design, repos_to_evaluate.md,
>          session38 spec + plan files.
> Exhaustive — every reference captured.

---

## Section 1: Every Rule Referenced or Created (Sessions 38–44)

### Global Rules (~/.claude/rules/)

| # | Rule File | What It Does | Status |
|---|-----------|--------------|--------|
| 00 | `00_public_actions.md` | Blocks all public actions (git push, GitHub issues, posting) without explicit Sage approval per-action | ACTIVE |
| 01 | `01_agent_system.md` | Agent architecture: Initializer→amnesiac Workers→Judge, two tiers only, episodic runtimes. Delegation model: Opus orchestrates, Sonnet executes, Haiku trivial tasks. | ACTIVE |
| 02 | `02_build_philosophy.md` | Research-first; never answer from training data; cite third-party sources; libraries over custom code; versioning discipline (copy, never edit originals); standard plugin sequence | ACTIVE |
| 03 | `03_memory_discipline.md` | Write to brain files without asking; save after every major task; target: short_term.md, OPEN_BRAIN.md, claude_code_log.md | ACTIVE |
| 04 | `04_integrity.md` | Read first, report second; no hallucinated file/folder descriptions; verify key files directly before presenting | ACTIVE |
| 05 | `05_research_protocol.md` | ASK for corridor before starting; 1-2 questions per NLM query; max 5 follow-up rounds; save to research/ folder; unverifiable claims → quarantine | ACTIVE |
| 06 | `06_agent_reporting.md` | After any subagent: tell Sage immediately → dispatch audit agent → report 2-3 bullets after audit passes | ACTIVE |
| 07 | `07_memory_verification.md` | Schema-driven verification (5 fields); confidence bouncer (<0.6 → quarantine); chain of verification before promoting to long_term | ACTIVE |
| 08 | `08_bootup_ritual.md` | Orchestrator reads propagation manifest + project brain short_term.md + long_term.md + connections.md at session start. Sub-agents get minimum viable context only. | ACTIVE |
| 09 | `09_hostile_audit_tools.md` | Every hostile audit MUST include Semgrep scan + CodeRabbit + manual review; include in all audit agent prompts | ACTIVE |
| 10 | `10_notebooklm_orchestrator_only.md` | NLM MCP stays with orchestrator session only; never dispatch sub-agents to query NLM; Gemini as fallback | ACTIVE |
| 11 | `11_creator_reference.md` | All tracked files use "creator" or "Sage" — no real names. Memory/private files may use real names. | ACTIVE |
| 12 | `12_delegation_protocol.md` | 6-state execution pipeline (Task Spec → Write Permit → Dispatch → Audit Trigger → Review Audit → Resolution). Opus NEVER writes code. Opus NEVER reads unaudited code. All subprojects inherit this. | ACTIVE — codified session 31 |
| ZT | `zero_trust_architecture.md` | Deterministic enforcement via hooks (not text pleas). Research gate blocks .py writes. Zero-context reviewer runs after writes. Episodic operation (context washing). | ACTIVE |

**22 archived rules** moved from `~/.claude/rules/_archive/` → `~/.claude/rules_archive_inactive/` during session 42. This saved ~3,000 tokens per session. These are inactive and NOT loaded.

### Project Rules (<WORKSPACE>/OpenBrainLM/.claude/rules/)

| # | Rule File | What It Does | Status |
|---|-----------|--------------|--------|
| 00 | `00_session_context.md` | Ask "What's the context today?" at every session start; record answer in short_term.md as session header; check for drift | ACTIVE |
| 01 | `01_creator_reference.md` | Same as global rule 11 — project-level copy for OB | ACTIVE |
| 01 | `01_trading_rules.md` | Trading-specific rules (exact content not read in this audit, but file exists) | ACTIVE |

### Rules Referenced / Proposed But Not Yet Files

| Rule | Description | Session Proposed | Status |
|------|-------------|------------------|--------|
| Research Gate v2 approved-source whitelist | Only Sage can add approved sources; URL must match approved_sources.json domain + resolve | Session 41 design, Session 42 implemented in validate_research.py | IMPLEMENTED in hook, not a separate rule file |
| Edit Mode rule | /sagex:edit-mode unlocks config files; /sagex:lock re-engages + validates JSON; hooks still fire during edit mode | Session 43 design | PENDING — SageX scaffold exists but rules/ is empty |
| Sandbox rules (SB-01 through SB-06) | Open-source only, no custom code, stdlib-first Python, outputs to handoffs/ only. SB-05: NLM is mandatory research gate for sandbox work. | Session 44 | ACTIVE — written to sandbox/SANDBOX_RULES.md |
| SageX rules/ directory | All sagex enforcement rules — currently empty directory in scaffold | Session 43 | MISSING — needs content |

---

## Section 2: Every Skill Referenced or Created

### Project Skills (<WORKSPACE>/OpenBrainLM/.claude/skills/)

| Skill | File Path | What It Does | Status |
|-------|-----------|--------------|--------|
| audit-loop | `.claude/skills/audit-loop.md` | Automated coder-auditor loop: Sonnet writes → ZCR + Semgrep audit → fix loop, max 3 iterations, Opus can break | CREATED session 42, UNTESTED as of session 43 |
| brain-harness | `.claude/skills/brain-harness.md` | Content unknown (file exists) | EXISTS — content not audited |
| coding-harness | `.claude/skills/coding-harness.md` | Content unknown (file exists) | EXISTS — content not audited |
| notebooklm-research | `.claude/skills/notebooklm-research.md` | NLM research loop skill | EXISTS — content not audited |
| worktree-isolation | `.claude/skills/worktree-isolation.md` | Worktree isolation pattern | EXISTS — content not audited |

### Agent Skills (<WORKSPACE>/OpenBrainLM/.agents/skills/) — Created Session 44

| Skill | File Path | What It Does | Status |
|-------|-----------|--------------|--------|
| notebooklm-research | `.agents/skills/notebooklm-research/SKILL.md` | Research loop skill with source citations | CREATED session 44 |
| notebooklm-mcp-auth | `.agents/skills/notebooklm-mcp-auth/SKILL.md` | Exact auth how-to (setup_auth tool steps) | CREATED session 44 |

### SageX Scaffold Skills (Downloads/sagex-plugin-scaffold.tar.gz — reviewed session 43)

| Skill | Status | Notes |
|-------|--------|-------|
| skills/audit-loop/SKILL.md | GOOD — keep as-is | ZCR+Semgrep+Opus triad, well defined |
| skills/research-gate/SKILL.md | GOOD — keep as-is | Per-project sources, URL resolution check |
| skills/brain-harness/ | MISSING SKILL.md | Dir exists, no content |
| skills/coding-harness/ | MISSING SKILL.md | Dir exists, no content |
| skills/edit-mode/ | MISSING SKILL.md | Dir exists, no content |
| GitHub agent + skill | NOT IN SCAFFOLD | Needs full design |
| NotebookLM research skill | NOT IN SCAFFOLD | — |
| Multi-session/worktree skill | NOT IN SCAFFOLD | — |
| Sandbox mode | NOT IN SCAFFOLD | — |
| Cross-model handoff skill | NOT IN SCAFFOLD | This handoff pattern needs automation |

### Installed Claude Code Plugins (Session 42)

| Plugin | Source | What It Adds | Status |
|--------|--------|--------------|--------|
| dev-process-toolkit | nesquikm/dev-process-toolkit | Deterministic gate-check, bounded TDD, spec hierarchy | INSTALLED session 42, TESTED session 43 |
| deep-plan | piercelamb/plugins | Multi-LLM plan review, section-based planning | INSTALLED session 42, TESTED session 43 |
| autoresearch | uditgoenka/autoresearch | Autonomous iteration loop, Goal/Scope/Metric/Verify | INSTALLED session 42, TESTED session 43 |
| ecc-agentshield | npm (ecc-agentshield) | Security scan of CLAUDE.md, settings, hooks, MCP | INSTALLED session 42; Baseline: Grade D (43/100), 39 HIGH (permission bloat) |
| Ralph | frankbria/ralph-claude-code | Overnight loop, exit detection, circuit breaker | CLONED to ~/.ralph session 42; NOT assigned any task yet |
| superpowers | github.com/obra/superpowers v5.0.6 | 14 skills, 1 hook, 1 agent | RESEARCHED session 42; referenced for SageX skills structure |
| coderabbit | claude-plugins-official | AI code review | UNINSTALLED session 42 — CLI was never installed, was fake Sonnet fallback |

---

## Section 3: Every Hook Referenced or Created

### Global Hooks (~/.claude/hooks/)

| Hook | File | Trigger | What It Does | Status |
|------|------|---------|--------------|--------|
| brainstem_inject.sh | `~/.claude/hooks/brainstem_inject.sh` | PreToolUse (all tool calls matching pattern) | Re-broadcasts core principles before every decision tool; L4 Action Selection inhibition-by-default | ACTIVE, TESTED |
| validate_research.py | `~/.claude/hooks/validate_research.py` | PreToolUse: Write\|Edit on .py files | Blocks .py writes without fresh research.md at project root (<1hr mtime, >50 chars, URL from approved_sources.json). v2 fixes: cross-cwd (resolves from target file), URL quality check, citation logging to .claude/research_citations.log, PROJECT_ROOT env bypass removed | ACTIVE — v2 FIXED session 42 |
| destructive_command_guard.py | `~/.claude/hooks/destructive_command_guard.py` | PreToolUse: Bash | Blocks rm -rf, force push, echo/printf/cat/tee file-write bypasses. FILE_WRITE_EXEMPTIONS: /dev/null, stderr, .log, .tmp | ACTIVE, TESTED 4/4 |
| audit_gate_check.sh | `~/.claude/hooks/audit_gate_check.sh` | PreToolUse: Bash (git commit* only, conditional if) | Validates .audit_receipt.json exists + is fresh + timestamp not spoofed before git commit. Was in project hooks only — copied to global hooks session 42. | ACTIVE — PATH FIX applied session 42, TESTED 3/3 |
| auto_reviewer_trigger.sh | `~/.claude/hooks/auto_reviewer_trigger.sh` | PostToolUse: Write\|Edit\|Bash on .py + .sh | Spawns zero-context reviewer for .py/.sh writes. Changed exit 0 → exit 2 (real gate, not nudge) in session 42. | ACTIVE — now a hard gate |
| agent_result_capture.sh | `~/.claude/hooks/agent_result_capture.sh` | PostToolUse (agent results) | Captures agent results for logging | ACTIVE (existence confirmed, full content not audited) |
| precompact_save.sh | `~/.claude/hooks/precompact_save.sh` | Stop (session end) | Session state snapshot — saves progress before context compaction | ACTIVE |
| propagation_check.sh | `~/.claude/hooks/propagation_check.sh` | PostToolUse (propagation events) | Checks propagation state | ACTIVE (existence confirmed) |
| session_savepoint_inject.sh | `~/.claude/hooks/session_savepoint_inject.sh` | SessionStart | Injects save-point context (progress.txt + features.json) at session start | ACTIVE |

**PostCompact hook** (wired in session 41): SessionStart compact matcher re-injects brainstem after compaction. Wired in `~/.claude/settings.json`. UNTESTED as of session 41 handoff.

### Project Hooks (<WORKSPACE>/OpenBrainLM/.claude/hooks/)

| Hook | File | Trigger | What It Does | Status |
|------|------|---------|--------------|--------|
| audit_reminder.sh | `.claude/hooks/audit_reminder.sh` | PostToolUse: Edit\|Write\|Bash | Layer 1 nudge: writes .claude/active_audit_state.md when no receipt exists. Exit 0 (never blocks). | ACTIVE — state file approach (session 31 fix) |
| write_audit_receipt.sh | `.claude/hooks/write_audit_receipt.sh` | (called manually after 3-agent audit) | Writes .audit_receipt.json; clears active_audit_state.md | ACTIVE |
| audit_read_blocker.sh | `.claude/hooks/audit_read_blocker.sh` | PreToolUse: Read | Blocks Opus from reading code files (.py, .sh) that are newer than the audit receipt. Uses mtime comparison. | ACTIVE — TESTED 4/4 (session 32 T14-T17) |
| audit_gate_check.sh | `.claude/hooks/audit_gate_check.sh` | PreToolUse: Bash | Project-level copy. Validates receipt before git commit. | ACTIVE (copy — global copy is the authoritative one post-session 42 fix) |
| opus_write_guard.sh | `.claude/hooks/opus_write_guard.sh` | PreToolUse: Write\|Edit | Blocks Opus from writing .py/.sh files directly; requires write_permit.json + Sonnet dispatch. Clock skew bug fixed session 40 ([/\] paths, stat -c %Y + python time.time()). | ACTIVE — FIXED session 40 |

### Git Hook

| Hook | File | What It Does | Status |
|------|------|--------------|--------|
| pre-commit | `<WORKSPACE>/OpenBrainLM/.git/hooks/pre-commit` | Native git pre-commit: validates .audit_receipt.json before any commit. Migrated from PreToolUse regex (session 32). Template at docs/templates/pre-commit. Installer: scripts/setup_git_hooks.sh | ACTIVE — TESTED (session 32 live commit) |
| pre-commit (NT) | `<WORKSPACE>/nautilus_trader/.git/hooks/pre-commit` | Same as above, installed for NT repo session 37 | ACTIVE |

### Hook Bugs Found and Fixed (Sessions 38–42)

| Bug | Session Found | Fix Applied | Status |
|-----|---------------|-------------|--------|
| audit_gate_check.sh in wrong path (project hooks, not global) | Session 42 | Copied to ~/.claude/hooks/ | FIXED |
| validate_research.py cross-cwd: os.getcwd() checked OB's research.md when editing NT files | Sessions 40, 41, 42 | resolve_project_root() walks from target file dir | FIXED session 42 |
| validate_research.py citation quality: size > 50 chars only, no URL check | Session 41 design, session 42 fix | APPROVED_DOMAINS whitelist (9 domains) + urlparse check | FIXED session 42 |
| validate_research.py denial message referenced "research/ directory" but code only checks research.md | Session 40 (Sage-flagged) | Corrected in session 42 | FIXED |
| validate_research.py PROJECT_ROOT env bypass (ZCR critical finding) | Session 42 ZCR | Removed entirely | FIXED |
| auto_reviewer_trigger.sh exit 0 → was a nudge, not a gate | Session 42 | Changed to exit 2 | FIXED |
| opus_write_guard.sh backslash path exemption: Windows \ paths, grep matched / only | Session 40 | [/\] character class | FIXED session 40 |
| opus_write_guard.sh clock skew: hook's date +%s ~32,000s ahead of Bash tool | Sessions 37, 40 | stat -c %Y + python time.time() fallback. ZCR caught fallback reintroducing skew → fixed to echo "0" (fail open) | FIXED session 40 |
| PostToolUse stdout suppressed on exit 0 (framework limitation — nudge text never reached agent) | Session 31 | State file approach: audit_reminder.sh writes .claude/active_audit_state.md | FIXED (workaround) |
| git commit regex false-positive (matched inside quoted arguments) | Session 32 | Anchored regex to command position + subshell coverage | FIXED session 32 |
| Bash file-write bypass: Opus switched to Bash echo > file to bypass Write hook | Session 28 | FILE_WRITE_PATTERNS in destructive_command_guard.py | FIXED session 29 |
| Security plugin (security-guidance) false positive on serialization keyword in .md files | Session 30 | Plugin DISABLED (replaced by Semgrep in receipt gate) | RESOLVED |
| T02 framework limitation: stderr from command hooks on exit 0 not surfaced | Session 32 | CONDITIONAL (accepted limitation — state file workaround in place) | KNOWN LIMITATION |

### Hook Gaps Still Outstanding

| Gap | Session Noted | Priority | Status |
|-----|---------------|----------|--------|
| OB-H2: Objective verification gate — research gate checks existence, not truth | Session 29, todos.md | P1 | NOTED, not blocking NT |
| OB-H3: Escalation trigger hook — ambiguity → halt + ask human (text rules only, not mechanical) | Session 29, todos.md | P1 | NOTED, not blocking NT |
| OB-H4: Concurrency control — merge queue for parallel writes | Session 29, todos.md | P2 | DORMANT (single-agent episodic) |
| CodeRabbit 3rd auditor slot | Session 42 | HIGH | PENDING — Sage deciding replacement |
| PostCompact hook untested | Session 41 | MED | Wired but not verified |
| SageX hooks/ directory empty | Session 43 | CRITICAL | Needs validate_research.py + audit_gate_check.sh + all current hooks ported |

---

## Section 4: Uncompleted Todo Items (All Sources)

### NT Critical Path — Pending

| Task ID | Description | Status | Notes |
|---------|-------------|--------|-------|
| NT-04 | Write reassembly script for NT venv (fresh SJM + Scaler from .npz params) | PENDING | Spec ready; agents were blocked by permit expiry in session 39 |
| NT-05 | Wire SJM into NT Strategy.on_start() — predict_online only | PENDING | Needs NT-04 first |
| NT-06 | NT BacktestEngine validate 6 Sharpe configs | PENDING | Needs NT-05 first |
| NT-13 | Build 30s bars from raw aggTrades | PENDING | bars_30s/ directory does not exist; backtest returns None without it |
| NT-14 | Implement predict_online in SparseJumpAdapter | PENDING | BaseRegimeModel raises NotImplementedError; blocks live inference |
| NT-15 | Fix df_to_nt_bars → use BarDataWrangler | PENDING | Manual Bar() construction has precision mismatch risk; use TradeTickDataWrangler per audit |
| NT-16 | Build NautilusFibChikouStrategy (currently shell) | PENDING | on_bar, on_start, subscribe_bars, on_stop ALL MISSING |
| NT-17 | Rewrite indicator_hub.py (vectorized → stateful) | PENDING | NT event-driven model requires incremental stateful Indicators |
| NT-18 | Verify rebuilt bars match NT BarBuilder output | PENDING | After NT-13 |
| NT-20 | Re-run Track A Optuna gate audit with predict_online | PENDING | +18.81 Sharpe flagged: deprecated adapter + Optuna selection bias |
| NT-21 | Re-run alpha pool modules with predict_online gate | PENDING | Top modules Sharpe 46-53 used batch predict; need causal re-run |
| NT-22 | Verify fullyear_summary.csv Sharpe range validity | PENDING | Pre-fix or post-fix? |
| NT-23 | NautilusTrader local backtest — all custom indicators | PENDING | Visual parity → GCP |
| SJM-NT-01 | SJM predict_online in NT BacktestEngine | PENDING | Load via model_loader, correct pipeline |
| DTMC-01 | DTMC sanity check with own indicator patterns | PENDING | After SJM evaluation. Scope TBD. |

### NT Partial / Blocked

| Task ID | Description | Status | Notes |
|---------|-------------|--------|-------|
| NT-09 | Wire NT brain — bootup ritual + context_today | PARTIAL | rules/02 created; bootup ritual + context_today still needed |
| NT-10 | Create NT Documentation notebook in NotebookLM | PENDING | Upload key NT docs; becomes research corridor |
| Precompute script | precompute_sjm_regime.py | SPEC READY, NOT WRITTEN | Agents blocked by permit expiry in session 39; spec in handoff_session39_github_cleanup.md |

### OB System Integrity — Pending

| Task ID | Description | Priority | Status |
|---------|-------------|----------|--------|
| OB-S9 | PII scrub — replace real name with "Sage" in ALL tracked files across ALL 3 projects | P1 | PENDING — Sage directive session 32 |
| OB-S11 | Execute Phase 3 epic | P0 | docs/backlog/epic_phase3_readiness.md — 4 components; after commit |
| OB-S12 | GitHub airlock — seal both repos after Phase 3 | P0 | Push OB + NT to GitHub after Phase 3 sealed; Sage approval required |

### SageX Plugin Build — Pending (All from Session 43)

| Item | Priority | Status |
|------|----------|--------|
| Port existing hooks into sagex/hooks/ | CRITICAL | PENDING |
| Write sagex rules/ directory content | CRITICAL | PENDING |
| Write brain-harness SKILL.md | HIGH | PENDING |
| Write coding-harness SKILL.md | HIGH | PENDING |
| Write edit-mode SKILL.md | HIGH | PENDING |
| Design + build GitHub agent + skill | HIGH | PENDING |
| Research gate: add URL resolution check (verify link works, not just domain match) | MED | PENDING — session 43 noted, partial in session 42 |
| Move approved_sources.json to sagex/config/ | MED | PENDING |
| Fix NotebookLM auth (cleanup + re-auth in terminal) | IMMEDIATE | PENDING — Playwright scraper, auth failing as of session 43; fixed in session 44 per short_term |
| Build sandbox mode for SageX | MED | PENDING |
| Cross-model handoff skill | MED | PENDING |
| Multi-session/worktree skill | MED | PENDING |

### NT Phase 2 / Option A (LLM-Guided Indicator Pipeline)

| Item | Description | Status |
|------|-------------|--------|
| Tear down [redacted-sandbox], create new clean sandbox | Sage directive sessions 41-43 | PENDING |
| [redacted-sandbox] cleanup (remove charts/output bloat) | Keep 3 specific charts Sage wants (<100MB); rest → Google Drive | PENDING |
| Option A indicator visual setup | Sage must see ALL indicators visualized before any code touches them | PENDING |
| mRMR pre-screener (feature-engine MRMR) | feature-engine 1.9.4 already installed; method="MIQ", max_features=20 | PENDING |
| OPRO wiring to BacktestEngine.reset() | github.com/google-deepmind/opro | NOT YET STARTED |
| Independent verification of mRMR, OPRO, ReEvo repos | Sage directive: don't trust LLM research doc blindly | PENDING |
| GCP control flow setup | Short jobs, fluid control, automation once set up | PENDING |
| Re-run original positive-Sharpe SJM configs with predict_online + corrected labels | Sage directive | PENDING |
| Indicator groupings from Sage (~2000 words) | Sage has specifics to provide | WAITING ON SAGE |

### Postponed (Sage Activates When Ready)

| # | Description | Priority |
|---|-------------|----------|
| 2 | Test memory consolidation — 4-field schema check | P1 |
| 3 | Test rules 06/07 — agent reporting + memory verification | P1 |
| 4 | Test context survival through compaction | P1 |
| 5 | Test skills/communication — notebook routing, Sonnet dispatch | P2 |
| 6 | Test Trinity dialectic end-to-end | P2 |
| 7 | Test researcher role using all of the above | P2 |
| 8 | Package OpenBrainLM as Claude Code plugin | P1 — after NT ships |
| 10 | Check community engagement (OpenEvolve #447, Khoj #1294, OB1 Discord) | P3 |
| 11 | HN Show HN post | P3 — account too new |
| 13 | Migrate audit records to JSON schema | P2 |
| 14 | Investigate Ralph loop retry cap | P2 |
| 16 | Regime gate research — DTMC vs SJM vs both | P2 |
| 18 | Rule scan — "must implement custom" contamination | P2 |
| 23 | Set up Pinecone for textbook library RAG | P2 |
| 24 | Clone ALL referenced repos to _repos/ | P1 — 5 done; move to NT when needed |
| 27 | NotebookLM naming standards research | P1 |
| 28 | Reorganize _repos/ into trading/ subfolder | P2 |
| 29 | Clean up stale .claude/memory/ in NT project | P2 — needs Sage approval |
| 31 | Audit/remove unused plugins | P2 |
| 32 | Evaluate Plugin Dev Toolkit | P1 — after NT ships |
| 33 | Install 3 new plugins (skill-creator, mcp-server-dev, pr-review-toolkit) | P0 |
| 34 | Connect GitHub services | P1 |
| 35 | Test blackboard with Gemini | P0 — Phase 5 |
| 36 | Set up GitHub Actions for Stage 2 remote audit | P1 |
| 37 | Record MCP architecture rules in long_term.md | P1 |
| 38 | Wire trading bot audit pipeline | P1 — after OB airlock proven |
| 39 | Overnight job: package brain as plugin | P1 |
| 40 | Update OpenBrainLM on GitHub after wiring confirmed | P1 |

### Memory Gap Fixes (From Session 28 Audit — Still Outstanding)

| Task | Priority |
|------|----------|
| Add cross-brain read rule for SJM/NT tasks (bootup reads trading_bot memory too) | MED |
| Write SJM summary to OPEN_BRAIN.md | MED |
| Create trading_bot/memory/sjm_results.md (categorical topic file) | MED |
| Add SJM pointer to connections.md | MED |

### Step 0 Bug Fixes Status (From Sessions 41-42)

| Bug | Status |
|-----|--------|
| validate_research.py cross-cwd bug | FIXED session 42 |
| validate_research.py citation quality (URL check) | FIXED session 42 |
| Citation logging | FIXED session 42 |
| auto_reviewer_trigger.sh exit 0 → exit 2 | FIXED session 42 |
| CodeRabbit CLI install OR replace with alternative | OPEN — CodeRabbit uninstalled; 3rd auditor slot TBD |
| PostCompact hook wired | WIRED session 41, UNTESTED |

---

## Section 5: The Original Install Order Plan vs What Actually Happened

### Install Order from repos_to_evaluate.md (Sage's research, 2026-03-28)

**Planned sequence:**
1. Fix Step 0 bugs first (research gate cross-cwd, archive rules, auto_reviewer exit code)
2. Build harness as plugin (loadable skills)
3. Install plugins: dev-process-toolkit, deep-plan, autoresearch, Ralph, ecc-agentshield
4. Load ML repos as needed for NT work (DO NOT INSTALL YET)

### What Actually Happened

| Step | Planned | Actual | Gap |
|------|---------|--------|-----|
| Step 0 bugs | Fix first | Fixed in session 42 (cross-cwd, URL quality, citation log, exit 2) | DONE — mostly |
| CodeRabbit | Install or confirm | Discovered it was never installed; removed | OPEN — 3rd auditor slot empty |
| Archived rules | — | 22 rules moved to _archive_inactive/ (session 42) | DONE |
| Build harness as plugin | Step 2 | SageX scaffold reviewed (session 43); build NOT started | PENDING |
| dev-process-toolkit | Step 3 | INSTALLED session 42 | DONE |
| deep-plan | Step 3 | INSTALLED session 42 | DONE |
| autoresearch | Step 3 | INSTALLED session 42 | DONE |
| Ralph | Step 3 | CLONED to ~/.ralph session 42; NOT deployed | PARTIAL |
| ecc-agentshield | Step 3 | INSTALLED session 42; baseline scan done (Grade D) | DONE |
| ML repos (OPRO, ReEvo, OpenEvolve) | Step 4 — do NOT install yet | NOT installed | CORRECT (held) |
| GEPA, CodeEvolve, LA-MCTS, MOTiFS | Research-phase repos | NOT installed | CORRECT (held) |

### ML Repos Status (All on Hold Per Sage)

| Repo | URL | Fit | Install Status |
|------|-----|-----|----------------|
| OPRO | github.com/google-deepmind/opro | START HERE — wire to BacktestEngine.reset() | NOT installed |
| ReEvo | github.com/ai4co/reevo | After OPRO plateaus | NOT installed |
| OpenEvolve | github.com/codelion/openevolve | LATER — after SJM live | NOT installed |
| GEPA | github.com/gepa-ai/gepa | Meta-layer optimizer | NOT installed |
| CodeEvolve | github.com/inter-co/science-codeevolve | Island-based GA | NOT installed |
| LA-MCTS | research code (no single repo) | Most powerful meta-solver | NOT installed |
| MOTiFS | research code | MCTS for feature selection | NOT installed |

### Plugin Fork Decision (Session 43)

| Repo | Action | Reason |
|------|--------|--------|
| superpowers | Adapt skills pattern (don't fork) | Conceptual borrowing for SageX skills structure |
| dev-process-toolkit | Link/use as-is | Already installed; study structure |
| autoresearch | Link/use as-is | Already installed; study loop design |
| hookify | Adapt (copy patterns) | Rule-from-conversation pattern for sagex rule management |
| deep-plan | Link/use as-is | Already installed |

---

## Section 6: Key File Paths (All Significant Paths Across Sessions 38–44)

### OpenBrainLM Core

| Purpose | Path |
|---------|------|
| Project root | `<WORKSPACE>/OpenBrainLM/` |
| Session activity log | `<WORKSPACE>/OpenBrainLM/memory/short_term.md` |
| Verified findings | `<WORKSPACE>/OpenBrainLM/memory/long_term.md` |
| Persistent task list | `<WORKSPACE>/OpenBrainLM/memory/todos.md` |
| Cross-refs / what works | `<WORKSPACE>/OpenBrainLM/memory/connections.md` |
| Progress event log | `<WORKSPACE>/OpenBrainLM/progress.txt` |
| Session 38 handoff | `<WORKSPACE>/OpenBrainLM/memory/handoff_session38_pipeline_audit.md` |
| Session 39 handoff | `<WORKSPACE>/OpenBrainLM/memory/handoff_session39_github_cleanup.md` |
| Session 40 handoff | `<WORKSPACE>/OpenBrainLM/memory/handoff_session40_option_a_pivot.md` |
| Session 41 handoff | `<WORKSPACE>/OpenBrainLM/memory/handoff_session41_option_a_brainstorm.md` |
| Session 42 handoff | `<WORKSPACE>/OpenBrainLM/memory/handoff_session42_guardrails_fix.md` |
| Session 43 handoff | `<WORKSPACE>/OpenBrainLM/handoffs/2026-03-29-session43-sagex-design.md` |
| Session 38 pipeline audit design spec | `<WORKSPACE>/OpenBrainLM/docs/superpowers/specs/2026-03-27-session38-pipeline-audit-design.md` |
| Session 38 track 1+2 plan | `<WORKSPACE>/OpenBrainLM/docs/superpowers/plans/2026-03-27-session38-track1-track2.md` |
| Option A LLM indicator pipeline design spec | `<WORKSPACE>/OpenBrainLM/docs/superpowers/specs/2026-03-28-option-a-llm-indicator-pipeline-design.md` |
| Phase 3 epic backlog | `<WORKSPACE>/OpenBrainLM/docs/backlog/epic_phase3_readiness.md` |
| Native git hook template | `<WORKSPACE>/OpenBrainLM/docs/templates/pre-commit` |
| Git hook installer | `<WORKSPACE>/OpenBrainLM/scripts/setup_git_hooks.sh` |
| Repos to evaluate | `<WORKSPACE>/OpenBrainLM/memory/repos_to_evaluate.md` |
| NLM brain tracking | `<WORKSPACE>/OpenBrainLM/memory/notebooklm_brain.md` |

### Research Files

| Purpose | Path |
|---------|------|
| SJM + indicator deep review (800+ lines) | `<WORKSPACE>/OpenBrainLM/research/sjm_indicator_review_2026-03-27.md` |
| AST execution guard research | `<WORKSPACE>/OpenBrainLM/research/ast_execution_guard_research.md` |
| SJM parameter extraction verification | `<WORKSPACE>/OpenBrainLM/research/sjm_parameter_extraction_verification.md` |
| Plugin review 2026-03-30 | `<WORKSPACE>/OpenBrainLM/research/plugin_review_2026-03-30.md` |
| This inventory | `<WORKSPACE>/OpenBrainLM/research/session38_44_full_inventory.md` |

### Hooks (Global)

| Purpose | Path |
|---------|------|
| Brainstem inject | `~/.claude/hooks/brainstem_inject.sh` |
| Research gate v2 | `~/.claude/hooks/validate_research.py` |
| Destructive command guard | `~/.claude/hooks/destructive_command_guard.py` |
| Audit gate check | `~/.claude/hooks/audit_gate_check.sh` |
| Auto reviewer trigger | `~/.claude/hooks/auto_reviewer_trigger.sh` |
| Agent result capture | `~/.claude/hooks/agent_result_capture.sh` |
| Precompact save | `~/.claude/hooks/precompact_save.sh` |
| Propagation check | `~/.claude/hooks/propagation_check.sh` |
| Session savepoint inject | `~/.claude/hooks/session_savepoint_inject.sh` |

### Hooks (OB Project)

| Purpose | Path |
|---------|------|
| Audit reminder (Layer 1 nudge) | `<WORKSPACE>/OpenBrainLM/.claude/hooks/audit_reminder.sh` |
| Write audit receipt | `<WORKSPACE>/OpenBrainLM/.claude/hooks/write_audit_receipt.sh` |
| Audit read blocker | `<WORKSPACE>/OpenBrainLM/.claude/hooks/audit_read_blocker.sh` |
| Audit gate check (project copy) | `<WORKSPACE>/OpenBrainLM/.claude/hooks/audit_gate_check.sh` |
| Opus write guard | `<WORKSPACE>/OpenBrainLM/.claude/hooks/opus_write_guard.sh` |
| Pre-commit git hook | `<WORKSPACE>/OpenBrainLM/.git/hooks/pre-commit` |
| Audit receipt (runtime artifact) | `<WORKSPACE>/OpenBrainLM/.audit_receipt.json` |
| Audit state (runtime artifact) | `<WORKSPACE>/OpenBrainLM/.claude/active_audit_state.md` |
| Research citations log | `<WORKSPACE>/OpenBrainLM/.claude/research_citations.log` (TSV, append-only) |

### NautilusTrader

| Purpose | Path |
|---------|------|
| NT project root | `<WORKSPACE>/nautilus_trader/` |
| 43-finding pipeline audit reference | `<WORKSPACE>/nautilus_trader/docs/pipeline_audit_43_findings.md` |
| Custom Semgrep safety rules (5 rules) | `<WORKSPACE>/nautilus_trader/.semgrep/nt_safety.yml` |
| MLflow model registry | `<WORKSPACE>/nautilus_trader/mlruns/` |
| Model loader (ONLY MLflow bridge) | `<WORKSPACE>/nautilus_trader/strategies/model_loader.py` |
| NT research gate evidence | `<WORKSPACE>/nautilus_trader/research.md` |
| NT memory short term | `<WORKSPACE>/nautilus_trader/memory/short_term.md` |
| NT pre-commit hook | `<WORKSPACE>/nautilus_trader/.git/hooks/pre-commit` |
| NT audit receipt | `<WORKSPACE>/nautilus_trader/.audit_receipt.json` |
| Ralph config | `<WORKSPACE>/nautilus_trader/PROMPT.md` |

### SJM Artifacts (<TRADING_PROJECT> — DO NOT TOUCH production)

| Purpose | Path |
|---------|------|
| Contaminated production pipeline | `<WORKSPACE>/<TRADING_PROJECT>/sandbox/shadow_b_bot_pipeline/pre_phase3_shadow_b/shadow_b_lockdown_2025/run_shadow_b_multimonth_train.py` |
| Clean OOS script (reference) | `<WORKSPACE>/<TRADING_PROJECT>/sandbox/02_SJM_clean_api/sjm_oos_june_clean_2026-03-20.py` |
| Clean gated sim script (reference) | `<WORKSPACE>/<TRADING_PROJECT>/sandbox/02_SJM_clean_api/sjm_gated_sim_june_2026-03-20.py` |
| Sandbox directory (DO NOT touch originals) | `<WORKSPACE>/<TRADING_PROJECT>/sandbox/` |

### Global Identity

| Purpose | Path |
|---------|------|
| Global identity / rules | `~/.claude/CLAUDE.md` |
| Rules directory | `~/.claude/rules/` |
| Archived/inactive rules | `~/.claude/rules_archive_inactive/` |
| Open brain cross-project | `~/.claude/OPEN_BRAIN.md` (or `<WORKSPACE>/OpenBrainLM/OPEN_BRAIN.md`) |
| Approved sources config | `~/.claude/approved_sources.json` (or sagex/config/ when SageX built) |
| Brainstem | `~/.claude/brainstem.md` |
| Agent zero-context reviewer | `~/.claude/agents/zero_context_reviewer.md` |
| Write permit (runtime) | `<WORKSPACE>/OpenBrainLM/.claude/write_permit.json` |
| SageX scaffold (tarball) | `~/Downloads/sagex-plugin-scaffold.tar.gz` |
| Ralph install | `~/.ralph/` |

### GitHub Repos

| Repo | URL | Status |
|------|-----|--------|
| OpenBrainLM | https://github.com/Architect/OpenBrainLM | PRIVATE. Last push: eadfc2a (session 42). |
| nautilus-trader | https://github.com/Architect/nautilus-trader | PRIVATE. Last push: d0c0063 (session 40). |
| [redacted-sandbox] | https://github.com/Architect/[redacted-sandbox] | PRIVATE. Last push: 8fb9191 (session 39). Needs cleanup. |

---

## Critical Findings Summary (For Quick Reference)

### SJM Contamination (VERIFIED — do not re-verify)
- Production pipeline `run_shadow_b_multimonth_train.py` line 165: `_predict_states()` calls `model.predict()` (look-ahead) on ALL windows including OOS eval. CONTAMINATED.
- 4 contaminated OOS predict() sites total across 19 reviewed scripts.
- Clean scripts exist: sjm_oos_june_clean + sjm_gated_sim_june use correct pattern.
- Locked June model requires 7 features (Pattern B: obv_raw + obv_osc as 7th column append). Clean-API produces 6. DIMENSION MISMATCH unless Pattern B used.
- Sage decision (session 38): Option B — use 7-feature Pattern B to match locked model.

### SageX Architecture (Session 43 Decision)
- SageX = enforcement layer (hooks, rules, skills, agents, gates, commands) at `~/.claude/plugins/sagex/`
- OpenBrain = memory layer at `<WORKSPACE>/OpenBrainLM/`
- Two-session architecture: OB session + NT session; shared ~/.claude/ + sagex config; separate project memory.
- Neither works without the other by design.

### Current 3-Auditor Status
- ZCR: WORKING (tested session 42)
- Semgrep: WORKING (0 findings on all hooks)
- CodeRabbit: UNINSTALLED — was fake Sonnet fallback; 3rd slot OPEN

### Sage Carry-Forward Directives (Active As of Session 43)
- OpenBrainLM is umbrella overseer for ALL projects
- NT = `<WORKSPACE>/nautilus_trader/` ONLY — DO NOT use <TRADING_PROJECT>
- <TRADING_PROJECT> is OLD — DO NOT TOUCH
- Only open source with 1K+ GitHub stars
- Step-by-step with Sage at every piece — no autonomous deployment
- Plugin fork on hold — Sage researching Hermes agent and open resources
- Agents are defined and locked — only change in edit mode
- All 24 notebooks: ZERO ACCESS until Sage re-assigns
- Approved sources: arXiv + github.com only until Sage adds more via /sagex:approve-source

---

*End of inventory. Generated 2026-03-29 by research agent from sessions 38–44 source files.*
