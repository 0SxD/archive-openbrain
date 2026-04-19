# Memory Architecture Research — Agents_Arcs Notebook
Date: 2026-03-24
Source: NotebookLM Agents_Arcs (slug: strategic-implementation-of-ze)
Session ID: 299beed2

---

## Question 1: Chronological vs Categorical

The notebook does not recommend a simple either/or. The findings are:

**Schema-Driven Consolidation is mandatory.**
Naive summarization during consolidation strips edge cases, decision structures, and constraints — turning multi-step reasoning into "vague, overarching glossy soup." Memory promotion must extract structured fields (e.g., JSON facts), not narrative text, to prevent context rot.

**The Passive Accumulation Fallacy.**
AI models have no native decay mechanism. Without an automated deprecation/decay trigger, a promoted-facts store becomes wildly noisy over time — the agent cannot distinguish a critical rule from five days ago from noise from five minutes ago. Both chronological and categorical structures need explicit decay/deprecation logic.

**Two-Stage Retrieval is required for correctness.**
Semantic/vector retrieval recalls broad themes but fails on exact specifics. For knowledge that must be retrieved by topic AND by time, the pattern is:
1. Fuzzy semantic search (topic-level retrieval)
2. Strict second-stage exact verification pass against known ground truth

**Self-modification (sleep cycles) requires external state isolation.**
Knowledge that evolves must live in an external, structurally isolated state file (JSON log, Git commit) — never in the agent's context window. The agent wakes, reads the external file, starts fresh. Evolution lives in the file architecture, not in memory.

---

## Question 2: Indexing and Routing

**Flat file with tags = anti-pattern.**
A single monolithic bucket creates a "memory wall": retrieval becomes noisy, expensive, and jams the agent's context window. Research explicitly rejects this approach.

**Tiered Memory Architecture is the production pattern** (sourced from Google's Agent Development Kit ADK and supporting research):

| Store Type | Query Pattern |
|---|---|
| Semantic/Vector Storage | Topic or meaning-based retrieval ("what similar work have we done?") |
| Event Logs | Chronological/procedural retrieval — exact trajectory of past actions |
| Structured Data (Key-Value) | Permanent categorical facts and preferences |

Large documents/artifacts should be referenced by tags or handles — never stuffed directly into the active context window.

**Agent default working context should contain "nearly nothing."**
Rather than pinning a massive flat file to every prompt, the agent actively queries and retrieves highly relevant, structured information on demand. Volume increases noise: a 1-million-token unsorted context is practically worse than a tightly curated 10,000-token window.

**Retrieval accuracy benchmarks (from the research):**
- Sonnet 4.5: 18.5% needle-in-haystack retrieval success rate across massive context
- Gemini 3 Pro: ~26.3%
- Claude Opus 4.6: 76% at 1M tokens, 93% at 256k tokens

**Two-stage retrieval applies here too:**
Fuzzy semantic search + strict verification pass against ground truth. Relying on semantic search alone for precise facts causes hallucination bleed from quarantine.

**Routing table (pointer architecture) > flat file.**
The correct pattern is a routing/pointer layer that directs queries to the correct tier/topic-specific store. The routing layer is lean; the stores hold the content.

---

## Key Takeaways

1. **Use a tiered routing architecture, not a flat file.** Three distinct stores minimum: semantic/vector (topic retrieval), event log (chronological), key-value (categorical facts). A routing table points to the right store per query type. Never consolidate these into one file.

2. **Schema-driven consolidation only.** Promote structured fields (JSON facts, decision records with statement + confidence + source + status) — never narrative summaries. Narrative consolidation produces context rot that is unrecoverable.

3. **Agent working context must be nearly empty by default.** Pin nothing large to the prompt. Retrieve on demand from the appropriate tier. A 10k curated context outperforms 1M tokens of unsorted memory.

4. **Two-stage retrieval is mandatory for precision.** Semantic search finds the neighborhood; a strict verification pass against ground truth finds the exact fact. Single-stage semantic search alone will hallucinate on specifics.

5. **Decay/deprecation logic is required, not optional.** AI has no native forgetting. Without explicit expiry triggers or confidence decay, any promoted-facts store degrades into noise over time. Every long_term.md entry needs a `last_verified_date` and a review trigger.
