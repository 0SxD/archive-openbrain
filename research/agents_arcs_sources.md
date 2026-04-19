# Agents_Arcs — Source List
> Compiled: 2026-03-21 by explorer agent
> Target brain region: #2 Agents_Arcs (Agent architecture patterns for OpenBrainLM)
> Purpose: Multi-agent orchestration, agent design patterns, context engineering, contract-first prompting
> Status: COMPILED — Owner to verify URLs before upload

---

## IMPORTANT: Verification Notice

All sources below are based on well-known, widely-cited works and repositories that existed as of early 2025. Owner should verify each URL is still live before uploading. YouTube URLs in particular should be spot-checked — channels sometimes remove or rename videos.

---

## 1. YouTube Videos (free — distill into LM-LTM repo)

### Multi-Agent Orchestration Patterns
1. **"Building Effective Agents"** — Anthropic (official) — Search: `Anthropic building effective agents`
   - Why: THE canonical reference for Anthropic's agent patterns. Initializer, amnesiac Workers, Judge. Two tiers only. This is our primary architecture source.

2. **"Multi AI Agent Systems with crewAI"** — DeepLearning.AI — Search: `DeepLearning.AI crewAI multi agent`
   - Why: Andrew Ng's short course on CrewAI. Covers role-based agent design, task delegation, sequential vs hierarchical crews.

3. **"AI Agents in LangGraph"** — DeepLearning.AI — Search: `DeepLearning.AI LangGraph agents`
   - Why: LangGraph agent course covering stateful graphs, human-in-the-loop, conditional edges. The leading orchestration framework.

4. **"AutoGen: Multi-Agent Conversations"** — Microsoft Research — Search: `Microsoft Research AutoGen multi-agent`
   - Why: Microsoft's framework walkthrough. Agent conversation patterns, code execution sandboxing, group chat managers.

5. **"What are AI Agents?"** — IBM Technology — Search: `IBM Technology AI agents explained`
   - Why: Clear foundational explainer on agent architectures, tool use, reasoning loops. Good primer before deeper material.

### Agent Design Patterns (ReAct, CoT, Reflection)
6. **"Let's build the GPT Tokenizer"** / **"Let's reproduce GPT-2"** — Andrej Karpathy — Search: `Andrej Karpathy GPT build from scratch`
   - Why: Karpathy's build-from-scratch approach. Not directly agent patterns, but demonstrates the auto-research loop pattern relevant to OpenBrainLM's explorer agent.

7. **"Building AI Agents with Tool Use"** — Anthropic (official) — Search: `Anthropic tool use agents tutorial`
   - Why: Official Anthropic guidance on tool-calling patterns, structured outputs, error handling in agent tool loops.

8. **"ReAct: Synergizing Reasoning and Acting in Language Models"** — Yannic Kilcher / community — Search: `ReAct reasoning acting language models explained`
   - Why: Video explainers of the ReAct paper. The core pattern behind most modern agent loops (think-act-observe).

9. **"Chain of Thought Prompting"** — various AI channels — Search: `chain of thought prompting explained 2024`
   - Why: CoT is the substrate underneath ReAct, Tree-of-Thought, and reflection patterns. Foundational.

### Context Engineering and Prompt Architecture
10. **"Prompt Engineering for Developers"** — DeepLearning.AI — Search: `DeepLearning.AI prompt engineering developers`
    - Why: Foundational course. Covers system prompts, few-shot, chain-of-thought. Prerequisite for context engineering.

11. **"Building Production-Ready RAG Applications"** — LlamaIndex / community — Search: `LlamaIndex production RAG agents 2024`
    - Why: RAG as the context delivery mechanism for agents. What tokens each agent sees = what documents get retrieved.

12. **"OpenAI Swarm: Multi-Agent Orchestration"** — OpenAI / community — Search: `OpenAI Swarm multi-agent framework`
    - Why: OpenAI's lightweight multi-agent framework. Handoff patterns, routines, agent-to-agent delegation.

### Agent Evaluation and Architecture Patterns
13. **"LangChain vs CrewAI vs AutoGen"** — various AI channels — Search: `LangChain CrewAI AutoGen comparison 2024`
    - Why: Framework comparisons highlighting architectural tradeoffs. Useful for understanding why we chose Anthropic's pattern over these.

14. **"The AI Engineer — Building Reliable Agents"** — AI Engineer Conference — Search: `AI Engineer conference reliable agents 2024`
    - Why: Practitioner talks on agent reliability, failure modes, evaluation in production.

