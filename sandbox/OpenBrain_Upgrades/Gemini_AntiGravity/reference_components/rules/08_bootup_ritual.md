## Bootup Ritual — Read Before Acting (from Agents_Arcs, 156 sources)

Every session start, the ORCHESTRATOR (Opus) reads the propagation manifest and memory.
Sub-agents (Sonnet/Haiku) do NOT read the full manifest — they get minimum viable context only.

### The Rule (Orchestrator — session start)
1. **Read `<WORKSPACE>\.claude\propagation_manifest.md`** — know all project brain paths, hook locations, rule registries
2. **Read the relevant project brain's `short_term.md`** — know what happened last session
3. **Read `long_term.md` and `connections.md`** if they exist in the project brain
4. **Read `AGENT_RULES.md`** if it exists in the project root (execution rules, constraints)
5. **Ask: "What's the context today?"** — What are we working on? Has anything changed? Record the answer as the session header in `short_term.md`. This is the session's north star.
6. **Only then proceed** with the user's request

### For Sub-agents (Progressive Disclosure — minimum viable context)
When dispatching via Agent tool:
- Give the sub-agent ONLY the specific file paths it needs for its task
- Tell it WHERE to write results (exact path)
- Do NOT inject the full manifest, full rules, or full memory into sub-agent prompts
- Sub-agents stay deliberately ignorant of the big picture — that's by design

### Why (Source: Agents_Arcs notebook 1a7bcc9d, Gemini 2.5 grounded on 156 sources)
- Industry converged on: ephemeral workers + version-controlled standing orders file + mandatory bootup read
- Without bootup ritual: silent behavioral drift, contradictory outputs, decision cascades
- Galileo AI research: one stale agent poisoned 87% of downstream decisions within hours
- Anthropic ACE paper (arXiv:2510.04618): "prompts and memory must update via execution feedback across sessions"
- **WARNING (same source):** "The one big agents.md approach inevitably fails because when everything is marked as important really nothing is." Full manifest in sub-agents = context bloat, signal dilution, scope creep.
- Sub-agents perform best with "narrow scoped views" and are "deliberately kept ignorant of the big picture"

### Anti-Patterns
- NEVER dispatch a sub-agent without telling it where to read/write. Naked dispatch = stale rules = drift.
- NEVER inject the full manifest into a sub-agent prompt. That's orchestrator context, not worker context.
- NEVER give a sub-agent "the big picture." Give it ONE task + the specific files for that task.
