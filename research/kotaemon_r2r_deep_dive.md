# Kotaemon vs R2R Deep Dive -- OpenBrainLM Integration Research

**Date:** 2026-03-21
**Researcher:** ai-researcher (Claude Opus 4.6)
**Purpose:** Evaluate Kotaemon and R2R as RAG backends for OpenBrainLM brain regions
**Status:** RESEARCH ONLY -- no code written

---

## 1. KOTAEMON (github.com/Cinnamon/kotaemon)

**Stars:** 25,234 | **Language:** Python | **License:** Apache-2.0
**Last updated:** 2026-03-21

### 1.1 Architecture: Two Separate Packages

Kotaemon is split into TWO installable packages inside `libs/`:

| Package | Install | Purpose |
|---------|---------|---------|
| `kotaemon` | `pip install -e "libs/kotaemon"` | Core library: embeddings, LLMs, vector stores, doc loaders, indexing/retrieval pipelines |
| `ktem` | `pip install -e "libs/ktem"` | Application layer: Gradio UI, user management, SQLite DB, index manager, reasoning pipelines |

**Critical finding:** The `kotaemon` core library CAN be imported as a standalone Python package without the Gradio UI. The `ktem` layer adds the application shell (UI, auth, collection management via SQL). For OpenBrainLM, we would use `kotaemon` core directly and skip `ktem` entirely, OR selectively import from `ktem` for collection management logic.

### 1.2 Core Package Structure (`libs/kotaemon/kotaemon/`)

```
kotaemon/
  __init__.py
  cli.py
  agents/          # Agent pipelines (ReAct, ReWOO)
  base/            # BaseComponent, Document, Param, Node, schema types
  chatbot/         # Chat interface components
  contribs/        # Community contributions
  embeddings/      # All embedding backends
  indices/         # VectorIndexing, VectorRetrieval, splitters, extractors, QA
  llms/            # All LLM backends (chat, completion, prompts)
  loaders/         # PDF, DOCX, HTML, TXT, Excel, OCR, web loaders
  parsers/         # Document parsers
  rerankings/      # Reranking models
  storages/        # Vector stores + document stores
```

### 1.3 Key Classes and Import Paths

**Base types:**
```python
from kotaemon.base import BaseComponent, Document, DocumentWithEmbedding, RetrievedDocument, Param
```

**Embeddings (local options):**
```python
from kotaemon.embeddings import FastEmbedEmbeddings    # LOCAL -- uses fastembed/ONNX, no GPU needed
from kotaemon.embeddings import LCHuggingFaceEmbeddings # LOCAL -- sentence-transformers
from kotaemon.embeddings import OpenAIEmbeddings        # Cloud (but works with Ollama via base_url)
```

**Vector stores:**
```python
from kotaemon.storages import ChromaVectorStore         # Local, persistent, collection-based
from kotaemon.storages import LanceDBVectorStore        # Local, columnar
from kotaemon.storages import InMemoryVectorStore       # Ephemeral
from kotaemon.storages import MilvusVectorStore         # Local or server
from kotaemon.storages import QdrantVectorStore         # Local or server
```

**Document stores (text storage alongside vectors):**
```python
from kotaemon.storages import LanceDBDocumentStore      # Default
from kotaemon.storages import InMemoryDocumentStore
from kotaemon.storages import ElasticsearchDocumentStore # Full-text search
from kotaemon.storages import SimpleFileDocumentStore
```

**Indexing and retrieval pipelines:**
```python
from kotaemon.indices import VectorIndexing, VectorRetrieval
```

**LLMs (local options):**
```python
from kotaemon.llms import LCOllamaChat    # Ollama backend
from kotaemon.llms import LlamaCppChat    # llama.cpp direct
from kotaemon.llms import LlamaCpp        # llama.cpp completions
from kotaemon.llms import ChatOpenAI      # OpenAI-compatible (works with Ollama endpoint)
```

**Document loaders:**
```python
from kotaemon.loaders import PDFThumbnailReader  # PyMuPDF-based
# Also: docx_loader, html_loader, txt_loader, excel_loader, unstructured_loader
```

**Splitters:**
```python
from kotaemon.indices.splitters import TokenSplitter, SentenceWindowSplitter
```

### 1.4 Multi-Collection Support

**How collections work:** Each `ChromaVectorStore` (or `LanceDBVectorStore`) takes a `collection_name` parameter. Multiple collections = multiple store instances pointing to the same path but different collection names.