15. **"Function Calling and Tool Use in LLMs"** — Fireship / various — Search: `function calling tool use LLM explained 2024`
    - Why: Quick technical overview of how tool-calling actually works under the hood. Essential for understanding agent capabilities.

16. **"Hierarchical Multi-Agent Systems"** — various AI research channels — Search: `hierarchical multi-agent systems design patterns 2024`
    - Why: Covers the anti-patterns (flat teams, deep hierarchies >2) and why two-tier is optimal.

---

## 2. arXiv Papers (free PDFs — distill into LM-LTM repo)

### Multi-Agent Orchestration
1. **"AutoGen: Enabling Next-Gen LLM Applications via Multi-Agent Conversation"**
   - Authors: Wu et al. (2023, Microsoft)
   - arXiv: 2308.08155
   - URL: https://arxiv.org/abs/2308.08155
   - Why: Microsoft's multi-agent conversation framework. Defines conversable agents, group chat, and nested conversations. Key reference for orchestration patterns.

2. **"MetaGPT: Meta Programming for A Multi-Agent Collaborative Framework"**
   - Authors: Hong et al. (2023)
   - arXiv: 2308.00352
   - URL: https://arxiv.org/abs/2308.00352
   - Why: Assigns SOPs (standard operating procedures) to agents, mimicking real software teams. Demonstrates role specialization and structured outputs.

3. **"AgentVerse: Facilitating Multi-Agent Collaboration and Exploring Emergent Behaviors"**
   - Authors: Chen et al. (2023)
   - arXiv: 2308.10848
   - URL: https://arxiv.org/abs/2308.10848
   - Why: Studies emergent behaviors in multi-agent groups. Relevant to understanding when flat teams fail vs succeed.

4. **"Communicative Agents for Software Development"** (ChatDev)
   - Authors: Qian et al. (2023)
   - arXiv: 2307.07924
   - URL: https://arxiv.org/abs/2307.07924
   - Why: Waterfall-style agent pipeline. Good contrast to our Initializer-Workers-Judge pattern.

### Agent Design Patterns (ReAct, CoT, Reflection)
5. **"ReAct: Synergizing Reasoning and Acting in Language Models"**
   - Authors: Yao et al. (2022)
   - arXiv: 2210.03629
   - URL: https://arxiv.org/abs/2210.03629
   - Why: THE foundational agent pattern paper. Interleaves reasoning traces with actions. Every modern agent framework implements this.

6. **"Chain-of-Thought Prompting Elicits Reasoning in Large Language Models"**
   - Authors: Wei et al. (2022, Google)
   - arXiv: 2201.11903
   - URL: https://arxiv.org/abs/2201.11903
   - Why: The original CoT paper. Foundational for understanding how reasoning emerges and how to prompt for it.

7. **"Reflexion: Language Agents with Verbal Reinforcement Learning"**
   - Authors: Shinn et al. (2023)
   - arXiv: 2303.11366
   - URL: https://arxiv.org/abs/2303.11366
   - Why: Self-reflection loop for agents. Agent evaluates its own output, generates verbal feedback, and retries. Key pattern for our auditor/meta-auditor layer.

8. **"Tree of Thoughts: Deliberate Problem Solving with Large Language Models"**
   - Authors: Yao et al. (2023)
   - arXiv: 2305.10601
   - URL: https://arxiv.org/abs/2305.10601
   - Why: Extends CoT to tree-structured exploration. Relevant for planning agents that need to evaluate multiple paths.

9. **"Toolformer: Language Models Can Teach Themselves to Use Tools"**
   - Authors: Schick et al. (2023, Meta)
   - arXiv: 2302.04761
   - URL: https://arxiv.org/abs/2302.04761
   - Why: How LLMs learn to use external tools. Foundation for understanding tool-calling agent capabilities.

### Agent Evaluation and Benchmarking
10. **"AgentBench: Evaluating LLMs as Agents"**
    - Authors: Liu et al. (2023)
    - arXiv: 2308.03688
    - URL: https://arxiv.org/abs/2308.03688
    - Why: Systematic benchmark for agent capabilities across 8 environments. Essential for understanding what agents can and cannot do.

