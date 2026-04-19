# Agents_Arcs — Propagation + Hooks Audit
> Source: Agents_Arcs notebook (1a7bcc9d), sessions 017d36b9 + ac7402a9, 2026-03-24
> Query by: review-hooks Sonnet agent

## What's Strong
- Tiered scopes (global → workspace → project) correct
- Git-driven standing orders pattern = our propagation_manifest.md
- Bootup ritual (context injection at session start) is the standard
- Repository as institutional memory (Codex pattern) = our rules in Git

## 4 Missing Hooks
1. **Destructive action intercepts**: Pre-tool hooks to block rm -rf, force push, etc. before execution
2. **Objective verification gates**: Not just "did you save?" but "is what you saved TRUE?" — tie to external tests
3. **Escalation triggers**: When instructions are ambiguous or goals conflict — halt and ask human
4. **Concurrency control**: Merge queue or "refinery" agent for parallel writes to same files

## Manifest Warning — Progressive Disclosure
- NEVER inject full manifest into sub-agent context windows
- Full manifest = context bloat, signal dilution, "graveyard of rules"
- Sub-agents get MINIMUM VIABLE CONTEXT only — the specific path they need
- Manifest is orchestrator-layer (Opus reads it), not worker-layer (Sonnet doesn't)
- Evolution: semantic search or MCP to retrieve "just in time" context

## Action Items
- [ ] Create destructive action intercept hook (hookify bash event, pattern rm -rf etc.)
- [ ] Update Rule 08: bootup ritual is for ORCHESTRATOR only, not sub-agents
- [ ] Design escalation trigger hook (ambiguous instructions → halt + ask)
- [ ] Design verification gate (save → verify truth, not just existence)
- [ ] Sub-agents receive only: task description + specific file paths, NOT full manifest
