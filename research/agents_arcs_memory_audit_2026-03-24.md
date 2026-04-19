# Agents_Arcs Memory Architecture Audit + Drift Detection
> Source: Agents_Arcs notebook (1a7bcc9d), session e9611ef3, 2026-03-24
> Query by: review-memory Sonnet agent

## Memory Architecture — What's Strong
- Lifecycle separation avoids "passive accumulation fallacy"
- 4-field schema (statement/confidence/source/status) solves "confidence illusion"
- Productive forgetting via episodic termination prevents "lost in the middle"
- Quarantine notebook protects core context from pollution
- Rejecting frequency-based pruning avoids deleting rare but critical boundaries

## Memory Architecture — What's Missing
1. **Test-driven memory updates**: Consolidation should tie to external verification (tests, API pings), not just LLM judgment
2. **Staleness management**: Add 5th field "Last Verified Date" to long_term.md schema. Scheduled background agent scans for stale entries.
3. **Prefix caching discipline**: Layer 1 + 2 must be at TOP of prompt (static), Layer 3 at bottom (dynamic) for cache efficiency
4. **JSON queue at scale**: short_term.md creates file-locking contention with parallel agents. Transition to JSON/DB queue if scaling.

## Drift Detection — 6 Patterns
1. **Auto-policing agents** (Codex/OpenAI): Background agents scan for deviations from "golden principles," open refactoring PRs. Repository polices itself.
2. **External holdout scenarios** (StrongDM): Behavioral specs live OUTSIDE codebase. Agent can't see them during dev. Like ML holdout set.
3. **Writer-critic loops**: One agent generates, second validates independently. Catches drift before propagation.
4. **Extensive observability**: Audit trail of all tool calls, inputs, docs retrieved, intermediate outputs, validation status. Assume "subtle failure world."
5. **Automated rubric passes**: Defined quality rubric, designated LLM scores agent output before human review. Consistent behavioral audit.
6. **Zero-trust behavioral monitoring**: Treat agents as untrusted. Escalation triggers at critical decision boundaries.

## Action Items
- [ ] Add "Last Verified Date" as 5th field in long_term.md schema
- [ ] Design auto-policing hook (golden principles check)
- [ ] Design external holdout test for behavioral verification
- [ ] Writer-critic loop = our existing hostile-twin/auditor pattern — verify it's wired in
- [ ] Audit trail already partially exists via hooks — need to formalize
