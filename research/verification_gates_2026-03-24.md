# Objective Verification Gates — Research
> Date: 2026-03-24
> Sources: Agents_Arcs notebook (1a7bcc9d, 156 sources) + live arXiv/GitHub verification
> Context: 4th missing hook identified in OpenBrainLM hook audit — structural gate that forbids
> marking a task complete unless an external test/linter/verifier passes.

---

## The Problem

LLM self-critique is insufficient as a completion gate for three structural reasons:

1. **Same failure mode as the output itself.** The LLM that generated flawed output uses the
   same weights to critique it. It cannot reliably detect its own systematic errors.
2. **Syntactic validity ≠ semantic correctness.** A response can be grammatically valid,
   schema-conformant, and internally consistent while being factually wrong or incomplete.
3. **No enforcement surface.** Self-critique produces a suggestion to revise, not a hard stop.
   An agent can acknowledge a critique and still mark the task done.

Source: arXiv:2603.15676 confirms this — their gate requires deterministic route/schema checks
PLUS LLM-graded content checks PLUS human calibration. Any single layer alone is insufficient.
Human evaluator κ agreement with automated gate was 0.167–0.000, confirming structural failures
are only visible in traces while content hallucinations are only visible in content evaluation.
The two layers detect non-overlapping failure classes.

---

## Patterns Found

### Pattern 1: JSON Task List + Status Flag (Anthropic Agent Harness)

Source: Agents_Arcs notebook, attributed to Anthropic's internal agent harness pattern.

The agent harness forces workers to interact with a structured JSON task list. A worker:
1. Reads the JSON backlog
2. Picks a single failing task
3. Implements the change
4. **Updates the JSON status flag to "passing" — but ONLY after the external test suite passes**
5. Commits to Git
6. Terminates

The "passing" flag is NOT set by the agent's self-assessment. It is set by running the
actual test suite against the output. The agent cannot mark a task done without that flag
flipping — and the flag only flips when the external test runner confirms it.

This is the canonical hard gate: **agent writes → external runner validates → flag updates → task closes**.
Self-declaration without external confirmation is architecturally impossible.

Key property: "non-deterministic idempotence" — the workflow survives agent crashes and context
compaction because state lives externally in Git + JSON, not in the agent's context window.

### Pattern 2: Multi-Dimensional Quality Gate with Hard Thresholds

Source: arXiv:2603.15676 — "Automated Self-Testing as a Quality Gate: Evidence-Driven Release
Management for LLM Applications"

Five dimensions, each with a binary threshold. Gate decision = three-state machine:

| Dimension              | Target    | Critical Floor | Measurement Method                              |
|------------------------|-----------|----------------|-------------------------------------------------|
| Task Success Rate      | ≥80%      | <56%           | passed-tests / total-tests                      |
| Context Preservation   | ≥90%      | <63%           | context-preserved / history-tests               |
| P95 Latency            | <15,000ms | >21,500ms      | OpenTelemetry wall-clock traces                 |
| Safety Pass Rate       | ≥95%      | <66.5%         | safety-tests-passing / safety-tests             |
| Evidence Coverage      | ≥80%      | <56%           | web-tests-with-evidence / web-tests (citations) |

**Gate states:**
- **PROMOTE**: all dimensions meet/exceed thresholds
- **HOLD**: narrowly fails, no critical floor breach — human triage required
- **ROLLBACK**: any dimension breaches critical floor — automatic rejection, no human override

Question bank stratified into four tiers: (1) core functional, (2) complex orchestration,
(3) hallucination traps (queries for non-existent features — tests faithfulness),
(4) adversarial/safety (prompt injection, PII extraction).

Non-LLM verification layer: OpenTelemetry traces capture routing, schema validation, latency —
deterministic checks that run independently of LLM content evaluation.

Finding: structural failures (latency, routing errors) are ONLY visible in traces.
Content hallucinations are ONLY visible in content evaluation. Both layers are required.

### Pattern 3: Validator Chain with OnFailAction.EXCEPTION (Guardrails-AI)

Source: github.com/guardrails-ai/guardrails — active open source, widely used.

Guards = composable Python objects that intercept LLM inputs/outputs. Validators chain:

```python
Guard().use(RegexMatch(...), ToxicLanguage(...), CompetitorCheck(...))
```

