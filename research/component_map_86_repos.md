# OpenBrainLM: plug-and-play building blocks from 86 open-source repos

**Every component of the OpenBrainLM architecture — from hippocampal memory to stigmergic pheromone trails — already exists as a tested, documented, peer-reviewed open-source building block.** This report maps 86+ repos and 60+ papers across all 14 categories, confirming the core principle: you never build something new, you take what works and make it better. The strongest candidates include HippoRAG (NeurIPS 2024/ICML 2025) for hippocampal indexing, LangGraph for graph-based agent orchestration with cycles, semantic-router for embedding-based action selection, and CraniMem for multi-tier memory with consolidation. Every primary recommendation carries a permissive license (MIT/Apache 2.0/BSD) and runs fully self-hosted.

> Source: OpenBrainLM research compilation, 2026-03-21
> Status: APPROVED — owner-provided, verified

---

## 1. Self-hosted NotebookLM clone: Kotaemon leads the pack

The open-source ecosystem for grounded document Q&A is mature and competitive. The critical requirement — **source grounding that refuses to hallucinate beyond provided documents** — narrows the field significantly.

**Kotaemon** (Cinnamon, Apache 2.0, **~25.2k stars**) is the strongest match. It provides advanced citations with in-document highlighting and relevance scores, warns when retrieval returns low-relevance passages, supports hybrid RAG (full-text + vector + re-ranking), GraphRAG integration (NanoGraphRAG, LightRAG, MS GraphRAG), and runs fully local via Ollama + llama-cpp-python. Its Python framework layer (`import kotaemon`) enables CLI/programmatic usage beyond the default Gradio UI. GitHub: `github.com/Cinnamon/kotaemon`

**RAGFlow** (InfiniFlow, Apache 2.0, **~73.2k stars**) offers the most feature-rich pipeline with layout-aware chunking using vision models, traceable citations with quick-reference views, and "needle in a haystack" unlimited-token search. The trade-off is a heavier infrastructure footprint (Docker Compose with MinIO, Elasticsearch, Redis, MySQL). GitHub: `github.com/infiniflow/ragflow`

**PrivateGPT** (Zylon, Apache 2.0, **~57.1k stars**) remains the pioneer for 100% offline document Q&A with a native CLI. Its LlamaIndex-based RAG pipeline returns source documents with relevance scores, though source grounding enforcement requires prompt engineering. GitHub: `github.com/zylon-ai/private-gpt`

For strict anti-hallucination enforcement layered onto any of these, two additional tools are essential. **NeMo Guardrails** (NVIDIA, Apache 2.0, ~5.2k stars) provides programmable output rails with a fact-checking rail (`self_check_facts`) that uses NLI-style verification against retrieved chunks and can block non-grounded responses entirely. **Self-RAG** (UW/IBM, MIT, ~2.3k stars, ICLR 2024 Oral) trains LMs to generate special reflection tokens — `[IsREL]`, `[IsSUP]`, `[IsUSE]` — that self-critique whether output is supported by evidence, achieving 91% pass@1 on HumanEval.

| Tool | Stars | License | Source grounding | Runs local | CLI |
|------|-------|---------|-----------------|------------|-----|
| **Kotaemon** | 25.2k | Apache-2.0 | ✅ Citations + highlighting + warnings | ✅ Ollama | Via Python API |
| **RAGFlow** | 73.2k | Apache-2.0 | ✅ Traceable citations | ✅ Docker | REST API |
| **PrivateGPT** | 57.1k | Apache-2.0 | ⚠️ Returns sources, needs prompting | ✅ Ollama/llama-cpp | ✅ Native |
| **NeMo Guardrails** | 5.2k | Apache-2.0 | ✅ Blocks ungrounded responses | ✅ | Python SDK |
| **Self-RAG** | 2.3k | MIT | ✅ Reflection tokens for support scoring | ✅ HuggingFace models | ✅ |
| **AnythingLLM** | 56.5k | MIT | ⚠️ Moderate | ✅ Ollama | ✅ CLI tool |
| **Khoj** | 32.8k | AGPL-3.0 | ✅ Clickable source citations | ✅ Ollama | ✅ |

