# Agents_Arcs — Local Long-Term Memory Recall Patterns
> Source: Agents_Arcs notebook (1a7bcc9d), session ecc77265, 2026-03-24
> Query by: review-recall Sonnet agent

## 4 Patterns for Local Memory with Semantic Recall

### 1. Vector-Backed Semantic Memory (Qdrant + pgvector)
- "OpenBrain pattern" — database-backed, agents query via MCP
- On save: edge function generates vector embedding + metadata
- On recall: semantic search by meaning, not keywords
- Stack: Qdrant (vector search) + Neo4j (relationships) + PostgreSQL (system of record)
- Also: PostgreSQL + pgvector is most frequently recommended

### 2. Local Markdown + Obsidian
- File-based, offline, portable
- Custom TypeScript agents connect to Obsidian directories
- WARNING: writing to markdown from automated agents = "brittle syncing and plumbing friction"
- Better for human use than agent use

### 3. NotebookLM-PI (Agent-Readable RAG)
- NotebookLM = most precise RAG system, low hallucination
- NotebookLM-PI: unofficial Python API for programmatic access
- Agent uploads markdown → queries semantically in future sessions
- WE ARE ALREADY USING THIS via MCP (24 notebooks)

### 4. MCP as Search Interface (The Key Pattern)
- NEVER dump files into context window — causes signal dilution, context rot, degraded reasoning
- MCP server + vector store = agent fetches only relevant chunks
- Keep default context nearly empty, query on demand
- This is the bridge between local files and semantic recall

## Application to OpenBrainLM
- We have pattern 3+4 (NotebookLM MCP)
- Missing: local research/ files aren't semantically queryable
- Quick fix: research/INDEX.md routing table (topic → file mapping)
- Proper fix: vectorize into Qdrant/Pinecone, expose via MCP
- Also available: Pinecone MCP already installed as plugin
