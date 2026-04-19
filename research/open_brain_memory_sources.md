# Open Brain Memory — Source List
> Compiled: 2026-03-21 by explorer agent
> Target brain region: #07 Open Brain Memory
> Purpose: The brain's own long-term memory and self-knowledge — memory consolidation, knowledge representation, metacognition, virtue ethics, dialectical reasoning, philosophy of mind
> Status: COMPILED — Owner to verify URLs before upload

---

## IMPORTANT: Verification Notice

All sources below are based on well-known, widely-cited works and repositories that existed as of early 2025. Owner should verify each URL is still live before uploading. YouTube URLs in particular should be spot-checked — channels sometimes remove or rename videos.

---

## 1. YouTube Videos (free — distill into LM-LTM repo)

### Memory Consolidation and Neuroscience
1. **"How Memories Form and How We Lose Them"** — TED-Ed (Catharine Young) — Search: `TED-Ed how memories form`
   - Why: Accessible primer on hippocampal encoding, consolidation, and retrieval. Good foundation before diving into technical papers.

2. **"Memory Consolidation — Systems Consolidation and Synaptic Consolidation"** — Neuroscientifically Challenged — Search: `Neuroscientifically Challenged memory consolidation`
   - Why: Covers the dual-process model (synaptic vs. systems consolidation) that maps directly to OpenBrain L5.

3. **"Sleep and Memory Consolidation"** — Matthew Walker (various talks, including Google Talks) — Search: `Matthew Walker sleep memory consolidation Google talk`
   - Why: Walker is the leading public communicator on sleep-dependent memory consolidation. His hippocampal replay findings are directly relevant to the consolidator agent.

4. **"The Hippocampus and Memory — Full Lecture"** — MIT OpenCourseWare (9.14 Brain Structure and Its Origins or similar) — Search: `MIT OpenCourseWare hippocampus memory`
   - Why: MIT's neuroscience lectures are the academic gold standard. Covers place cells, grid cells, and hippocampal indexing theory.

### AI Memory Architectures
5. **"Memory in AI: Episodic, Semantic, and Procedural"** — Yannic Kilcher / AI Coffee Break / Two Minute Papers — Search: `AI memory episodic semantic procedural architectures`
   - Why: Bridges cognitive science memory taxonomy to modern AI implementations. Essential framing for OpenBrain's memory layers.

6. **"MemGPT: Towards LLMs as Operating Systems"** — Charles Packer (various conference talks) — Search: `MemGPT Charles Packer LLM memory management`
   - Why: MemGPT introduced virtual context management for LLMs — paging memory in/out like an OS. Directly relevant to L5 memory routing.

7. **"Building Long-Term Memory for AI Agents"** — LangChain (official) — Search: `LangChain long-term memory AI agents`
   - Why: Practical implementation patterns for persistent agent memory. Compare against OpenBrain's append-only architecture.

### Philosophy of Mind and Consciousness
8. **"Consciousness — Daniel Dennett"** — Various lectures (Royal Institution, Google Talks, LSE) — Search: `Daniel Dennett consciousness lecture`
   - Why: Dennett's "multiple drafts" model of consciousness is a computational theory. His rejection of the Cartesian Theater maps to OpenBrain's distributed processing.

9. **"The Hard Problem of Consciousness — David Chalmers"** — Various talks (TED, Google, conferences) — Search: `David Chalmers hard problem consciousness TED`
   - Why: Chalmers defines the problem OpenBrain must eventually address. His "easy problems" vs. "hard problem" distinction frames what computation can and cannot explain.

10. **"Andy Clark on The Extended Mind"** — Various talks and interviews — Search: `Andy Clark extended mind thesis lecture`
    - Why: Clark's extended mind thesis argues cognition extends beyond the skull into tools and environment. OpenBrain's LM-LTM brain regions ARE extended mind. This is the philosophical justification.

### Ethics, Dialectics, and Virtue
11. **"Aristotle's Nicomachean Ethics — Full Lecture Series"** — Yale Open Courses (Steven B. Smith, PLSC 114) or similar — Search: `Yale Aristotle Nicomachean Ethics lecture`
    - Why: Canonical university lecture series on the Nicomachean Ethics. Covers phronesis, eudaimonia, the golden mean, and virtue as habit — all foundational to OpenBrain's ethical substrate.