Additional evaluation benchmarks: **ALCE** (Princeton NLP, MIT, EMNLP 2023) measures citation precision/recall via NLI; **RAGAS** (Apache 2.0, EACL 2024) scores faithfulness, relevance, and context quality; **TruLens** (MIT) provides the "RAG Triad" — groundedness, context relevance, answer relevance; and the **Vectara HHEM** (Apache 2.0, ~3.1k stars) hallucination evaluation model scores factual consistency 0–1.

---

## 2. Semantic routing and active inference for the basal ganglia layer

The L4 Basal Ganglia requires two complementary mechanisms: fast embedding-based routing (the "direct pathway") and learned active inference routing that improves over time (the "indirect pathway").

**semantic-router** (Aurelio Labs, MIT, **~3.3k stars**, 509 dependent repos) routes queries via embedding cosine similarity with **zero LLM calls** — millisecond latency versus seconds for LLM-based routing. Routes are defined by example utterances; at runtime, the query embedding is matched to the nearest route via kNN. It supports `HybridRouteLayer` combining dense embeddings with sparse TF-IDF, dynamic routes with parameter extraction, and runs fully offline with `pip install "semantic-router[local]"` using HuggingFace encoders + llama.cpp. Associated paper: Manias et al., IEEE GlobeCom 2024 (arXiv:2404.15869). GitHub: `github.com/aurelio-labs/semantic-router`

**pymdp** (infer-actively, MIT, **~619 stars**, JOSS 2022) implements the full Active Inference loop: perception → belief updating → policy inference → action selection. Its Expected Free Energy (EFE) computation decomposes into **epistemic value** (information gain) and **pragmatic value** (preference alignment), directly implementing Friston's free energy principle. The agent API provides `infer_states()`, `infer_policies()`, and `sample_action()` methods operating on POMDP generative models. The v1.0 alpha branch migrates to a JAX backend for GPU acceleration. Paper: arXiv:2201.03904. GitHub: `github.com/infer-actively/pymdp`

**RouteLLM** (LMSYS, Apache 2.0, ~4.5k stars, ICLR 2025) provides learned routing with 4 built-in routers (BERT classifier, matrix factorization, similarity-weighted ranking) that reduce costs up to 85% while maintaining 95% GPT-4 quality. GitHub: `github.com/lm-sys/RouteLLM`

For prediction error signals specifically, **PyHGF** (GPL-3.0) implements generalized Hierarchical Gaussian Filters for precision-weighted prediction errors on JAX, and **ngc-learn** (BSD-3, *Nature Communications* 2022) provides neural generative coding circuits with first-class prediction error neurons and reward prediction error (RPE) components.

A critical recent paper — **D-MEM: Dopamine-Gated Agentic Memory** (arXiv:2603.14597, 2026) — maps biological RPE gating directly onto LLM agent architecture, using a lightweight Critic Router that evaluates stimuli for **Surprise × Utility**, with low-RPE inputs bypassed via O(1) cache and high-RPE inputs triggering full memory evolution. This is the first architecture to explicitly map biological RPE gating onto LLM memory systems.

---

## 3. HippoRAG brings hippocampal indexing theory to retrieval

**HippoRAG** (OSU NLP Group, **~3.3k stars**) is the only framework explicitly designed around hippocampal memory indexing theory for LLMs. It maps neuroscience directly to computation: the LLM serves as the **neocortex** (processing input into a schemaless knowledge graph), the KG serves as the **hippocampal index** (interconnected associations between entities pointing to memory passages), and **Personalized PageRank** traversal performs pattern completion during retrieval — mimicking the hippocampus's role in associative recall. GitHub: `github.com/OSU-NLP-Group/HippoRAG`

