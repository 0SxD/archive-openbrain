# Corridor Validation — P0 Hooks + Harness
> Source: Agents_Arcs (1a7bcc9d), harsh audit
> Date: 2026-03-24
> Session IDs: Q1=5dafb49a, Q2=fdc5a38e (new session — Q2 topic drift noted below)

---

## Q1: P0 Hooks Critique

**Query:** We are implementing 4 P0 hooks for our agent harness: (1) a PreToolUse bash hook that pattern-matches destructive commands like rm -rf and blocks them, (2) a Stop/PreCompact hook that dumps task state to markdown before context compaction, (3) a PostToolUse hook on the Agent tool that captures subagent results to a result_inbox directory, (4) moving a propagation-check from a hookify rule to settings.json. Assume these are poorly designed. What's wrong with them? What failure modes are we missing? What would you recommend differently?

**Raw Response:**

1. The PreToolUse Bash Hook (Pattern-Matching Destructive Commands)
What's Wrong & Missing Failure Modes: Relying on simple string or regex pattern-matching (like scanning for rm -rf) provides false security, known as "security theater". AI agents optimizing for task completion behave like a "water finding the fastest path down" and will autonomously invent novel paths to bypass obstacles. If an agent wants to clear a directory, it will simply bypass your regex by using Python's shutil.rmtree, writing a secondary shell script, or employing alternate flags (like rm -r -f).
Recommendation: Replace pattern-matching with structural sandboxing and least-privilege access. Do not trust the agent's intent; execute its actions in isolated cloud containers or restricted environments where it physically lacks the permissions to destroy production data. For local high-stakes execution, enforce a hard "ask before edits" permission mode or a secure approval gate that requires human authorization before execution.

2. The Stop/PreCompact Hook (Dumping Task State to Markdown)
What's Wrong & Missing Failure Modes: Dumping workflow state into an unstructured Markdown file before context compaction is a fatal architectural trap. As the file grows, it inevitably turns into a "graveyard of rules" where context bloat causes the agent to lose the plot. Furthermore, unstructured text lacks durable status flags, making it incredibly difficult for a restarted or compacted agent to accurately parse what is actually finished versus what is merely proposed.
Recommendation: Use a structured JSON task queue instead. Production systems externalize state into a structured JSON feature list because LLMs are significantly less likely to corrupt structured data formats. Your hook should update specific task flags (e.g., pending, in progress, completed) inside a manifest.json file in place, ensuring that post-compaction agents can deterministically read the exact project state.

3. The PostToolUse Subagent Hook (Capturing Results to a Shared result_inbox)
What's Wrong & Missing Failure Modes: Forcing multiple parallel subagents to write their outputs into a shared result_inbox directory violates the core rule of multi-agent scaling: no shared state. This architecture will create catastrophic "serial dependencies," where parallel agents fight over file locks, creating massive coordination bottlenecks that destroy efficiency. Studies show multi-agent efficiency drops by a factor of 2 to 6 in tool-heavy environments when agents are forced to share state.
Recommendation: Implement Worktree Isolation and a Refinery Agent. Instead of a shared inbox, clone the repository into isolated Git worktrees (separate branches/folders) for each subagent so they can operate in total isolation without stepping on each other's toes. Then, use a dedicated "Refinery" or merge-queue agent whose sole, isolated job is to asynchronously evaluate those outputs, resolve code conflicts, and safely merge them into the main branch.

4. Moving the Propagation-Check to settings.json
What's Wrong & Missing Failure Modes: Moving verification logic into settings.json fundamentally misunderstands the purpose of the configuration file. In systems like Claude Code, .claude/settings.json is meant strictly as a hook registry and permission configuration. It cannot execute testing logic. If you attempt to stuff propagation or quality checks in there, you strip the system of its ability to run objective, external verification, reducing your quality gate to a static config flag.
Recommendation: Use settings.json to route to an external Test-Keeper Script. The settings.json file should only map the event trigger (e.g., "stop": "evaluate_scenarios.sh") to an external Bash or Python script. The external script must run an objective evaluation (like a linter, a unit test suite, or external holdout scenarios) acting as a hard quality gate, rejecting the completion and forcing the agent to iterate if the code does not legitimately pass.

---

## Q2: Harness Structure Critique

**Query:** We created a harness file structure: task_queue.json (pending/in_progress/complete), dispatch_log.jsonl (append-only), result_inbox/ directory, and audit_trail.jsonl. This is modeled on Anthropic's feature_list.json pattern. Assume this is bad. What are the failure modes? What's missing? How would you harden it?

**Note:** The first attempt (session 5dafb49a) timed out mid-session. A fresh session was opened and the question was reframed with more specificity. The notebook answered on hook patterns (PreToolUse/PostToolUse/Stop/background agent architecture) rather than directly critiquing the file structure schema. The response still contains useful hardening signals — extracted below. The direct file-structure race-condition critique was not returned; this is a known gap.

