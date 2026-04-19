## Hostile Audit — MUST Use Code Review Tools

Every hostile audit MUST include automated code review, not just manual agent review.

### Required audit sequence:
1. Manual file read + logic verification (existing pattern)
2. **Semgrep scan** — run `semgrep scan` on all files produced/modified
3. **CodeRabbit review** — run code-review on the changes
4. Cross-reference all three results before issuing PASS/FAIL

### When dispatching audit agents, include in prompt:
```
"After manual review, run semgrep scan AND coderabbit code-review on all files.
Cross-reference automated findings with your manual review.
Report: manual verdict + semgrep findings + coderabbit findings."
```

This applies to ALL code audits — NT, OpenBrainLM, trading bot, any project.