```python
# This is how you would create 8 brain region collections:
from kotaemon.storages import ChromaVectorStore, LanceDBDocumentStore

regions = ["active_sensing", "ganglion", "stigmergy", "action_selection",
           "memory", "relevance", "chromatophore", "pathos_dmn"]

stores = {}
for region in regions:
    stores[region] = {
        "vector": ChromaVectorStore(path="./brain_data", collection_name=region),
        "docs": LanceDBDocumentStore(path="./brain_data/docstore", collection_name=region),
    }
```

**The `ktem.index.manager.IndexManager`** handles collection CRUD via SQLAlchemy + SQLite, but it requires the full `ktem` app context (Gradio, settings, etc.). For headless use, you would manage collections directly through the store objects above.

### 1.5 Minimal Headless Integration (Pseudocode)

```python
from kotaemon.base import Document
from kotaemon.embeddings import FastEmbedEmbeddings
from kotaemon.storages import ChromaVectorStore, LanceDBDocumentStore
from kotaemon.indices import VectorIndexing, VectorRetrieval

# 1. Setup local embedding model (no network calls)
embedder = FastEmbedEmbeddings(model_name="BAAI/bge-small-en-v1.5")

# 2. Create a brain region store
vs = ChromaVectorStore(path="./brain_data", collection_name="memory_region")
ds = LanceDBDocumentStore(path="./brain_data/docstore", collection_name="memory_region")

# 3. Build indexing pipeline
indexer = VectorIndexing(
    vector_store=vs,
    doc_store=ds,
    embedding=embedder,
)

# 4. Ingest a document
doc = Document(text="Shu and Mulvey 2024 regime labeling uses state-conditional mean return...")
indexer.run([doc])

# 5. Build retrieval pipeline
retriever = VectorRetrieval(
    vector_store=vs,
    doc_store=ds,
    embedding=embedder,
    top_k=5,
    retrieval_mode="hybrid",  # vector + full-text
)

# 6. Query
results = retriever.run("How does regime labeling work?")
for r in results:
    print(r.text, r.score)
```

### 1.6 Can It Work with ZERO Network Calls?

**YES, with caveats:**
- Embeddings: `FastEmbedEmbeddings` uses ONNX runtime locally, downloads model once then cached
- LLM: `LlamaCppChat` or `LCOllamaChat` (Ollama runs locally)
- Vector store: `ChromaVectorStore` or `LanceDBVectorStore` are fully local
- Doc store: `LanceDBDocumentStore` is fully local
- PDF parsing: `PyMuPDF` is fully local

**What CANNOT be local:** Reranking (Cohere default), some advanced loaders (Azure Doc Intelligence). These are optional.

### 1.7 Dependencies (HEAVY)