HippoRAG v1 was published at **NeurIPS 2024** (arXiv:2405.14831, 103+ citations). **HippoRAG v2** was accepted at **ICML 2025** (arXiv:2502.14802), introducing deeper passage integration into the KG, query-to-triple matching (12.5% improvement in Recall@5), and outperforming GraphRAG, RAPTOR, and LightRAG across factual, sense-making, and associative memory tasks while being more resource-efficient. Install via `pip install hipporag` (v2.0.0-alpha.4), supports local LLMs via vLLM (Llama-3.3-70B) and local embeddings (NV-Embed-v2, GritLM, Contriever).

Complementary graph-RAG tools provide alternative approaches:

- **GraphRAG** (Microsoft, MIT, ~30.9k stars, arXiv:2404.16130, 902+ citations): Entity KG extraction with Leiden community detection and hierarchical community summaries. Best for corpus-wide "sensemaking" queries via map-reduce over summaries.
- **LightRAG** (HKU, MIT, ~29k stars, EMNLP 2025): Dual-level retrieval (entity-specific + thematic), incremental KG updates without reprocessing, runs on 8GB RAM via Ollama. Best for lightweight local deployment.
- **Graphiti/Zep** (Apache 2.0, arXiv:2501.13956): Temporal knowledge graph with bitemporal modeling — facts have validity windows tracking when they became true and when superseded. The episodic/semantic/community subgraph architecture implicitly mirrors hippocampal theory. **94.8% accuracy** on Deep Memory Retrieval benchmark.

---

## 4. LangGraph provides the orchestration backbone with cycles and checkpoints

The L2 Ganglion/Orchestrator requires stateful directed graphs with cycles (for dialectic loops), conditional edges, checkpoints, and parallel dispatch. **LangGraph** (langchain-ai, MIT, **~26.2k stars**, 36,700+ downstream repos) is the clear winner across all five requirements.

Its core abstraction is `StateGraph` with typed state schemas, inspired by Google's Pregel and Apache Beam. It provides **first-class cycle support** (critical for dialectic loops), conditional edge routing, native checkpointing with time-travel debugging, parallel node execution, human-in-the-loop interrupt/resume, and subgraph composition. It runs standalone without LangChain and is production-proven at Klarna, Replit, Uber, LinkedIn, and GitLab. GitHub: `github.com/langchain-ai/langgraph`

| Framework | License | Stars | Directed graph | Cycles | Checkpoints | Parallel |
|-----------|---------|-------|---------------|--------|-------------|----------|
| **LangGraph** | MIT | 26.2k | ✅ Core (Pregel) | ✅ | ✅ Native | ✅ |
| **CrewAI** | MIT | 44.7k | ❌ Role-based | ⚠️ Limited | ❌ | ✅ |
| **AutoGen** | MIT | 54.5k | ❌ Conversation | ✅ Implicit | ❌ | ✅ |
| **PocketFlow** | MIT | 10.1k | ✅ Core | ✅ | ❌ | ✅ Async |
| **smolagents** | Apache-2.0 | 25.4k | ❌ Code loop | ⚠️ | ❌ | ⚠️ |

**PocketFlow** (MIT, ~10.1k stars) deserves special mention as a minimalist alternative: the entire framework is **100 lines of Python with zero dependencies**, providing the right graph abstractions (nodes, flows, conditional edges, async execution) without checkpointing. It could serve as inspiration for a custom lightweight orchestrator. Note that **AutoGen** is now in maintenance mode, having merged with Semantic Kernel into the Microsoft Agent Framework (Oct 2025).

---

## 5. Multi-agent debate and the Trinity dialectic engine

Two distinct mechanisms are needed: a **quorum system** (L6) where multiple agents must agree before proceeding, and a **structured dialectic** (L8) where Logos fights Pathos and Ethos arbitrates.

For the **Trinity Engine** structure, the closest architectural match is **MAD** (Multi-Agents Debate) by Liang et al. (ACL 2024, arXiv:2305.19118, GPL-3.0). It assigns explicit roles — **affirmative** (devil), **negative** (angel), and **moderator** — mapping directly to Logos/Pathos/Ethos. The moderator judges debate outcomes across configurable rounds, explicitly designed to counter "Degeneration of Thought" in self-reflection. GitHub: `github.com/Skytliang/Multi-Agents-Debate`

