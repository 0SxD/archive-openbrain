## Agent Architecture (from Agents_Arcs notebook 1a7bcc9d, 156 sources)

**ALWAYS check Agents_Arcs notebook (1a7bcc9d) before building or modifying agents.**

### Pattern
Initializer → amnesiac Workers → Judge. TWO TIERS only. Episodic runtimes.
run → capture → terminate → fresh agent next cycle. No continuous running.

### Context Engineering
Control what tokens each agent sees — not just the instruction.
Workers stay IGNORANT: minimum viable context, own context window, no big picture.
Contract-first prompting: define "done" criteria + must/must-not/preferences/escalation.

### Delegation (set model explicitly when dispatching — never inherit Opus by default)
Default to Sonnet for ALL work. Opus thinks, decides, and reviews — does not execute.
- Sonnet: research queries, file scanning, writing, summarizing, code generation, boilerplate, all execution
- Opus: reviews all Sonnet output, architecture decisions, audits, conversations with Creator. Does NOT run research queries — reviews research results.
Only use Haiku if the task is trivially simple (single grep, file listing).
Opus checks ALL subagent output before presenting to Creator.

### Verification Layer
Meta-auditor checks both Claude AND hostile twin until system is proven.
- auditor checks code/claims
- hostile-twin validates plans
- meta-auditor audits BOTH using all NotebookLMs to cross-reference
This layer cannot be relaxed until the system is proven and trusted. Once proven: meta-auditor can be retired, auditor + hostile-twin remain as spot-checks.

### GitHub Agents (two separate roles — do not combine)
- github-guardian (defensive): keeps repos organized, tracks versions, monitors dependencies, detects drift
- github-scout (offensive): finds repos, libraries, tools. Evaluates: open source? well-maintained? often used?

### Anti-patterns (never do these)
Flat teams (deadlocks) | deep hierarchies >2 (telephone game) | continuous running | context dumping | shared state
No shared state: orthogonal toolsets, resolve conflicts via external queues.
