---
name: notebooklm-research
description: Repeatable pattern for conducting NotebookLM research via Gemini handoff. Use when research needs to go through a NotebookLM corridor.
---

# NotebookLM Research Pattern

## When to use
- Creator assigns a research corridor that involves a NotebookLM notebook
- Any research question that should be grounded in notebook sources
- Cross-referencing findings against curated notebook content

## The Pattern

### Step 1: Identify the corridor
ASK Creator which notebook. Never assume. Record the notebook URL.

### Step 2: Write the prompts
For each research question:
1. Write the context isolation preface: "You are NOT talking about the same project. Focus ONLY on third-party sources. Do NOT rely on user-uploaded material."
2. Write the question — specific, one topic per question
3. Specify number of turns (default: 3 per topic)
4. Group related questions to use same session

### Step 3: Create handoff file
Write prompts to `research/gemini_handoff_{date}.md` with:
- Context section (what Gemini needs to know)
- Numbered questions per notebook
- Output location (where to save responses)

### Step 4: Track in notebooklm_brain.md
Update `memory/notebooklm_brain.md` with:
- Which notebook was queried
- What questions were asked
- Status (pending/complete)
- Date

### Step 5: Audit returns
When Gemini saves results to `research/`:
- Read the research file
- Verify claims have citations
- Flag anything without a third-party source
- Consolidate key findings to relevant project brain's memory
- Update notebooklm_brain.md status

## Rules
- NotebookLM MCP = orchestrator only (rule 10). No subagents.
- Gemini handles queries for now (native Google auth)
- Max 1-2 questions per query turn (more = compressed answers)
- Same session_id for follow-ups (builds context)
- Source hierarchy: arXiv → top-tier academic → open source GitHub
