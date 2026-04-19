## NotebookLM — Orchestrator Only (No Subagents)

NotebookLM MCP tools stay with the orchestrator session ONLY. Never dispatch subagents to query NotebookLM.

### Why (Gemini research, 2026-03-25):
- All community MCP servers for NotebookLM are Playwright web scrapers — no public API exists
- Subagents can't handle headless Chromium (sandboxed, permission fails)
- Auth cookies rot quickly under Google bot detection
- 15-30s latency per query (browser boot → load → type → wait for DOM)

### Pattern:
- Orchestrator (Opus/OpenBrainLM session) owns the NotebookLM MCP tool
- If a subagent needs notebook research: give Creator the prompts, or query from orchestrator
- Gemini handles NotebookLM queries for now (faster, native Google auth)
- Future: local RAG over source PDFs (Chroma/FAISS) OR Enterprise API if available

### Relay pattern (if we must use MCP from Claude):
- Subagent requests research via shared file or message
- Orchestrator queries NotebookLM
- Orchestrator passes results back to subagent
- Subagent never touches the MCP tool directly

### ASK corridor first:
Before ANY NotebookLM query, ASK Creator which notebook. Default = ASK, not assume.
