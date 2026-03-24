# Destructive Action Intercepts — Research
> Date: 2026-03-24
> Author: Claude Code Sonnet (research agent)
> Trigger: agents_arcs_hooks_audit_2026-03-24.md — Gap #1 "Destructive action intercepts"
> Status: VERIFIED — all sources fetched live

---

## Sources

1. **Claude Code Hooks documentation** — https://code.claude.com/docs/en/hooks (fetched 2026-03-24)
2. **AEGIS paper** — arXiv:2603.12621 — "AEGIS: No Tool Call Left Unchecked — A Pre-Execution Firewall and Audit Layer for AI Agents" (fetched 2026-03-24)
3. **\tool paper** — arXiv:2503.18666v1 — "Customizable Runtime Enforcement for Safe and Reliable LLM Agents" (fetched 2026-03-24)
4. **mattpocock/skills — block-dangerous-git.sh** — https://github.com/mattpocock/skills/blob/main/git-guardrails-claude-code/scripts/block-dangerous-git.sh (fetched 2026-03-24)
5. **NVIDIA NeMo Guardrails** — https://github.com/NVIDIA-NeMo/Guardrails + https://docs.nvidia.com/nemo/guardrails/latest/user-guides/guardrails-library.html
6. **Guardrails-AI** — https://github.com/guardrails-ai/guardrails

---

## Industry Patterns Found

### Pattern 1: Exit-code blocking (Claude Code native — simplest)
Source: Claude Code hooks docs (code.claude.com/docs/en/hooks)

PreToolUse hooks receive JSON on stdin:
```json
{
  "tool_name": "Bash",
  "tool_input": {
    "command": "rm -rf /tmp/build"
  }
}
```

Three response modes:
- **Exit 2** → command blocked immediately, stderr fed to Claude as error
- **Exit 0 + JSON stdout** → structured decision with `permissionDecision: "deny" | "allow" | "ask"`
- **Exit 0 (no JSON)** → command proceeds

JSON denial (preferred — gives Claude context):
```json
{
  "hookSpecificOutput": {
    "hookEventName": "PreToolUse",
    "permissionDecision": "deny",
    "permissionDecisionReason": "Destructive command blocked. Requires explicit user authorization."
  }
}
```

The `updatedInput.command` field can also redirect a dangerous command to a safer alternative before execution.

---

### Pattern 2: Regex pattern list against `tool_input.command`
Source: mattpocock/skills block-dangerous-git.sh (GitHub, fetched live)

Production implementation reads stdin JSON, extracts `.tool_input.command` via `jq`, then loops a hardcoded array of prohibited patterns using `grep -qE`. On match: stderr message + exit 2.

Patterns used in the wild:
```
git push
git reset --hard
git clean -fd
git clean -f
git branch -D
git checkout \.
git restore \.
push --force
reset --hard
```

Key design: **pattern list is maintained in the script itself**, not in a config file. Simple, auditable, zero dependencies beyond `jq`.

---

### Pattern 3: Multi-category risk scanner (AEGIS architecture)
Source: arXiv:2603.12621 (fetched live 2026-03-24)

AEGIS implements a three-stage pipeline:
1. **Deep string extraction** — recursively extracts all string values from tool arguments (depth 32, 10k-string cap). Defeats nested payload evasion.
2. **Content-based risk scanning** — 22 detection patterns across 7 risk categories:
   - SQL: DROP, ALTER, CREATE, TRUNCATE, stacked queries
   - Shell injection: metacharacters, process substitution, IFS splitting
   - Path traversal: `../`, URL-encoded variants, null bytes
   - Prompt injection: jailbreak keywords (ignore, DAN, bypass, roleplay) — 17 sub-patterns
   - Sensitive files: `.ssh`, `.aws`, `.kube`, `/etc/passwd`, `.env` (14 paths)
   - Destructive git ops: force push, hard reset
   - Data destruction: `rm -rf`, DROP TABLE, TRUNCATE
