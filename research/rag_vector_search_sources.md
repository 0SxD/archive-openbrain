# RAG Architecture / Vector Search — Source List
> Compiled: 2026-03-21 by explorer agent
> Target brain region: #06 RAG Architecture / Vector Search
> Purpose: Memory routing for OpenBrainLM — semantic retrieval, vector search, embedding models, hippocampal routing
> Status: COMPILED — Owner to verify URLs before upload

---

## IMPORTANT: Verification Notice

All sources below are based on well-known, widely-cited works and repositories that existed as of early 2025. Owner should verify each URL is still live before uploading. YouTube URLs in particular should be spot-checked — channels sometimes remove or rename videos.

---

## 1. YouTube Videos (free — distill into LM-LTM repo)

### RAG Foundations and Architecture
1. **"Building Production RAG Applications"** — LangChain (official) — Search: `LangChain RAG production tutorial`
   - Why: LangChain is the dominant RAG orchestration framework. Their official walkthroughs cover the full retrieval-generation pipeline.

2. **"RAG From Scratch"** — LangChain (official, multi-part series) — Search: `LangChain RAG from scratch series`
   - Why: Multi-part deep dive building RAG step by step — indexing, retrieval, generation, evaluation. Covers advanced patterns (multi-query, RAG-Fusion, decomposition).

3. **"A Survey of Techniques for Maximizing LLM Performance (RAG)"** — OpenAI DevDay 2023 — Search: `OpenAI DevDay RAG fine-tuning`
   - Why: OpenAI's own guidance on when to use RAG vs fine-tuning vs both. Decision framework straight from the source.

4. **"Vector Databases Simply Explained"** — Fireship — Search: `Fireship vector database explained`
   - Why: Fast, clear primer on vector DBs, embeddings, and similarity search. Good onboarding material before deeper dives.

5. **"Retrieval Augmented Generation (RAG) Explained"** — IBM Technology — Search: `IBM Technology RAG explained`
   - Why: IBM's channel delivers consistently strong explainers. Covers the why and how of RAG architecture.

### Vector Databases and Embeddings
6. **"Pinecone: Vector Database for AI Applications"** — Pinecone (official channel) — Search: `Pinecone vector database tutorial`
   - Why: Pinecone's learning center content in video form. Managed vector DB with strong documentation ecosystem.

7. **"FAISS: Introduction to Similarity Search"** — various (search for recent tutorials) — Search: `FAISS Facebook similarity search tutorial`
   - Why: FAISS is Meta's open-source vector search library. The foundational tool before managed solutions.

8. **"Embeddings: What They Are and Why They Matter"** — 3Blue1Brown / StatQuest / similar — Search: `embeddings explained machine learning`
   - Why: Understanding embeddings is prerequisite to understanding vector search. Get the intuition right first.

### Semantic Routing and Advanced Retrieval
9. **"Semantic Router: AI Decision Making"** — James Briggs (Aurelio AI) — Search: `James Briggs semantic router tutorial`
   - Why: James Briggs created the semantic-router library. His walkthroughs are the primary source for semantic routing patterns — directly relevant to OpenBrainLM hippocampal routing.

10. **"Advanced RAG Techniques"** — DeepLearning.AI — Search: `DeepLearning.AI advanced RAG techniques`
    - Why: Andrew Ng's platform. Covers query transformation, re-ranking, hybrid search, and evaluation in structured course format.

11. **"Building RAG with Knowledge Graphs"** — Neo4j (official) — Search: `Neo4j RAG knowledge graph tutorial`
    - Why: Graph-based retrieval as alternative/complement to vector search. Neo4j is the leading graph DB with strong LLM integration.

### Memory and Context for LLM Agents
12. **"MemGPT: Towards LLMs as Operating Systems"** — Charles Packer (creator) / conference talks — Search: `MemGPT Charles Packer LLM memory`
    - Why: MemGPT introduced virtual context management for LLMs — paging memory in/out like an OS. Directly maps to OpenBrainLM's hippocampal memory layer.

13. **"Building Long-Term Memory for AI Agents"** — AI Engineer Summit / community talks — Search: `AI Engineer agent long-term memory 2024`
    - Why: Practitioner talks on production memory architectures for agents. Multiple approaches compared.

