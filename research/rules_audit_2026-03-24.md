# Rules Directory Audit
> Audited: 2026-03-24, 30 files (8 numbered active + 22 archived)

---

## Summary

The rules directory contains two tiers of files:
- **8 numbered active rules** (`01_agent_system.md` through `08_bootup_ritual.md`) — these load every session
- **22 archived rules** (`_archived_*.md`) — legacy individual rules, now partially consolidated into the numbered files

The numbered rules were clearly written as a consolidation effort. However, the migration is incomplete. Several archived files contain content — sometimes entire rule categories — that was not carried forward into the numbered rules. Additionally, the archived files are still present with no indication they are deactivated; Claude Code loads all `.md` files in `~/.claude/rules/` by default, meaning all 30 files are currently active simultaneously. This is the most critical finding.

---

## Critical Issue: Are Archived Files Still Loading?

Claude Code's rules system loads ALL `.md` files in `~/.claude/rules/` unless filtered. The `_archived_` prefix is a naming convention only — it does NOT suppress loading. This means all 22 archived files are currently being injected into every session alongside the 8 numbered files. The archive files are not inert. **This doubles the rule load and creates genuine contradictions (see below).**

**Action required**: Either move archived files to a subdirectory (e.g., `rules/_archive/`) or confirm Claude Code's actual loading behavior for `_`-prefixed files.

---

## Duplicates Found

The following archived rules are substantially or fully covered by their numbered counterparts:

| Archived File | Covered By | Coverage Level |
|---|---|---|
| `_archived_agent_architecture_patterns.md` | `01_agent_system.md` | Full — same Initializer→Workers→Judge pattern, same anti-patterns |
| `_archived_auditor_of_auditors.md` | `01_agent_system.md` (Verification Layer section) | Full — same 3-layer auditor/hostile-twin/meta-auditor chain |
| `_archived_two_github_agents.md` | `01_agent_system.md` (GitHub Agents section) | Full — same guardian/scout split |
| `_archived_subagent_delegation.md` | `01_agent_system.md` (Delegation section) | Mostly full — model assignments covered; see Gap 1 below |
| `_archived_never_first_principles_alone.md` | `02_build_philosophy.md` (Foundational Principle) | Full — same "research first, cite always" mandate |
| `_archived_creators_teaching.md` | `02_build_philosophy.md` (Build Rules 1-2) | Full — same "research what exists, build on it" principle |
| `_archived_code_from_reference.md` | `02_build_philosophy.md` (Build Rule 3) | Full — same "find GitHub repo, study it, build from it" |
| `_archived_no_writing_code.md` | `02_build_philosophy.md` (Build Rule 3-4) | Full — same "assemble don't originate" mandate |
| `_archived_no_adapter_wrappers.md` | `02_build_philosophy.md` (Build Rule 5) | Full — same "use library directly as documented" |
| `_archived_library_selection.md` | `02_build_philosophy.md` (Build Rule 4) | Full — same open-source/maintained/community criteria |
| `_archived_copy_discipline.md` | `02_build_philosophy.md` (Versioning & Copy Discipline) | Full — same copy-not-edit, SHA256-hash, audit MD |
| `_archived_innovation_philosophy.md` | `02_build_philosophy.md` (Build Rule 6) | Full — same 80/20 restructuring principle |
| `_archived_minimal_renaming.md` | `02_build_philosophy.md` (Naming section) | Full — same "don't rename unless necessary" rule |
| `_archived_plugin_role.md` | `02_build_philosophy.md` (Plugins section) | Full — same plugin manager role + standard sequence |
| `_archived_auto_consolidation.md` | `03_memory_discipline.md` | Full — same autonomous write mandate, same triggers |
| `_archived_write_everything_down.md` | `03_memory_discipline.md` | Full — same "write after every action, don't batch" rule |
| `_archived_memory_above_compression.md` | `03_memory_discipline.md` (Core Principle) | Full — same "memory sits above compression" |
| `_archived_no_hallucination.md` | `04_integrity.md` | Full — same "read first, report second" rules |
| `_archived_research_sources_strict.md` | `05_research_protocol.md` (Source Hierarchy) | Full — same banned sources list and approved tiers |
| `_archived_research_corridor.md` | `05_research_protocol.md` (Research Corridor section) | Full — same quarantine → verify → promote pipeline |
| `_archived_the_loop.md` | `05_research_protocol.md` (The Loop section) | Full — same research → notebook → verify → redo loop |
| `_archived_never_act_alone.md` | `05_research_protocol.md` + `02_build_philosophy.md` | Full — covered across both numbered files |

