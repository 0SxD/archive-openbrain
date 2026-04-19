## Zero-Trust Agent Architecture — Deterministic Enforcement

This workspace uses structural hooks to enforce behavior, not text-based pleas.
The following constraints are MECHANICAL — they cannot be rationalized past.

### PreToolUse: Research Gate (validate_research.py)
- **What it does:** Intercepts every Write|Edit call on .py files
- **What it checks:** Whether research evidence exists (research.md or research/*.md, >50 chars, <1 hour old)
- **If missing:** Returns exit code 2 — hard block. The file WILL NOT be written.
- **To unblock:** Spawn a read-only Scout agent, retrieve official documentation, save to research.md, retry
- **Exempt:** memory files, .claude/ config, .md docs, research output, agent_sync/

### PostToolUse: Zero-Context Reviewer (zero_context_reviewer.md)
- **What it is:** An isolated sub-agent spawned with zero prior context and read-only permissions
- **When to use:** After any significant code write — spawn it with ONLY the raw file, no reasoning
- **Why:** When an agent writes code, its context window is biased by its own decisions. A blank-slate reviewer catches errors the author is blind to.
- **Its output:** Structured PASS/FAIL/CONDITIONAL report with specific issues
- **Your obligation:** Address all Critical Issues before marking the task complete

### Episodic Operation (Context Washing)
- **The problem:** Agents running continuously fill their context with failed attempts, compounding noise until original instructions are compressed out
- **The fix:** When blocked multiple times on the same issue, DO NOT loop. Log progress to memory/short_term.md, log the exact error, and STOP. A fresh session resumes from the save point with a clean context window.
- **Save points:** progress goes to memory/short_term.md, decisions to memory/long_term.md, cross-refs to memory/connections.md
- **Boot-up ritual:** Every session reads these files first — the external state IS the memory, not the conversation history

### What This Replaces
The old system used probabilistic text rules ("NEVER answer from your own reasoning alone")
injected via brainstem.md. Agents ignore text rules when optimizing for task completion —
they rationalize past them. This architecture makes unauthorized behavior mechanically
impossible rather than merely discouraged.

Source: Open Agent Passport (OAP) specification, Orchestral AI framework,
disler/claude-code-hooks-multi-agent-observability, jayminwest/overstory.
