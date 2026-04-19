# Escalation Trigger Patterns — Research
> Date: 2026-03-24
> Sources: arXiv:2307.01928, arXiv:2602.23005, arXiv:2602.17753, Agents_Arcs notebook (1a7bcc9d, 156 sources),
>          Anthropic "Building Effective Agents", LangGraph interrupt docs, CrewAI human-input docs
> Existing OpenBrainLM spec: `docs/specs/ALLOSTATIC_DECISION_GATE.md` (4-tier biological model — read this first)

---

## Critical Context: What OpenBrainLM Already Has

The `ALLOSTATIC_DECISION_GATE.md` covers escalation for **internal system health** (when a
pathway fails, when the brain self-repairs). That document is complete for that scope.

This research covers a DIFFERENT problem: **when the agent should halt task execution and
ask the human**, not when the brain self-heals. These are orthogonal mechanisms.

The existing hooks audit (`agents_arcs_hooks_audit_2026-03-24.md`) identified this as
**Missing Hook #3**: escalation when instructions are ambiguous or goals conflict.

---

## Industry Patterns Found

### Pattern 1: Constraint Architecture Taxonomy (Agents_Arcs notebook, 156 sources)

The foundational production taxonomy divides agent instructions into four categories:

```
MUSTS          — hard requirements (always do these)
MUST NOTS      — hard prohibitions (never do these)
PREFERENCES    — soft guidance (do these when possible)
ESCALATION TRIGGERS — the exact conditions that fire halt-and-ask
```

**Key mechanism:** When an assigned objective directly conflicts with a MUST NOT or
boundary constraint, the agent fires the explicit instruction:
> "If accomplishing the goal seems to require violating one of these constraints, just stop and ask."

This is hard-coded text in the agent's prompt — not a runtime confidence calculation.
The agent does not decide whether to escalate; the constraint architecture makes that
decision for it. This prevents "creative workaround" behavior where agents satisfy
task goals by silently bypassing safety boundaries.

**Source:** Agents_Arcs notebook 1a7bcc9d, session fc81746b. 156 sources grounded on
Anthropic, DeepMind, and production multi-agent deployments.

---

### Pattern 2: Three-Tier Uncertainty Routing (Agents_Arcs notebook, 156 sources)

Prevents "premature coherence" — where agents confidently fill ambiguous inputs with
guesses. Dictates how agents handle information based on volatility:

| Tier | Type | Action |
|------|------|--------|
| Tier 1 | Timeless information | Answer directly, no pause |
| Tier 2 | Slow-changing information | Answer, then offer to verify with human |
| Tier 3 | Live/volatile information | Halt, route immediately to search or human |

Additional threshold: "Calibrated uncertainty" — explicit system-level teaching of
*when no answer is acceptable* and escalation is mandatory. The agent provides no
answer rather than a low-confidence guess.

**Source:** Agents_Arcs notebook 1a7bcc9d, session fc81746b.

---

### Pattern 3: KNOWNO / Conformal Prediction Uncertainty Threshold
(arXiv:2307.01928, Ren et al., Princeton + Google DeepMind, 2023)

> "KnowNo builds on the theory of conformal prediction to provide **statistical guarantees**
> on task completion while **minimizing human help** in complex multi-step planning settings."

The key insight: rather than asking the human every time uncertainty exists, KNOWNO
**quantifies** uncertainty via conformal prediction and only escalates when the
uncertainty set (set of plausible next actions) is too large to resolve autonomously.

Two goals the framework balances:
1. Ensure task completion at a user-specified statistical success level
2. Minimize total number of help requests by narrowing down ambiguities first

**Implementation model for us:** Calibrate an uncertainty tolerance level ε. If the
agent's probability mass over correct actions falls below (1 − ε), escalate. Otherwise,
proceed with the highest-confidence action. This is the quantitative version of Tier 3 routing.

**Source:** arXiv:2307.01928 — https://arxiv.org/abs/2307.01928

---

### Pattern 4: PSUM Uncertainty Lifecycle — Six-State Model
(arXiv:2602.23005 — "Managing Uncertainty in LLM-based Multi-Agent System Operation")

Full taxonomy of uncertainty types that should trigger escalation:

**Epistemological Uncertainty (reducible):**
- Structural: dynamic orchestration choices
- Behavioral: non-deterministic execution
- Semantic: meaning correspondence gaps
- Inferential/Prediction: output doubt
- Calibration: confidence unreliability

**Ontological Uncertainty (irreducible):**
- Aleatory: inherent randomness in environment
- Interaction: conflicting outcomes from decentralized agents