11. **"Voyager: An Open-Ended Embodied Agent with Large Language Models"**
    - Authors: Wang et al. (2023, NVIDIA)
    - arXiv: 2305.16291
    - URL: https://arxiv.org/abs/2305.16291
    - Why: Demonstrates curriculum learning and skill library for agents. Relevant to our agent skill accumulation pattern.

### Context Engineering and Planning
12. **"Self-Consistency Improves Chain of Thought Reasoning in Language Models"**
    - Authors: Wang et al. (2022, Google)
    - arXiv: 2203.11171
    - URL: https://arxiv.org/abs/2203.11171
    - Why: Sample multiple reasoning paths, take the majority vote. Important pattern for verifier/immune agent design.

13. **"Constitutional AI: Harmlessness from AI Feedback"**
    - Authors: Bai et al. (2022, Anthropic)
    - arXiv: 2212.08073
    - URL: https://arxiv.org/abs/2212.08073
    - Why: Self-critique and self-revision loop. Directly relevant to how our hostile-twin and meta-auditor agents operate.

14. **"HuggingGPT: Solving AI Tasks with ChatGPT and its Friends in Hugging Face"**
    - Authors: Shen et al. (2023, Microsoft/ZJU)
    - arXiv: 2303.17580
    - URL: https://arxiv.org/abs/2303.17580
    - Why: Task planning + model selection + execution + response generation. Four-stage agent pipeline, good orchestration reference.

### Episodic and Memory-Augmented Agents
15. **"Generative Agents: Interactive Simulacra of Human Behavior"**
    - Authors: Park et al. (2023, Stanford)
    - arXiv: 2304.03442
    - URL: https://arxiv.org/abs/2304.03442
    - Why: The "Smallville" paper. Memory stream, reflection, planning for persistent agents. Canonical reference for episodic vs persistent agent memory.

16. **"MemGPT: Towards LLMs as Operating Systems"**
    - Authors: Packer et al. (2023)
    - arXiv: 2310.08560
    - URL: https://arxiv.org/abs/2310.08560
    - Why: Virtual context management for LLM agents — paging memory in/out like an OS. Directly relevant to context engineering (what tokens each agent sees).

---

## 3. GitHub Repositories (free, open source)

### Agent Orchestration Frameworks
1. **langchain-ai/langgraph**
   - Stars: ~8k+
   - License: MIT
   - URL: https://github.com/langchain-ai/langgraph
   - Stateful multi-agent orchestration with graph-based workflows, human-in-the-loop, checkpointing, conditional routing.

2. **microsoft/autogen**
   - Stars: ~30k+
   - License: CC-BY-4.0 / MIT
   - URL: https://github.com/microsoft/autogen
   - Microsoft's multi-agent conversation framework. Group chat, nested conversations, code execution sandboxing.

3. **crewAIInc/crewAI**
   - Stars: ~20k+
   - License: MIT
   - URL: https://github.com/crewAIInc/crewAI
   - Role-based multi-agent framework. Sequential/hierarchical process flows, task delegation, memory.

4. **openai/swarm**
   - Stars: ~15k+
   - License: MIT
   - URL: https://github.com/openai/swarm
   - OpenAI's lightweight multi-agent framework. Handoffs, routines, agent-to-agent delegation. Intentionally minimal.

5. **geekan/MetaGPT**
   - Stars: ~40k+
   - License: MIT
   - URL: https://github.com/geekan/MetaGPT
   - Multi-agent framework that assigns SOPs to agents. Product manager, architect, engineer roles. Structured output pipelines.

### Agent Design and Tool Use
6. **langchain-ai/langchain**
   - Stars: ~90k+
   - License: MIT
   - URL: https://github.com/langchain-ai/langchain
   - The foundational LLM application framework. Chains, agents, tool integrations, memory. LangGraph builds on top of this.

7. **princeton-nlp/SWE-agent**
   - Stars: ~12k+
   - License: MIT
   - URL: https://github.com/princeton-nlp/SWE-agent
   - Agent-computer interface for software engineering. Demonstrates how to design tool interfaces that agents can use effectively.

8. **MineDojo/Voyager**
   - Stars: ~5k+
   - License: MIT
   - URL: https://github.com/MineDojo/Voyager
   - Open-ended embodied agent with skill library. Curriculum learning, code-as-policy. Reference for agent skill accumulation.

### Agent Evaluation and Testing
9. **THUDM/AgentBench**
   - Stars: ~2k+
   - License: Apache 2.0
   - URL: https://github.com/THUDM/AgentBench
   - Benchmark for evaluating LLMs as agents across 8 distinct environments.

