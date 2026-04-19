## Memory Verification — Patterns from Agents_Arcs Research (14 patterns, 156 sources)

### Schema-Driven Verification (Pattern 2)
Every entry promoted to long_term.md MUST include 4 fields:
1. **Statement** — the claim itself
2. **Confidence** — 0-1 score
3. **Source** — exact citation (paper, file, URL, notebook)
4. **Status** — verified | disputed | needs_review

Entries missing any field stay in short_term.md until complete.

### Confidence Bouncer (Pattern 5)
Claims with confidence < 0.6 get quarantined, NOT promoted. Flag "needs_review" and notify Creator.
Do NOT auto-promote low-confidence findings.

### Timestamp Discipline (Pattern 7)
Every consolidation event in long_term.md must include `[YYYY-MM-DD]` date.
Every promotion must record WHEN it was verified and BY WHOM (which agent/notebook).

### Frequency Anti-Pattern (Pattern 8 — WARNING)
NEVER prune memory based on access frequency or recency.
AI optimizes for statistical saliency (noise), not importance.
Human-in-the-loop or confidence bouncer ONLY for pruning decisions.

### Chain of Verification (Pattern 1)
Before promoting ANY finding to long_term.md, self-check:
1. List the finding
2. Identify how it might be wrong
3. Cite the exact source that confirms/refutes
4. Revise if needed BEFORE writing

### Pre-Delivery Health Check (Pattern 9)
Before presenting results to Creator:
- Verify every claim has a source, or mark it "unknown"
- "I don't know" is a VALID and REQUIRED answer when confidence is low
- Do NOT force an answer when uncertain — park it

### Already Implemented
- Position Hacking (#11) — brainstem PreToolUse re-broadcasts principles at every tool call
- Episodic Termination (#14) — Initializer→Worker pattern, session termination + Trinity Consolidation
- Lifecycle Separation (#6) — short_term.md → long_term.md → archival hierarchy
- Adversarial Audit (#10) — immune/hostile-twin agent as separate sub-agent context