**All 22 archived files are duplicated in the 8 numbered files at least partially.** However, 3 archived files contain material gaps — see next section.

---

## Gaps Found

Archived files with content NOT fully present in the numbered rules:

### Gap 1 — Model assignment for Opus is inverted between files
**File**: `_archived_subagent_delegation.md`
> "Haiku: simple lookups, grep tasks, file listing, boilerplate"
> "Sonnet: research, file scanning, writing, summarizing, code generation"
> "Opus: reviews, audits, architecture decisions, **research (default for research unless told otherwise)**"

`01_agent_system.md` says:
> "Default to Sonnet for ALL work. Opus thinks, decides, and reviews — does not execute."

These **directly contradict each other** on who does research (see Contradictions section). The archived file assigns Opus to research by default; the numbered file assigns Sonnet to research. The archived file's note "research (default for research unless told otherwise)" is absent from `01_agent_system.md`.

### Gap 2 — Specific file targets for memory writes
**File**: `_archived_auto_consolidation.md` specifies:
> "Write to brain files WITHOUT asking the operator. Never announce consolidation. Just do it."

`03_memory_discipline.md` says:
> "Write to brain files WITHOUT asking the operator. Never announce consolidation. Just do it."

Coverage is identical here. No gap — this is a duplicate.

### Gap 3 — Verification layer relaxation condition
**File**: `_archived_auditor_of_auditors.md`:
> "Once the system is proven and trusted, this layer **can be relaxed** — but NOT before"

`01_agent_system.md` (Verification Layer):
> "This layer **cannot be relaxed** until the system is proven and trusted."

The numbered file states the condition correctly (cannot relax until proven) but does NOT include the follow-on: what happens AFTER it's proven (relaxation is permitted). This is a minor omission — the archived version is slightly more complete.

### Gap 4 — "Never announce consolidation" is explicit only in archived file
**File**: `_archived_auto_consolidation.md`, rule 6:
> "Do NOT announce consolidation to the operator — just do it silently"

`03_memory_discipline.md`:
> "Write to brain files WITHOUT asking the operator. Never announce consolidation. Just do it."

Both files cover this — no gap. This is a duplicate.

### Gap 5 — Research assignment for Opus (actual gap)
`_archived_subagent_delegation.md` contains a parenthetical not present anywhere in the numbered rules:
> "Opus: reviews, audits, architecture decisions, research **(default for research unless told otherwise)**"

This conflicts with the numbered rules' "Default to Sonnet for ALL work." The parenthetical is the only place this exception/default appears. It is absent from `01_agent_system.md`. Whether the intent is Sonnet-default or Opus-default for research is ambiguous — both framings exist simultaneously in the active rule set.

### Gap 6 — Specific bootup sub-agent instructions
`08_bootup_ritual.md` is entirely new content — it has no archived counterpart. This is correct; it appears to be a new rule added during the numbered consolidation. No gap issue here, just noting it has no archive origin.

### Gap 7 — Memory verification schema (07) has no archived counterpart
`07_memory_verification.md` is entirely new content (Pattern 2, 5, 7, 8, 9 from Agents_Arcs). No archived file corresponds to it. No gap — just noting it's additive.

### Gap 8 — Agent reporting rule (06) has no archived counterpart
`06_agent_reporting.md` is entirely new content. No archived file corresponds to it. Additive, no gap.

---

## Contradictions

### Contradiction 1 — Who does research: Sonnet or Opus? (HIGH SEVERITY)

| File | Rule |
|---|---|
| `01_agent_system.md` | "Default to Sonnet for ALL work. Opus thinks, decides, and reviews — does not execute." |
| `_archived_subagent_delegation.md` | "Opus: reviews, audits, architecture decisions, research (default for research unless told otherwise)" |

These are mutually exclusive. If both files load every session, the agent receives contradictory instructions about who runs research tasks. Since archived files currently load alongside numbered files, this contradiction is live in every session.

**Resolution needed**: The numbered rule (`01_agent_system.md`) is more recent and more clearly stated. The archived file's Opus-for-research default should be superseded. But this requires either removing the archived file from the load path or explicitly overriding it.

