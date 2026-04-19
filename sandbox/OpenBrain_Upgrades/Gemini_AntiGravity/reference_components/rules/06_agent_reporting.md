## Agent Reporting — Status Updates + Audit Before Results

When ANY subagent completes:
1. **Tell Creator immediately** — "Agent came back — running audit now" (brief status, not results)
2. **Dispatch audit agent** — NEW agent via Agent tool (Sonnet model), assumes first agent was wrong. Do NOT present results until audit passes.
3. **After audit passes** — report 2-3 bullet points: key findings, action items, blockers, audit verdict
4. **If agent failed or returned garbage** — say so explicitly, don't silently retry
5. **Track all dispatched agents** — Creator should always know what's out and what came back
6. **Before responding to any Creator message** — check for unreported agent results FIRST
7. **Before ending session** — verify all completed agents have been reported

## Audit Gate (fires after EVERY execution agent)

**How to dispatch the audit agent:**
```
Agent tool call:
  subagent_type: general-purpose
  model: sonnet
  prompt: "Hostile audit. Assume the previous agent did everything wrong.
           Read [exact file paths produced]. Check:
           1. Did it complete the task? (yes/no — state what's missing if no)
           2. CODE: Is it clean, correct, complete? No hallucinated APIs, no partial implementations?
              RESEARCH: Does every claim have a direct quote and citation? No unsourced assertions?
           Report PASS or FAIL with specific issues. Be hostile. Find the problems."
```

**After audit agent returns:**
```
PASS → report to Creator: findings + "Audit: PASS"
FAIL → fix the specific issues, re-dispatch audit (max 2 iterations)
       if still failing after 2 → report to Creator: what failed and why
```

This rule exists because:
- Agents never do it right on the first pass (Creator's observation, 2026-03-24)
- Silent retry without telling Creator = broken
- Presenting unaudited output as truth = broken