**Du et al.'s** foundational debate paper (ICML 2024, arXiv:2305.14325) establishes the core pattern: multiple LLM instances independently generate answers, exchange responses, and critique each other over multiple rounds until convergence. GitHub: `github.com/composable-models/llm_multiagent_debate`

**DebateLLM** (InstaDeep, Apache 2.0, arXiv:2311.17371) is the most practical library, encompassing multiple debate protocols with configurable agreement intensity thresholds (e.g., 90% quorum). GitHub: `github.com/instadeepai/DebateLLM`

For quorum-based consensus specifically, the **Aegean** system (arXiv:2512.20184) provides progressive quorum detection with configurable α (quorum size) and β (stability rounds) parameters, achieving **4.4× token reduction** on GSM8K via early termination when consensus is reached.

**Reflexion** (Shinn et al., MIT, ~3.1k stars, NeurIPS 2023, arXiv:2303.11366) provides the self-critique loop foundation. Its successor **MAR** (Multi-Agent Reflexion, arXiv:2512.20845) extends this with persona-guided critics — factual grounding, logical consistency, alternative hypothesis generation — debating under a coordinator/judge, mapping directly to the Logos/Pathos differentiation with Ethos arbitration.

The **SIEV framework** (arXiv:2510.18134) evaluates reasoning through explicit Hegelian dialectics — thesis, antithesis, synthesis — providing a formal scaffold for the Trinity Engine's dialectical structure. For constitutional principles governing the Ethos arbiter role, the **HuggingFace Alignment Handbook** (Apache 2.0) provides recipes for Constitutional AI with open-source models.

---

## 6. NEAT and TensorNEAT evolve agent topologies at GPU scale

The Morphogen agent needs to evolve agent connection topologies — not hand-design them. Two tools form a natural prototyping → production pipeline.

**neat-python** (CodeReclaimers, BSD-3, **~1.5k stars**) is the prototyping choice: pure Python with **zero dependencies**, it implements the full NEAT algorithm — evolving both network topology (adding nodes/connections) and weights simultaneously. It supports speciation, fitness sharing, incremental complexification, parallel evaluation, feed-forward and recurrent networks, and JSON export for framework-agnostic deployment. The original NEAT paper (Stanley & Miikkulainen, 2002, *Evolutionary Computation*) won Outstanding Paper of the Decade. GitHub: `github.com/CodeReclaimers/neat-python`

**TensorNEAT** (EMI-Group, **~343 stars**, **GECCO 2024 Best Paper**) is the production choice: it achieves **500× speedup** over neat-python by transforming diverse network topologies into uniform-shape tensors for GPU-parallel execution across entire populations via JAX. It supports NEAT, CPPN, HyperNEAT, spiking neural networks, and integrates with Gym/Brax environments. Extended journal version in ACM Transactions on Evolutionary Learning (2025). GitHub: `github.com/EMI-Group/tensorneat`

**EvoX** (EMI-Group, GPL-3.0, ~2k stars, IEEE TEVC 2024) provides the distributed multi-GPU execution framework with 50+ evolutionary algorithms, 100+ benchmarks, and PyTorch compatibility. TensorNEAT integrates directly as its topology evolution module. Complementary tools include **QDax** (MIT, JMLR 2024) for quality-diversity search maintaining diverse archives of evolved topologies, and **EvoTorch** (NNAISENSE, Apache 2.0, ~1.1k stars, arXiv:2302.12600) for PyTorch-native weight optimization downstream of topology decisions.

---

## 7. Agent memory: CraniMem and Letta implement multi-tier consolidation

The L5 memory layer requires multi-tier memory (working → short-term → long-term) with consolidation cycles — the computational equivalent of sleep.