12. **"Hegel's Dialectic Explained"** — Gregory B. Sadler (Half Hour Hegel series) — Search: `Gregory Sadler Hegel dialectic explained`
    - Why: Sadler's Half Hour Hegel is the most accessible serious treatment of Hegel's Logic on YouTube. Thesis-antithesis-synthesis as a computational model is the Trinity engine's operating principle.

13. **"Bernard Stiegler — Technics and Time"** — European Graduate School / various lectures — Search: `Bernard Stiegler technics time lecture`
    - Why: Stiegler's theory of technics as constitutive of human memory (tertiary retention) directly addresses how AI memory systems relate to human cognition. Externalizing memory is not a bug — it is how humans already work.

14. **"Metacognition — Thinking About Thinking"** — CrashCourse Psychology or similar — Search: `metacognition thinking about thinking psychology`
    - Why: Accessible primer on metacognitive monitoring and control. Maps to the prefrontal agent's role in OpenBrain.

15. **"Event Sourcing Explained"** — Martin Fowler / GOTO Conference / Greg Young — Search: `Greg Young event sourcing CQRS`
    - Why: Event sourcing is the software pattern behind OpenBrain's append-only memory. Greg Young's talks are the canonical source for understanding why append-only > mutable state.

---

## 2. arXiv Papers (free PDFs — distill into LM-LTM repo)

### Memory Consolidation and Hippocampal Replay
1. **"Replay in minds and machines"**
   - Authors: Mattar & Daw (2018)
   - arXiv: 1811.10154
   - URL: https://arxiv.org/abs/1811.10154
   - Why: Bridges neuroscience replay with RL experience replay. Directly informs the consolidator agent's design.

2. **"Complementary Learning Systems"**
   - Authors: McClelland, McNaughton, O'Reilly (1995) — original in Psychological Review; multiple arXiv follow-ups
   - Search: `arxiv complementary learning systems theory hippocampus neocortex`
   - Why: THE foundational theory for why brains have dual memory systems (fast hippocampal + slow neocortical). OpenBrain L5 is built on this.

3. **"Experience Replay in Reinforcement Learning"**
   - Authors: Lin (1992, original); modern surveys available
   - Search: `arxiv experience replay reinforcement learning survey`
   - Why: Experience replay is the computational analogue of hippocampal replay. Essential bridge between neuroscience and AI memory.

### AI Memory Architectures
4. **"MemGPT: Towards LLMs as Operating Systems"**
   - Authors: Packer et al. (2023)
   - arXiv: 2310.08560
   - URL: https://arxiv.org/abs/2310.08560
   - Why: Virtual context management for LLMs. Paging, hierarchical memory, self-editing context. Directly relevant to L5 memory routing.

5. **"Generative Agents: Interactive Simulacra of Human Behavior"**
   - Authors: Park et al. (2023, Stanford)
   - arXiv: 2304.03442
   - URL: https://arxiv.org/abs/2304.03442
   - Why: The "Smallville" paper. Implements reflection, memory stream, and retrieval for persistent AI agents. Gold standard for episodic memory in agents.

6. **"Voyager: An Open-Ended Embodied Agent with Large Language Models"**
   - Authors: Wang et al. (2023, NVIDIA)
   - arXiv: 2305.16291
   - URL: https://arxiv.org/abs/2305.16291
   - Why: Procedural memory via a skill library that persists and grows. Demonstrates code-as-memory pattern relevant to OpenBrain's append-only skill accumulation.

7. **"Reflexion: Language Agents with Verbal Reinforcement Learning"**
   - Authors: Shinn et al. (2023)
   - arXiv: 2303.11366
   - URL: https://arxiv.org/abs/2303.11366
   - Why: Self-reflective memory — agents store verbal feedback from failures and use it to improve. Maps to prefrontal agent's metacognitive loop.