On validation failure, `OnFailAction.EXCEPTION` raises an exception — halting execution
entirely. The LLM output never reaches downstream code. This is the hard gate surface.

Validator categories relevant to truth-checking:
- **Schema validators**: Pydantic model enforcement — output must conform to schema
- **RegexMatch**: pattern-level structural checks
- **Custom validators**: user-defined logic (e.g., run a linter, check a hash, compare to ground truth)
- **ToxicLanguage / ContentFilter**: semantic content gates

For our use case: a custom validator can call `pytest`, `ruff`, `mypy`, or any external
process. If it returns non-zero, `OnFailAction.EXCEPTION` fires. The agent cannot proceed.

### Pattern 4: Fact-Level Grounding Check (MiniCheck)

Source: arXiv:2404.10774 — "MiniCheck: Efficient Fact-Checking of LLMs on Grounding Documents"

Trains a small (770M param) model to verify whether LLM outputs are grounded in source
documents. Binary classifier: **grounded** (pass) or **not grounded / contradicted** (fail).

Two verification subtasks:
1. Fact-level checking — individual claims verified against source
2. Cross-sentence synthesis detection — flags inappropriate combination of evidence across sentences

GPT-4 accuracy at 400x lower cost. Key insight: verification does not require the same
large model that generated the output. A small specialized verifier is cheaper and often
more reliable for this specific task.

Application: in our system, a MiniCheck-equivalent call could verify that agent memory
writes actually reflect what is in the source files, not hallucinated summaries.

### Pattern 5: Execution-Based Validation (Gorilla Framework)

Source: arXiv:2507.21504v1 — "Evaluation and Benchmarking of LLM Agents: A Survey"

For tool-using agents, the Gorilla framework introduced execution-based evaluation:
**run the tool call and assess the actual outcome**, not just the syntactic form of the call.

This catches semantic errors — incorrect parameter values, hallucinated API endpoints —
that pass syntactic validation but fail in execution.

For our system: when an agent writes a file, reads from memory, or calls a function,
the gate is not "did the agent say it did X" but "did X actually happen, verifiably."

Verified against: arXiv survey confirms code-based method is "the most deterministic and
objective approach" relying on "explicit rules, test cases, or assertions."

### Pattern 6: Co-Sight Shared Facts Module (Multi-Agent Truth Synchronization)

Source: arXiv:2510.21557v1 — "Co-Sight: Conflict-Aware Meta-Verification and Trustworthy Reasoning"

In multi-agent systems where agents share a knowledge state, a dedicated Shared Facts module
continuously organizes, validates, and synchronizes evidence across agents. Three-tier context
compression: tool level → notes level → facts level. Only facts that pass inter-agent
consistency checks graduate to the shared facts tier.

For our system: relevant for the Trinity Consolidation step — findings promoted to
long_term.md should pass a consistency check against existing entries (contradiction detection).

---

## Implementation for Our System

### Immediate: hookify rule — `hookify.objective-verification-gate.local.md`

The hook fires at the PostToolUse stage when an agent writes to a task status field,
memory file, or marks anything as "complete" / "verified" / "passing."

**Gate logic:**
```
IF agent writes status="complete"|"passing"|"verified"|"done" to any tracked file:
  THEN: require one of the following to be present in the same tool call context:
    (a) pytest exit code = 0 from the relevant test path
    (b) ruff/mypy linter exit code = 0 on modified files
    (c) explicit external hash/checksum match logged
    (d) Judge agent sign-off (separate context, not the same agent)
  ELSE: BLOCK the write, return error: "Verification gate: no external confirmation present"
```

### For Memory Writes (short_term.md / long_term.md)

Minimum bar before promoting a finding:
1. Source field present and non-empty (from rule 07_memory_verification.md — already exists)
2. Confidence ≥ 0.6 (already in schema)
3. **NEW**: at least one of: (a) direct file read confirming the claim, (b) cross-reference
   against a second source, (c) external validator result attached

This prevents the current failure mode: agent summarizes what it thinks a file contains
without having read it, writes that summary to memory as verified fact.

### For Code/Script Outputs

Pattern from Anthropic harness (Pattern 1):
- Agent produces output → external `pytest` run → exit code 0 required → THEN status="passing"
- Implement as a pre-commit hook OR as a required step in the agent's contract prompt:
  "You may not set status=passing until you have run the test suite and pasted the exit code."
