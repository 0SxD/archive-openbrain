# OpenBrain Plugin Briefing v2: Actual State + Gap-Fill Plan

**Date:** 2026-03-28
**For:** Claude Code Opus (the agent that will set up and test these plugins)
**From:** Austin (SageX Research) via Claude Opus 4.6 research session

---

## 1. WHAT AUSTIN ALREADY HAS (Do Not Duplicate)

### Mechanical Hooks (14 total -- these WORK and should NOT be replaced)

**Global PreToolUse (4 hooks):**
- `brainstem_inject.sh` -- injects progress.txt tail + state on Edit/Write/Agent/Bash/NotebookEdit
- `validate_research.py` -- blocks .py writes without fresh research.md (HAS 3 KNOWN BUGS: cross-cwd check uses os.getcwd() not target root; only checks text length >50 chars not actual URLs; no citation logging)
- `destructive_command_guard.py` -- blocks rm, reset --hard, file redirects on Bash
- `audit_gate_check.sh` -- blocks git commit without fresh audit receipt (just fixed path bug)

**Global PostToolUse (3 hooks):**
- `agent_result_capture.sh` -- captures agent results to file on Agent events
- `propagation_check.sh` -- checks if CLAUDE.md or rules changed on Edit/Write
- `auto_reviewer_trigger.sh` -- nudges about 3-agent audit on Edit/Write (EXIT 0 = ignorable)

**Global Session (3 hooks):**
- `session_savepoint_inject.sh` -- SessionStart: injects progress.txt + last session state
- `brainstem_inject.sh` -- SessionStart (compact): re-injects after compaction (UNTESTED)
- `precompact_save.sh` -- Stop: saves session state before exit

**Project PreToolUse (2 hooks -- OpenBrainLM-specific):**
- `opus_write_guard.sh` -- blocks Opus from writing code without write permit
- `audit_read_blocker.sh` -- blocks Opus reading code newer than audit receipt

**Project PostToolUse (1 hook):**
- `audit_reminder.sh` -- writes state file for audit tracking on Edit/Write/Bash

**Native Git Hook (1):**
- `.git/hooks/pre-commit` -- validates audit receipt covers all staged files

### Text Rules (16 total -- the ones hooks DON'T enforce)

14 global rules (00-12 + zero_trust_architecture.md) covering: public actions, agent system, build philosophy, memory discipline, integrity, research protocol, agent reporting, memory verification, bootup ritual, hostile audit tools, NotebookLM orchestrator-only, creator reference (PII), delegation protocol, zero trust architecture.

2 project rules: session context prompt, creator reference (duplicate of global 11).

17 archived rules still loading in _archive/ (wasting context tokens).

### 3 Named Auditors
- ZCR (Zero-Context Reviewer) -- custom agent, tested PASS
- Semgrep -- plugin semgrep@claude-plugins-official, tested PASS (0 findings)
- CodeRabbit -- plugin coderabbit@claude-plugins-official, NOT YET TESTED

### Known Gaps (from Austin's own audit)

| Gap | Severity | What Plugin Could Fix It |
|-----|----------|--------------------------|
| Research gate checks wrong cwd | HIGH | Fix the bug (not a plugin issue) |
| Research gate only checks length, not URLs | HIGH | Fix the bug OR add citation-quality hook |
| No citation logging (which research justified which code) | MEDIUM | autoresearch's log pattern |
| CodeRabbit diff comparison missing | MEDIUM | Test CodeRabbit plugin properly |
| Auto-reviewer is exit 0 (ignorable) | LOW | Change to exit 1 (make it a gate) |
| 17 archived rules bloating context | LOW | Delete or move out of rules/ |

### Trading System
- NautilusTrader BTCUSDT perpetual futures (Binance)
- SJM regime detection, MLflow model registry
- Location: `C:\apps_ai\trading_bot_build_2026`
- Pipeline: versioned v1-v5+, SJM loads via MLflow (never pickle)
- BacktestEngine.reset() loop for parameter sweeps
- 43-finding codebase audit complete, preparing to go live

