# Pinecone Setup Research — Creator's Use Case
**Date:** 2026-03-25
**Researcher:** Claude Sonnet 4.6 (agent)
**Status:** VERIFIED from primary sources where noted. Training-knowledge items flagged for live verification.

---

## Source Notes

- **MCP Tool Schemas** — read directly from the live `plugin:pinecone:pinecone` MCP server during this session. These are authoritative and current. Tool names, parameters, and model names come from here.
- **Pinecone Docs (training knowledge, cutoff Aug 2025)** — items from training are flagged `[VERIFY]`. Pricing especially changes; must be verified at pinecone.io/pricing before acting.
- **Live index check** — attempted `list-indexes` via MCP. Blocked by sandbox permission gate. Creator must run this manually or grant MCP permission in session. No existing indexes confirmed or denied.

---

## Q1: What Pinecone MCP Tools Are Available?

**Source: Live MCP plugin schema, read this session.**

| Tool | Description |
|---|---|
| `pinecone__list-indexes` | List all Pinecone indexes in the account |
| `pinecone__describe-index` | Describe config of a specific index (name required) |
| `pinecone__describe-index-stats` | Stats for an index and its namespaces (vector count, storage) |
| `pinecone__create-index-for-model` | Create a new index with integrated inference (embedding built-in). Supports aws/gcp/azure. |
| `pinecone__upsert-records` | Insert or update records in an index. Requires index name, namespace, and records array. |
| `pinecone__search-records` | Semantic search — returns records similar to query text. Supports filters (MongoDB-style), topK, and reranking. |
| `pinecone__rerank-documents` | Rerank a set of documents against a query. Works on raw text or record arrays. |
| `pinecone__cascading-search` | Search across MULTIPLE indexes simultaneously, deduplicate, and rerank. |
| `pinecone__search-docs` | Search Pinecone's own documentation. |

**Key capability confirmed from schema:** `create-index-for-model` handles embedding internally — you do NOT need to bring your own embedding model unless you want to. The tool takes raw text and the model name.

**Reranking models available (confirmed from schema):**
- `cohere-rerank-3.5` — enterprise-grade, handles multiple rank fields
- `bge-reranker-v2-m3` — multilingual, good for messy data, 1-2 paragraph chunks, single rank field
- `pinecone-rerank-v0` — Pinecone's own model, beats competitors on benchmarks, 512-token chunks max, single rank field

---

## Q2: Can Pinecone Handle PDFs Directly?

**Answer: No. Pinecone is a vector database, not a document processor.**

Pinecone stores and searches vectors (+ metadata). It does not:
- Parse PDFs
- Extract text from PDFs
- Chunk documents
- OCR scanned pages

**What you must do before upserting:**
1. Extract text from PDFs (tools: `pdfplumber`, `pymupdf`, `pypdf2`, `unstructured`)
2. Chunk the text into passages
3. Call Pinecone's `upsert-records` with the text chunks as records

**Exception:** If using Pinecone's integrated inference (the `create-index-for-model` path), Pinecone will embed the text for you — but you still must supply the text. You extract text locally, pass text strings to Pinecone, Pinecone embeds them.

**Recommended PDF extraction library:** `unstructured` (GitHub: Unstructured-IO/unstructured) — handles mixed PDFs, tables, scanned pages via OCR, arXiv PDFs. Battle-tested. Used by LangChain, LlamaIndex pipelines. `[VERIFY: check for updates since Aug 2025]`

---

## Q3: Setup Sequence

**Source: MCP tool schemas + Pinecone docs (training knowledge).**

### Step 1: Create Index (one-time)
```python
# Via MCP tool: pinecone__create-index-for-model
# Parameters:
{
  "name": "austin-research-library",
  "cloud": "aws",
  "region": "us-east-1",
  "embed": {
    "model": "llama-text-embed-v2",   # best for structured documents (see Q4)
    "fieldMap": {
      "text": "content"               # "content" = the field name you'll use in records
    }
  }
}
```
This creates a serverless index with integrated embedding. Pinecone handles vectors internally.