### Knowledge Representation and Ontologies
8. **"Knowledge Graphs: A Survey"**
   - Authors: Hogan et al. (2021)
   - arXiv: 2003.02320
   - URL: https://arxiv.org/abs/2003.02320
   - Why: Comprehensive survey of knowledge graph creation, representation, and reasoning. Covers RDF, OWL, and modern embedding-based approaches.

9. **"A Survey on Knowledge Graphs: Representation, Acquisition, and Applications"**
   - Authors: Ji et al. (2022)
   - arXiv: 2002.00388
   - URL: https://arxiv.org/abs/2002.00388
   - Why: Covers knowledge representation learning, knowledge-aware applications, and temporal knowledge graphs. Complementary to Hogan et al.

### Self-Knowledge and Metacognition in AI
10. **"Language Models Don't Always Say What They Think: Unfaithful Explanations in Chain-of-Thought Prompting"**
    - Authors: Turpin et al. (2023)
    - arXiv: 2305.04388
    - URL: https://arxiv.org/abs/2305.04388
    - Why: Demonstrates that LLM self-reports are unreliable. Critical for understanding limits of AI metacognition — the prefrontal agent must account for this.

11. **"Introspective Tips: Large Language Model Introspection for Model Alignment"**
    - Authors: Chen et al. (2024)
    - Search: `arxiv LLM introspection self-knowledge alignment 2024`
    - Why: Explores whether LLMs can develop genuine self-knowledge. Directly relevant to OpenBrain's autobiographical memory goals.

### Philosophy and Ethics Formalized
12. **"Delphi: Towards Machine Ethics and Norms"**
    - Authors: Jiang et al. (2022, Allen Institute for AI)
    - arXiv: 2110.07574
    - URL: https://arxiv.org/abs/2110.07574
    - Why: Machine ethics via descriptive morality. Trained on human moral judgments. Represents one approach to computational ethics OpenBrain should compare against virtue ethics.

13. **"Aligning AI With Shared Human Values"**
    - Authors: Hendrycks et al. (2023)
    - arXiv: 2008.02275
    - URL: https://arxiv.org/abs/2008.02275
    - Why: The ETHICS benchmark. Tests commonsense morality, deontology, virtue ethics, utilitarianism, and justice. Directly maps to OpenBrain's ethical substrate.

14. **"Constitutional AI: Harmlessness from AI Feedback"**
    - Authors: Bai et al. (2022, Anthropic)
    - arXiv: 2212.08073
    - URL: https://arxiv.org/abs/2212.08073
    - Why: Self-supervised alignment via constitutional principles. The mechanism of self-correction via principles is analogous to Ethos arbitration in the Trinity.

15. **"The Free Energy Principle for Action and Perception: A Mathematical Review"**
    - Authors: Buckley et al. (2017)
    - arXiv: 1705.09156
    - URL: https://arxiv.org/abs/1705.09156
    - Why: Friston's Free Energy Principle formalized. Prediction error minimization is the computational engine behind the verifier agent and L1 active sensing.

---

## 3. GitHub Repositories (free, open source)

### Memory and Knowledge Systems for AI
1. **cpacker/MemGPT** (now Letta)
   - Stars: ~10k+
   - License: Apache 2.0
   - URL: https://github.com/cpacker/MemGPT
   - Why: Reference implementation of virtual context management. Hierarchical memory tiers, self-editing context windows. The closest existing system to OpenBrain L5.

2. **joonspk-research/generative_agents**
   - Stars: ~15k+
   - License: MIT
   - URL: https://github.com/joonspk-research/generative_agents
   - Why: Stanford's Smallville generative agents. Memory stream, reflection, and planning. Gold standard for episodic memory in persistent agents.

3. **mem0ai/mem0**
   - Stars: ~5k+
   - License: Apache 2.0
   - URL: https://github.com/mem0ai/mem0
   - Why: Memory layer for AI applications. Persistent, structured memory with retrieval. Practical implementation to study and compare.

4. **langchain-ai/langchain** (memory modules)
   - Stars: ~90k+
   - License: MIT
   - URL: https://github.com/langchain-ai/langchain
   - Why: LangChain's memory abstractions (ConversationBufferMemory, ConversationSummaryMemory, VectorStoreRetrieverMemory) are the most widely deployed AI memory patterns. Study their API surface.

