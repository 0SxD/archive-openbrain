# OpenBrain Plugin Briefing: Current State, Tools, and Build Plan

**Date:** 2026-03-28
**Author:** Creator (SageX Research) via Claude Opus 4.6 research session
**Purpose:** Hand this to Claude Code Opus to set up and test plugins off-the-shelf, then plan the OpenBrain fork/plugin layer.

---

## 1. CURRENT STATE: What Creator Has

### Trading System (NautilusTrader)
- **Location:** `<WORKSPACE>\<TRADING_PROJECT>`
- **Stack:** NautilusTrader (BTCUSDT perpetual futures, Binance), Python
- **Model:** Sparse Jump Model (SJM) regime detection strategy
- **Tracking:** MLflow model registry (all experiment tracking, model versioning, nested runs)
- **Pipeline:** Multi-script versioned pipeline (v1-v5+) for ingesting Binance aggTrades data, running backtests, integrating jumpmodels-based regime classifier
- **Key Decision:** SJM model loading through MLflow rather than direct pickle (avoids environment coupling failures)
- **Status:** Just completed 43-finding codebase audit. Preparing to go live.

### Agent Infrastructure
- **Claude Code:** Max 5x subscription, active daily use
- **Superpowers plugin:** Already installed and in active use
- **Agent coordination:** Blackboard/agent_sync pattern between Claude Code sessions and other agents (Gemini/"Open Brain")
- **Remote access:** Tailscale/tmux stack for remote Claude Code sessions
- **RAG:** Pinecone MCP for private book collection and NautilusTrader source code (Windows: requires `cmd /c` wrapper for npx)
- **GitHub:** `Architect/OpenBrainLM` under pseudonym "SageX Research" (no real name in tracked files)

### Existing Hooks (verify on Creator's machine)
Creator reports having "good hooks" already. Before adding anything, Claude Code should run:
```bash
cat ~/.claude/settings.json  # Check existing hook configuration
ls ~/.claude/hooks/ 2>/dev/null  # Check for hook files
ls .claude/hooks/ 2>/dev/null   # Check project-level hooks
```

### MLflow Integration Requirement
**CRITICAL:** Any tooling must plug into the existing MLflow tracking infrastructure. All experiments, model versions, and metrics already flow through MLflow. Do NOT introduce competing tracking systems. Any autoresearch/optimization loop must log to MLflow nested runs.

---

## 2. LLM-GUIDED OPTIMIZATION REPOS (for indicator selection pipeline)

Creator's pipeline needs LLMs during training for indicator selection over 101 Boolean modules. Here are the repos, ordered by complexity (simplest first):

### Tier 1: OPRO (Start Here -- ~60 lines, $0.50/run)
- **Repo:** `google-deepmind/opro` -- https://github.com/google-deepmind/opro
- **What it is:** Optimization by PROmpting. LLM generates new candidate solutions, evaluates them, feeds scores back into prompt for next iteration. Dead simple loop.
- **API support:** OpenAI and PaLM natively. Anthropic via `prompt_utils.py` modification (swap API call). Also works with any OpenAI-compatible endpoint.
- **MLflow integration:** NOT built in. You wrap the optimization loop yourself. Each OPRO step = one MLflow nested run logging the candidate solution + Sharpe/metric score.
- **Fit for Creator:** Ideal first step. Write a Python function that takes a subset of Boolean indicators, runs NautilusTrader `BacktestEngine.reset()` loop, returns Sharpe ratio. OPRO proposes subsets, you evaluate, log to MLflow.
- **Paper:** "Large Language Models as Optimizers" (ICLR 2024)

