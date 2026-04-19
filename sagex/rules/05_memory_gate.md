---
name: memory-gate
description: "Only the orchestrator writes to memory/long_term.md. Sandbox and sub-agents write to handoffs/ only."
---

# Rule 05 — Memory Write Gate

## The Rule

Only the orchestrator (Opus/main session) promotes findings to `memory/long_term.md`.

### Who can write where

| Actor | short_term.md | long_term.md | handoffs/ | research/ |
|---|---|---|---|---|
| Opus (orchestrator) | YES | YES | YES | YES |
| Sonnet (sub-agent) | NO | NO | YES | YES |
| Gemini AG (sandbox) | NO | NO | YES | YES |
| Any sandbox agent | NO | NO | YES | YES |

### The promotion path

```
Sub-agent/sandbox → writes to handoffs/
Orchestrator reads handoffs/ → verifies → promotes to memory/
```

### Why

Memory is the persistence layer that survives context compression. Unverified writes to long_term.md corrupt the brain. The orchestrator immune-challenges every finding before promotion (Trinity Consolidation).

### Sandbox rule

Sandbox code NEVER imports from or writes to `memory/long_term.md` directly. Outputs go to `handoffs/` only. The orchestrator reads, verifies, and promotes.