- For our hookify system: hook reads the agent's tool call, checks for test output artifact
  in the same commit/write. Missing artifact = blocked write.

### For Research/Claim Outputs

Pattern from arXiv:2603.15676 (Pattern 2) applied to research:
- Hallucination trap tier: include "impossible queries" — ask for details about something
  that doesn't exist in the codebase/memory. Agent that self-critiques will hallucinate;
  external verifier catches it.
- Evidence coverage metric: track what % of agent claims have an explicit citation.
  Gate threshold: ≥80% evidence coverage required before findings are accepted.

### For Multi-Agent Trinity Consolidation

Pattern from Co-Sight (Pattern 6):
- Before promoting from short_term → long_term: run a contradiction check against existing
  long_term entries. If new finding contradicts an existing verified finding, HOLD — do not
  promote either. Flag for human review.
- This is a deterministic text comparison, not an LLM self-check.

---

## Verification Summary (What We Confirmed Live)

| Claim | Verified Against | Status |
|-------|-----------------|--------|
| Anthropic harness uses JSON task list + external test runner to flip status flags | Agents_Arcs notebook (session 3a4160aa), attributed to Anthropic pattern | VERIFIED (notebook) |
| arXiv:2603.15676 implements 5-dimension gate with PROMOTE/HOLD/ROLLBACK | Direct fetch of paper HTML | VERIFIED |
| guardrails-ai uses OnFailAction.EXCEPTION as hard gate | Direct fetch of github.com/guardrails-ai/guardrails | VERIFIED |
| MiniCheck achieves GPT-4 accuracy at 400x lower cost for grounding verification | arXiv:2404.10774 abstract | VERIFIED |
| Code-based evaluation is "most deterministic" per agent eval survey | arXiv:2507.21504v1 | VERIFIED |
| Structural failures (latency/routing) only visible in traces; content hallucinations only in content eval | arXiv:2603.15676 | VERIFIED |

---

## Citations

1. **Anthropic agent harness pattern** (JSON task list + "passing" flag gate)
   — Agents_Arcs notebook, id: 1a7bcc9d, session 3a4160aa, attributed to Anthropic internal
   multi-agent coding harness. 156 sources.

2. **arXiv:2603.15676** — "Automated Self-Testing as a Quality Gate: Evidence-Driven Release
   Management for LLM Applications" (2026)
   https://arxiv.org/abs/2603.15676

3. **arXiv:2404.10774** — "MiniCheck: Efficient Fact-Checking of LLMs on Grounding Documents"
   https://arxiv.org/abs/2404.10774

4. **arXiv:2510.21557v1** — "Co-Sight: Enhancing LLM-Based Agents via Conflict-Aware
   Meta-Verification and Trustworthy Reasoning with Structured Facts"
   https://arxiv.org/abs/2510.21557

5. **arXiv:2507.21504v1** — "Evaluation and Benchmarking of LLM Agents: A Survey"
   https://arxiv.org/abs/2507.21504
   (Source of Gorilla execution-based evaluation finding)

6. **guardrails-ai/guardrails** — GitHub, active open source
   https://github.com/guardrails-ai/guardrails
   OnFailAction.EXCEPTION mechanism, validator chain composition

7. **arXiv:2509.02761v2** — "Plan Verification for LLM-Based Embodied Task Completion Agents"
   https://arxiv.org/abs/2509.02761
   (Negative result — soft iterative loop, not a hard gate. Useful contrast.)

8. **Steve Yegge "Gas Town" pattern** — cited in Agents_Arcs notebook as source for
   queue-based write / Refinery serializer pattern. Referenced as multi-agent coordination
   best practice within the notebook's 156-source corpus.

---

## Key Takeaway for OpenBrainLM

The research converges on one structural principle across all sources:

> **The agent that produces output cannot be the same agent that certifies it correct.**
> Verification must be structurally separate — different process, different context, or
> deterministic external tool — and task completion must be architecturally impossible
> without its sign-off.

This is Pattern 1 (Anthropic harness), Pattern 2 (PROMOTE gate), Pattern 3 (Guardrails
exception), and Pattern 5 (Gorilla execution eval) all saying the same thing from different
angles. The implementation surface for our system is the hookify layer.
