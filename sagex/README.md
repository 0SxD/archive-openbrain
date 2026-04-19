# SageX

**Deterministic agent governance for Claude Code.**

Research gates. Audit loops. Approved-source enforcement. Coder/auditor cycling with zero-context review. Structural enforcement that the agent literally cannot bypass.

## What makes SageX different

Most Claude Code plugins offer *suggestions*. SageX enforces *gates*.

- **Research gate** — No code writes without approved-source research. URLs are verified, domains are whitelisted per-project, citations are logged.
- **Audit loop** — Every code change passes a 3-agent triad: zero-context reviewer (reads code cold), static analyzer (Semgrep), and orchestrator (cross-references both). All three must PASS.
- **Build loop** — Coder → Auditor → Retry, max 3 rounds. If the coder can't satisfy the auditors, the orchestrator breaks the deadlock.
- **Approved sources** — Per-project whitelists of domains, URLs, and NotebookLM notebooks. The agent reads the list. Only you modify it.
- **Edit mode** — Rules are locked by default. Explicit unlock/lock cycle for modifications, with full change logging.

## Install

```bash
/plugin marketplace add Architect/sagex
/plugin install sagex
```

## Commands

| Command | What it does |
|---------|-------------|
| `/sagex:build-loop <task>` | Coder → audit → retry loop (max 3 rounds) |
| `/sagex:edit-mode` | Unlock governance for rule/source modification |
| `/sagex:lock` | Re-engage governance after edits |
| `/sagex:approve-source <type> <value> for <project>` | Add approved domain/URL/notebook |

## Philosophy

> "Instructions guide. Hooks enforce." — The agent is a probabilistic system. Under context pressure, after compaction, after 40 minutes of deep implementation, text rules aren't constraints — they're suggestions. The only way to reliably govern an LLM is through deterministic, event-based enforcement that fires every time, regardless of what the model remembers.

## Structure

```
sagex/
  .claude-plugin/
    plugin.json              # Plugin manifest
    marketplace.json         # Distribution config
  skills/
    audit-loop/SKILL.md      # 3-agent audit triad
    research-gate/SKILL.md   # Approved-source enforcement
    brain-harness/SKILL.md   # Memory + context management
    coding-harness/SKILL.md  # Code write rules
    build-loop/SKILL.md      # Coder/auditor retry cycle
    edit-mode/SKILL.md       # Governance unlock/lock
  hooks/
    validate_research.py     # PreToolUse: blocks writes without research
    destructive_command_guard.py  # PreToolUse: blocks rm, reset --hard
    audit_gate_check.sh      # PreToolUse: blocks commit without audit
    brainstem_inject.sh      # PreToolUse: injects context on tool use
  agents/
    zero-context-reviewer.md # ZCR: reads code cold, no project context
  commands/
    build-loop.md            # /sagex:build-loop
    edit-mode.md             # /sagex:edit-mode
    lock.md                  # /sagex:lock
    approve-source.md        # /sagex:approve-source
  config/
    approved_sources.json    # Per-project source whitelists (user-controlled)
    notebook_assignments.json  # Per-project NotebookLM access (user-controlled)
  rules/
    (enforcement rules loaded by hooks)
```

## Requirements

- Claude Code v2.1.0+
- Semgrep (for static analysis in audit loop): `pip install semgrep`

## License

MIT. Free forever. Go build something governed.

---

*Built by [SageX Research](https://github.com/Architect). The brain harness for people who don't trust the brain.*
