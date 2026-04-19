---
name: research-gate
description: |
  Use when writing or editing .py files. Enforces approved-source research before code writes.
  Trigger: any .py file creation or modification.
  This skill reads config/approved_sources.json and validates that research.md contains
  URLs from approved domains that actually resolve. Blocks writes without valid research.
---

# Research Gate

## What it enforces

Before ANY .py file can be written or edited:
1. A `research.md` file must exist at the target project root
2. It must be fresh (modified within the configured window)
3. It must contain URLs from domains listed in `config/approved_sources.json` for the active project
4. URLs must actually resolve (not just domain-match — the link must be real)
5. Citations are logged to `.claude/research_citations.log` (append-only TSV)

## Approved sources

Sources are defined per-project in `config/approved_sources.json`. The agent NEVER modifies this file. Only Sage adds entries via `/sagex:approve-source` or `/sagex:edit-mode`.

Default approved domains: `arxiv.org`, `github.com`

Project-specific domains inherit from global + project-level entries.

## What happens on failure

- **No research.md**: BLOCK. Agent must research first.
- **Stale research.md**: BLOCK. Agent must refresh research.
- **No approved URLs**: BLOCK. Agent must find approved sources.
- **URLs from unapproved domains**: BLOCK. Denial message lists approved domains.
- **URL doesn't resolve**: BLOCK. Agent must verify the link works.

## Integration

This skill describes the behavior. The mechanical enforcement is in `hooks/validate_research.py` which fires as a PreToolUse hook on Write/Edit events. The skill exists so agents understand WHY they're being blocked and what to do about it.