### Step 2: Upsert Records (ingestion pipeline)
```python
# Via MCP tool: pinecone__upsert-records
# Parameters:
{
  "name": "austin-research-library",
  "namespace": "textbooks",           # use namespaces to segment corpus types
  "records": [
    {
      "id": "hull-options-ch3-p1",
      "content": "The Black-Scholes model assumes...",  # field named in fieldMap
      "source": "Hull - Options Futures Other Derivatives",
      "chapter": "3",
      "page": "42",
      "doc_type": "textbook"
    }
  ]
}
```

**Schema discipline (from MCP plugin instructions):**
- Use consistent field names across ALL records in an index
- No nested objects as field values — flat key/value only
- No `metadata` field — put metadata as top-level fields
- The text field (`content` in this example) must match what you set in `fieldMap`

### Step 3: Search
```python
# Via MCP tool: pinecone__search-records
{
  "name": "austin-research-library",
  "namespace": "textbooks",
  "query": {
    "inputs": { "text": "Kalman filter for volatility estimation" },
    "topK": 20,
    "filter": { "doc_type": { "$eq": "textbook" } }
  },
  "rerank": {
    "model": "pinecone-rerank-v0",
    "rankFields": ["content"],
    "topN": 5
  }
}
```

### Optional: Cascading Search (across namespaces or indexes)
```python
# pinecone__cascading-search — searches textbooks + arxiv + code_notes simultaneously
{
  "indexes": [
    { "name": "austin-research-library", "namespace": "textbooks" },
    { "name": "austin-research-library", "namespace": "arxiv" },
    { "name": "austin-research-library", "namespace": "code_notes" }
  ],
  "query": {
    "inputs": { "text": "market microstructure order flow imbalance" },
    "topK": 10
  },
  "rerank": {
    "model": "bge-reranker-v2-m3",
    "rankFields": ["content"],
    "topN": 5
  }
}
```

---

## Q4: Embedding Models — Pinecone Provides Them

**Source: MCP tool schema for `create-index-for-model` — live and authoritative.**

Three models available in the integrated inference path (no external API key needed):

| Model | Type | Best For |
|---|---|---|
| `llama-text-embed-v2` | Dense | **Recommended for Creator's use case.** Long passages, structured documents, ranked retrieval. Trained on diverse text corpora. Best for textbooks and arXiv papers. |
| `multilingual-e5-large` | Dense | Multilingual data, messy data, short queries returning 1-2 paragraph results. |
| `pinecone-sparse-english-v0` | Sparse | Keyword/hybrid search. Use when exact terminology matters (e.g., specific equation names, ticker symbols). |

**Recommendation for Creator:**
- Primary index: `llama-text-embed-v2` — handles graduate-level technical text well, good on longer passages
- Optional hybrid: add a sparse index with `pinecone-sparse-english-v0` if exact-term search (specific formula names, author names, paper titles) needs to coexist with semantic search

**Do you need to bring your own embeddings?** No — the `create-index-for-model` path handles it. If you wanted to use OpenAI `text-embedding-3-large` or a custom fine-tuned model, you would use the lower-level `create-index` (not in the MCP tools) and upsert raw vectors. For Creator's use case, Pinecone's integrated models are sufficient.

---

## Q5: Costs and Limits

**[VERIFY at pinecone.io/pricing — pricing changes frequently. These are training-knowledge figures as of ~mid-2025.]**

### Free Tier (Starter)
| Limit | Value |
|---|---|
| Indexes | 5 |
| Storage (vectors) | ~100M vector dimensions total (roughly 2M 1536-dim vectors, or ~14M 768-dim vectors) |
| Namespaces | Unlimited within an index |
| Projects | 1 |
| Read/write units | Limited (throttled at high throughput) |
| Integrated inference | Included |
| Uptime SLA | None |