**CraniMem** (arXiv:2603.15642, March 2026) is the most architecturally aligned tool found. It implements three explicit tiers: **working memory** (transient traces), an **episodic buffer** (bounded short-term), and a **long-term knowledge graph** (structured semantic recall). Critically, it features a **scheduled consolidation loop** that replays high-utility traces into the graph while pruning low-utility items — the closest found to a "sleep" consolidation mechanism. It outperforms both Vanilla RAG and Mem0 baselines on long-horizon benchmarks.

**Letta/MemGPT** (Apache 2.0, **~19.3k stars**, arXiv:2310.08560, 287+ citations) is the most production-ready option, using an OS-inspired virtual memory metaphor: Core Memory Blocks as "RAM" (always in-context, editable by the agent), a FIFO message queue with recursive summarization on overflow, and Archival/Recall Storage as "disk" (read/write database + searchable conversation history). Memory pressure warnings trigger context compression — continuous consolidation rather than batch "sleep" cycles. GitHub: `github.com/letta-ai/letta`

**Mem0** (Apache 2.0, **~41k stars**, arXiv:2504.19413) is the most battle-tested at scale (186M API calls in Q3), using a hybrid data store — vector DB + key-value store + graph DB — with automatic memory extraction, deduplication, and contradiction resolution. Selected as AWS's exclusive memory provider for its Agent SDK. GitHub: `github.com/mem0ai/mem0`

Other notable tools: **A-MEM** (MIT, NeurIPS 2025, arXiv:2502.12110) uses a Zettelkasten-inspired interconnected knowledge network with dynamic linking; **MemOS** (~4.7k stars) provides a full Memory Operating System with MemCube abstractions and Redis Streams scheduling; and the **Generative Agents** memory architecture (Park et al., UIST 2023, ~20.7k stars) established the foundational observation → reflection consolidation pattern. The comprehensive survey **"Memory in the Age of AI Agents"** (arXiv:2512.13564, Dec 2025, CC BY 4.0) catalogs the full taxonomy with a curated paper list at `github.com/Shichun-Liu/Agent-Memory-Paper-List` (~1.4k stars).

---

## 8. Stigmergy and Hebbian plasticity from spiking neural networks

**Stigmergy (L3 pheromone communication)** requires file-based artifact communication with decaying pheromone trails. The most directly applicable implementation is **KeepALifeUS/autonomous-agents** — a production multi-agent system where 4 AI agents coordinate via file-based stigmergy: tasks live in `queue.json` → claimed by moving to `active.json`, reviews flow through `pending/` → `approved/`, and knowledge accumulates in `patterns.jsonl` and `lessons.jsonl` with Git's conflict detection as distributed locking. GitHub: `github.com/KeepALifeUS/autonomous-agents`

For the core pheromone deposit/decay/evaporation algorithm, **ACOpy** (Apache 2.0) implements ant colony optimization with pheromone matrices on NetworkX graphs, where each edge has a dynamic `pheromone` property with configurable evaporation rate (ρ). Two key papers formalize digital stigmergy for multi-agent systems: **SIRL** (IEEE TNNLS, arXiv:1911.12504) provides mathematical models for pheromone impact with decay in independent RL agents, and **S-MADRL** (arXiv:2510.03592, 2025) implements a virtual pheromone map overlaid on environments where traces diffuse and decay over time.

**Hebbian plasticity (STDP for adaptive agent connections)** is best sourced from spiking neural network frameworks. **BindsNET** (AGPL-3.0, ~1.7k stars, *Frontiers in Neuroinformatics* 2018) provides built-in STDP and **reward-modulated STDP (R-STDP)**, where connection weights between neuron populations adapt based on correlated firing and reward signals — directly applicable to strengthening successful agent-to-agent connections. GitHub: `github.com/BindsNET/bindsnet`

