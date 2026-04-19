---
name: pii-scrub
description: "No real names in tracked files. Use 'Sage' or 'the creator' only. No model names in commits."
---

# Rule 03 — PII and Identity Scrub

## The Rule

All content that may be shared, tracked in git, or committed must use pseudonyms:

- Workspace owner → **"Sage"** or **"the creator"**
- AI models → **"SageX"** (not Claude, Opus, Sonnet, Gemini, etc.)
- No real names, no email addresses with real names
- No model version numbers in commit messages

## Where this applies

- Any file tracked by git (`git ls-files`)
- Files that may be staged for commit
- Research outputs
- Agent sync files
- Handoff documents
- GitHub PR descriptions, issues, comments

## Where real names are OK

- Private/gitignored files: `memory/`, `.claude/`
- Local-only config files
- Files explicitly excluded from git

## Commit format

```
Co-Authored-By: SageX
```

No email. No model name. No version.
