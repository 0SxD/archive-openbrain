---
name: sonnet-executes-only
description: "Sonnet agents write code. They do not apply reasoning skills, brainstorm, or make architecture decisions."
---

# Rule 02 — Sonnet Executes Only

## The Rule

Sonnet agents are dispatched to EXECUTE code tasks. They do not:

- Apply reasoning or brainstorming skills
- Make architecture decisions
- Choose between approaches
- Expand scope beyond the specification
- Read full CLAUDE.md or rules — they get minimum viable context only

## What Sonnet receives

1. Exact file paths to modify
2. The specification (what to change, why)
3. Constraints (what NOT to change)
4. If a fix iteration: the auditor findings verbatim
5. Verification command to self-check

## What Sonnet does NOT receive

- Full project memory
- Architecture context
- Other agents' outputs
- The "big picture"

## Enforcement

- Opus sets `model: sonnet` explicitly on every dispatch
- Opus writes the contract (Phase 1 of coding-harness)
- Sonnet returns results — Opus reviews audit output, not code directly
- If Sonnet starts reasoning about approach → the spec was underspecified. Fix the spec, don't let Sonnet decide.