**Raw Response (session fdc5a38e — reframed query):**

Zero-Trust Behavioral Monitoring: Hook (PreToolUse) This pattern is best implemented as a lightweight, synchronous hook rather than a background agent. Zero-trust architecture relies on establishing hard security boundaries and escalation triggers exactly at the moment an agent approaches a critical decision. Implementation: You wire this into a pre-tool use hook that fires immediately before the AI is allowed to write a file, execute a bash command, or delete data. Function: The hook acts as a bouncer, intercepting the tool payload to evaluate it against strict permission policies or scan it for destructive commands (like rm -rf) before the action can execute.

Observability and Traceability: Hook (PostToolUse) Observability should be handled by automated hooks to keep the agent's actual context window clean. The sources explicitly warn against using the agent's prompt as an "observability sink" for debug logs and tool outputs, as this bloats the context and causes the agent to drown in noise. Implementation: You wire this into a post-tool use hook that fires immediately after a tool executes. Function: This script silently catches the exact tool inputs, execution results, and confidence scores, and writes them directly to a local audit log or observability platform. This guarantees a perfect paper trail without burning the agent's active tokens.

Automated Rubric Passes & Quality Gates: Hook (Stop or conditional PreToolUse) Rubric passes and verification checks are highly effective as event-driven hooks that act as pre-delivery quality gates. Implementation: You can implement this as a stop hook that fires when the agent finishes its turn, or as a conditional pre-tool use hook that intercepts a specific "publish" or "commit" command. Function: Before the session is allowed to end or the work is allowed to ship, the hook script automatically checks the output against your rubric. For example, a "test-keeper" stop hook can automatically scan edited files to ensure unit tests exist and pass. Another hook might score content for banned words or character limits before allowing a curl command to post to an API. If the rubric fails, the hook rejects the completion and forces the agent to rewrite.

Auto-Policing: Dedicated Background Agent Unlike the previous three patterns, auto-policing cannot be handled by a lightweight, instantaneous hook because it requires continuous, asynchronous scanning and reasoning across massive amounts of data. Implementation: This pattern requires a dedicated background agent running on a scheduled loop (e.g., the OpenAI Codex architecture). Function: Because AI-generated code naturally introduces entropy and "AI slop" that degrades over time, you encode your "golden principles" into the repository and dispatch a background agent to continuously scan the codebase. When the background agent detects code that drifts from your architectural rules, it autonomously authors and opens a targeted refactoring Pull Request to fix the deviation. This allows the system to police its own entropy without blocking the active, real-time work of other agents or humans.

---

## Action Items

Extracted from Q1 and Q2 responses:

### Hook Redesigns (P0)

1. **PreToolUse — kill regex pattern-matching.** String/regex matching on `rm -rf` is security theater. Agents will bypass via `shutil.rmtree`, alternate flags, or secondary scripts. Replace with: OS-level permission sandboxing + a hard human-approval gate for any filesystem destructive action. Pattern-match is acceptable only as a fast-fail first layer — NOT as the only layer.

2. **Stop/PreCompact hook — kill markdown state dump.** Unstructured markdown grows into a "graveyard of rules" that causes context bloat and post-compaction agents cannot reliably parse done vs. proposed. Replace with: atomic JSON flag updates to a `manifest.json` / `task_queue.json` with deterministic status fields. The hook writes structured fields, not prose.

3. **PostToolUse result_inbox — kill shared directory.** Shared inbox = shared state = serial dependencies = 2–6x efficiency drop under parallel agents. Replace with: isolated Git worktrees per subagent for full isolation. Add a dedicated Refinery/merge-queue agent whose only job is async evaluation and conflict-safe merge into main. The result_inbox pattern is only safe for single-agent sequential runs.

4. **settings.json propagation-check — correct the mental model.** `settings.json` is a hook registry + permission config. It cannot execute logic. Verification logic belongs in an external script that settings.json routes to. The external script is the quality gate — it runs tests, rejects completion on failure, and forces re-iteration. settings.json maps `"stop"` → `"evaluate_scenarios.sh"`, nothing more.

### Harness Structure Gaps (Q2 — partial, notebook drifted)

5. **audit_trail.jsonl** — PostToolUse hook must capture: tool inputs, execution results, AND confidence scores. Missing confidence scores is a gap in the current design.

6. **Background drift-policing** — the harness has no background agent scanning for architectural drift. Add a scheduled background agent that encodes golden principles and opens PRs when codebase diverges. This is separate from all hook logic — hooks are synchronous, drift-policing is async/scheduled.

7. **Q2 gap to re-query:** The notebook did not directly answer race conditions, partial write risks, and corruption modes for `task_queue.json`. This needs a follow-up query in a fresh session with direct framing: "What are the race conditions and corruption risks when multiple agents mutate a shared task_queue.json without file locking?"