### Contradiction 2 — "Agents do not write code" vs. "write code if nothing exists" (LOW SEVERITY)

| File | Rule |
|---|---|
| `_archived_no_writing_code.md` | "Agents do NOT write code. They ASSEMBLE existing, working pieces." (absolute) |
| `02_build_philosophy.md` | "If writing something truly novel, document WHY no reference exists" (permits novel code) |
| `02_build_philosophy.md` | "If code MUST be written → full agent loop: write → code-review → coderabbit → hostile audit → verify" |

The archived file is absolute (never write code). The numbered file permits code writing under conditions. The numbered rule is correct and more nuanced — the archived file's absolutism was clearly softened intentionally during consolidation. Low severity because the numbered rule subsumes and clarifies.

### Contradiction 3 — Memory write frequency: "every action" vs. "every ~10 tool calls" (LOW SEVERITY)

| File | Rule |
|---|---|
| `_archived_write_everything_down.md` | "After every significant action: update Open Brain, memory files, or session log" |
| `03_memory_discipline.md` | "Every ~10 tool calls or when context feels long: check if there's unsaved work, save it" |

The archived file says every significant action. The numbered file says every ~10 tool calls OR when context is long. These are compatible in intent but different in cadence trigger. The numbered file also says "After every significant action, learning, or decision: write it down immediately" — so both frequencies actually appear in `03_memory_discipline.md`. No real contradiction within the numbered file; the tension is between "immediately" and "every ~10 calls." Minor.

---

## Recommendations

### Priority 1 — Move archived files out of the load path (CRITICAL)
Move all `_archived_*.md` files to `~/.claude/rules/_archive/` subdirectory. This prevents them from loading every session and eliminates all live contradictions. Until this is done, Contradiction 1 (Sonnet vs. Opus for research) is active every session.

```
mkdir ~/.claude/rules/_archive/
move _archived_*.md _archive\
```

### Priority 2 — Resolve the Opus/Sonnet research contradiction explicitly (HIGH)
In `01_agent_system.md`, add a single line under Delegation:
> "Research tasks: Sonnet by default. Opus reviews findings — does not run the research queries."

This closes the ambiguity left by the archived file's parenthetical.

### Priority 3 — Add the "relaxation permitted after proven" note to numbered rules (LOW)
In `01_agent_system.md` Verification Layer section, add:
> "Once the system is proven and trusted, the meta-auditor layer may be relaxed — not before."

This restores the nuance lost from `_archived_auditor_of_auditors.md`.

### Priority 4 — Confirm Claude Code's `_`-prefix loading behavior (INFORMATIONAL)
The `_archived_` prefix convention was presumably chosen to signal "inactive." Verify whether Claude Code's rules loader actually suppresses files with leading underscores. If it does, Priority 1 is already resolved — but the contradictions documented here would still be latent if those files are ever moved back. Recommend keeping them in a subdirectory regardless.

### Priority 5 — Tag numbered rules with their archive origins (LOW)
Each numbered file could include a comment header like:
> `# Consolidates: _archived_agent_architecture_patterns.md, _archived_auditor_of_auditors.md, ...`

This creates a traceable lineage and makes future audits faster.

---

## File Inventory (all 30 files)

### Active Numbered Rules (8)
- `01_agent_system.md` — Agent architecture, delegation, verification, GitHub agents, anti-patterns
- `02_build_philosophy.md` — Foundational research-first principle, build rules, versioning, naming, plugins, the loop
- `03_memory_discipline.md` — Autonomous memory writes, timing triggers, targets, rules
- `04_integrity.md` — No hallucination, read-first, verify-before-presenting
- `05_research_protocol.md` — Research trigger, source hierarchy, NotebookLM query strategy, research corridor, freshness
- `06_agent_reporting.md` — Never let agent results disappear, track dispatched agents
- `07_memory_verification.md` — Schema-driven verification, confidence bouncer, timestamp discipline, chain of verification
- `08_bootup_ritual.md` — Orchestrator reads manifest + short_term.md before acting; sub-agent minimum context

### Archived Rules (22) — currently loading unless subdirectory fix applied
All 22 files listed in the duplicates table above. All have counterparts in the numbered rules, with the single live contradiction noted in Gap 5 / Contradiction 1.