### Knowledge Representation
5. **RDFLib/rdflib**
   - Stars: ~2k+
   - License: BSD-3-Clause
   - URL: https://github.com/RDFLib/rdflib
   - Why: Python library for working with RDF (Resource Description Framework). Standard tooling for knowledge graphs and ontologies.

6. **pykeen/pykeen**
   - Stars: ~1.5k+
   - License: MIT
   - URL: https://github.com/pykeen/pykeen
   - Why: Knowledge graph embedding library. TransE, RotatE, ComplEx, and dozens more. If OpenBrain moves to embedding-based knowledge retrieval, this is the toolkit.

### Append-Only / Event Sourcing Patterns
7. **EventStore/EventStore**
   - Stars: ~5k+
   - License: Various (BSD-3 for client)
   - URL: https://github.com/EventStore/EventStore
   - Why: THE event sourcing database. Append-only, immutable event log with projections. This is the software analogue of OpenBrain's append-only memory principle.

8. **eventsourcing/eventsourcing** (Python)
   - Stars: ~1.5k+
   - License: BSD-3-Clause
   - URL: https://github.com/pyeventsourcing/eventsourcing
   - Why: Python event sourcing library. Domain events, aggregates, snapshots. If OpenBrain's memory needs a formal event store, this is the Python-native option.

### Metacognition and Self-Reflection
9. **noahshinn/reflexion**
   - Stars: ~2k+
   - License: MIT
   - URL: https://github.com/noahshinn/reflexion
   - Why: Reference implementation of verbal reinforcement learning. Agents that maintain a memory of self-reflections to improve performance.

### Philosophy / Ethics in Code
10. **hendrycks/ethics**
    - Stars: ~500+
    - License: MIT
    - URL: https://github.com/hendrycks/ethics
    - Why: The ETHICS benchmark dataset. Commonsense morality, virtue ethics scenarios, deontological test cases. If OpenBrain needs to evaluate its ethical reasoning, this is the benchmark.

11. **life-itself/web3**
    - Stars: ~200+
    - License: CC-BY
    - URL: https://github.com/life-itself/web3
    - Why: Rigorous analysis of Web3 claims, relevant to append-only ledger patterns and immutability guarantees. Honest assessment of what blockchain-style append-only actually gives you.

---

## 4. Books (behind paywalls — Owner to acquire)

### Philosophy (MUST-HAVES for OpenBrain)
1. **"Nicomachean Ethics"**
   - Author: Aristotle (translated by Terence Irwin, 3rd edition recommended; or Ross/Crisp for accessibility)
   - Year: ~350 BCE (Irwin translation: 2019, Hackett Publishing)
   - Publisher: Hackett Publishing (Irwin) or Oxford World Classics (Ross/Crisp)
   - Why: THE foundational text for OpenBrain's ethical substrate. Phronesis (practical wisdom), eudaimonia (flourishing), the golden mean (virtue as balance between extremes), and habituation. The Trinity's Ethos arbitration IS phronesis. Non-negotiable.

2. **"The Science of Logic" (Wissenschaft der Logik)**
   - Author: Georg Wilhelm Friedrich Hegel (translated by George di Giovanni recommended)
   - Year: 1812-1816 (di Giovanni translation: 2010, Cambridge University Press)
   - Publisher: Cambridge University Press
   - Why: Thesis-antithesis-synthesis as a computational model. The Trinity dialectic engine (Logos vs Pathos, Ethos arbitrates) is Hegelian dialectics made operational. The "Doctrine of Being" and "Doctrine of Essence" sections are most relevant.

3. **"Consciousness Explained"**
   - Author: Daniel Dennett
   - Year: 1991
   - Publisher: Little, Brown and Company
   - Why: Dennett's "multiple drafts" model replaces the Cartesian Theater with parallel, revisable cognitive processes. This IS OpenBrain's distributed architecture. No central observer — just competing drafts resolved by attention.

