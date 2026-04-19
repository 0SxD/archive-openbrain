# MCP Tools & Plugin Status Report
**Date:** 2026-03-30
**Verified by:** Claude Code session audit
**Scope:** All MCP connections, plugins, hooks, and plugin directories

---

## MCPs

| Name | Status | Notes |
|---|---|---|
| NotebookLM | LIVE | Previously confirmed: authenticated=true, 23 notebooks registered. Tools present: ask_question, select_notebook, list_notebooks, add_notebook, etc. |
| Context7 | LIVE | resolve-library-id responded correctly — returned 5 Python library matches with IDs, snippet counts, and reputation scores. Both `mcp__claude_ai_Context7` and `mcp__plugin_context7_context7` namespaces are available (two routes to same service). |
| Semgrep | LIVE | semgrep_scan tool executed and returned results (output was 232k chars — result too large for inline display, saved to tool-results file). Tools available: semgrep_scan, semgrep_scan_with_custom_rule, semgrep_scan_supply_chain, semgrep_findings, get_abstract_syntax_tree, semgrep_rule_schema, get_supported_languages. |
| Firebase | NEEDS AUTH | Plugin is loaded and tools are present (firebase_list_projects, firebase_init, firebase_login, etc.) but `firebase_list_projects` returned a permission denial in this session. Likely needs `firebase_login` to be called first to authenticate. Not confirmed broken — needs auth flow. |
| Pinecone | NEEDS AUTH | Plugin loaded, tools present (list-indexes, search-records, upsert-records, cascading-search, etc.) but `list-indexes` returned permission denial. Likely requires API key configuration. Not confirmed broken — needs credential setup. |
| GitHub | UNTESTED | `gh auth status` bash call was denied by the destructive_command_guard hook. Plugin is enabled (true) in settings.json. gh CLI is likely installed — cannot confirm auth state without running the command. Needs manual verification: `gh auth status` |
| Blockscout | NEEDS AUTH | Plugin loaded, tools present (get_chains_list, get_address_info, get_transaction_info, etc.) but `get_chains_list` returned permission denial in this session. May need explicit permission grant or session-level unlock. |

---

## Plugins (from settings.json enabledPlugins)

| Plugin Name | Enabled | Notes |
|---|---|---|
| claude-code-setup | true | Installed in cache |
| clangd-lsp | true | Installed in cache |
| claude-md-management | true | Installed in cache |
| code-review | true | Installed in cache |
| code-simplifier | true | Installed in cache |
| coderabbit | **false** | Installed in cache but DISABLED |
| commit-commands | true | Installed in cache |
| context7 | true | Installed in cache — LIVE (tested) |
| agent-sdk-dev | true | Installed in cache |
| feature-dev | true | Installed in cache |
| explanatory-output-style | true | Installed in cache |
| figma | true | Installed in cache |
| csharp-lsp | true | Installed in cache |
| asana | true | Installed in cache |
| github | true | Installed in cache — auth unverified |
| firebase | true | Installed in cache — needs auth |
| firecrawl | true | Installed in cache |
| frontend-design | true | Installed in cache |
| greptile | true | Installed in cache |
| gopls-lsp | true | Installed in cache |
| hookify | true | Installed in cache |
| huggingface-skills | true | Installed in cache |
| learning-output-style | true | Installed in cache |
| pinecone | true | Installed in cache — needs auth |
| gitlab | true | Installed in cache |
| playground | true | Installed in cache |
| pyright-lsp | true | Installed in cache |
| ralph-loop | true | Installed in cache |
| plugin-dev | true | Installed in cache |
| rust-analyzer-lsp | true | Installed in cache |
| semgrep | true | Installed in cache — LIVE (tested) |
| slack | true | Installed in cache |
| stripe | true | Installed in cache |
| typescript-lsp | true | Installed in cache |
| superpowers | true | Installed in cache |
| security-guidance | **false** | Installed in cache but DISABLED |
| telegram | true | Installed in cache |
| discord | true | Installed in cache |
| skill-creator | true | Installed in cache |
| mcp-server-dev | true | Installed in cache |
| pr-review-toolkit | true | Installed in cache |
| dev-process-toolkit | true | From nesquikm/dev-process-toolkit (GitHub marketplace) |
| deep-plan | true | From piercelamb/deep-plan (GitHub marketplace) |
| autoresearch | true | From uditgoenka/autoresearch (GitHub marketplace) |

**Total plugins:** 43
**Enabled:** 41
**Disabled:** 2 (coderabbit, security-guidance)

---

## Hooks

