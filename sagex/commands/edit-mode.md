---
description: "Enter edit mode to modify rules, skills, hooks, and approved sources. Only Sage can invoke. Re-lock with /sagex:lock."
---

## /sagex:edit-mode

**SAGE-ONLY COMMAND.** Unlocks the governance layer for modification.

### What unlocks:
- `config/approved_sources.json` — add/remove domains, URLs, notebooks
- `config/notebook_assignments.json` — assign notebooks to projects
- `rules/` — modify enforcement rules
- `skills/` — modify skill definitions
- `hooks/` — modify hook behavior
- `agents/` — modify agent definitions

### What stays locked:
- The edit-mode command itself (cannot be modified while in edit mode)
- The lock command (always available)
- Hook enforcement (hooks still fire — you're editing the rules, not disabling the gates)

### Protocol:
1. Sage invokes `/sagex:edit-mode`
2. Agent confirms: "Edit mode active. What do you want to change?"
3. Agent makes ONLY the changes Sage specifies
4. Agent reads back every change for confirmation
5. Sage invokes `/sagex:lock` to re-engage

### Safety:
- Edit mode does NOT disable hooks — it enables modification of the files hooks read
- All changes are logged to `.claude/edit_mode_log.md` with timestamp and what changed
- If session ends without `/sagex:lock`, next session starts locked (fail-safe)
