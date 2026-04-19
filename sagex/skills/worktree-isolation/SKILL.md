---
name: worktree-isolation
description: Create and manage git worktrees for parallel coding agent isolation. Invoke when two independent coding tasks need to run simultaneously (max 2).
---

# Worktree Isolation Pattern

## When to Use

- Two independent coding tasks can run in parallel (no shared files)
- Each task is self-contained (different feature branches)
- Max 2 worktrees active at any time (= max 2 concurrent agents)

## Step 1 — Create Worktree

Use the EnterWorktree tool or bash equivalent:

```bash
git worktree add _worktrees/{task-id} -b feature/{task-id}-{short-description}
```

Each worktree gets its own:
- Working directory: `_worktrees/{task-id}/`
- Feature branch: `feature/{task-id}-{short-description}`
- Complete copy of the codebase (shares .git objects, not files)

## Step 2 — Dispatch Agent to Worktree

In Agent tool call, direct the agent to work within the worktree path:
- Agent reads/writes ONLY within `_worktrees/{task-id}/`
- Agent has NO access to main working tree files
- Agent has NO knowledge of what the other worktree agent is doing

## Step 3 — Stage 1 Audit (before merge)

Each worktree's output goes through the full 5-gate audit pipeline:
1. Semgrep (plugin)
2. CodeRabbit (plugin)
3. Code-review + pr-review-toolkit (plugins)
4. Security-guidance (plugin)
5. Clone repo comparison (_repos/)

ALL gates must PASS before merge is allowed.

## Step 4 — Merge Back

After Stage 1 PASS + Creator approval:

```bash
# Return to main working tree
git checkout main

# Merge the feature branch (no fast-forward for audit trail)
git merge feature/{task-id}-{short-description} --no-ff

# Clean up
git worktree remove _worktrees/{task-id}
git branch -d feature/{task-id}-{short-description}
```

## Step 5 — Stage 2 (GitHub PR Airlock)

After merge to local main:
1. Push branch → open PR (Creator approval required)
2. GitHub Actions: remote semgrep + CodeRabbit
3. Creator reviews → merges

## Rules

- NEVER share files between worktrees
- NEVER run more than 2 worktrees simultaneously
- ALWAYS delete worktree after merge (no stale worktrees)
- ALWAYS run full audit before merge
- Worktree directory: `_worktrees/` (gitignored)

## Multi-Agent Worktree Usage

All coding agents use worktrees — not just Claude sub-agents:

| Agent | Worktree? | Branch pattern | Notes |
|---|---|---|---|
| Claude (Opus) | NO — stays on main | n/a | Orchestrator. Never leaves main working tree. |
| Claude (Sonnet) | YES | feature/{task-id}-claude-{desc} | Dispatched by Opus |
| Gemini (AntiGravity) | YES | feature/{task-id}-gemini-{desc} | Works in IDE on its own worktree |
| Codex | YES | feature/{task-id}-codex-{desc} | Works in IDE on its own worktree |

- Opus NEVER works in a worktree — it stays on main to orchestrate and review
- Each coding agent gets its own worktree and feature branch
- No two agents share a worktree
- All worktree output goes through Claude's 5-gate audit pipeline before merge

## Emergency Cleanup

```bash
git worktree list              # see all active worktrees
git worktree remove --force _worktrees/{task-id}  # force remove
git worktree prune             # clean up stale entries
```