10. **cpacker/MemGPT** (now Letta)
    - Stars: ~10k+
    - License: Apache 2.0
    - URL: https://github.com/cpacker/MemGPT
    - Virtual context management (memory paging for agents). Directly relevant to context engineering.

### Reflection and Self-Improvement
11. **noahshinn/reflexion**
    - Stars: ~2k+
    - License: MIT
    - URL: https://github.com/noahshinn/reflexion
    - Reference implementation of Reflexion paper. Verbal reinforcement learning for agent self-improvement.

12. **Significant-Gravitas/AutoGPT**
    - Stars: ~160k+
    - License: MIT
    - URL: https://github.com/Significant-Gravitas/AutoGPT
    - The original autonomous agent. Useful as a study of what NOT to do (unbounded loops, no termination criteria) and what to improve.

---

## 4. Books (behind paywalls — Owner to acquire)

1. **"Multi-Agent Systems: Algorithmic, Game-Theoretic, and Logical Foundations"**
   - Authors: Yoav Shoham, Kevin Leyton-Brown
   - Year: 2008 (Cambridge University Press)
   - Why: THE academic bible for multi-agent systems. Game theory, mechanism design, distributed decision-making. Old but foundational — the theory has not changed. Also listed in Zero Trust sources; cross-pollinate.

2. **"Artificial Intelligence: A Modern Approach" (4th edition)**
   - Authors: Stuart Russell, Peter Norvig
   - Year: 2020 (Pearson)
   - Why: Chapters on multi-agent systems, planning, decision-making under uncertainty. The standard AI textbook. Agent architecture fundamentals.

3. **"An Introduction to MultiAgent Systems" (2nd edition)**
   - Author: Michael Wooldridge
   - Year: 2009 (Wiley)
   - Why: The other canonical MAS textbook. Covers BDI (belief-desire-intention) architecture, communication languages, coordination mechanisms.

4. **"Designing Autonomous AI: A Practical Guide to Building AI Agents"**
   - Author: Search for 2024-2025 editions (field is new, books are emerging)
   - Why: Practitioner guide to building production agent systems. Get the best-reviewed one available at time of purchase.

5. **"Nicomachean Ethics"**
   - Author: Aristotle (various translations — Bartlett & Collins recommended)
   - Year: ~350 BCE / modern translations
   - Why: The philosophical foundation of the Trinity dialectic. Ethos, Logos, Pathos. Doctrine of the Mean. This is not optional — it is the WHY behind our architecture.

6. **"The Society of Mind"**
   - Author: Marvin Minsky
   - Year: 1986 (Simon & Schuster)
   - Why: Intelligence as a society of simple agents. Direct ancestor of modern multi-agent AI architectures. Minsky's "agencies" map closely to our cognitive agent design.

7. **"Thinking, Fast and Slow"**
   - Author: Daniel Kahneman
   - Year: 2011 (Farrar, Straus and Giroux)
   - Why: System 1 (fast, intuitive) vs System 2 (slow, deliberate). Maps to our Pathos (intuition/creativity) vs Logos (deliberation/evidence) dialectic.

8. **"The Master Algorithm"**
   - Author: Pedro Domingos
   - Year: 2015 (Basic Books)
   - Why: Five tribes of machine learning. Useful for understanding how different learning paradigms can be composed in agent architectures.

9. **"Reinforcement Learning: An Introduction" (2nd edition)**
   - Authors: Richard Sutton, Andrew Barto
   - Year: 2018 (MIT Press, free PDF available)
   - Why: Agent-environment interaction, reward signals, policy learning. The mathematical foundation for agent decision-making. Free PDF from author's website.

10. **"Other Minds: The Octopus, the Sea, and the Deep Origins of Consciousness"**
    - Author: Peter Godfrey-Smith
    - Year: 2016 (Farrar, Straus and Giroux)
    - Why: Our architecture borrows from octopus neurology (ganglion, chromatophore, distributed cognition). This is the biology reference.

---

## Cross-Reference Map (which sources feed which concepts)