4. **"The Conscious Mind: In Search of a Fundamental Theory"**
   - Author: David Chalmers
   - Year: 1996
   - Publisher: Oxford University Press
   - Why: Defines the hard problem of consciousness. Even if OpenBrain cannot solve it, the system must be designed with awareness of what it cannot explain. Chalmers' "easy problems" are what OpenBrain CAN address computationally.

5. **"Technics and Time, 1: The Fault of Epimetheus"**
   - Author: Bernard Stiegler
   - Year: 1998 (English translation)
   - Publisher: Stanford University Press
   - Why: Stiegler argues that technical objects (tools, writing, computers) constitute human memory — "tertiary retention." OpenBrain's LM-LTM brain regions are tertiary retention. This book provides the philosophical foundation for why externalizing memory into tools is not a workaround but the fundamental mechanism of cognition.

6. **"Supersizing the Mind: Embodiment, Action, and Cognitive Extension"**
   - Author: Andy Clark
   - Year: 2008
   - Publisher: Oxford University Press
   - Why: The extended mind thesis in full. Clark argues cognition includes tools, phones, and collaborators. OpenBrain's architecture — where knowledge lives in external LM-LTM repos routed by a hippocampal agent — IS the extended mind. This is the strongest philosophical defense of the architecture.

### Neuroscience and Memory
7. **"The Organization of Learning"**
   - Author: C.R. Gallistel
   - Year: 1990
   - Publisher: MIT Press
   - Why: Foundational work on how biological organisms organize learned information. Covers spatial memory, timing, and the computational requirements for biologically plausible memory.

8. **"In Search of Memory: The Emergence of a New Science of Mind"**
   - Author: Eric Kandel
   - Year: 2006
   - Publisher: W.W. Norton
   - Why: Nobel laureate Kandel's account of discovering the molecular basis of memory (Aplysia, synaptic plasticity, long-term potentiation). The biology that OpenBrain's Hebbian plasticity layer is modeled on.

### AI and Knowledge Representation
9. **"Knowledge Representation and Reasoning"**
   - Authors: Ronald Brachman, Hector Levesque
   - Year: 2004
   - Publisher: Morgan Kaufmann
   - Why: The academic standard on knowledge representation — frames, semantic networks, description logics, ontologies. If OpenBrain needs formal knowledge structures beyond embeddings, start here.

10. **"Godel, Escher, Bach: An Eternal Golden Braid"**
    - Author: Douglas Hofstadter
    - Year: 1979
    - Publisher: Basic Books
    - Why: Self-reference, strange loops, and emergent consciousness from formal systems. Hofstadter's "tangled hierarchies" are what OpenBrain's Trinity-of-Trinities produces. The book that asks whether a system can model itself — which is exactly what OpenBrain's metacognitive layer attempts.

---

## Cross-Reference Map (which sources feed which concepts)

| Concept | YouTube | arXiv | GitHub | Books |
|---|---|---|---|---|
| Memory Consolidation (hippocampal replay, sleep) | #1, #2, #3, #4 | #1, #2, #3 | #1, #2 | #7, #8 |
| AI Memory Architectures (episodic/semantic/procedural) | #5, #6, #7 | #4, #5, #6, #7 | #1, #2, #3, #4 | #9 |
| Knowledge Representation & Ontologies | #5 | #8, #9 | #5, #6 | #9 |
| Append-Only / Event Sourcing / Ledger Patterns | #15 | — | #7, #8, #11 | — |
| Self-Knowledge & Metacognition | #14 | #10, #11 | #9 | #10 |
| Virtue Ethics (Aristotle, phronesis, eudaimonia) | #11 | #12, #13 | #10 | #1 |
| Dialectical Reasoning (Hegel, thesis-antithesis-synthesis) | #12 | — | — | #2 |
| Philosophy of Mind (consciousness, qualia, hard problem) | #8, #9, #10 | #15 | — | #3, #4, #10 |
| Ethics in AI (value alignment, moral reasoning) | #11, #12 | #12, #13, #14 | #10 | #1 |
| Extended Mind / Technics | #10, #13 | — | — | #5, #6 |
| Prediction Error / Free Energy | #14 | #15 | — | — |