### LLM Indicator Selection Pipeline (detailed doc attached)
- 101 Boolean indicator modules, need optimal 3-7 subset
- mRMR pre-screening to ~20 orthogonal features
- OPRO for fast combinatorial search (~60 lines, $0.50/run)
- ReEvo for heuristic evolution ($2-5/run, NeurIPS 2024)
- OpenEvolve for full codebase evolution (later)
- All must log to MLflow nested runs

---

## 2. WHAT THE PLUGINS ADD (Gap Analysis)

### Plugins That Fill Real Gaps

| Plugin | What It Adds That Austin DOESN'T Have | Conflicts? |
|--------|---------------------------------------|------------|
| **dev-process-toolkit** | Deterministic gate-check phase (compiler exit codes > agent judgment), bounded TDD (red/green/refactor enforced), max 2 self-review rounds then escalate, spec hierarchy (requirements > testing > technical > plan) | No conflict. His audit_gate_check.sh blocks commit without receipt, but dev-process-toolkit gates BEFORE commit at the build phase. Complementary. |
| **deep-plan** | Multi-LLM external review of plans (sends to Gemini/OpenAI for independent review), structured Research > Interview > External Review > TDD Plan > Section splitting | No conflict. Austin has no planning plugin. His research gate checks for research.md but doesn't structure the planning process itself. |
| **autoresearch** | Autonomous iteration loop with Goal/Scope/Metric/Verify framework, /autoresearch:plan wizard, scientific-method debugging, security auditor | Partially overlaps with his research protocol (rule 05) but adds mechanical iteration. His protocol is text-only. |
| **Ralph (frankbria)** | Overnight autonomous loop with intelligent exit detection, confidence scoring, PROMPT.md > specs/ > fix_plan.md hierarchy, circuit breaker patterns | No conflict. Austin has no autonomous loop. His agent system (rule 01) defines roles but not loop execution. |

### Plugins That Duplicate What He Has (Skip or Evaluate Carefully)

| Plugin | Why It Might Duplicate |
|--------|----------------------|
| **Everything Claude Code** | Its PreToolUse hooks (block --no-verify, detect secrets) overlap with his destructive_command_guard.py. Its hook profiles (minimal/standard/strict) are interesting but he already has 14 working hooks. Risk: conflicts. |
| **claude-ctrl** | Its 10 deterministic rules enforced by hooks overlap heavily with Austin's 14 hooks. The deep-research skill (multi-model synthesis) is the only unique piece. |
| **gstack /careful + /freeze** | His destructive_command_guard.py already blocks dangerous commands. His opus_write_guard.sh already restricts writes. gstack's versions are slightly different (directory-scoped freeze vs. permit-based) but core function overlaps. |

### Plugins for LLM Optimization (New Category -- No Overlap)

| Repo | What It Is | MLflow Integration | Fit |
|------|-----------|-------------------|-----|
| **OPRO** (google-deepmind/opro) | ~60 line optimization loop, describe task + show (solution, score) pairs, LLM proposes better | NOT built in. Wrap with mlflow.start_run(nested=True) per eval | START HERE. Wire to BacktestEngine.reset() loop. |
| **ReEvo** (ai4co/reevo) | Evolves heuristic CODE via GA + verbal gradients. NeurIPS 2024. | NOT built in. Wrap eval function. | After OPRO plateaus. Evolves the selection ALGORITHM, not just subsets. |
| **OpenEvolve** (codelion/openevolve) | Full AlphaEvolve: MAP-Elites + island evolution + LLM ensemble | NOT built in. Has own checkpoint system. | LATER. For evolving entire strategy code after SJM is live. |
| **GEPA** (gepa-ai/gepa) | Genetic-Pareto optimization for any text parameter. DSPy integration. | NOT built in. | Meta-layer: optimize prompts you use for OPRO/ReEvo. |

---

## 3. INSTALL AND TEST OFF-THE-SHELF (Do This First)

### Step 0: Fix Your Known Bugs First
Before adding plugins, fix the 3 research gate bugs and the archived rules bloat. These are your foundation.