**snnTorch** (MIT, ~2k stars, *Proceedings of the IEEE* 2023) offers the most modern, well-documented SNN framework with configurable decay rates modeling how connection strengths fade over time, and with MIT licensing. **Norse** (LGPLv3, ~795 stars) provides PyTorch-native spiking neuron primitives with adaptive thresholds. For the theoretical foundation, **Differentiable Plasticity** (Miconi/Uber, arXiv:1804.02464, 2018) provides the key formula: `effective_weight = w_fixed + α × hebbian_trace`, where the plastic component stores rolling correlation between pre/post activity and can be trained end-to-end via backprop.

---

## 9. LLM serving and vector databases: a mature infrastructure layer

The local LLM serving landscape has a clear hierarchy. **Ollama** (MIT, **~120k stars**) is the easiest on-ramp — one-command install, built on llama.cpp, with an OpenAI-compatible API at `/v1/chat/completions`. **llama.cpp** (MIT, **~80k stars**) provides the best CPU performance with zero dependencies, GGUF quantization from 1.5-bit to 8-bit, and runs on everything from Raspberry Pi to multi-GPU servers. For production GPU throughput, **vLLM** (Apache 2.0, ~70.2k stars) is the standard with PagedAttention and continuous batching, while **SGLang** (Apache 2.0, ~23.5k stars, powering xAI's Grok) shows **29%+ higher throughput** than vLLM in 2025/2026 benchmarks via RadixAttention prefix caching. Note that **TGI entered maintenance mode in December 2025**; HuggingFace now recommends vLLM or SGLang.

For vector databases, the local-first winners are:

- **LanceDB** (Apache 2.0, ~9.3k stars): Truly embedded/serverless — `pip install lancedb`, no server process, Lance columnar format on local disk, vector + full-text search, multimodal support. Best embedded experience.
- **Qdrant** (Apache 2.0, ~29.7k stars): Rust-native, in-memory or on-disk with rich JSON filtering, sparse+dense hybrid search, **up to 64× memory reduction** via quantization. AutoMem (implementing HippoRAG 2 principles) uses Qdrant as its vector layer.
- **ChromaDB** (Apache 2.0, ~26k stars): 4-line API, auto-embedding, 90k+ dependent codebases. Best for rapid prototyping.
- **FAISS** (MIT, ~34k stars): Maximum raw search performance as a library (no DB overhead), proven at Meta scale with 1.5 trillion vectors.
- **Milvus** (Apache 2.0, ~43.4k stars): Distributed architecture for billions of vectors, with Milvus Lite for embedded local use.

| LLM server | Best for | API compat | License | Stars |
|-----------|----------|------------|---------|-------|
| **Ollama** | Dev/prototyping | ✅ OpenAI | MIT | 120k |
| **llama.cpp** | CPU/edge | ✅ OpenAI | MIT | 80k |
| **vLLM** | Production GPU | ✅ OpenAI | Apache-2.0 | 70k |
| **SGLang** | Max throughput | ✅ OpenAI+Anthropic | Apache-2.0 | 23.5k |

---

## 10. The complete component map across all eight layers

Every layer of the OpenBrainLM architecture maps to production-ready open-source building blocks. The table below shows the primary recommendation and its associated peer-reviewed paper for each architectural component:

| Layer / Component | Primary tool | License | Stars | Paper |
|-------------------|-------------|---------|-------|-------|
| **L1 Bridge** (LLM backend) | Ollama → vLLM/SGLang | MIT/Apache | 120k/70k | — |
| **L1 Bridge** (Vector DB) | Qdrant / LanceDB | Apache-2.0 | 30k/9k | — |
| **L2 Ganglion** (Orchestrator) | LangGraph | MIT | 26.2k | — |
| **L3 Stigmergy** (Pheromone) | ACOpy + file-based patterns | Apache-2.0 | — | SIRL (IEEE TNNLS) |
| **L4 Basal Ganglia** (Routing) | semantic-router + pymdp | MIT | 3.3k/619 | GlobeCom 2024 / JOSS 2022 |
| **L5 Hippocampus** (Memory retrieval) | HippoRAG v2 | Open | 3.3k | NeurIPS 2024, ICML 2025 |
| **L5 Consolidation** (Memory tiers) | CraniMem + Letta | Apache-2.0 | —/19.3k | arXiv:2603.15642 / arXiv:2310.08560 |
| **L6 Relevance** (Quorum debate) | DebateLLM + Aegean pattern | Apache-2.0 | 53 | arXiv:2311.17371 / arXiv:2512.20184 |
| **L8 Trinity** (Dialectic engine) | MAD framework + Reflexion | GPL-3.0/MIT | 400+/3.1k | ACL 2024 / NeurIPS 2023 |
| **Morphogen** (Topology evolution) | neat-python → TensorNEAT | BSD-3/— | 1.5k/343 | Stanley 2002 / GECCO 2024 Best Paper |
| **NotebookLM clone** (Document Q&A) | Kotaemon + NeMo Guardrails | Apache-2.0 | 25.2k/5.2k | GaRAGe (ACL 2025) |
| **Source grounding** (Citation) | Self-RAG + ALCE benchmark | MIT | 2.3k/511 | ICLR 2024 / EMNLP 2023 |
| **Prediction error** (Free energy) | pymdp + PyHGF + D-MEM | MIT/GPL | 619/— | JOSS 2022 / arXiv:2603.14597 |
| **Hebbian plasticity** (STDP) | snnTorch / BindsNET | MIT/AGPL | 2k/1.7k | Proc. IEEE 2023 / Frontiers 2018 |

---

## Conclusion: assembly, not invention

The OpenBrainLM architecture is buildable today from existing, peer-reviewed components. Three integration priorities emerge. **First**, the NotebookLM clone stack (Kotaemon + NeMo Guardrails + Self-RAG reflection tokens) delivers the critical source-grounding guarantee — the system that never goes beyond what sources say. **Second**, the basal ganglia routing chain (semantic-router for fast paths + pymdp for active inference slow paths + D-MEM-style RPE gating) creates the core dispatch intelligence. **Third**, the hippocampal memory system (HippoRAG v2 for knowledge graph indexing + CraniMem for multi-tier consolidation + Qdrant as the embedding backend) provides neurobiologically-grounded long-term memory.

The most novel finding is the **D-MEM paper** (March 2026), which already maps biological reward prediction error gating onto LLM agent memory — precisely the cross-cutting mechanism OpenBrainLM needs for surprise-based routing. Combined with MAD's affirmative/negative/moderator debate structure for the Trinity Engine, and TensorNEAT's GPU-accelerated topology evolution for the Morphogen agent, the full biomimetic stack — octopus distributed processing, insect stigmergy, human cognition — assembles from parts that already exist and already work.

The primary licensing risk is GPL-3.0 on TensorNEAT/EvoX (use neat-python BSD-3 as fallback), MAD (use DebateLLM Apache-2.0 as alternative), and PyHGF (isolate via wrapper). All other primary recommendations carry MIT, Apache 2.0, or BSD licenses. Every tool runs fully self-hosted and offline.

---

## Knowledge Backend Strategy (Swappable, NOT Core Brain)

Knowledge backends are PLUGGABLE via bridge.py — they are NOT the brain:

1. **LocalMarkdownStore** — works now, keyword search, zero dependencies (fallback)
2. **Kotaemon** — local document Q&A with embeddings (primary local backend)
3. **NotebookLM MCP** — Google's service, works now, v1 integration (temporary)
4. **Google Drive** — source document storage (integration layer)
5. **[Community Request]** — build open-source NotebookLM replacement

## Brain Core (LOCKED IN — must self-evolve)

These are the parts that ARE the brain — not swappable, they self-improve:

- L4 routing (semantic-router + pymdp active inference)
- L5 hippocampal indexing (HippoRAG v2)
- L5 consolidation (CraniMem tiers + Letta memory)
- L6 quorum (DebateLLM + Aegean)
- Trinity dialectic (MAD framework)
- Hebbian plasticity (snnTorch STDP)
- Morphogen evolution (neat-python → TensorNEAT)
- Prediction error (D-MEM RPE gating)
