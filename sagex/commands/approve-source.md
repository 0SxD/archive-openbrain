---
description: "Add an approved source (domain, URL, or notebook) to a project's allowed list. Sage-only."
---

## /sagex:approve-source

**SAGE-ONLY COMMAND.** Adds a source to the approved list for a specific project.

### Usage:
```
/sagex:approve-source domain arxiv.org for OpenBrainLM
/sagex:approve-source url https://github.com/nautechsystems/nautilus_trader for nautilus_trader
/sagex:approve-source notebook "NT Trading Signals" for nautilus_trader
```

### Protocol:
1. Parse the source type (domain/url/notebook), value, and target project
2. Read current `config/approved_sources.json`
3. Check for duplicates
4. Add the entry
5. Read back the full project source list for Sage confirmation
6. Write the updated file

### Rules:
- Only Sage can invoke this command
- Agent NEVER suggests sources to add — only Sage initiates
- If project doesn't exist in config, create the entry with the new source only
- Log the addition to `.claude/edit_mode_log.md`
