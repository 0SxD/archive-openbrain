# TASK: Migrate Audit Gate to Native Git Pre-Commit Hook

## 1. CONTEXT
Currently, our 3-part zero-context audit (Zero-Context Reviewer + Semgrep + CodeRabbit) is enforced via a Claude `PreToolUse` hook (`audit_gate_check.sh`). While this stops standard `git commit` commands, it relies on fragile bash string regex matching, leaving us vulnerable to subshell or alias bypasses by autonomous agents. We need an immutable, system-level lock before initiating the heavy Phase 3 NautilusTrader development.

## 2. INTENT ENGINEERING
**The Objective:** Transfer the commit-blocking logic into Git's native execution pipeline so that it is mathematically impossible to commit unaudited code, regardless of the terminal syntax used by the agent or human.
**Success Looks Like:** A `git commit` command is cleanly rejected by Git itself with a clear `stderr` message if `.audit_receipt.json` is missing OR if any `.py` or `.sh` file is newer than the receipt.
**Failure Looks Like:** The hook blocks commits incorrectly (false positives), fails to check subdirectories, or relies on the old `PreToolUse` hook for validation.

## 3. SPECIFICATION
Execute the following steps:
1. **Create the Hook:** Create a new file at `.git/hooks/pre-commit`.
2. **Write the Validation Logic:** Implement a bash script that performs the following checks:
   - If `.audit_receipt.json` does not exist at the repository root, output a `DENY` message to `stderr` and `exit 1`.
   - Find the most recently modified source file (`*.py`, `*.sh`), explicitly ignoring the `.git/` and `.claude/` directories.
   - Compare the UNIX timestamp of the latest source file against `.audit_receipt.json`. If the source code is newer, output a `DENY: Code modified since last audit` message to `stderr` and `exit 1`.
   - If all checks pass, `exit 0`.
3. **Set Permissions:** Ensure the file is executable (`chmod +x .git/hooks/pre-commit`).
4. **Clean Up:** Remove the legacy `audit_gate_check.sh` logic from the `PreToolUse` configuration, as it is now redundant.

## 4. STRICT CONSTRAINTS & BOUNDARIES
* **DO NOT** track `.git/hooks/pre-commit` in standard version control (Git does not track the `.git/hooks` folder by default). Instead, create a setup script (e.g., `scripts/setup_git_hooks.sh`) that copies the hook from a tracked `docs/templates/` folder into `.git/hooks/` during environment initialization.
* **DO NOT** block commits if the only modified files are markdown (`.md`), JSON configuration, or memory files. The timestamp comparison must strictly target executable code (`.py`, `.sh`).