### Tier 2: ReEvo ($2-5/run, NeurIPS 2024)
- **Repo:** `ai4co/reevo` -- https://github.com/ai4co/reevo
- **What it is:** Reflective Evolution. Genetic algorithm where individuals are CODE SNIPPETS (heuristics), not direct solutions. LLM generates mutations + "verbal gradients" (text reflections on why a combination worked/failed). Evolutionary search + LLM reflection.
- **API support:** OpenAI (default), plus LiteLLM for Claude/Gemini/Llama/GLM/Qwen. Config-driven: `llm_client=openai` or `llm_client=litellm`.
- **MLflow integration:** NOT built in. Uses Hydra for config, outputs to `./outputs/main/`. You'd wrap the evaluation function to log to MLflow.
- **Fit for Creator:** Use when OPRO plateaus. ReEvo evolves the INDICATOR SELECTION HEURISTIC itself (the Python function that decides which indicators to combine), not just the indicator subsets. More powerful but more expensive. Can use Claude via Anthropic API or Gemini on GCP.
- **Key distinction from OPRO:** OPRO optimizes parameters/selections. ReEvo evolves the optimization ALGORITHM itself.
- **Paper:** "Large Language Models as Hyper-Heuristics with Reflective Evolution" (NeurIPS 2024)

### Tier 3: OpenEvolve (Full AlphaEvolve reimplementation)
- **Repo (primary, most stars):** `codelion/openevolve` -- https://github.com/codelion/openevolve (also mirrored at algorithmicsuperintelligence/openevolve)
- **Repo (codebase-scale):** `ryanrudes/openevolve` -- https://github.com/ryanrudes/openevolve (MIT license, evolves entire codebases not just single functions)
- **What it is:** Full evolutionary coding agent. Prompt Sampler + LLM Ensemble + Evaluator Pool + Program Database (MAP-Elites with island-based evolution). Async pipeline, checkpoint/resume, artifact side-channel for build errors.
- **API support:** Gemini (default), configurable for any LLM. Uses LLM ensemble (primary + secondary models).
- **MLflow integration:** NOT built in. Has its own checkpoint system. You'd need to write a custom evaluator that logs to MLflow, or post-process checkpoints into MLflow.
- **Fit for Creator:** This is the "later" tool. Use after SJM is live and you want to evolve the entire trading strategy codebase. Overkill for indicator selection alone, but perfect for evolving your Python evaluation function + indicator logic end-to-end.

### Also Consider: GEPA (Genetic-Pareto, newest)
- **Repo:** `gepa-ai/gepa` -- https://github.com/gepa-ai/gepa
- **What it is:** Optimizes ANY text parameter (prompts, code, configs) using LLM reflection + Pareto-efficient evolutionary search. Integrates with DSPy. CEO of Shopify called it "severely under-hyped."
- **Fit for Creator:** Could optimize the system prompts you use for Claude-guided indicator selection. Meta-optimization layer.

### Also Consider: CodeEvolve (open-source, beats AlphaEvolve on some benchmarks)
- **Repo:** `inter-co/science-codeevolve` -- referenced in arxiv paper
- **What it is:** Island-based GA + weighted LLM ensemble. Open-source, claims to surpass AlphaEvolve on several mathematical benchmarks.

---

## 3. CLAUDE CODE PLUGINS TO INSTALL AND TEST OFF-THE-SHELF

Install these FIRST. Test them as-is before forking or modifying anything.

### 3A. Already Using
```bash
# Superpowers -- already installed, keep it
/plugin update superpowers  # make sure it's current
```

### 3B. Code Enforcement / Gates
```bash
# dev-process-toolkit -- deterministic gate checks, bounded TDD
/plugin marketplace add nesquikm/dev-process-toolkit
/plugin install dev-process-toolkit@nesquikm-dev-process-toolkit
/dev-process-toolkit:setup  # reads your project, generates gate commands

# Test: run /dev-process-toolkit:gate-check on your NT repo
# This alone -- making the agent run tests as a non-negotiable phase -- is the biggest win
```

### 3C. Deep Planning + Research
```bash
# deep-plan -- Research > Interview > External LLM Review > TDD Plan > Sections
/plugin marketplace add piercelamb/deep-plan
/plugin install deep-plan

# Requires API keys for external review:
# export OPENAI_API_KEY="..." (for GPT review)
# export GEMINI_API_KEY="..." (for Gemini review)
# If no keys, uses Opus subagent instead

# Test: /deep-plan @planning/sjm-live-spec.md
```

### 3D. Autoresearch Loop
```bash
# autoresearch -- Karpathy-inspired autonomous iteration loop
/plugin marketplace add uditgoenka/autoresearch
/plugin install autoresearch@uditgoenka-autoresearch

# Test: /autoresearch:plan Goal: Improve test coverage on NT backtester
# This will walk you through defining Scope, Metric, Verify
```