Core `kotaemon` pulls in:
- **LlamaIndex 0.10.x** (mandatory, deeply integrated -- splitters, vector store wrappers)
- **LangChain <2** (for LLM wrappers: LCOllamaChat, LCAnthropicChat, etc.)
- **chromadb <=0.5.16** (default vector store)
- **Gradio >=4.31** (even in core library! theflow dependency)
- **openai >=1.23** (for OpenAI-compatible endpoints)
- **PyMuPDF** (PDF parsing)
- **pandas, plotly, matplotlib** (data handling/viz)
- **theflow >=0.8.6** (Cinnamon's own flow framework -- settings, component system)
- **pydantic <=2.10.6**

Optional (`[adv]`):
- `fastembed` + `onnxruntime` (local embeddings)
- `sentence-transformers` (local embeddings)
- `llama-cpp-python` (local LLM)
- `unstructured` (advanced doc parsing)
- `mcp[cli]` (MCP server support)

**Total dependency footprint: LARGE.** LlamaIndex + LangChain + Gradio is a significant install.

### 1.8 Gotchas and Concerns

1. **Gradio in core package.** Even `pip install kotaemon` pulls Gradio as a dependency (through theflow). This is unnecessary for headless library use.
2. **theflow framework.** Cinnamon's own component framework (`theflow`). All components inherit from it. Settings system (`flowsettings.py`) is deeply coupled. May conflict with OpenBrainLM's own component system.
3. **LlamaIndex + LangChain dual dependency.** Kotaemon wraps BOTH. ChromaVectorStore wraps `llama_index.vector_stores.chroma`. LLMs wrap LangChain chat models. This is a lot of abstraction layers.
4. **Collection management requires ktem.** The `IndexManager` that handles collection CRUD needs the full `ktem` app (SQLAlchemy session, Gradio state). Without `ktem`, you manage stores manually (which is actually simpler for our use case).
5. **No standalone "create collection" API.** You just instantiate a new `ChromaVectorStore(collection_name="x")` -- Chroma handles creation automatically.

---

## 2. R2R (github.com/SciPhi-AI/R2R)

**Stars:** 7,737 | **Version:** 3.6.6 | **License:** MIT
**Last updated:** 2026-03-21

### 2.1 Architecture: Client-Server ONLY

**Critical finding: R2R is fundamentally a SERVER application.** It is NOT a library you import.

The architecture:
```
py/
  r2r/          # Server entry point (serve.py, mcp.py)
  core/         # Server-side: providers, parsers, agents, configs
  sdk/          # Client SDK: R2RClient talks to the server via HTTP
  shared/       # Shared models/schemas
```

**How it works:**
1. You start a server: `python -m r2r.serve` (or via Docker)
2. The server runs FastAPI on port 7272
3. You interact via `R2RClient(base_url="http://localhost:7272")`
4. ALL operations go through HTTP REST calls

```python
from r2r import R2RClient
client = R2RClient(base_url="http://localhost:7272")

# Ingest
client.documents.create(file_path="/path/to/file.pdf")

# Search
results = client.retrieval.search(query="regime labeling")

# RAG
response = client.retrieval.rag(query="How does regime labeling work?")
```

### 2.2 Server Dependencies (VERY HEAVY)

Core server (`r2r[core]`) requires:
- **PostgreSQL** (mandatory! `psycopg-binary`, `asyncpg`) -- uses pgvector for embeddings
- **FastAPI** (server framework)
- **litellm** (unified LLM proxy -- supports 100+ providers)
- **hatchet-sdk** (workflow orchestration)
- **openai, anthropic, google-genai, mistralai, ollama** (all LLM providers)
- **networkx** (knowledge graphs)
- **boto3** (AWS S3 storage)
- Plus: bcrypt, gunicorn, firecrawl, etc.

**No SQLite option. PostgreSQL is mandatory.**

### 2.3 Multi-Collection Support

R2R calls them "collections":
```python
# Create collection (via HTTP)
client.collections.create(name="memory_region", description="Brain region: memory")

# Add document to collection
client.documents.create(file_path="doc.pdf", collection_id="<uuid>")

# Search within collection
results = client.retrieval.search(query="...", search_settings={"collection_ids": ["<uuid>"]})
```

Collections are managed in PostgreSQL. Full CRUD via REST API.

### 2.4 Can It Work Locally / Offline?

**Partially, but with significant overhead:**
- Requires PostgreSQL running (pgvector extension for embeddings)
- LLM: Supports Ollama via litellm proxy
- Embeddings: Supports Ollama embeddings
- No lightweight local embedding option (no fastembed/sentence-transformers direct)
- Docker is the recommended deployment

**Cannot work with zero network calls** in practice -- PostgreSQL is a separate process, and the R2R server itself is a separate process. Even "local" means running 2-3 services.

### 2.5 R2R as a Python Library?

**NO.** The SDK (`R2RClient`) is a thin HTTP client. There is no way to use R2R's ingestion, embedding, or retrieval logic as library imports without running the server. The `core/` module requires the full server context (database connections, orchestration providers, etc.).

```python
# This is the ONLY way to use R2R:
from r2r import R2RClient
client = R2RClient(base_url="http://localhost:7272")  # Server must be running
```

There is no equivalent of Kotaemon's:
```python
from kotaemon.storages import ChromaVectorStore  # Direct library use
```

---

## 3. HEAD-TO-HEAD COMPARISON

| Criterion | Kotaemon | R2R |
|-----------|----------|-----|
| **Library vs App** | BOTH -- core is a library, ktem is an app | APP ONLY -- client-server architecture |
| **Can import as package** | YES (`from kotaemon.storages import ...`) | NO (must run server + use HTTP client) |
| **Server required** | NO (core library is headless) | YES (FastAPI + PostgreSQL mandatory) |
| **Local embeddings** | FastEmbed (ONNX), sentence-transformers, Ollama | Ollama only (through server) |
| **Local LLM** | llama.cpp direct, Ollama | Ollama only (through litellm) |
| **Vector store** | ChromaDB, LanceDB, Milvus, Qdrant, InMemory | PostgreSQL pgvector ONLY |
| **Document store** | LanceDB, SQLite, Elasticsearch, InMemory | PostgreSQL ONLY |
| **Multi-collection** | Yes (via collection_name param on stores) | Yes (via REST API collections) |
| **Zero network calls** | YES (with FastEmbed + ChromaDB + llama.cpp) | NO (PostgreSQL + server always needed) |
| **Dependency weight** | HEAVY (LlamaIndex + LangChain + Gradio) | HEAVIER (PostgreSQL + 50+ packages) |
| **PDF parsing** | PyMuPDF, unstructured, Azure DI, Docling | pypdf, unstructured, OCR |
| **Knowledge graphs** | GraphRAG, NanoGraphRAG, LightRAG | NetworkX-based KG |
| **Framework coupling** | theflow (Cinnamon's own) | Pydantic + FastAPI |
| **MCP support** | Yes (optional, `mcp[cli]`) | Yes (built-in MCP server) |
| **Reranking** | Cohere, VoyageAI | Built-in |
| **Python version** | >=3.10 | >=3.10, <3.13 |
| **LlamaIndex dependency** | YES (0.10.x, deeply integrated) | NO |
| **LangChain dependency** | YES (<2, for LLM wrappers) | NO (uses litellm) |

---

## 4. INTEGRATION ASSESSMENT FOR OPENBRAIN LM

### 4.1 Kotaemon Integration Path

**Viability: MODERATE -- usable but brings baggage.**

What works well:
- Core library imports work without UI
- ChromaVectorStore with `collection_name` maps perfectly to brain regions
- FastEmbed for local embeddings is clean and fast
- VectorIndexing/VectorRetrieval pipelines are well-designed
- Hybrid retrieval (vector + full-text) built in

What is concerning:
- `theflow` framework imposes its own component model (conflicts with OpenBrainLM's `BaseComponent`)
- Gradio pulled in even for headless use (through theflow's settings system)
- LlamaIndex + LangChain dual dependency is heavy and version-sensitive
- ChromaVectorStore wraps LlamaIndex's wrapper of ChromaDB -- three layers of abstraction
- `flowsettings.py` configuration system is app-centric, not library-centric

**Recommended approach:** Use Kotaemon's individual components selectively, NOT the full framework. Specifically:
1. Use `chromadb` directly (skip Kotaemon's LlamaIndex wrapper)
2. Use `fastembed` directly (skip Kotaemon's wrapper)
3. Use `PyMuPDF` directly for PDF parsing
4. Write our own thin indexing/retrieval layer (around 100 lines)

This gives us the same functionality with 1/10th the dependencies.

### 4.2 R2R Integration Path

**Viability: LOW -- fundamentally wrong architecture for our use case.**

R2R is designed for production SaaS deployments where you want a managed RAG service. It requires:
- PostgreSQL running at all times
- FastAPI server running at all times
- HTTP round-trips for every operation

For OpenBrainLM's brain regions (which need to be in-process, fast, embeddable), R2R is the wrong tool. It would turn every memory lookup into an HTTP call to a local server.

### 4.3 RECOMMENDATION: Neither -- Build a Thin Layer on Raw Components

**The honest assessment:** Both Kotaemon and R2R add more complexity than they solve for OpenBrainLM's specific needs.

What OpenBrainLM actually needs:
1. Chunk documents (PDF/MD) into segments
2. Embed those segments locally
3. Store embeddings in a local vector DB
4. Query by similarity within a specific brain region
5. No UI, no auth, no user management

This is around 150 lines of Python using:
- `chromadb` (vector store, built-in collection support)
- `fastembed` (local ONNX embeddings, no GPU)
- `PyMuPDF` (PDF text extraction)

```python
# What the ACTUAL integration would look like -- no framework needed:
import chromadb
from fastembed import TextEmbedding

class BrainRegionStore:
    def __init__(self, path: str, region_name: str):
        self.client = chromadb.PersistentClient(path=path)
        self.collection = self.client.get_or_create_collection(
            name=region_name,
            metadata={"hnsw:space": "cosine"}
        )
        self.embedder = TextEmbedding(model_name="BAAI/bge-small-en-v1.5")

    def ingest(self, doc_id: str, text: str, metadata: dict = None):
        embedding = list(self.embedder.embed([text]))[0]
        self.collection.add(
            ids=[doc_id],
            embeddings=[embedding.tolist()],
            documents=[text],
            metadatas=[metadata or {}],
        )

    def query(self, query_text: str, top_k: int = 5):
        query_emb = list(self.embedder.embed([query_text]))[0]
        results = self.collection.query(
            query_embeddings=[query_emb.tolist()],
            n_results=top_k,
        )
        return results

# Usage: 8 brain regions, each with its own collection
regions = {}
for name in ["active_sensing", "ganglion", "stigmergy", "action_selection",
             "memory", "relevance", "chromatophore", "pathos_dmn"]:
    regions[name] = BrainRegionStore("./brain_data", name)

# Ingest into a specific region
regions["memory"].ingest("shu_mulvey_2024", "Regime labeling uses state-conditional mean return...")

# Query a specific region
results = regions["memory"].query("How does regime labeling work?")
```

**Dependencies for this approach:**
- `chromadb` (vector DB, around 50MB)
- `fastembed` (embeddings, around 30MB + model download around 130MB one-time)
- `PyMuPDF` (PDF, around 30MB)
- `onnxruntime` (for fastembed, around 50MB)

Total: around 260MB vs Kotaemon's 2GB+ (LlamaIndex + LangChain + Gradio + everything)

---

## 5. ALTERNATIVE: Kotaemon Components Worth Extracting

If we want specific Kotaemon capabilities without the framework, these are worth studying:

| Component | Kotaemon Source | Direct Alternative |
|-----------|----------------|-------------------|
| Hybrid retrieval (vector + BM25) | `kotaemon.indices.VectorRetrieval` | chromadb + `rank_bm25` package |
| Sentence window splitting | `kotaemon.indices.splitters.SentenceWindowSplitter` | LlamaIndex `SentenceWindowNodeParser` direct |
| PDF parsing with thumbnails | `kotaemon.loaders.PDFThumbnailReader` | PyMuPDF `fitz` direct |
| GraphRAG indexing | `ktem.index.file.graph` | `nano-graphrag` or `lightrag` direct |
| Reranking | `kotaemon.rerankings` | `flashrank` (local, MIT) or `sentence-transformers` cross-encoder |

---

## 6. SOURCES

All findings from direct source code inspection of:
- Kotaemon repo: github.com/Cinnamon/kotaemon (commit as of 2026-03-21)
  - `libs/kotaemon/pyproject.toml` -- full dependency list
  - `libs/kotaemon/kotaemon/storages/` -- vector store and doc store implementations
  - `libs/kotaemon/kotaemon/embeddings/fastembed.py` -- local embedding implementation
  - `libs/kotaemon/kotaemon/indices/vectorindex.py` -- VectorIndexing/VectorRetrieval classes
  - `libs/ktem/ktem/index/manager.py` -- IndexManager (collection management)
  - `libs/ktem/ktem/components.py` -- store factory functions
  - `flowsettings.py` -- full configuration reference
- R2R repo: github.com/SciPhi-AI/R2R (commit as of 2026-03-21)
  - `py/pyproject.toml` -- full dependency list
  - `py/r2r/serve.py` -- server entry point (confirms server-only architecture)
  - `py/sdk/__init__.py` -- client SDK (HTTP client only)
  - `py/core/providers/` -- all provider implementations (database = PostgreSQL only)

---

## 7. DECISION MATRIX

| Factor | Weight | Kotaemon | R2R | Raw Components |
|--------|--------|----------|-----|----------------|
| Library usage (no server) | HIGH | 7/10 | 1/10 | 10/10 |
| Dependency weight | HIGH | 3/10 | 1/10 | 9/10 |
| Multi-collection | HIGH | 8/10 | 9/10 | 10/10 |
| Local-only operation | HIGH | 8/10 | 2/10 | 10/10 |
| PDF parsing quality | MED | 8/10 | 7/10 | 7/10 |
| Hybrid retrieval | MED | 9/10 | 8/10 | 6/10 |
| Framework conflict risk | HIGH | 4/10 | 2/10 | 10/10 |
| Community/maintenance | LOW | 8/10 | 7/10 | N/A |
| **WEIGHTED TOTAL** | | **around 6.0** | **around 3.5** | **around 9.0** |

**Verdict: Use raw components (chromadb + fastembed + PyMuPDF) for OpenBrainLM. Skip both Kotaemon and R2R.**

If a more feature-rich option is needed later (GraphRAG, reranking, hybrid search), those capabilities can be added individually without buying into either framework's full dependency tree.
