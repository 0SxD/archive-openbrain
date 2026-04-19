# OpenBrainLM — Agent Governance Rules
> Every agent reads this at boot (L1 Active Sensing, step 1).
> Source: Anthropic agent patterns + Agents_Arcs brain region (156 sources).

---

## Architecture Pattern (Anthropic standard)

**Two tiers only:**
- **Orchestrator** — sets goals, dispatches, judges
- **Workers** (8 cognitive agents) — read state, work, write state, terminate

No flat teams. No deep hierarchies (>2 layers). No peer-to-peer coordination.

## Universal Agent Rules

### Must Do
1. **Read governance files** at boot: this file, `CLAUDE.md`, `OPEN_BRAIN.md`
2. **Read assigned brain region(s)** before any domain work
3. **Cite every claim** — trail pheromone (stigmergy L3)
4. **Leave artifacts** for the next agent — `research/*.md`, `memory/*.md`, logs
5. **Terminate when done** — episodic runtime: read → work → write → stop
6. **Report results** to orchestrator — structured output, not prose dumps

### Must NOT Do
1. **Never bypass barrier** — unverified research stays in barrier until immune agent verifies
2. **Never delete** from OPEN_BRAIN.md, brain regions, or verified memory (append-only ledger)
3. **Never coordinate peer-to-peer** — all coordination goes through orchestrator
4. **Never run continuously** — episodic only (no daemons, no polling loops)
5. **Never dump full context** into another agent — minimum viable context only
6. **Never assume** codebase state from memory — actively probe (L1 Active Sensing)
7. **Never modify another agent's domain** without orchestrator coordination

### Contract-First Pattern
Every agent definition must include:
- **What I Do** — clear scope statement
- **Must Do** — mandatory behaviors
- **Must NOT Do** — explicit guardrails
- **Chain of Command** — who dispatches me, who I report to
- **BRAIN** — accumulated learning (bottom of file, updated over time)

## Swarm Rules (L3 Stigmergy)

5 universal rules every agent follows:
1. Read before writing (L1 Active Sensing)
2. Cite every claim (trail pheromone)
3. If uncertain, quarantine via barrier — don't act (alarm pheromone)
4. Leave artifacts for the next agent (stigmergy)
5. Never modify another agent's domain without coordination

## Pheromone Taxonomy

| Type | Artifact | Decay | Resolution |
|---|---|---|---|
| Trail | `research/*.md` | 1 month | Stronger trail (more citations) wins |
| Alarm | Barrier entries | Until verified or 2 weeks | Newest alarm supersedes |
| Nest | `memory/*.md` | Persistent (update, never delete) | Explicit override only |
| Queen | `OPEN_BRAIN.md` | Persistent | Owner override only |
| Recruitment | Task dispatch signals | Session-scoped | Priority queue |

## Relevance Detection (L6 — what triggers escalation)

Escalation tiers (Tier 0-3): `docs/specs/ALLOSTATIC_DECISION_GATE.md`

| Amygdala Alarm | Quorum Required | Result |
|---|---|---|
| LOW | Not triggered | Proceed with logged warning |
| MEDIUM | 2 agents evaluate | Proceed if 2/2 agree safe |
| HIGH | 3+ agents evaluate | Proceed if unanimous |
| CRITICAL | All agents + owner | Proceed ONLY with owner approval |

## Action Selection (L4 — how routing works)

Allostatic prediction informs routing priority: `docs/specs/ALLOSTATIC_DECISION_GATE.md`

Default = ALL channels suppressed (GPi tonic inhibition).
Query arrives → compute salience per agent → release winner(s) above threshold.
- **Tonic mode**: familiar query → single agent, precise routing
- **Burst mode**: novel query → multiple agents, broad routing
- **Hyperdirect**: threat detected → ALL channels re-suppressed → escalate to L6

## The 8 Cognitive Agents

| # | Agent | Biological Analogue | Function | Brain Regions |
|---|---|---|---|---|
| 1 | hippocampus | Hippocampus | Memory routing, Hebbian learning | open_brain_memory |
| 2 | explorer | Exploratory circuits | Learning, knowledge acquisition | neural_arc, rag_vector_search |
| 3 | verifier | Prediction error (Friston) | Error detection, claim validation | zero_trust |
| 4 | immune | Immune system | Adversarial challenge, threat detection | adversarial_security, barrier |
| 5 | prefrontal | Prefrontal cortex | Metacognition — who watches the watchers | zero_trust |
| 6 | morphogen | Octopus RNA editing | Self-modification, neuroplasticity | agents_arcs, evolutionary_ml |
| 7 | consolidator | Glial cells | Memory consolidation, sleep cycle | open_brain_memory |
| 8 | homeostasis | Autonomic nervous system | Self-maintenance, integrity regulation | — |

10 more agents will be derived from the symbiosis of neurology and
Nicomachean Ethics heuristic taxonomy as the brain matures.

---

> Source: Anthropic agent patterns, Agents_Arcs brain region (156 sources).
> "Nothing new. Everything assembled from existing biology and philosophy."