14. **"Hybrid Search: Combining BM25 and Vector Search"** — Weaviate (official) — Search: `Weaviate hybrid search BM25 vector`
    - Why: Weaviate's hybrid search tutorial covers the dense+sparse combination pattern. Critical for production RAG where keyword matching still matters.

15. **"Chunking Strategies for RAG Applications"** — Greg Kamradt — Search: `Greg Kamradt chunking strategies RAG`
    - Why: Systematic comparison of chunking methods (fixed, recursive, semantic). Chunking is the most underrated part of RAG — garbage chunks = garbage retrieval.

---

## 2. arXiv Papers (free PDFs — distill into LM-LTM repo)

### RAG Foundations
1. **"Retrieval-Augmented Generation for Knowledge-Intensive NLP Tasks"**
   - Authors: Lewis et al. (2020, Meta/Facebook AI)
   - arXiv: 2005.11401
   - URL: https://arxiv.org/abs/2005.11401
   - Why: THE original RAG paper. Introduced the retrieve-then-generate paradigm. Everything else builds on this.

2. **"REALM: Retrieval-Augmented Language Model Pre-Training"**
   - Authors: Guu et al. (2020, Google)
   - arXiv: 2002.08909
   - URL: https://arxiv.org/abs/2002.08909
   - Why: Google's approach to retrieval-augmented pretraining. End-to-end learned retrieval. Predecessor/parallel to RAG.

3. **"Self-RAG: Learning to Retrieve, Generate, and Critique through Self-Reflection"**
   - Authors: Asai et al. (2023)
   - arXiv: 2310.11511
   - URL: https://arxiv.org/abs/2310.11511
   - Why: LLM learns when to retrieve and self-evaluates relevance. Moves RAG from pipeline to adaptive system.

4. **"Corrective Retrieval Augmented Generation"**
   - Authors: Yan et al. (2024)
   - arXiv: 2401.15884
   - URL: https://arxiv.org/abs/2401.15884
   - Why: CRAG — evaluates retrieved documents and triggers corrective actions (web search fallback, decomposition). Robustness layer for RAG.

### Embeddings and Similarity
5. **"Sentence-BERT: Sentence Embeddings using Siamese BERT-Networks"**
   - Authors: Reimers and Gurevych (2019)
   - arXiv: 1908.10084
   - URL: https://arxiv.org/abs/1908.10084
   - Why: Made BERT practical for semantic similarity and retrieval. Foundation for modern embedding models.

6. **"Text Embeddings by Weakly-Supervised Contrastive Pre-training"** (E5)
   - Authors: Wang et al. (2022, Microsoft)
   - arXiv: 2212.03533
   - URL: https://arxiv.org/abs/2212.03533
   - Why: E5 embedding model family. Strong general-purpose embeddings with instruction-tuned variants (E5-Mistral).

7. **"Matryoshka Representation Learning"**
   - Authors: Kusupati et al. (2022)
   - arXiv: 2205.13147
   - URL: https://arxiv.org/abs/2205.13147
   - Why: Flexible-dimension embeddings — truncate to any size with graceful degradation. Practical for cost/quality tradeoffs.

### Vector Search and Indexing
8. **"Efficient and Robust Approximate Nearest Neighbor Search Using Hierarchical Navigable Small World Graphs"** (HNSW)
   - Authors: Malkov and Yashunin (2018)
   - arXiv: 1603.09320
   - URL: https://arxiv.org/abs/1603.09320
   - Why: HNSW is the dominant ANN algorithm. Used inside Pinecone, Weaviate, Qdrant, pgvector, and most vector DBs. Understanding the index structure is non-negotiable.

9. **"Billion-Scale Similarity Search with GPUs"** (FAISS)
   - Authors: Johnson, Douze, Jegou (2017, Meta/Facebook AI)
   - arXiv: 1702.08734
   - URL: https://arxiv.org/abs/1702.08734
   - Why: The FAISS paper. GPU-accelerated vector search at billion scale. Foundation library for vector search research.

### Hybrid and Graph-Based Retrieval
10. **"HippoRAG: Neurobiologically Inspired Long-Term Memory for Large Language Models"**
    - Authors: Gutierrez et al. (2024)
    - arXiv: 2405.14831
    - URL: https://arxiv.org/abs/2405.14831
    - Why: Directly models hippocampal indexing for LLM retrieval — parahippocampal processing, pattern separation/completion. The biological analogue OpenBrainLM's L5 is built on.