```bash
# Ask your agent to:
# 1. Fix validate_research.py cross-cwd bug (use target project root, not os.getcwd())
# 2. Fix validate_research.py citation quality (check for URLs, not just length > 50)
# 3. Add citation logging (which research.md entry justified which .py write)
# 4. Move _archive/ rules out of the rules loading path
# 5. Test CodeRabbit plugin that's been sitting untested
# 6. Change auto_reviewer_trigger.sh from exit 0 to exit 1 (make it a real gate)
```

### Step 1: Install dev-process-toolkit (Gate-Check Phase)
```bash
/plugin marketplace add nesquikm/dev-process-toolkit
/plugin install dev-process-toolkit@nesquikm-dev-process-toolkit
/dev-process-toolkit:setup
```
**Test:** Run `/dev-process-toolkit:gate-check` on your NT repo. Does it find your test commands? Does it conflict with your existing audit_gate_check.sh? The gate-check runs compiler/linter/test commands and blocks on non-zero exit. Your audit gate blocks commit without receipt. They should be complementary (gate-check runs DURING development, audit gate runs AT commit time).

### Step 2: Install deep-plan (Planning Phase)
```bash
/plugin marketplace add piercelamb/deep-plan
/plugin install deep-plan
```
**Test:** Create a simple spec file like `planning/sjm-live-prep.md` with a few lines about going live with SJM. Run `/deep-plan @planning/sjm-live-prep.md`. Does the Research > Interview > Plan flow work? Does it conflict with your research protocol (rule 05)?

**API keys for external review (optional but recommended):**
```bash
export GEMINI_API_KEY="..."  # for Gemini review
# If no keys, uses Opus subagent instead
```

### Step 3: Install autoresearch (Autonomous Iteration)
```bash
/plugin marketplace add uditgoenka/autoresearch
/plugin install autoresearch@uditgoenka-autoresearch
```
**Test:** Run `/autoresearch:plan Goal: Improve test coverage on NT backtester`. This walks you through defining Scope, Metric, and Verify command. Small, safe test. Does it respect your existing hooks? Does brainstem_inject.sh fire correctly when autoresearch triggers edits?

### Step 4: Install Ralph (Overnight Loop) -- AFTER Steps 1-3 are stable
```bash
git clone https://github.com/frankbria/ralph-claude-code.git ~/.ralph
# Follow setup in .ralph/docs/
```
**Test:** Give it a tiny task (not your trading system). Verify the exit detection works, the loop doesn't run away, and your destructive_command_guard.py still fires inside the loop.

### Step 5: Run Security Scan
```bash
npx ecc-agentshield scan        # audit your current config
npx ecc-agentshield scan --fix  # auto-fix safe issues
```
This scans your CLAUDE.md, settings.json, MCP configs, hooks, agent definitions, and skills. Good baseline before adding more plugins.

---

## 4. WHAT TO ASK YOUR AGENT (Information I Need)

To finalize the OpenBrain plugin design, I need the agent to provide:

### A. Current settings.json structure
```bash
cat ~/.claude/settings.json | head -100
# I need to see the exact hook configuration format you're using
# to ensure new plugins don't conflict with existing hook entries
```

### B. The validate_research.py source
```bash
cat ~/.claude/hooks/validate_research.py
# I need to see the 3 bugs in context to recommend fixes
# and to see if the citation-quality fix can be a hook upgrade vs. new hook
```

### C. Your agent definitions
```bash
ls ~/.claude/agents/
cat ~/.claude/agents/zero_context_reviewer.md
# I need to see your ZCR agent format to ensure new plugin agents are compatible
```

### D. Your CLAUDE.md for the NT project
```bash
cat C:/apps_ai/trading_bot_build_2026/CLAUDE.md 2>/dev/null || echo "No CLAUDE.md"
# Need to know what project-level context exists for the trading system
```

### E. MLflow tracking URI and experiment names
```bash
# From within your NT project:
python -c "import mlflow; print(mlflow.get_tracking_uri())"
python -c "import mlflow; [print(e.name) for e in mlflow.search_experiments()]"
# Need to know the exact MLflow setup to write the mlflow-check skill
```