**Uncertainty lifecycle states (in order):**
```
Detected → Characterized → Mitigated → {Resolved | Expired | ESCALATED}
```

**Escalation fires when:**
1. Uncertainty severity threshold exceeded — risk exceeds reliable automated handling
2. Persistent disagreement among expert agents — multiple unresolved conflicts
3. High-impact decisions — safety, legal, or ethical implications require human risk acceptance
4. Uncertainty stays in "Mitigated" state but associated risk remains HIGH

**Four human roles when escalated:** Interpretation (semantic), Judgment (inferential),
Risk Acceptance (high-impact), Governance (compliance validation).

**Critical finding from the 2026 AI Agent Index (arXiv:2602.17753):** Most production
agents (21/30 surveyed) lack documented default escalation behavior. Stop mechanisms
are documented in only 20/30 agents. The gap: oversight is *preventive* (approval gates
at design time) not *reactive* during execution. This is the exact gap we are closing.

**Source:** arXiv:2602.23005 — https://arxiv.org/html/2602.23005v1
**Source:** arXiv:2602.17753 — https://arxiv.org/html/2602.17753v1

---

### Pattern 5: Irreversible Action Detection (Anthropic + Agents_Arcs)

From Anthropic's "Building Effective Agents":
> "Pause for human feedback at checkpoints or when encountering blockers."

From Agents_Arcs (156 sources):
> "Before executing the high-stakes tool call, the agent must trigger a 'surfaced
> interpretation and a clarifying question' to the user... especially when a prompt
> has multiple plausible meanings."

**Concrete trigger conditions:**
- Action cannot be undone (file deletion, financial transaction, deployment, external API write)
- Action has multiple plausible interpretations ("delete the old ones" — which ones?)
- Action scope is larger than what was explicitly authorized
- Action requires credentials or permissions beyond what was granted

**Source:** Anthropic — https://www.anthropic.com/research/building-effective-agents
**Source:** Agents_Arcs notebook 1a7bcc9d, session fc81746b.

---

### Pattern 6: LangGraph interrupt() — Dynamic, Developer-Placed Halt Points
(LangGraph official docs, 2025)

LangGraph's production pattern: `interrupt()` is called **at the exact code location**
where human judgment is needed. No automatic detection — the developer encodes the
trigger condition directly in logic.

```python
from langgraph.types import interrupt

def risky_action_node(state):
    if state["action"].is_irreversible:          # explicit condition
        approved = interrupt("Approve this irreversible action?")
        if not approved:
            return {"aborted": True}
    # proceed
```

**Emerging adaptive pattern (2025):** High-confidence decisions proceed automatically;
uncertain ones wait. Hierarchical approval routing: low-risk → auto-approve, medium-risk
→ junior reviewer, high-risk → escalate to expert.

**Key characteristic:** No automatic thresholds — the interrupt condition is
**code**, not configuration. This is the correct pattern for our hookify system.

**Source:** https://docs.langchain.com/oss/python/langgraph/interrupts
**Source:** https://blog.langchain.com/making-it-easier-to-build-human-in-the-loop-agents-with-interrupt/

---

### Pattern 7: CrewAI human_input Flag
(CrewAI docs, 2025)

Simpler static pattern: `human_input=True` on a Task causes the agent to pause before
delivering final output. Triggers in two scenarios:
1. **Complex decision-making** — additional context or clarification needed
2. **Task completion** — validate output quality before delivering

**Limitation:** Binary flag (static on/off at design time), no dynamic evaluation.
Not suitable as the sole mechanism — but the task-level granularity is useful: each
task knows whether it is the kind of task that needs human sign-off.

**Source:** https://docs.crewai.com/en/learn/human-input-on-execution

---

## Synthesis: The Six Escalation Trigger Classes

Based on all sources, production escalation triggers fall into exactly six classes:

| Class | Trigger Condition | Detection Method | Response |
|-------|------------------|------------------|----------|
| **C1: Constraint conflict** | Task goal requires violating a MUST NOT | Hard-coded constraint architecture in prompt | Halt, state conflict, ask |
| **C2: Ambiguous instruction** | Multiple plausible interpretations exist | Pre-execution interpretation check | Surface interpretation, ask to confirm |
| **C3: Irreversible action** | Action cannot be undone | Action type classification | Explicit approval required before execution |
| **C4: Uncertainty overload** | Confidence below calibrated threshold | Conformal prediction / calibrated uncertainty | Halt, narrow ambiguity, then ask if still unresolved |
| **C5: Conflicting goals** | Two valid goals produce incompatible actions | Constraint architecture + goal comparison | Stop, expose conflict, ask for priority |
| **C6: Scope creep** | Required action exceeds explicit authorization | Authorization boundary check | Stop, state what is needed, ask for scope extension |

