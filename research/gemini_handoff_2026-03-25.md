# Gemini Research Handoff — 2026-03-25
> From: Claude Code (OpenBrainLM orchestrator)
> To: Gemini (Antigravity / local IDE)
> Purpose: NotebookLM research that Claude can't do (MCP auth broken)

---

## CONTEXT FOR GEMINI

You are helping Creator with the OpenBrainLM project — a brain harness for LLMs. The system uses:
- **Trinity dialectic** (Ethos/Logos/Pathos) for decision-making
- **Memory files** (short_term.md, long_term.md, decisions.md, connections.md) per project
- **3 active projects:** OpenBrainLM (brain itself), Trading Bot 2026, NautilusTrader
- **Orchestration:** OpenBrainLM session runs first, dispatches up to 2 agents
- **Code review:** semgrep + coderabbit plugins available in Claude Code
- **NotebookLM:** 23 notebooks as archival/research brain regions

Claude Code handles deep reasoning, agent dispatch, and memory. Gemini handles UI, architecture validation, and NotebookLM research.

---

## RESEARCH TASK 1: Agents_Arcs Notebook
**URL:** https://notebooklm.google.com/notebook/1a7bcc9d-4397-4d6b-8fb2-d85ab86363ce

Preface EVERY question with: "You are NOT talking about the same project. Focus ONLY on third-party sources and best practices. Do NOT rely on any user-uploaded material."

### Questions (ask one at a time, use same session):

1. How should an AI agent system retain memories across MULTIPLE projects and MULTIPLE sessions? Centralized vs distributed memory — what do academic papers and industry frameworks recommend? Cite sources.

2. Trade-offs of centralized brain (one store for all projects) vs distributed brains (each project owns its memory)? Which scales? Which prevents cross-contamination? For 3-5 active projects?

3. Multiple concurrent agent sessions vs single orchestrator session — when does parallelism help vs hurt? How to prevent drift between concurrent sessions sharing project state?

4. (Claude Code specific) Managing multiple Claude Code session windows — one as orchestrator, others for project work. Patterns for coordinating via shared files, memory files, git state?

5. (Claude Code specific) Memory persistence across sessions when context compresses. System uses markdown files read at startup. Right pattern? Consolidation — when, how often, what schema?

6. Best practices for using automated code review tools (semgrep, coderabbit) as part of an agent self-audit loop. Should these run locally via CLI plugins, through GitHub Actions/CI, or both? How to integrate into a hostile audit pattern where one agent checks another's work?

7. For a multi-project workspace using GitHub — what's the recommended CI/CD audit pipeline? When should semgrep run (pre-commit, PR, post-merge)? How to version audit results alongside code?

---

## RESEARCH TASK 2: Strategy/Audit Notebook
**URL:** https://notebooklm.google.com/notebook/9e81e17d-99a8-4898-8e38-705cb75124c3

Same preface on every question.

### Topic A: Naming Standards (3 questions)
A1. Best practices for naming files, scripts, research outputs, and memory files in a multi-project AI workspace? Versioning conventions, date formats, folder structures. Third-party sources.

A2. How should an AI brain system name and structure memory files across multiple projects? (short_term.md, long_term.md, decisions.md, connections.md) — is this right? What would industry recommend?

A3. How to enforce naming standards automatically — linters, hooks, what tools exist?

### Topic B: Dual-Stage Directory Containment (3 questions)
B1. How to ensure files are audited before being filed permanently. Staging → verified → archived. Best practices.

B2. What patterns prevent lost/misplaced files across projects? How to track current vs archived versions?

B3. How to use checksums (SHA256) and audit logs to verify file integrity across versions?

### Topic C: Self-Checking in Dialectic Loops (3 questions)
C1. When an AI agent uses code review plugins (semgrep, coderabbit) to audit itself within a dialectic loop (Trinity: Ethos/Logos/Pathos), how should it structure the self-check?

C2. How to prevent the checker from being contaminated by the same errors? Separation of concerns in self-audit.

C3. What do sources say about AI agents verifying their own outputs? Minimum viable audit for a code change before it's trusted?

---

## BONUS: NotebookLM MCP Fix

The NotebookLM MCP server in Claude Code shows `authenticated: false`. It uses headless Playwright browser automation. `setup_auth` opens a browser for Google login but keeps failing. Can you help troubleshoot? Options:
- Close all Chrome instances → cleanup_data → setup_auth
- Check if cookies directory is corrupted
- Check if Google account has 2FA blocking headless auth
- Consider: should we create a dedicated "OpenBrainLM Brain" notebook in NotebookLM where all architecture decisions and memory patterns get stored?

---

## OUTPUT

Save all research responses to: `<WORKSPACE>\OpenBrainLM\research\`
- `notebooklm_agents_arcs_research_2026-03-25.md` — Task 1 results
- `notebooklm_naming_standards_research_2026-03-25.md` — Task 2 results

Claude will read these files, audit the findings, and consolidate to memory.