### F. Current Superpowers version and skills
```bash
/plugin list  # show all installed plugins
# I need to see what Superpowers skills are active
# to know what the fork base looks like
```

### G. The _archive/ rules (for cleanup)
```bash
ls ~/.claude/rules/_archive/
wc -l ~/.claude/rules/_archive/*.md | tail -1
# How many tokens are these burning?
```

---

## 5. LLM OPTIMIZATION REPOS: Correct Names and Links

For your GitHub docs and reference:

| Name | Full Name | Repo | Paper | What It Does |
|------|-----------|------|-------|-------------|
| **OPRO** | Optimization by PROmpting | github.com/google-deepmind/opro | ICLR 2024 | LLM proposes solutions, you evaluate, feed scores back. ~60 lines. |
| **ReEvo** | Reflective Evolution | github.com/ai4co/reevo | NeurIPS 2024 | Evolves heuristic CODE via GA + LLM "verbal gradients" (reflections). |
| **OpenEvolve** | Open-source AlphaEvolve | github.com/codelion/openevolve | Based on DeepMind 2025 | Full evolutionary coding agent. MAP-Elites + LLM ensemble. |
| **GEPA** | Genetic-Pareto | github.com/gepa-ai/gepa | -- | Optimizes any text parameter. DSPy integration. Pareto-efficient. |
| **CodeEvolve** | (inter-co) | github.com/inter-co/science-codeevolve | arXiv 2510.14150 | Island-based GA + weighted LLM ensemble. Claims to beat AlphaEvolve on some benchmarks. |
| **LA-MCTS** | Latent Action MCTS | (research code, not a single repo) | -- | K-means + SVM partition of search space. Most powerful meta-solver. |
| **MOTiFS** | MCTS for Feature Selection | (research code) | -- | Classic binary include/exclude tree for features. |

**NOT a thing:** "Tre Evo", "Rev-Evo" -- the correct name is **ReEvo** (one word, capital R capital E).

---

## 6. PLUGIN ARCHITECTURE: OpenBrain Fork (AFTER Off-the-Shelf Testing)

Only build this AFTER Steps 1-4 in Section 3 are tested and stable.

The fork adds Austin's enforcement layer ON TOP of Superpowers. It does not replace any existing hooks. It adds:

### New Skills (things no existing plugin provides)
```
skills/
  mlflow-check/SKILL.md      -- Verify MLflow experiment state before/after operations
  indicator-search/SKILL.md   -- OPRO/ReEvo wrapper with BacktestEngine.reset() evaluator
  nt-context/SKILL.md         -- NautilusTrader-specific context (versioning rules, SJM constraints)
  writing-gate/SKILL.md       -- No em dashes, source verification, no inferential leaps
```

### New Hooks (things existing hooks don't cover)
```
hooks/
  mlflow-required.sh          -- PreToolUse: block BacktestEngine runs without active MLflow context
  no-pickle-direct.sh         -- PreToolUse: block pickle.load/joblib.load without MLflow wrapper
  citation-quality.sh         -- PreToolUse: upgrade to validate_research.py with URL checking
```

### New Rules (things text rules don't enforce mechanically)
```
rules/
  no-em-dashes.md             -- Mechanical: hook checks output for em dashes
  strict-versioning.md        -- Mechanical: block writes to v1/v2/v3 originals
  bounded-review.md           -- Mechanical: max 2 self-review rounds, then escalate
```

---

## 7. DEPLOYMENT ORDER

1. **NOW:** Fix the 3 validate_research.py bugs + clean archived rules
2. **THIS WEEK:** Install and test dev-process-toolkit, deep-plan, autoresearch off-the-shelf
3. **NEXT WEEK:** Install and test Ralph for overnight loops on a non-trading task
4. **PARALLEL (with trading work):** Implement OPRO loop wired to BacktestEngine + MLflow
5. **AFTER TESTING:** Fork Superpowers, add OpenBrain enforcement layer
6. **AFTER SJM LIVE:** Graduate to ReEvo for heuristic evolution
7. **LATER:** OpenEvolve for full codebase evolution
