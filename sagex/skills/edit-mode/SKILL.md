---
name: edit-mode
description: |
  Governance unlock/lock cycle. Use /sagex:edit-mode to unlock rules, skills, hooks,
  approved sources for modification. Use /sagex:lock to re-engage. Only Sage can invoke.
---

# Edit Mode — Governance Unlock/Lock

## When to Use
Only when Sage explicitly requests to modify governance components (rules, skills, hooks, configs).

## Protocol
1. Sage invokes /sagex:edit-mode
2. Confirm: "Edit mode active. What do you want to change?"
3. Make ONLY the changes Sage specifies
4. Read back every change for confirmation
5. Sage invokes /sagex:lock to re-engage

## What unlocks
- config/approved_sources.json
- config/notebook_assignments.json
- rules/ directory
- skills/ directory
- hooks/ directory
- agents/ directory

## What stays locked
- The edit-mode command itself
- The lock command
- Hook enforcement (hooks still fire)

## Safety
- Edit mode does NOT disable hooks — it enables modification of files hooks READ
- All changes logged to .claude/edit_mode_log.md with timestamp
- If session ends without /sagex:lock, next session starts locked (fail-safe)
