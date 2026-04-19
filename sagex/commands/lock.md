---
description: "Exit edit mode. Re-engage all governance gates. Verify config integrity."
---

## /sagex:lock

Re-engages governance after `/sagex:edit-mode`.

### Protocol:
1. Verify all config files are valid JSON (approved_sources.json, notebook_assignments.json)
2. Verify no rules files were deleted (only modified or added)
3. Log the lock event to `.claude/edit_mode_log.md`
4. Confirm: "Governance locked. [N] rules, [M] hooks, [K] approved sources active."