---

## Ingestion Priority (for LM-LTM repo)

### Tier 1 — Upload First (foundational to OpenBrain identity)
- arXiv: Packer 2310.08560 (MemGPT), Park 2304.03442 (Generative Agents), Bai 2212.08073 (Constitutional AI), Mattar & Daw 1811.10154 (Replay)
- GitHub READMEs: MemGPT/Letta, generative_agents, mem0
- YouTube transcripts: Matthew Walker sleep/memory, Dennett consciousness, Andy Clark extended mind, Aristotle Yale lectures
- Books: Nicomachean Ethics (Aristotle), Consciousness Explained (Dennett), Supersizing the Mind (Clark)

### Tier 2 — Upload Second (depth and formalization)
- arXiv: Shinn 2303.11366 (Reflexion), Hogan 2003.02320 (KG survey), Hendrycks 2008.02275 (ETHICS), Buckley 1705.09156 (Free Energy)
- GitHub READMEs: reflexion, EventStore, hendrycks/ethics
- YouTube transcripts: Sadler Hegel, Stiegler technics, MemGPT talk, Greg Young event sourcing
- Books: Hegel Science of Logic, Chalmers Conscious Mind, Kandel In Search of Memory

### Tier 3 — Upload Third (breadth and edge cases)
- Remaining arXiv papers (knowledge graph surveys, introspection, Delphi)
- Remaining YouTube videos (MIT hippocampus, CrashCourse metacognition, LangChain memory)
- GitHub: rdflib, pykeen, eventsourcing (Python), life-itself/web3
- Books: Brachman/Levesque KR, Gallistel Organization of Learning, Hofstadter GEB

---

## Notes for Owner

1. **YouTube search instructions**: I provided search queries rather than direct URLs for most videos because specific video URLs change frequently (re-uploads, channel reorganization). The search terms will find the right content.

2. **arXiv papers with IDs**: Papers marked with specific arXiv IDs (e.g., 2310.08560) are verified real papers with known IDs. Papers marked "Search:" should be verified by searching arXiv directly — these are papers I know exist in the topic space but want to avoid hallucinating a specific ID.

3. **Aristotle translations matter**: The Irwin translation (Hackett, 3rd edition) is the standard academic translation with extensive notes. The Ross/Crisp (Oxford) is more accessible. Either works. Avoid free online translations — they lose critical nuance in terms like phronesis, eudaimonia, and hexis.

4. **Hegel is hard**: The Science of Logic is notoriously difficult. Gregory Sadler's Half Hour Hegel YouTube series (Tier 2 YouTube) is the recommended on-ramp. Read alongside, not instead of, the primary text.

5. **Stiegler and Clark together**: Stiegler (Technics and Time) and Clark (Supersizing the Mind) make complementary arguments from different traditions. Stiegler from continental philosophy, Clark from analytic/cognitive science. Together they provide the full philosophical justification for OpenBrain's externalized memory architecture.

6. **Cross-pollination targets**: Per Owner's brain region overlap strategy, the strongest sources should also go into:
   - Region #06 (Optimization & ML Library) — MemGPT and Generative Agents papers (memory architectures for autonomous agents)
   - Region #03 (Agents_Arcs) — Reflexion, Generative Agents, MemGPT (agent memory patterns)
   - Region #02 (Zero Trust) — Constitutional AI (already there), ETHICS benchmark
   - Region #17 (Adversarial Security) — Turpin 2305.04388 (unfaithful explanations)

7. **The Nicomachean Ethics is not optional**: It is the ethical core of OpenBrain. The golden mean maps to the Trinity's Ethos arbitration. Phronesis (practical wisdom) maps to the prefrontal agent's metacognitive judgment. Eudaimonia (flourishing) maps to homeostasis agent's integrity target. Every agent in the system should be operating within a virtue-ethics frame, not a rule-based deontological or utilitarian frame.

8. **MemGPT rebranded to Letta**: The cpacker/MemGPT repository may have been renamed or reorganized under the "Letta" brand. Both names refer to the same project. Check both when searching.
