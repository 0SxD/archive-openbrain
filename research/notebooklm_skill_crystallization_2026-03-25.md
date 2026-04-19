# Skill Crystallization & Knowledge Persistence Research
**Date:** 2026-03-25
**Source:** Gemini via Agents_Arcs NotebookLM
**Status:** RECEIVED — awaiting Claude audit

---

## Formalizing Repeatable Agent Workflows into Persistent Skills

### The Folder Architecture
A skill is a directory (e.g., `.claude/skills/skill-name/`) with:
- **`skill.md`** — Core "signpost" file with sequential checklist and decision trees
- **`scripts/`** — Pre-written code (Python, Bash). Agent RUNS the script, doesn't regenerate it.
- **`references/` & `assets/`** — Context docs, templates, guidelines

### Token Efficiency via Progressive Disclosure
- Skills use YAML front matter (name, description, allowed tools)
- At session start, agent only reads the tiny front matter
- Full body loads ONLY when user's prompt matches the description
- Prevents context window degradation from loading all rules at once

### Creation via Execution
- Execute workflow manually with AI first
- Then use a "skill creator" tool to package the interaction into a reusable skill folder
- Captures scripts, formatting, and decision logic automatically

---

## Knowledge Crystallization in Multi-Agent Systems

### Intent Crystallization and Semantic Commits
- Ambiguous tasks have intent that "crystallizes" over conversation
- Once crystallized: document into a **semantic commit** — permanent artifact recording goals, trade-offs, failure conditions
- Future agents don't have to guess project purpose

### Schema-Driven Compaction
- Naive summarization strips constraints → "glossy soup"
- Force agents to extract into rigid schema fields
- Preserves edge cases and semantics

### Persistent Expertise and Memory Files
- Agents read/write structural files (memory.md, expertise logs)
- "Update in place, replace outdated info" on corrections
- Creates self-improving loop

### Repository as System of Record
- Knowledge crystallized INTO the codebase, not hidden in agent memory
- "Golden principles" encoded as permanent documentation
- Background agents scan for deviations and police automatically
- Source: OpenAI Codex architecture pattern
