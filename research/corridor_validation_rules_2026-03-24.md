# Corridor Validation — Rule Updates
> Source: Agents_Arcs (1a7bcc9d), harsh audit
> Date: 2026-03-24

## Q1: Rule Changes Critique

**Query:** Assume these changes are poorly implemented. What are the failure modes of: (1) a merge-queue pattern for consolidating agent outputs — race conditions, priority inversion, deadlocks? (2) AI-generated confidence scores gating memory promotion — does research show these scores are reliable or do they create false security? (3) escalation trigger systems in multi-agent pipelines — what happens when thresholds are miscalibrated too sensitive vs too deaf?

**Raw Response (session da1103b5 + 2409cb48):**

On the merge-queue / agent output consolidation pattern:

The research surfaces four distinct failure modes in production harnesses when agents write to shared coordination structures:

1. **Hook-based enforcement is the correct pattern, not queue-based**: The sources indicate that agent output consolidation is best handled by synchronous PreToolUse/PostToolUse hooks rather than a shared merge queue. A merge queue introduces concurrency problems by design — agents writing to a shared JSON task list can corrupt state if two workers claim the same "pending" task simultaneously. The recommended production fix is strict status flags (pending → in_progress → completed) with the worker atomically updating the flag before touching the task. Without atomic compare-and-swap semantics, race conditions are guaranteed.

2. **Interrupt storms from miscalibrated escalation**: Zero-trust hooks fire at every tool boundary. If the escalation sensitivity is too high, every benign write triggers a human interrupt, grinding throughput to zero. If too low (too deaf), destructive commands (e.g., `rm -rf`) slip through undetected. The sources give no explicit calibration formula — this is identified as a gap requiring empirical tuning per domain.

3. **Context bloat from observability misplacement**: A common failure mode is writing audit/observability output into the agent's active context window. This floods the token budget and causes the agent to "drown in noise." The correct pattern is PostToolUse hooks writing silently to an external audit log — never into the agent's prompt.

4. **Auto-policing background agent required for entropy**: Rule changes that rely on static rule files without a background enforcement agent will drift. The sources cite OpenAI Codex architecture: a background agent continuously scans the codebase against "golden principles" and opens targeted refactoring PRs when drift is detected. Without this, rule entropy accumulates silently.

On AI self-reported confidence scores (session 2409cb48):

**Raw Response:**

Research, specifically a paper published by OpenAI, confirms that relying naively on self-reported confidence scores creates a sense of false security. The research argues that common evaluation setups inherently reward confident answers over honest uncertainty. Because models are optimized to satisfy literal objectives — a phenomenon known as reward hacking — this pressure teaches them to guess confidently rather than admitting they don't know, which actively keeps hallucinations alive.

However, confidence scores can be made reliable for gating memory promotion if they are transformed from a subjective self-critique into a strict structural pattern known as a "bouncer" or "confidence filter". To prevent the "confidence illusion" and safely curate memory, production systems implement the following rules:

- **Explicitly Define "High Confidence"**: You cannot leave the concept of confidence ambiguous. You must get extremely specific with the model about exactly what conditions qualify as high confidence so it does not resolve ambiguities on its own.
- **Permit Honest Uncertainty**: The model must be explicitly given permission to say "I don't know" so it is not pressured to fabricate a fluent answer just to complete the prompt.
- **Enforce Strict Numerical Thresholds**: When an agent attempts to classify or store a piece of context, it must return a specific numerical confidence score (e.g., between 0 and 1) alongside the data.
- **Default to Graceful Failure**: If the AI's confidence score falls below your hard threshold (such as 0.6), the system must structurally block the information from being filed into the main memory database. Instead, the system should log the item in a pending inbox or review log and trigger a message asking the human for clarification.

By shifting the consequence of low confidence from "failing the task" to "safely holding for human review," this architecture prevents low-quality, confidently hallucinated outputs from polluting long-term memory storage.

---

## Q2: Research Scope Enforcement

**Query:** Our research loop now has this pattern: The operator assigns corridor → research in that corridor only → find gaps → follow up within corridor → verify claims against arXiv/GitHub → validate output against corridor before closing. We added depth limits and corridor defaults. But agents still searched ALL notebooks instead of staying in the assigned one. How do production multi-agent systems enforce research scope boundaries? What mechanisms prevent scope creep in autonomous research agents?

**Raw Response (session fb657ce0):**

Production multi-agent systems solve the exact "scope creep" you are experiencing by shifting away from behavioral instructions (like telling the agent "only research in this corridor") and moving toward strict, structural isolation.

When autonomous agents are given access to the "big picture" or broad tool sets, they naturally experience scope creep because they decide adjacent tasks need doing or they reinterpret their assignments based on the overarching goal. To enforce strict research boundaries, production architectures use the following mechanisms:

**1. Deliberate Ignorance and Minimum Viable Context**
The most common reason agents wander outside their assigned "corridor" is that the orchestrator gave them too much context. Production systems enforce boundaries through strict information hiding. Worker agents must remain completely ignorant of the broader project context, the overarching goal, and the existence of other notebooks or workers. An agent should be spawned with "minimum viable context" — receiving exactly enough information to complete its assigned corridor and absolutely nothing more. If the research agent does not know other notebooks exist, it will not attempt to search them.