---

## Recommended Implementation for Our hookify/Rule System

### Hook Type: Pre-Tool Escalation Gate

This is a **PreToolUse hook** that fires before any tool execution. It is NOT a
confidence score — it is a **rule-based classifier** over the action being taken.

```python
# Pseudo-code for hookify escalation gate
ESCALATION_RULES = [
    # C1: Constraint conflict
    lambda action, rules: action.would_violate_any(rules.must_nots),

    # C2: Ambiguous instruction
    lambda action, context: action.has_multiple_plausible_interpretations(context),

    # C3: Irreversible action
    lambda action, _: action.is_irreversible,  # delete, overwrite, deploy, pay, push --force

    # C4: Uncertainty overload
    lambda action, context: action.confidence < context.uncertainty_tolerance,

    # C5: Conflicting goals
    lambda action, context: action.conflicts_with_another_active_goal(context.goals),

    # C6: Scope creep
    lambda action, context: action.exceeds_authorized_scope(context.authorization),
]

def should_escalate(action, context, rules) -> tuple[bool, str]:
    for rule in ESCALATION_RULES:
        if rule(action, context, rules):
            return True, rule.__doc__  # return the reason
    return False, None
```

### Integration with OpenBrainLM Layer Architecture

- **L4 (Action Selection / Basal Ganglia):** Escalation gate sits here. Inhibition-by-default
  already IS the biological model — actions are RELEASED only when safe. Escalation = action
  stays inhibited and bubbles up to L6 for human routing.
- **L6 (Relevance Detection / Amygdala):** Escalation signals route through L6 Stage 1
  (fast threat detection) for C3 (irreversible actions) and L6 Stage 2 (slow prefrontal
  deliberation) for C1/C2/C5.
- **hookify file:** `hookify.escalation-gate.local.md` — mirrors the destructive action
  intercept pattern already designed in hooks audit.

### Constraint Architecture in AGENT_RULES.md

Per Agents_Arcs Pattern 1: each agent's instructions should have an explicit `ESCALATION_TRIGGERS`
section with the exact conditions that fire halt-and-ask, written in plain language. Not
inferred — explicit. Example:

```markdown
## ESCALATION_TRIGGERS
HALT and ask the operator when:
- The task requires deleting, overwriting, or pushing to main (C3: irreversible)
- Instructions contradict a rule in AGENT_RULES.md or CLAUDE.md (C1: constraint conflict)
- "These files" or "those records" is ambiguous with 2+ plausible readings (C2: ambiguity)
- The goal requires modifying something not mentioned in the original task (C6: scope creep)
```

---

## Relationship to ALLOSTATIC_DECISION_GATE.md

The allostatic gate handles **internal system health escalation** (when a brain pathway
is degrading). This escalation trigger research handles **external task execution escalation**
(when a human decision is required before proceeding).

They are two separate mechanisms that live at different layers:

```
Allostatic Gate:  Internal health → self-repair tiers (Tier 0–3)
Escalation Gate:  External task → human approval (Classes C1–C6)
```

Both share the same foundational principle: **inhibition-by-default**. The cheapest
response is tried first. In the escalation gate, "cheapest" = clarify instruction scope
before execution, not after a mistake.

---

## Citations

| Source | URL / Reference |
|--------|----------------|
| KNOWNO paper | https://arxiv.org/abs/2307.01928 — Ren et al. (2023), Princeton + Google DeepMind |
| PSUM uncertainty taxonomy | https://arxiv.org/html/2602.23005v1 — "Managing Uncertainty in LLM-based Multi-Agent Systems" (2026) |
| AI Agent Index (2026) | https://arxiv.org/html/2602.17753v1 — "The 2025 AI Agent Index" |
| Anthropic effective agents | https://www.anthropic.com/research/building-effective-agents |
| LangGraph interrupt docs | https://docs.langchain.com/oss/python/langgraph/interrupts |
| LangGraph interrupt blog | https://blog.langchain.com/making-it-easier-to-build-human-in-the-loop-agents-with-interrupt/ |
| CrewAI human input | https://docs.crewai.com/en/learn/human-input-on-execution |
| Agents_Arcs notebook | NotebookLM 1a7bcc9d, session fc81746b (156 sources, Anthropic/DeepMind grounded) |
| Toward Safe AI Agents (arXiv) | https://arxiv.org/html/2601.06223v1 |