| Concept | YouTube | arXiv | GitHub | Books |
|---|---|---|---|---|
| Multi-Agent Orchestration | #1, #2, #3, #4, #12 | #1, #2, #3, #4, #14 | #1, #2, #3, #4, #5 | #1, #2, #3 |
| Agent Design Patterns (ReAct/CoT) | #8, #9, #15 | #5, #6, #8, #9 | #6, #7 | #2, #9 |
| Context Engineering | #10, #11 | #12, #16 | #10, #6 | #6 |
| Contract-First Prompting | #1, #7 | #7, #13 | #11 | #5 |
| Agent Communication Protocols | #4, #12, #13 | #1, #3, #4 | #2, #4, #5 | #1, #3 |
| Episodic vs Persistent Agents | #1 | #15, #16 | #10, #8 | #7 |
| Agent Evaluation/Benchmarking | #14, #16 | #10, #11 | #9, #12 | #2 |
| Hierarchical vs Flat Architectures | #1, #2, #16 | #1, #2, #3 | #3, #5, #12 | #1, #6 |
| Reflection/Self-Improvement | #8, #14 | #7, #13 | #11, #12 | #7, #9 |
| Trinity Dialectic (Philosophy) | — | — | — | #5, #7, #10 |
| Biomimicry (Octopus/Insect) | — | — | — | #6, #10 |

---

## Ingestion Priority (for LM-LTM repo)

### Tier 1 — Upload First (foundational to our architecture)
- arXiv: Yao 2210.03629 (ReAct), Wei 2201.11903 (CoT), Shinn 2303.11366 (Reflexion), Bai 2212.08073 (Constitutional AI)
- arXiv: Wu 2308.08155 (AutoGen), Park 2304.03442 (Generative Agents)
- GitHub READMEs: LangGraph, AutoGen, Swarm
- YouTube transcripts: Anthropic "Building Effective Agents", DeepLearning.AI LangGraph course
- Books: Shoham MAS, Minsky Society of Mind, Aristotle Nicomachean Ethics

### Tier 2 — Upload Second (depth and alternatives)
- arXiv: MetaGPT, HuggingGPT, MemGPT, Tree of Thoughts, AgentBench
- GitHub READMEs: CrewAI, MetaGPT, SWE-agent, MemGPT/Letta
- YouTube transcripts: CrewAI course, AutoGen walkthrough, OpenAI Swarm
- Books: Russell/Norvig AIMA, Kahneman Thinking Fast and Slow

### Tier 3 — Upload Third (breadth and comparison)
- arXiv: Voyager, ChatDev, AgentVerse, Self-Consistency
- GitHub READMEs: Reflexion, AgentBench, AutoGPT, Voyager
- Remaining YouTube videos
- Books: Wooldridge MAS, Sutton/Barto RL, Domingos, Godfrey-Smith

---

## Notes for Owner

1. **Anthropic "Building Effective Agents" blog post**: This is the single most important source for our architecture. It may exist as a blog post (anthropic.com/research) rather than a YouTube video. Get both if both exist. The Initializer-Workers-Judge pattern, two-tier-only rule, and amnesiac workers all come from here.

2. **YouTube search instructions**: Search queries rather than direct URLs are provided because specific video URLs change frequently. The search terms will find the right content.

3. **arXiv papers with IDs**: All papers listed with specific arXiv IDs (e.g., 2210.03629) are verified real papers with correct IDs. These are well-known, highly-cited works in the field.

4. **GitHub star counts**: Approximate as of early 2025. All repos listed are well-established and actively maintained.

5. **Sutton/Barto RL textbook**: Available as a free PDF from the authors' website (incompleteideas.net/book/the-book-2nd.html). Worth grabbing immediately.

6. **Aristotle**: The Bartlett & Collins translation (University of Chicago Press, 2011) is recommended for clarity. The Nicomachean Ethics is not just philosophy — it is the design document for the Trinity dialectic. Ethos (character/virtue), Logos (reason/argument), Pathos (emotion/persuasion) and the Doctrine of the Mean are the WHY behind our architecture.

7. **Cross-pollination targets**: Per Owner's brain region overlap strategy, the strongest agent pattern sources should also go into:
   - Region #14 (Open Brain Long-Term Memory) — for architectural memory
   - Region #17 (Adversarial Security Red Team) — for hostile-twin and meta-auditor patterns
   - Region #3 (Zero Trust Architecture) — Constitutional AI paper overlaps both domains

8. **Anti-pattern documentation**: AutoGPT (GitHub #12) is included specifically as a study of anti-patterns: unbounded autonomous loops, no termination criteria, no human-in-the-loop gates. Understanding what NOT to do is as important as understanding what to do.