**2. Zero-Context Subagent Spawning**
To ensure this ignorance, systems utilize a strict parent-child architecture where the orchestrator spins up the research agent in a completely fresh, isolated context window. The subagent is spawned with a blank slate, meaning its entire "world" consists solely of the specific prompt for that single research task. Because the subagent has no access to the parent agent's chat history or the broader project backlogs, it cannot drift into unassigned territories.

**3. Structural Tool Restriction (Least Privilege)**
If your agents are searching all notebooks, they likely have access to a global search tool (like a broad grep or glob function). Production systems physically prevent scope creep by restricting the specific tools a subagent receives. Rather than giving a research agent a general file-search tool and telling it to "stay in your corridor," you must enforce disallowed tools. You provision the agent with restricted tools that are physically hard-coded to only read or query the exact directory or specific APIs mapped to that corridor. By enforcing a "least privilege" tool stance, you make it structurally impossible for the agent to access outside notebooks.

**4. Total State Isolation**
Frameworks mandate that parallel agents operate in total isolation with absolutely no shared state. If multiple research agents share access to a global tool set or a shared workspace, they experience tool contention and their selection accuracy drops, leading them to execute broader, sloppier searches. To prevent this, limit your research agents to a small, isolated set of three to five core tools tailored exclusively to their specific corridor.

**Direct implication for this pipeline:** The operator should not just assign a corridor; The operator must spawn a fresh subagent that only knows about that corridor, provide it with restricted tools that can only query that corridor's specific notebooks, and completely blind the agent to the existence of the rest of the research project.

---

## Action Items

Extracted from both responses — ranked by severity:

### CRITICAL — Rule 05 (Research Corridor)
- [ ] **Behavioral corridor rules do not work.** Telling an agent "stay in your corridor" is insufficient. The fix is structural: spawn a fresh subagent with ONLY the notebook_id for that corridor injected. The agent must not receive the full notebook list. Current rule 05 does not enforce this — it only instructs. **Must be rewritten as a dispatch protocol, not a behavioral instruction.**
- [ ] **Tool restriction is missing from Rule 05.** The rule says "ASK before expanding" but does not restrict tools. Production enforcement requires the subagent to receive a restricted tool set — only the `ask_question` call with the specific `notebook_id` hardcoded. No `list_notebooks`, no `search_notebooks`. This is a structural gap.

### CRITICAL — Rule 03 (Memory Schema / Confidence Scoring)
- [ ] **Confidence scores are unreliable by default.** OpenAI research confirms reward hacking causes models to guess confidently rather than admit uncertainty. Our Rule 03 schema includes a `confidence` field but does not define: (a) explicit conditions for high vs low confidence, (b) explicit permission to output "I don't know", (c) what happens below threshold. The field exists but the enforcement contract is absent — this is the "confidence illusion."
- [ ] **Add graceful-failure path to Rule 03.** Items scoring below 0.6 must NOT be promoted. They must route to a pending inbox (quarantine in `short_term.md`) with a human-review flag. The rule currently says "Confidence Bouncer" but does not define the routing behavior on failure.

### HIGH — Rule 01 (Refinery / Merge Queue)
- [ ] **Merge queue atomicity is not specified.** Without atomic status flag transitions (pending → in_progress must be a compare-and-swap), two workers can claim the same task. Rule 01 needs to specify that workers update the status flag BEFORE touching the task, and that the flag update is the claim mechanism.
- [ ] **No background entropy agent.** The Refinery merge-queue handles per-session consolidation but the research shows rule drift accumulates over time without a background policing agent. This is a gap in the architecture — no equivalent of the OpenAI Codex background PR-bot exists in the current design.

### HIGH — Rule 09 (Escalation Triggers)
- [ ] **No calibration guidance.** The 6 escalation classes are defined but the research shows miscalibration is the primary failure mode: too sensitive → interrupt storms, too deaf → silent destructive failures. Rule 09 needs explicit threshold definitions per class, not just class names.
- [ ] **Escalation must be hook-based, not agent-based.** The research is unambiguous: escalation triggers belong in synchronous PreToolUse hooks, not background agents. If Rule 09 routes escalation through an agent, it will have latency and miss real-time destructive actions.

### MEDIUM — Rule 08 (Orchestrator Bootup / Progressive Disclosure)
- [ ] **Progressive disclosure is behavioral, not structural.** Rule 08 says sub-agents get "minimum viable context" but this relies on the orchestrator correctly scoping prompts. The research shows the fix must be structural: subagents spawned in isolated context windows with no access to orchestrator history. Rule 08 should specify that sub-agents are ALWAYS spawned fresh (no session reuse, no context inheritance).

### MEDIUM — Rule 10 (Prefix Caching Discipline) — not validated
- [ ] **No notebook coverage for prefix caching.** The Agents_Arcs notebook did not surface research on prefix caching discipline. This rule needs to be validated against a different source before implementation. Mark as UNVERIFIED until cross-referenced.

### LOW — Observability gap (missing rule)
- [ ] **No rule for observability placement.** The research explicitly warns that writing audit logs into the agent's context window is a failure mode (context bloat, token starvation). There is no current rule that mandates PostToolUse hooks write to external audit logs rather than into the agent's active context. Consider adding to Rule 09 or as a new Rule 11.
