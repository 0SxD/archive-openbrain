# AST Execution Guard Research — Session 38
> Research for MLflow Phase 6: preventing accidental top-level engine execution
> Date: 2026-03-27
> Agent: Sonnet research agent

## Finding: Semgrep is the industry-standard tool for this

### Best Option: Semgrep `pattern-not-inside` (CHOSEN)

**Reference implementation:** Flask `app-run-security-config.yaml` in semgrep/semgrep-rules
- URL: https://github.com/semgrep/semgrep-rules/blob/develop/python/flask/security/audit/app-run-security-config.yaml
- Pattern: uses `pattern-not-inside` with `if __name__ == '__main__':` and `def $X(...):`
- Catches top-level `app.run(...)` calls not guarded by main block or function scope
- This is EXACTLY our pattern — just replace `app.run()` with `engine.run()` / `node.run()`

**Exemption mechanism:** `# nosemgrep: <rule-id>` inline comment (standard Semgrep)

### Alternatives Evaluated

| Tool | Rule | Verdict |
|------|------|---------|
| Semgrep | Custom rule with pattern-not-inside | CHOSEN — exact match for our need |
| Ruff | TID253 (banned-module-level-imports) | WRONG — bans imports, not execution calls |
| Ruff | B018 (useless-expression) | WRONG — catches statements with no effect, not function calls |
| Ruff | E402 (module-level-imports) | WRONG — import ordering, not execution |
| pylint | W0104 (pointless-statement) | WRONG — no concept of "guarded by __main__" |
| flake8 | No existing plugin found | NONE — no plugin for __main__ guard enforcement |
| pre-commit | check-ast | WRONG — only checks syntax validity |
| Custom AST hook | Python ast.parse + ast.walk | POSSIBLE but why build when Semgrep exists |

### Implementation

Our rule (in `.semgrep/nt_safety.yml`):
```yaml
- id: nt-no-toplevel-engine-run
  patterns:
    - pattern-not-inside: |
        if __name__ == "__main__":
          ...
    - pattern-not-inside: |
        def $FUNC(...):
          ...
    - pattern-either:
        - pattern: $ENGINE.run(...)
  message: >
    Top-level engine/node .run() detected. Wrap in __main__ guard or function.
  languages: [python]
  severity: WARNING
```

### Semgrep Pre-commit Integration (for future)

Can integrate with git pre-commit:
```yaml
# .pre-commit-config.yaml
repos:
  - repo: https://github.com/semgrep/pre-commit
    rev: 'v1.156.0'
    hooks:
      - id: semgrep
        args: ['--config', '.semgrep/nt_safety.yml', '--error']
```

## Confidence: 0.95
## Source: Semgrep official rules repo, Semgrep docs, web research
## Status: verified
## Last verified: 2026-03-27