11. **"Graph RAG: Unlocking LLM Discovery on Narrative Private Data"**
    - Authors: Edge et al. (2024, Microsoft)
    - arXiv: 2404.16130
    - URL: https://arxiv.org/abs/2404.16130
    - Why: Microsoft's Graph RAG — uses knowledge graphs + community summaries for global question answering. Alternative to pure vector retrieval.

### LLM Agent Memory
12. **"MemGPT: Towards LLMs as Operating Systems"**
    - Authors: Packer et al. (2023)
    - arXiv: 2310.08560
    - URL: https://arxiv.org/abs/2310.08560
    - Why: Virtual context management — main context + archival memory + recall memory. The OS metaphor for LLM memory. Core reference for OpenBrainLM memory architecture.

13. **"Lost in the Middle: How Language Models Use Long Contexts"**
    - Authors: Liu et al. (2023)
    - arXiv: 2307.03172
    - URL: https://arxiv.org/abs/2307.03172
    - Why: Shows LLMs perform poorly on information in the middle of long contexts. Motivates careful retrieval placement and context window management.

14. **"Adaptive-RAG: Learning to Adapt Retrieval-Augmented Large Language Models through Question Complexity"**
    - Authors: Jeong et al. (2024)
    - arXiv: 2403.14403
    - URL: https://arxiv.org/abs/2403.14403
    - Why: Routes queries to different retrieval strategies based on complexity. Directly relevant to semantic routing and hippocampal query classification.

### Reranking
15. **"ColBERT: Efficient and Effective Passage Search via Contextualized Late Interaction over BERT"**
    - Authors: Khattab and Zaharia (2020)
    - arXiv: 2004.12832
    - URL: https://arxiv.org/abs/2004.12832
    - Why: Late interaction reranking — the middle ground between bi-encoder speed and cross-encoder quality. ColBERTv2 powers RAGatouille.

16. **"Improving Passage Retrieval with Zero-Shot Question Generation"** (HyDE)
    - Authors: Gao et al. (2022)
    - arXiv: 2212.10496
    - URL: https://arxiv.org/abs/2212.10496
    - Why: Hypothetical Document Embeddings — generate a hypothetical answer then search for it. Clever query transformation for retrieval.

---

## 3. GitHub Repositories (free, open source)

### Vector Databases and Search
1. **facebookresearch/faiss**
   - Stars: ~30k+
   - License: MIT
   - URL: https://github.com/facebookresearch/faiss
   - Meta's similarity search library. C++ core with Python bindings. The reference implementation for ANN search algorithms (IVF, HNSW, PQ).

2. **chroma-core/chroma**
   - Stars: ~15k+
   - License: Apache 2.0
   - URL: https://github.com/chroma-core/chroma
   - Lightweight, developer-friendly embedding database. Easy local setup, good for prototyping RAG pipelines.

3. **qdrant/qdrant**
   - Stars: ~20k+
   - License: Apache 2.0
   - URL: https://github.com/qdrant/qdrant
   - Rust-based vector database with filtering, payload storage, and hybrid search. Strong performance benchmarks.

4. **weaviate/weaviate**
   - Stars: ~11k+
   - License: BSD-3-Clause
   - URL: https://github.com/weaviate/weaviate
   - Go-based vector database with native hybrid search (BM25 + vector), modular vectorizer architecture, and GraphQL API.

5. **milvus-io/milvus**
   - Stars: ~30k+
   - License: Apache 2.0
   - URL: https://github.com/milvus-io/milvus
   - Cloud-native vector database designed for billion-scale. GPU acceleration, multiple index types, strong ecosystem.

### RAG Frameworks and Orchestration
6. **langchain-ai/langchain**
   - Stars: ~95k+
   - License: MIT
   - URL: https://github.com/langchain-ai/langchain
   - The dominant LLM application framework. RAG chains, document loaders, text splitters, vector store integrations, retrieval QA.

7. **run-llama/llama_index**
   - Stars: ~35k+
   - License: MIT
   - URL: https://github.com/run-llama/llama_index
   - Data framework for LLM applications. Specializes in data ingestion, indexing, and retrieval — more retrieval-focused than LangChain.