3. **Policy validation** — JSON Schema policies compiled via AJV; cacheable.

Performance: 8.3ms median overhead (P99: 23.1ms). 100% block rate on 48 curated attacks. 1.2% false positive rate on benign SQL WHERE clauses.

Three decisions: **allow**, **block**, **pending** (routes to human review — agent fully pauses).

---

### Pattern 4: Rule-based enforcement DSL (\tool / LangChain)
Source: arXiv:2503.18666v1 (fetched live 2026-03-24)

\tool hooks into LangChain's `iter_next_step` at three points:
1. Before action execution (AgentAction) — **pre-execution intercept**
2. After observation (AgentStep)
3. On completion (AgentFinish)

Rules structured as: **Trigger → Check → Enforcement**

Enforcement options: stop execution, user inspection, LLM self-examination, invoke corrective action.

For destructive commands: predicate `is_destructive_cmd` detects "rm" and similar, triggers user inspection. Achieved >90% prevention of unsafe code-agent executions.

---

### Pattern 5: NeMo Guardrails (conversational / input rails)
Source: NVIDIA NeMo-Guardrails GitHub + docs (fetched via search 2026-03-24)

NeMo's approach: **input rails** applied before the LLM generates a tool call. Uses YARA rules (string/binary pattern matching + Boolean logic) for injection detection. Defense-in-depth — designed to complement, not replace, execution-layer intercepts.

Relevant for our system: NeMo handles the *intent* layer (before tool call is emitted). Claude Code hooks handle the *execution* layer (after tool call is emitted but before it runs). These are complementary, not competing.

---

### Pattern 6: Guardrails-AI validator model
Source: guardrails-ai/guardrails GitHub (fetched via search 2026-03-24)

Pre-execution policy checks validate every tool call before execution:
- Confirm user has permission
- Confirm action is allowed in current context
- Confirm request does not violate business rules

100+ community validators available as composable units. LLM-agnostic. Catches issues in the request/response cycle before bad outputs are delivered.

---

## Recommended Implementation

### Tier 1: Global bash intercept hook (implement NOW)
Covers: `rm -rf`, `git push --force`, `git reset --hard`, `git clean`, `git branch -D`, `git checkout .`, `git restore .`, `DROP TABLE`, `TRUNCATE TABLE`, `chmod -R 777`, `mkfs`, `dd if=`

**File:** `~/.claude/hooks/block-destructive-bash.sh`
**Registered in:** `~/.claude/settings.json` under `hooks.PreToolUse` with matcher `"Bash"`

Pattern (assembles mattpocock pattern + Claude Code native JSON denial):
```bash
#!/bin/bash
set -euo pipefail

INPUT=$(cat)
COMMAND=$(echo "$INPUT" | jq -r '.tool_input.command // ""')

DANGEROUS_PATTERNS=(
  'rm\s+-[a-zA-Z]*r[a-zA-Z]*f'   # rm -rf, rm -fr, rm -Rf etc
  'rm\s+--'                        # rm -- (flag terminator tricks)
  'git\s+push.*--force'
  'git\s+push.*-f\b'
  'git\s+reset\s+--hard'
  'git\s+clean\s+-[a-z]*f'
  'git\s+branch\s+-D'
  'git\s+checkout\s+\.'
  'git\s+restore\s+\.'
  'DROP\s+TABLE'
  'DROP\s+DATABASE'
  'TRUNCATE\s+TABLE'
  'chmod\s+-R\s+777'
  '\bdd\s+if='
  '\bmkfs\b'
  '>\s*/dev/sd'
)

for pattern in "${DANGEROUS_PATTERNS[@]}"; do
  if echo "$COMMAND" | grep -qiE "$pattern"; then
    jq -n \
      --arg reason "BLOCKED: Command matches destructive pattern '$pattern'. Requires explicit user authorization in chat before proceeding." \
      '{
        hookSpecificOutput: {
          hookEventName: "PreToolUse",
          permissionDecision: "deny",
          permissionDecisionReason: $reason
        }
      }'
    exit 0
  fi
done

exit 0
```

