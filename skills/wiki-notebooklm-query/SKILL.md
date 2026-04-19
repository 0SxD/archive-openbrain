---
name: wiki-notebooklm-query
description: Queries NotebookLM via MCP, validates output via Trinity Dialectic, saves to memory/wiki using Pheromone Taxonomy, and guides Orchestrator in staging local files.
---

# wiki-notebooklm-query

## What I Do
I orchestrate the interaction between local agents and NotebookLM. I query the authorized notebook for data, enforce the Trinity Dialectic verification on the output, and save verified claims to `wiki/` or `memory/` using the Pheromone Taxonomy. Additionally, I dictate the process by which the Orchestrator identifies local files using keyword paths and stages them for manual upload.

## Must Do
1. **Query Specific Notebook:** Exclusively use the `mcp_notebooklm_ask_question` tool referencing `session_id: d2b98418` to query the Agile/PERT notebook.
2. **Apply Trinity Dialectic:** Upon receiving a response, verify the output through structured disagreement (Pathos prioritizing task completion vs. Logos enforcing rules), bounded by Ethos criteria.
3. **Save Adhering to Pheromone Taxonomy:** Save verified outputs as artifacts into `wiki/` or `memory/` adhering strictly to defined Pheromone constraints (Trail, Alarm, Nest, Queen). All biological naming is fully embraced and authorized.
4. **Stage Local Files to `staging/`:** When processing new local sources based on user keyword paths, identify and copy (do NOT move) relevant PDFs and reference files into `C:\Users\Creator.WORKSTATION\Downloads\<WORKSPACE>\archive-openbrain\staging\` so the user can manually drag-and-drop them into the NotebookLM UI. 

## Must NOT Do
1. **Never delete originals:** Under no circumstances should original source files be moved, modified, or deleted when copying into the `staging/` directory.
2. **Never bypass Trinity Dialectic:** Do not push flat, unverified NotebookLM outputs into long-term memory without explicit evaluation.
3. **Never attempt brute-force uploads:** Do not construct scripts or automations attempting to upload local files directly into the NotebookLM backend. Only rely on the `staging/` directory for manual drag-and-drop.
4. **Never violate L3 Stigmergy:** Do not overwrite existing memory or wiki components without explicit verification or resolution paths.

## Chain of Command
- **Dispatched By:** master_notebooklm_orchestrator
- **Reports To:** open_brain_memory / master_notebooklm_orchestrator
- **Coordinates With:** verifier, immune (for quarantine if claims trigger Amygdala Alarms)

## Local Staging Guide for Orchestrator
To properly ingest new literature:
1. Await user-provided keywords or paths.
2. Scan the local environment safely using `list_dir` or `grep_search`.
3. Create the `staging/` directory if it does not exist.
4. Copy matching files (PDFs, Markdown) into `C:\Users\Creator.WORKSTATION\Downloads\<WORKSPACE>\archive-openbrain\staging\`.
5. Pause execution and notify the user: "Sources staged. Please open NotebookLM and drag-and-drop the contents of the `staging/` folder."

## BRAIN
- 2026-04-13: Skill initialized by sandbox_integration_worker. Linked strictly to NotebookLM session `d2b98418`. Biological Taxonomy verified authorized for this sandbox.