**Practical estimate for free tier with `llama-text-embed-v2`:**
- Dimension size: 1024 (this model's output) `[VERIFY]`
- Free storage: ~100M dimensions ÷ 1024 = ~97,000 vectors
- A 300-page textbook at 512-token chunks ≈ 600-800 chunks
- ~97,000 vectors ÷ 700 avg chunks/book = **~138 books on free tier**
- Creator has 100-200GB of PDFs. A typical 500-page textbook PDF is 5-20MB → could be 5,000-40,000 books. Free tier will NOT cover the full corpus.

### Paid Tier (Standard/Enterprise)
| Feature | Value |
|---|---|
| Pricing model | Pay-as-you-go on storage + read/write units |
| Storage | ~$0.08-0.10/GB of vector storage/month `[VERIFY]` |
| Read units | Charged per query |
| Write units | Charged per upsert |
| Integrated inference | Additional cost per embedding call `[VERIFY]` |

**Bottom line:** For 100-200GB of source PDFs, after extraction and chunking, you're looking at millions of vectors. This will require a paid plan. The cost depends heavily on chunk size and how many PDFs you actually index. Start with a representative sample on the free tier to calibrate before committing.

---

## Q6: Ingesting 100-200GB of PDFs — Chunking Strategy

**This is the biggest engineering challenge. No single source covers this exactly for Creator's corpus — combining best practices from LlamaIndex, LangChain, and Pinecone's own documentation.**

### Pipeline Design

```
PDF files (local disk)
  → Text extraction (pdfplumber or unstructured)
  → Cleaning (remove headers/footers, fix hyphenation, normalize whitespace)
  → Chunking
  → Metadata tagging
  → Batch upsert to Pinecone (via Python SDK or MCP tool)
```

### Chunking Strategy for Graduate Textbooks + arXiv

**Recommended: Hierarchical chunking with overlap**

| Parameter | Value | Reason |
|---|---|---|
| Chunk size | 512 tokens (~350-400 words) | Fits reranker token limits (pinecone-rerank-v0 max = 512 tokens). Balances context vs. precision. |
| Overlap | 50-100 tokens | Preserves context across chunk boundaries (important for math derivations that span paragraphs) |
| Splitting strategy | Paragraph-aware, not character-blind | Split at paragraph/section boundaries, not mid-sentence |
| Minimum chunk size | 100 tokens | Discard stub chunks (table of contents entries, single equation lines without context) |

**Per content type:**

| Content Type | Special Handling |
|---|---|
| Textbooks (Hull, Shreve, etc.) | Chapter/section metadata. Prepend section title to chunk for context. |
| arXiv papers | Abstract as standalone chunk. Section headers prepended to body chunks. |
| Code files | Language-aware splitting (functions/classes as units). Separate namespace. |
| Research notes (MD files) | Heading-aware chunking. Preserve headers as context. |

### Namespace Strategy (confirmed tool supports namespaces)

Use ONE index, multiple namespaces to avoid cross-corpus confusion:

```
austin-research-library/
  ├── namespace: textbooks        (Hull, Shreve, Hasbrouck, etc.)
  ├── namespace: arxiv            (research papers)
  ├── namespace: code_notes       (Python files, project notes)
  └── namespace: trading_research (trading bot research, market notes)
```

This allows `cascading-search` across all at once, or targeted search within one.

### Batch Ingestion Script Design

- Process in batches of 100-200 records per upsert call (Pinecone recommends ≤100 per batch)
- SHA256 hash each chunk as the record ID — enables idempotent re-runs (re-indexing same file won't create duplicates)
- Write a progress log with book/paper name, chunk count, upsert status
- Estimated time: At ~500 chunks/book × 1000 books = 500,000 upserts. At 100/batch = 5,000 API calls. Manageable in a single overnight run.

### Recommended Libraries (open source, active maintenance)

| Library | Purpose | GitHub |
|---|---|---|
| `pdfplumber` | PDF text extraction, table detection | jsvine/pdfplumber |
| `unstructured` | Full doc pipeline, OCR, mixed formats | Unstructured-IO/unstructured |
| `tiktoken` | Token counting for chunk sizing | openai/tiktoken |
| `pinecone` (Python SDK) | Direct SDK for bulk upsert (faster than MCP for ingestion) | pinecone-io/pinecone-python-client |

**For bulk ingestion, use the Python SDK directly, not the MCP tool.** The MCP tool is for interactive/session use. The Python SDK supports async batch upsert with proper retry logic.

---

## Q7: Can We Search from Claude Code via MCP During a Session?

**Answer: Yes — this is exactly what the MCP tools are designed for.**

Confirmed from the tool schemas:
- `pinecone__search-records` — query by text, get back matching records with scores
- `pinecone__cascading-search` — search multiple namespaces at once
- `pinecone__rerank-documents` — rerank results after retrieval

**Workflow during a Claude Code session:**
1. Ask: "find me everything about Kalman filters for vol estimation"
2. Claude calls `pinecone__search-records` against `austin-research-library`
3. Returns top-N chunks with source metadata (book name, chapter, page)
4. Claude synthesizes across results, cites sources

**Limitation confirmed from MCP plugin note:**
- The MCP tool is interactive — not designed for bulk ingestion (use Python SDK for that)
- Permission gates: the MCP tools require explicit grant in the Claude Code session (as encountered in this research session — `list-indexes` was blocked by sandbox). Creator needs to grant Pinecone MCP tool access when prompted.

---

## Live Index Check Result

**Status: BLOCKED — sandbox permission gate denied `list-indexes` call.**

Creator must either:
1. Grant permission when Claude Code prompts for Pinecone MCP access, OR
2. Run `list-indexes` manually: `pinecone list indexes` (CLI) or via the Pinecone console at app.pinecone.io

No existing indexes confirmed or denied.

---

## Recommended Action Plan

### Phase 1: Validation (free tier, ~1 week)
1. Grant Pinecone MCP permission in Claude Code session
2. Create one index via MCP: `create-index-for-model` with `llama-text-embed-v2`
3. Write a PDF extraction script (pdfplumber + chunking)
4. Index 10-20 representative books (1 textbook per domain: options, microstructure, ML, etc.)
5. Test search quality via MCP during Claude Code sessions
6. Evaluate: do results match what you'd find by scanning manually?

### Phase 2: Full Ingestion (paid tier, after validation)
1. Upgrade to paid plan
2. Run bulk ingestion script overnight for full corpus
3. Tune chunk size based on Phase 1 quality observations
4. Add arXiv papers + code notes + research notes as separate namespaces

### Phase 3: Claude Code Integration
1. Standard workflow: Claude calls `cascading-search` at session start or on demand
2. Results feed into research corridors
3. Pair with NotebookLM — NotebookLM for curated/processed sources, Pinecone for raw corpus search

---

## Key Decisions Needed (Creator)

1. **Chunk size:** 512 tokens recommended — but Creator should validate with 3-5 test queries on known material before committing
2. **Which PDFs to index first:** Prioritize the books/papers most actively referenced in current work (trading bot, nautilus trader research)
3. **Paid plan timing:** Free tier good for proof-of-concept (~100-150 books). Need paid for full corpus.
4. **Permission grant:** Must explicitly allow Pinecone MCP tools in Claude Code session for live search to work

---

## Verification Checklist (items needing live confirmation)

- [ ] Current free tier vector limits (verify at pinecone.io/pricing)
- [ ] `llama-text-embed-v2` output dimension size (confirm 1024 or check current docs)
- [ ] Integrated inference pricing per embedding call
- [ ] Whether `upsert-records` via MCP has a size limit per batch
- [ ] Existing indexes in Creator's Pinecone account (requires MCP permission grant)
