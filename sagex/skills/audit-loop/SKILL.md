---
name: audit-loop
description: |
  Use when code has been written or modified. Triggers the 3-agent audit cycle:
  ZCR (zero-context review) → Semgrep (static analysis) → Opus (cross-reference verdict).
  Code cannot be committed without passing all three.
---

# Audit Loop

## The triad

1. **ZCR (Zero-Context Reviewer)** — Sonnet agent reads the code cold. No project context, no assumptions about intent. Finds issues a fresh reviewer would find.
2. **Semgrep (Static Sentinel)** — Automated static analysis with auto config. Catches patterns, security issues, code smells mechanically.
3. **Opus (Orchestrator)** — Reviews both ZCR and Semgrep outputs. Cross-references findings. Issues final verdict: PASS, CONDITIONAL (with specific required fixes), or FAIL.

## Rules

- ZCR and Semgrep run INDEPENDENTLY — neither sees the other's output
- Opus sees BOTH outputs and makes the final call
- Opus reviews AUDIT RESULTS, not code directly (prevents bias)
- All three must agree for a PASS
- CONDITIONAL means: specific fixes listed, then re-audit
- FAIL means: back to coder with findings (triggers build-loop retry if in a loop)

## Commit gate

The `audit_gate_check.sh` hook blocks `git commit` without a fresh audit receipt. The receipt must:
- Cover all staged files
- Be less than 1 hour old
- Contain the PASS verdict from the triad

## Integration with build-loop

When invoked via `/sagex:build-loop`, the audit loop is step 2-3 of each round. Failures feed back to the coder for retry. Max 3 rounds before Opus breaks the deadlock.
