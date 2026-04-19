---
name: approved-sources-only
description: "Every code write must reference an approved source. The audit triad verifies this."
---

# Rule 01 — Approved Sources Only

## The Rule

Every `.py`, `.sh`, `.ts`, `.js` file write MUST be backed by a reference from an approved source listed in `config/approved_sources.json` for the active project.

## What counts as a valid reference

1. A URL from an approved domain that appears in `research.md` or `research/*.md`
2. The URL must actually resolve (not just domain-match)
3. The research file must be fresh (modified within the configured window)
4. The reference must be relevant to the code being written (not a generic link)

## What happens on violation

- `validate_research.py` fires as PreToolUse hook on Write/Edit
- Returns exit code 2 — hard block, file will NOT be written
- Agent must: research first, save to research.md with approved-domain URLs, retry

## Approved domains

Defined per-project in `config/approved_sources.json`. Sage controls this file.
Default: `arxiv.org`, `github.com`

## Audit verification

The zero-context reviewer checks that code follows documented patterns from the cited sources. If the code diverges from what the reference describes, the audit FAILS.
