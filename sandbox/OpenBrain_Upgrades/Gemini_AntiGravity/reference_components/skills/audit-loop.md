---
name: audit-loop
description: Automated coder-auditor loop. Dispatches Sonnet to write code, then ZCR + Semgrep audit. If either fails, Sonnet fixes and re-audits. Max 3 iterations. Opus observes and breaks if stuck.
---

# Audit Loop — Automated Coder-Auditor Cycle

## When to Use
Invoke this skill whenever code needs to be written and audited. This replaces manual orchestration of the delegation protocol.

## The Loop

For each code task:

### Step 1: DISPATCH CODER
- Spawn a Sonnet agent (`model: sonnet`) with:
  - Exact file paths to modify
  - The specification (what to change, why)
  - Constraints (what NOT to change)
  - If this is a FIX iteration: include the auditor findings verbatim

### Step 2: DISPATCH AUDITORS (parallel)
After coder completes, spawn BOTH in parallel:

**Auditor 1 — ZCR (Zero-Context Reviewer):**
```
Agent tool:
  subagent_type: zero-context-reviewer
  model: sonnet
  prompt: "Review [exact file paths]. Check logic, security, edge cases.
           Return PASS / FAIL / CONDITIONAL with specific findings."
```

**Auditor 2 — Semgrep (Static Analysis):**
```
Bash: semgrep scan [file paths] --config auto
```

### Step 3: EVALUATE
- If BOTH pass → write audit receipt → DONE
- If EITHER fails → collect findings → go to Step 4
- If iteration count >= 3 → STOP, report to Sage what's stuck

### Step 4: FIX LOOP
- Feed auditor findings back to a NEW Sonnet agent (fresh context)
- The fix prompt MUST include:
  - The original spec
  - The specific findings to fix
  - "Do NOT introduce new features. Fix ONLY the flagged issues."
- Return to Step 2

## Rules
- Max 3 iterations per task. After 3: stop and escalate.
- Coder NEVER sees auditor identities or knows which round it is.
- Each iteration uses a FRESH Sonnet agent (no accumulated context).
- Opus (orchestrator) monitors but does NOT read code directly.
- Opus reviews AUDIT RESULTS, not the code itself.
- All code must use documented APIs from official sources only.
- No custom code when a library exists. Research first, code second.

## Write Receipt After Pass
```
bash .claude/hooks/write_audit_receipt.sh \
  "<semgrep_pass>" "<approval_id>" "<zcr_notes>"
```

## Break Conditions (Opus intervenes)
- Same finding appears 3 times (loop is stuck)
- Coder introduces NEW findings while fixing old ones (regression)
- Auditors disagree on severity (need human judgment)
- Any finding rated CRITICAL that persists after 1 fix attempt