### 3E. Agent Orchestration (pick ONE to start)
```bash
# Ralph for Claude Code -- cleanest autonomous loop implementation
# Install manually (clone to project):
git clone https://github.com/frankbria/ralph-claude-code.git ~/.claude/skills/ralph

# OR for full orchestration:
# workflow-orchestration (barkain) -- parallel execution + delegation
/plugin marketplace add barkain/claude-code-workflow-orchestration
/plugin install workflow-orchestrator@barkain-plugins
```

### 3F. Security + Enforcement (optional but recommended)
```bash
# Everything Claude Code -- security scanner, hook profiles
# Quick scan (no install needed):
npx ecc-agentshield scan
npx ecc-agentshield scan --fix  # auto-fix safe issues
```

---

## 4. THE OPENBRAIN PLUGIN: WHAT TO BUILD

After testing the above off-the-shelf, the OpenBrain plugin wraps Creator's enforcement philosophy around the existing ecosystem.

### Architecture: Fork Superpowers + Layer Gates

```
openbrain-plugin/
  .claude-plugin/
    plugin.json          # Standard Anthropic plugin manifest
    marketplace.json     # For distribution
  hooks/
    hooks.json           # Hook configuration
    pre-tool-use.sh      # Deterministic gate enforcement (from claude-ctrl pattern)
    post-tool-use.sh     # MLflow logging gate
    session-start.sh     # Inject NT project context + agent_sync state
    stop.sh              # Session summary + blackboard update
  skills/
    gate-check/
      SKILL.md           # Deterministic compiler/linter/test gate (from dev-process-toolkit)
    research-loop/
      SKILL.md           # Auto-research with MLflow logging (from autoresearch pattern)
    writing-gate/
      SKILL.md           # Writing/editing enforcement (no em dashes, source verification)
    mlflow-check/
      SKILL.md           # Verify MLflow experiment state before/after operations
    nt-context/
      SKILL.md           # NautilusTrader-specific context injection
    indicator-search/
      SKILL.md           # LLM-guided indicator selection (OPRO/ReEvo wrapper)
  agents/
    code-reviewer.md     # Strict code review subagent
    test-writer.md       # TDD enforcement subagent
    mlflow-auditor.md    # Checks MLflow experiment integrity
  commands/
    gate-check.md        # /openbrain:gate-check
    research.md          # /openbrain:research
    audit.md             # /openbrain:audit
  rules/
    no-em-dashes.md      # Creator's formatting rules
    verify-sources.md    # No inferential leaps, source verification
    mlflow-required.md   # All experiments must log to MLflow
    no-pickle.md         # SJM loads through MLflow, never direct pickle
    strict-versioning.md # Originals never modified
    bounded-review.md    # Max 2 self-review rounds, then escalate
```

### Key Rules to Encode as PreToolUse Hooks

These fire EVERY time, regardless of what the model remembers:

1. **No direct pickle loading** -- block any `pickle.load`, `joblib.load` without MLflow wrapper
2. **No modifying originals** -- block writes to v1/v2/v3 original pipeline scripts
3. **MLflow logging required** -- any `BacktestEngine` run must have active MLflow run context
4. **No em dashes** -- in any output (writing, code comments, docs)
5. **Bounded self-review** -- max 2 rounds, then stop and escalate
6. **Gate check before commit** -- run typecheck + lint + test, non-zero exit = blocked
7. **No force push to main** -- block `git push --force` on main/master
8. **Source verification** -- any factual claim in writing must have verifiable source

### MLflow Integration Points

The plugin MUST check for and interact with MLflow at these points:
- **SessionStart hook:** Detect active MLflow tracking URI, inject into context
- **Before any backtest:** Verify `mlflow.active_run()` exists
- **After indicator selection:** Log selected subset as MLflow params
- **After SJM training:** Verify model registered in MLflow model registry
- **Research loop:** Each iteration = one MLflow nested run with metrics

---

## 5. NAMING CLARIFICATIONS

For Creator's reference when updating GitHub docs:

- **OPRO** = Optimization by PROmpting (Google DeepMind, ICLR 2024). Simple prompt-based optimizer.
- **ReEvo** = Reflective Evolution (ai4co, NeurIPS 2024). NOT "Rev-Evo" or "Tre Evo." Evolves heuristic CODE via genetic algorithm + LLM verbal gradients.
- **OpenEvolve** = Open-source AlphaEvolve reimplementation. Multiple repos exist; `codelion/openevolve` is the most complete.
- **GEPA** = Genetic-Pareto optimization framework. Newest entry, integrates with DSPy.
- **CodeEvolve** = Another open-source AlphaEvolve implementation from Inter (Brazilian fintech). Claims to beat AlphaEvolve on some math benchmarks.
- **LA-MCTS** = Latent Action Monte Carlo Tree Search. The "other MCTS" Creator mentioned. Uses K-means + SVM to partition search space.
- **MOTiFS / R-MOTiFS** = Classic MCTS wrapper for feature selection. Binary include/exclude tree.

---

## 6. DEPLOYMENT ROADMAP

### Phase 1: Test Off-the-Shelf (This Week)
1. Update Superpowers
2. Install dev-process-toolkit, run `/dev-process-toolkit:setup` on NT repo
3. Install deep-plan, test with a simple spec
4. Install autoresearch, test `/autoresearch:plan` on a small goal
5. Run `npx ecc-agentshield scan` to audit current config
6. Document what works, what conflicts, what's missing

### Phase 2: Build OpenBrain Plugin (Next)
1. Fork Superpowers as base
2. Add rules/ directory with Creator's enforcement rules
3. Add hooks/ with PreToolUse gates (start with no-pickle + MLflow-required)
4. Add skills/ for gate-check and mlflow-check
5. Test on NT repo with real backtest workflow
6. Iterate based on what breaks

### Phase 3: LLM Indicator Selection (Parallel)
1. Implement OPRO wrapper with NautilusTrader BacktestEngine evaluator
2. Log all OPRO iterations to MLflow nested runs
3. Run mRMR pre-screening over 101 Booleans (Creator can do this now)
4. Feed mRMR output to OPRO for combinatorial optimization
5. When OPRO plateaus, switch to ReEvo for heuristic evolution
6. OpenEvolve reserved for full-codebase evolution after SJM is live

### Phase 4: Orchestration (After Phase 1-2 Stable)
1. Set up Ralph for overnight autonomous runs
2. Add workflow-orchestration for parallel agent execution
3. Integrate agent-orchestrator for CI/CD reactive agents
4. Connect all to blackboard/agent_sync pattern

---

## 7. QUICK REFERENCE: ALL REPOS

| Category | Repo | URL | Stars | License |
|----------|------|-----|-------|---------|
| **Plugin Base** | Superpowers | github.com/obra/superpowers | 120K | MIT |
| **Gates** | dev-process-toolkit | github.com/nesquikm/dev-process-toolkit | ~new | MIT |
| **Gates** | claude-ctrl | github.com/juanandresgs/claude-ctrl | ~new | -- |
| **Gates** | Everything Claude Code | github.com/affaan-m/everything-claude-code | 100K | MIT |
| **Gates** | claude-code-skills | github.com/levnikolaevich/claude-code-skills | -- | -- |
| **Planning** | deep-plan | github.com/piercelamb/deep-plan | ~new | MIT |
| **Research** | autoresearch | github.com/uditgoenka/autoresearch | ~new | MIT |
| **Research** | ARIS | github.com/wanshuiyin/Auto-claude-code-research-in-sleep | -- | MIT |
| **Orchestration** | workflow-orchestration | github.com/barkain/claude-code-workflow-orchestration | -- | -- |
| **Orchestration** | agent-orchestrator | github.com/ComposioHQ/agent-orchestrator | -- | MIT |
| **Orchestration** | ralph-claude-code | github.com/frankbria/ralph-claude-code | -- | MIT |
| **LLM Optim** | OPRO | github.com/google-deepmind/opro | 4K+ | Apache 2.0 |
| **LLM Optim** | ReEvo | github.com/ai4co/reevo | 2K+ | MIT |
| **LLM Optim** | OpenEvolve | github.com/codelion/openevolve | 10K+ | MIT |
| **LLM Optim** | GEPA | github.com/gepa-ai/gepa | ~new | MIT |
| **Sprint** | gstack | github.com/garrytan/gstack | 45.7K | MIT |