---

### Tier 2: Project-level hookify rule (contextual — per project)
Covers: project-specific destructive patterns. Follows existing hookify format.

**File:** `[project]/.claude/hookify.block-destructive-bash.local.md`

```yaml
---
name: block-destructive-bash
enabled: true
event: bash
action: block
conditions:
  - field: command
    operator: regex_match
    pattern: "rm\\s+-[a-zA-Z]*r[a-zA-Z]*f|git\\s+push.*--force|git\\s+reset\\s+--hard|DROP\\s+TABLE|TRUNCATE\\s+TABLE"
---

**BLOCKED: Destructive bash command intercepted.**

This command matches a pattern known to cause irreversible damage:
- `rm -rf` variants
- `git push --force` / `git push -f`
- `git reset --hard`
- `DROP TABLE` / `TRUNCATE TABLE`

**To proceed:**
1. Explain in chat WHY this destructive action is necessary
2. Confirm you have a backup or this is intentional
3. The operator must explicitly authorize: "proceed with [command]"

**Why this rule exists:**
Source: AEGIS (arXiv:2603.12621) — "in most current stacks, once the model emits a tool call,
the framework forwards it with little or no pre-execution mediation, meaning a single crafted
injection can escalate into data destruction or credential leakage before any human is aware."
```

---

### Tier 3: Sensitive file access intercept
Covers: `.ssh`, `.aws`, `.env`, `.kube`, `/etc/passwd` — matches AEGIS category 5

**Separate hook** (don't bundle with bash destructive — different risk type, different escalation path):
```bash
SENSITIVE_PATHS=(
  '\.ssh/'
  '\.aws/'
  '\.kube/'
  '/etc/passwd'
  '/etc/shadow'
  '\.env\b'
  'id_rsa'
  'credentials\.json'
)
```
Decision: `"ask"` (not `"deny"`) — routes to user for approval rather than hard-blocking, since read access to these paths may be legitimate in some workflows.

---

### Architecture Note: Two-layer defense (from NeMo + AEGIS research)
NeMo Guardrails pattern: defense-in-depth means hooks at BOTH layers:
1. **Intent layer** (before tool call emitted) — the hookify rules on `event: stop` and `event: file` we already have
2. **Execution layer** (after tool call emitted, before it runs) — the PreToolUse bash hook above

Our existing hookify rules cover layer 1 for files. The bash intercept hook above adds layer 2 for shell execution. Together they close the architectural hole identified in agents_arcs_hooks_audit_2026-03-24.md.

---

## Citations

| Source | URL | Relevance |
|---|---|---|
| Claude Code Hooks docs | https://code.claude.com/docs/en/hooks | PreToolUse JSON schema, exit codes, permissionDecision field |
| AEGIS (arXiv:2603.12621) | https://arxiv.org/html/2603.12621 | 22-pattern risk scanner, 7 risk categories, 100% block rate on 48 attacks |
| \tool (arXiv:2503.18666v1) | https://arxiv.org/html/2503.18666v1 | DSL-based enforcement, Trigger→Check→Enforcement pattern, >90% unsafe prevention |
| mattpocock/skills | https://github.com/mattpocock/skills/blob/main/git-guardrails-claude-code/scripts/block-dangerous-git.sh | Production Claude Code hook implementation, pattern list |
| NVIDIA NeMo-Guardrails | https://github.com/NVIDIA-NeMo/Guardrails | YARA-rule pattern matching, input rail architecture |
| guardrails-ai | https://github.com/guardrails-ai/guardrails | Pre-execution policy check model, 100+ validators |
| NeMo ACL paper | https://aclanthology.org/2023.emnlp-demo.40.pdf | Peer-reviewed foundation paper for NeMo Guardrails |