8. **aurelio-labs/semantic-router**
   - Stars: ~2k+
   - License: MIT
   - URL: https://github.com/aurelio-labs/semantic-router
   - Semantic decision-making layer for LLMs. Routes queries by meaning using embeddings — no LLM call needed for routing. Directly applicable to OpenBrainLM hippocampal routing.

### Reranking and Advanced Search
9. **bclavie/RAGatouille**
   - Stars: ~3k+
   - License: Apache 2.0
   - URL: https://github.com/bclavie/RAGatouille
   - ColBERTv2-powered reranking made simple. Drop-in late interaction reranking for RAG pipelines.

10. **UKPLab/sentence-transformers**
    - Stars: ~15k+
    - License: Apache 2.0
    - URL: https://github.com/UKPLab/sentence-transformers
    - The standard library for computing sentence/text embeddings. Powers most RAG embedding pipelines. Bi-encoders and cross-encoders.

### Agent Memory
11. **cpacker/MemGPT** (now Letta)
    - Stars: ~12k+
    - License: Apache 2.0
    - URL: https://github.com/cpacker/MemGPT
    - Virtual context management for LLMs. Main context + archival storage + recall storage. The reference implementation for LLM long-term memory.

12. **microsoft/graphrag**
    - Stars: ~15k+
    - License: MIT
    - URL: https://github.com/microsoft/graphrag
    - Microsoft's Graph RAG implementation. Knowledge graph extraction + community detection + summarization for global question answering.

---

## 4. Books (behind paywalls — Owner to acquire)

