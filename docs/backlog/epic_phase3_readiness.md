# EPIC: Phase 3 NautilusTrader Readiness & Architecture Seal

## 1. CONTEXT
We are entering Phase 3, integrating the massive NautilusTrader (NT) framework. To prevent context pollution, hallucinated APIs, and parallel execution collisions, we must seal the development architecture. We require four specific structural locks to be implemented before feature development begins.

## 2. SPECIFICATIONS TO EXECUTE

### Component 1: The Context Boundary (`.claudeignore`)
If an agent roams the entire NT codebase, its context window will fill with noise.
**Task:** Create a `.claudeignore` file at the root of the repository.
**Logic:** Explicitly ignore all heavy/irrelevant directories (e.g., `tests/`, `docs/`, `venv/`, large datasets). Ensure that only the specific NautilusTrader stub files (e.g., `nautilus_trader/model/enums.py`, `nautilus_trader/persistence/wranglers.py`) and the active `strategy/` directory remain visible to the agent's file-reading tools.

### Component 2: Parallelization Sandbox (`scripts/spawn_worktree.sh`)
We will run parallel agents to test different Markov Chain combinations simultaneously. If they run in the same directory, they will overwrite each other's files and trigger lockouts.
**Task:** Create an executable bash script `scripts/spawn_worktree.sh`.
**Logic:**
1. The script should accept a branch name as an argument (e.g., `./spawn_worktree.sh strategy-velocity`).
2. It must execute `git worktree add ../<branch-name> <branch-name>`.
3. It must copy the `.claude/` configuration folder (including our `PreToolUse` hooks and `claude.md`) into the new isolated worktree.
4. It must output a success message directing the user to `cd` into the new isolated directory before dispatching the agent.

### Component 3: Indicator Hub "Read-Only" Lock
The 70+ indicators in `indicator_hub.py` are audited truth. They must not be optimized or altered.
**Task:** Create a system-level file-permission script `scripts/lock_core_math.sh`.
**Logic:**
1. The script must execute `chmod 444 strategy/indicator_hub.py` (making it strictly read-only for the user and agent).
2. Update the `.claude/settings.json` (or `vtcode.toml`) `PreToolUse` hook to globally deny the `Write` and `Edit` tools if the target file matches `indicator_hub.py`, returning exit code 2 and a hard DENY message.

### Component 3b: Indicator Hub Lock — NT Project Location
Note: `indicator_hub.py` lives in the NautilusTrader project at `<WORKSPACE>\nautilus_trader\`. The lock script and PreToolUse hook must target that project's settings, not OpenBrainLM.

### Component 4: Continuous Integration (CI) Eval Gate
A pre-commit hook stops un-audited code, but we must prove the code actually runs before the audit receipt is even generated.
**Task:** Create a headless execution script `scripts/run_atomic_backtest.sh` and attach it to the audit loop.
**Logic:**
1. Create a dummy Parquet dataset generator (if one doesn't exist) to feed the engine.
2. The script must initialize the core NT engine with the active strategy and exit with `0` on success, or `1` if a traceback occurs.
3. **Integration:** Update the instructions for the 3-agent Zero-Context Auditor (created in previous phases) to strictly require `scripts/run_atomic_backtest.sh` to pass with exit code `0` *before* the `.audit_receipt.json` can be generated.

## 3. STRICT CONSTRAINTS
* Do not modify the existing Git `pre-commit` hook; the Eval Gate must be positioned *before* the audit receipt is generated, not during the git commit itself.
* Make all newly generated bash scripts executable (`chmod +x`).