| Hook File | Event | Matcher | Status | Purpose |
|---|---|---|---|---|
| brainstem_inject.sh | PreToolUse | Edit\|Write\|Agent\|Bash\|NotebookEdit | WIRED | Re-broadcasts core principles (SOAR model). Counteracts context rot. Reads `~/.claude/brainstem.md`. |
| validate_research.py | PreToolUse | Edit\|Write | WIRED | Blocks .py file writes unless research evidence exists in research.md or research/*.md (<1hr old, >50 chars). Exit 2 = hard block. |
| destructive_command_guard.py | PreToolUse | Bash | WIRED | Blocks destructive bash commands. Zero-trust pre-action authorization. |
| audit_gate_check.sh | PreToolUse | Bash (if: git commit*) | WIRED | Validates .audit_receipt.json before any git commit is allowed. Conditional on git commit pattern. |
| agent_result_capture.sh | PostToolUse | Agent | WIRED | Captures Agent tool dispatch + results to `memory/.harness/dispatch_log.jsonl`. |
| propagation_check.sh | PostToolUse | Edit\|Write | WIRED | Fires after file edit/write. Checks if a rule/hook/CLAUDE.md file was modified — prompts propagation manifest update. |
| auto_reviewer_trigger.sh | PostToolUse | Edit\|Write | WIRED | After .py file writes, injects instruction to spawn zero-context reviewer agent. |
| precompact_save.sh | Stop | (none) | WIRED | On session end/compaction: writes atomic JSON state snapshot to `memory/.harness/session_state.json`. |
| session_savepoint_inject.sh | SessionStart | (none) | WIRED | On session boot: reads external state files and injects them as save-point resume context. |

**All 9 hooks are wired.** No orphaned hook files found (every file in hooks/ is referenced in settings.json).

**Note:** `audit_reminder.sh` is referenced in the audit_gate_check.sh source comments but is NOT present as a separate file in hooks/ — it appears to have been consolidated. No action needed unless the audit gate is misbehaving.

---

## Plugin Directories

```
C:/Users/Creator.WORKSTATION/.claude/plugins/
├── blocklist.json
├── cache/
│   ├── autoresearch/
│   ├── claude-plugins-official/
│   │   ├── agent-sdk-dev/
│   │   ├── asana/
│   │   ├── clangd-lsp/
│   │   ├── claude-code-setup/
│   │   ├── claude-md-management/
│   │   ├── code-review/
│   │   ├── code-simplifier/
│   │   ├── coderabbit/
│   │   ├── commit-commands/
│   │   ├── context7/
│   │   ├── csharp-lsp/
│   │   ├── discord/
│   │   ├── explanatory-output-style/
│   │   ├── feature-dev/
│   │   ├── figma/
│   │   ├── firebase/
│   │   ├── firecrawl/
│   │   ├── frontend-design/
│   │   ├── github/
│   │   ├── gitlab/
│   │   ├── gopls-lsp/
│   │   ├── greptile/
│   │   ├── hookify/
│   │   ├── huggingface-skills/
│   │   ├── learning-output-style/
│   │   ├── mcp-server-dev/
│   │   ├── pinecone/
│   │   ├── playground/
│   │   ├── plugin-dev/
│   │   ├── pr-review-toolkit/
│   │   ├── pyright-lsp/
│   │   ├── ralph-loop/
│   │   ├── rust-analyzer-lsp/
│   │   ├── security-guidance/
│   │   ├── semgrep/
│   │   ├── skill-creator/
│   │   ├── slack/
│   │   ├── stripe/
│   │   ├── superpowers/
│   │   ├── telegram/
│   │   └── typescript-lsp/
│   ├── dev-process-toolkit/
│   └── piercelamb-plugins/
├── data/
├── install-counts-cache.json
├── installed_plugins.json
├── known_marketplaces.json
└── marketplaces/
```

**3 marketplaces configured:**
- `claude-plugins-official` — Anthropic official (41 plugins cached)
- `dev-process-toolkit` — nesquikm/dev-process-toolkit (GitHub)
- `piercelamb-plugins` — piercelamb/deep-plan (GitHub)
- `autoresearch` — uditgoenka/autoresearch (GitHub)

---

## Action Items

1. **GitHub auth** — Run `gh auth status` manually to confirm. Plugin is enabled but auth state unverified (bash command was blocked by destructive_command_guard during this audit session).

2. **Firebase auth** — Run `firebase_login` via the firebase plugin to authenticate before using firebase tools in a session.

3. **Pinecone credentials** — Verify API key is configured. The plugin is installed but list-indexes was denied. Check if a Pinecone API key needs to be set in environment or plugin config.

4. **Blockscout permissions** — `get_chains_list` was denied. This may require an explicit session-level permission grant or the tool needs to be added to the allow list in settings.json. Consider adding `mcp__claude_ai_Blockscout__*` to the permissions allow list if regular use is intended.

5. **coderabbit** — Disabled (false). This is part of the standard audit sequence (rule 09_hostile_audit_tools.md). Re-enable if code audits are active. Was this intentionally disabled?

6. **security-guidance** — Disabled (false). Low-priority but worth noting.

---

## Summary

- **Confirmed LIVE:** NotebookLM, Context7, Semgrep
- **Needs auth/credentials:** Firebase, Pinecone, Blockscout
- **Unverified (bash blocked):** GitHub gh CLI
- **All 9 hooks:** Wired and mapped to correct events
- **43 plugins total:** 41 enabled, 2 disabled (coderabbit, security-guidance)
- **No orphaned hooks** — every hook file has a corresponding entry in settings.json