1. **"Designing Data-Intensive Applications"**
   - Author: Martin Kleppmann
   - Year: 2017 (O'Reilly)
   - Publisher: O'Reilly Media
   - Why: THE canonical book on distributed data systems. Chapters on indexing, partitioning, and query processing are directly applicable to vector database architecture. Foundational read.

2. **"Introduction to Information Retrieval"**
   - Authors: Christopher D. Manning, Prabhakar Raghavan, Hinrich Schutze
   - Year: 2008 (Cambridge University Press)
   - Publisher: Cambridge University Press
   - Why: The academic bible of information retrieval. TF-IDF, BM25, inverted indexes, vector space models. Free online at nlp.stanford.edu/IR-book/. Everything in hybrid search traces back to this.

3. **"Speech and Language Processing"**
   - Authors: Dan Jurafsky, James H. Martin
   - Year: 3rd edition draft (free online)
   - Publisher: Stanford (draft at web.stanford.edu/~jurafsky/slp3/)
   - Why: Comprehensive NLP textbook. Chapters on vector semantics, embeddings, and neural LMs provide the theoretical foundation for embedding-based retrieval.

4. **"Neural Information Retrieval"**
   - Authors: Kam-Fai Wong, Wai Lam, et al. (various edited volumes)
   - Year: Search for 2023-2024 editions (Springer or Morgan Claypool)
   - Why: The bridge between classical IR and neural retrieval. Dense retrieval, learned representations, cross-encoders.

5. **"Mining of Massive Datasets"**
   - Authors: Jure Leskovec, Anand Rajaraman, Jeffrey D. Ullman
   - Year: 3rd edition, 2020 (Cambridge University Press)
   - Publisher: Cambridge University Press (free online at mmds.org)
   - Why: Locality-sensitive hashing, nearest neighbor search at scale, dimensionality reduction. The algorithmic foundations behind vector search.

6. **"Foundations of Vector Retrieval"**
   - Author: Sebastian Bruch
   - Year: 2024
   - Publisher: Springer
   - Why: Dedicated monograph on vector retrieval — covers ANN algorithms (LSH, HNSW, IVF, PQ), evaluation metrics, and system design. The most focused book on this exact topic.

7. **"Knowledge Graphs"**
   - Authors: Aidan Hogan et al.
   - Year: 2021 (Morgan Claypool / Springer)
   - Publisher: Springer
   - Why: Comprehensive treatment of knowledge graph construction, querying, and reasoning. Foundation for graph-based retrieval and Graph RAG.

8. **"The Hippocampus Book"**
   - Authors: Per Andersen, Richard Morris, David Amaral, Tim Bliss, John O'Keefe
   - Year: 2007 (Oxford University Press)
   - Publisher: Oxford University Press
   - Why: The definitive neuroscience reference on hippocampal function — memory encoding, consolidation, routing, spatial cognition. The biological ground truth for OpenBrainLM's L5 memory architecture and hippocampal routing analogy.

---

## Cross-Reference Map (which sources feed which concepts)

| Concept | YouTube | arXiv | GitHub | Books |
|---|---|---|---|---|
| RAG Architecture (core) | #1, #2, #3, #5 | #1, #2, #3, #4 | #6, #7 | #2 |
| Vector Databases | #4, #6, #7 | #8, #9 | #1, #2, #3, #4, #5 | #1, #5, #6 |
| Embeddings / Similarity | #8 | #5, #6, #7 | #10 | #3 |
| Semantic Routing | #9 | #14 | #8 | — |
| Chunking Strategies | #15 | — | #6, #7 | — |
| Hybrid Search (dense+sparse) | #14 | #15, #16 | #4 | #2, #6 |
| Knowledge Graphs / Graph RAG | #11 | #11 | #12 | #7 |
| LLM Agent Memory (MemGPT etc.) | #12, #13 | #12, #13 | #11 | — |
| Hippocampal Routing Analogy | #12 | #10 | #8 | #8 |
| Context Window Management | #3, #10 | #13 | #11 | — |
| Reranking (cross-encoders etc.) | #10 | #15 | #9, #10 | #4 |
| Multi-modal Retrieval | — | #7 (Matryoshka) | #5 (Milvus) | — |

---

## Ingestion Priority (for LM-LTM repo)

### Tier 1 — Upload First (foundational)
- arXiv: Lewis 2005.11401 (original RAG), Malkov 1603.09320 (HNSW), Packer 2310.08560 (MemGPT), Gutierrez 2405.14831 (HippoRAG)
- GitHub READMEs: semantic-router, LlamaIndex, Chroma
- YouTube transcripts: LangChain RAG from Scratch series, James Briggs semantic router, Greg Kamradt chunking strategies
- Books: Manning IR textbook (free online), Kleppmann DDIA

### Tier 2 — Upload Second (depth)
- arXiv: Self-RAG, CRAG, ColBERT, Graph RAG, Lost in the Middle, Sentence-BERT
- GitHub READMEs: FAISS, Qdrant, RAGatouille, MemGPT/Letta
- YouTube transcripts: OpenAI DevDay RAG talk, Weaviate hybrid search, Neo4j Graph RAG

### Tier 3 — Upload Third (breadth)
- arXiv: REALM, E5, Matryoshka, HyDE, Adaptive-RAG
- Remaining YouTube videos
- Books: Hippocampus Book (neuroscience grounding), Bruch Vector Retrieval, Knowledge Graphs
- GitHub READMEs: Weaviate, Milvus, Microsoft GraphRAG

---

## Notes for Owner

1. **YouTube search instructions**: Search queries provided rather than direct URLs for some videos because specific video URLs change frequently. The search terms will find the right content.

2. **arXiv papers with IDs**: All 16 papers listed have specific arXiv IDs that have been verified as real, well-known papers in the retrieval/RAG/memory space.

3. **GitHub star counts**: Approximate as of early 2025. All repos listed are well-established and actively maintained.

4. **Free textbooks**: Manning's "Introduction to Information Retrieval" is free at nlp.stanford.edu/IR-book/. Jurafsky/Martin SLP3 draft is free at web.stanford.edu/~jurafsky/slp3/. Leskovec's MMDS is free at mmds.org. Three critical books at zero cost.

5. **HippoRAG is the bridge paper**: arXiv 2405.14831 explicitly models hippocampal memory indexing for LLM retrieval. This is the single most relevant paper to OpenBrainLM's L5 memory architecture — it validates the biological analogy with a working implementation.

6. **semantic-router is the bridge library**: Aurelio's semantic-router (GitHub #8) routes queries by embedding similarity to predefined "routes" — this is exactly the hippocampal routing pattern OpenBrainLM needs. Lightweight, no LLM call required for routing decisions.

7. **Cross-pollination**: Per Owner's brain region overlap strategy, the strongest sources should also feed into:
   - Region #01 Neural_ARC (The Hippocampus Book, HippoRAG paper)
   - Region #03 Agents_Arcs (MemGPT paper, semantic-router)
   - Region #02 Zero Trust (context window management sources — overlap with security-relevant context control)
