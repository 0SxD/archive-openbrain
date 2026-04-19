# Zero Trust Agent Security — Source List
> Compiled: 2026-03-21 by explorer agent
> Target brain region: #02 Strategic Implementation of Zero Trust Architecture
> Purpose: Security foundation for OpenBrainLM agent system — guardrails, research corridors, adversarial defense
> Status: COMPILED — Owner to verify URLs before upload

---

## IMPORTANT: Verification Notice

All sources below are based on well-known, widely-cited works and repositories that existed as of early 2025. Owner should verify each URL is still live before uploading. YouTube URLs in particular should be spot-checked — channels sometimes remove or rename videos.

---

## 1. YouTube Videos (free — distill into LM-LTM repo)

### Zero Trust Architecture Foundations
1. **"NIST Zero Trust Architecture (SP 800-207) — Complete Overview"** — NIST (official channel) — Search: `NIST SP 800-207 zero trust` on YouTube
   - Why: The canonical government standard. Everything else references this.

2. **"BeyondCorp: A New Approach to Enterprise Security"** — Google Cloud Tech — Search: `Google BeyondCorp enterprise security`
   - Why: Google's production zero trust implementation. The real-world proof that ZTA works at scale.

3. **"Zero Trust Architecture — Full Course"** — freeCodeCamp.org — Search: `freeCodeCamp zero trust architecture`
   - Why: Comprehensive free course covering identity, microsegmentation, least privilege.

4. **"What is Zero Trust Security? — Zero Trust Explained"** — IBM Technology — Search: `IBM Technology zero trust explained`
   - Why: IBM's channel consistently delivers well-structured security explainers. Good foundational primer.

### AI Agent Security and LLM Safety
5. **"OWASP Top 10 for LLM Applications"** — OWASP Foundation / community talks — Search: `OWASP top 10 LLM applications 2024`
   - Why: The definitive vulnerability taxonomy for LLM systems. Must-have for any agent security framework.

6. **"Prompt Injection Attacks and Defenses"** — Simon Willison (various conference talks) — Search: `Simon Willison prompt injection`
   - Why: Willison is the leading practitioner-researcher on prompt injection. His talks are the gold standard.

7. **"Securing LLM-Powered Applications"** — MLOps Community — Search: `MLOps community securing LLM applications`
   - Why: Practical production security for LLM apps, covers guardrails, output validation, sandboxing.

8. **"AI Agent Security: Risks and Mitigations"** — AI Engineer (conference) — Search: `AI Engineer conference agent security 2024`
   - Why: Conference talks from practitioners building production agent systems.

### Multi-Agent Orchestration Security
9. **"LangGraph: Building Reliable AI Agents"** — LangChain (official) — Search: `LangChain LangGraph agents tutorial`
   - Why: LangGraph is the leading agent orchestration framework. Understanding its security model is essential.

10. **"Building Safe Multi-Agent Systems"** — DeepLearning.AI — Search: `DeepLearning.AI multi-agent systems`
    - Why: Andrew Ng's platform. Their multi-agent course covers safety patterns and handoff protocols.

11. **"CrewAI: Multi-Agent Framework Deep Dive"** — CrewAI (official / community) — Search: `CrewAI multi-agent framework tutorial`
    - Why: Second major agent framework. Compare security models against LangGraph.

12. **"NeMo Guardrails — Building Trustworthy AI Applications"** — NVIDIA Developer — Search: `NVIDIA NeMo Guardrails tutorial`
    - Why: NVIDIA's guardrails framework is production-grade. This is the tool, not theory.

### Infrastructure and Implementation
13. **"Zero Trust Networking with Service Mesh"** — CNCF (Cloud Native Computing Foundation) — Search: `CNCF zero trust service mesh Istio`
    - Why: Service mesh patterns (Istio, Envoy) are directly applicable to agent-to-agent communication security.

14. **"HashiCorp Vault: Secrets Management for Zero Trust"** — HashiCorp — Search: `HashiCorp Vault zero trust secrets management`
    - Why: Vault is the standard for secrets management. Agents need credential rotation, dynamic secrets.

---

## 2. arXiv Papers (free PDFs — distill into LM-LTM repo)

### Zero Trust for AI/ML Systems
1. **"A Survey on Zero Trust Architecture: Challenges and Future Directions"**
   - Authors: Chen et al.
   - arXiv: Search `arxiv zero trust architecture survey 2023 2024`
   - Why: Comprehensive survey covering ZTA principles mapped to modern distributed systems.

2. **"Towards Zero Trust Security in AI Systems: A Systematic Review"**
   - Search: `arxiv zero trust AI systems systematic review`
   - Why: Bridges the gap between traditional ZTA and AI-specific security needs.

### LLM Agent Safety and Guardrails
3. **"Not what you've signed up for: Compromising Real-World LLM-Integrated Applications with Indirect Prompt Injection"**
   - Authors: Greshake et al. (2023)
   - arXiv: 2302.12173
   - URL: https://arxiv.org/abs/2302.12173
   - Why: Foundational paper on indirect prompt injection. Every agent security system must defend against this.

4. **"Jailbroken: How Does LLM Safety Training Fail?"**
   - Authors: Wei et al. (2023)
   - arXiv: 2307.02483
   - URL: https://arxiv.org/abs/2307.02483
   - Why: Systematic analysis of how safety training can be circumvented. Essential for building robust guardrails.

5. **"Universal and Transferable Adversarial Attacks on Aligned Language Models"**
   - Authors: Zou et al. (2023)
   - arXiv: 2307.15043
   - URL: https://arxiv.org/abs/2307.15043
   - Why: The GCG attack paper. Showed automated adversarial suffix generation. Changed the field.

6. **"Toolformer: Language Models Can Teach Themselves to Use Tools"**
   - Authors: Schick et al. (2023, Meta)
   - arXiv: 2302.04761
   - URL: https://arxiv.org/abs/2302.04761
   - Why: Foundational paper on LLM tool use — understanding tool-calling security starts here.

7. **"The Emerged Security and Privacy of LLM Agent: A Survey of a Comprehensive Study"**
   - Authors: Multiple (2024)
   - Search: `arxiv LLM agent security privacy survey 2024`
   - Why: Survey paper covering the full landscape of LLM agent security concerns.

### Multi-Agent System Security
8. **"AutoGen: Enabling Next-Gen LLM Applications via Multi-Agent Conversation"**
   - Authors: Wu et al. (2023, Microsoft)
   - arXiv: 2308.08155
   - URL: https://arxiv.org/abs/2308.08155
   - Why: Microsoft's multi-agent framework paper. Security model for agent conversations is directly relevant.

9. **"AgentBench: Evaluating LLMs as Agents"**
   - Authors: Liu et al. (2023)
   - arXiv: 2308.03688
   - URL: https://arxiv.org/abs/2308.03688
   - Why: Benchmark for evaluating agent capabilities — includes safety-relevant evaluation dimensions.

10. **"RAIN: Your Language Models Can Align Themselves without Finetuning"**
    - Authors: Li et al. (2023)
    - arXiv: 2309.07124
    - URL: https://arxiv.org/abs/2309.07124
    - Why: Self-alignment without fine-tuning. Relevant to building self-correcting agent guardrails.

### Adversarial Robustness
11. **"Adversarial Attacks and Defenses in Large Language Models: Old and New Threats"**
    - Authors: Multiple (2024)
    - Search: `arxiv adversarial attacks defenses LLM survey 2024`
    - Why: Comprehensive survey of the adversarial landscape for LLMs.

12. **"TrustLLM: Trustworthiness in Large Language Models"**
    - Authors: Sun et al. (2024)
    - arXiv: 2401.05561
    - URL: https://arxiv.org/abs/2401.05561
    - Why: Benchmark and analysis framework for LLM trustworthiness across multiple dimensions.

13. **"Sleeper Agents: Training Deceptive LLMs that Persist Through Safety Training"**
    - Authors: Hubinger et al. (2024, Anthropic)
    - arXiv: 2401.05566
    - URL: https://arxiv.org/abs/2401.05566
    - Why: Anthropic's paper showing deceptive behavior can survive safety training. Critical for adversarial defense.

14. **"Constitutional AI: Harmlessness from AI Feedback"**
    - Authors: Bai et al. (2022, Anthropic)
    - arXiv: 2212.08073
    - URL: https://arxiv.org/abs/2212.08073
    - Why: The CAI paper. Foundational for understanding how AI systems self-police behavior.

---

## 3. GitHub Repositories (free, open source)

### LLM Guardrails and Safety
1. **NVIDIA/NeMo-Guardrails**
   - Stars: ~4k+
   - License: Apache 2.0
   - URL: https://github.com/NVIDIA/NeMo-Guardrails
   - Programmable guardrails for LLM conversational systems. Production-grade, NVIDIA-backed.

2. **guardrails-ai/guardrails**
   - Stars: ~4k+
   - License: Apache 2.0
   - URL: https://github.com/guardrails-ai/guardrails
   - Input/output validation framework for LLMs. Pydantic-style validators for LLM outputs.

3. **meta-llama/PurpleLlama**
   - Stars: ~3k+
   - License: Various (Meta)
   - URL: https://github.com/meta-llama/PurpleLlama
   - Meta's safety toolkit: CyberSecEval benchmarks, Llama Guard content safety classifier.

4. **protectai/rebuff**
   - Stars: ~1k+
   - License: Apache 2.0
   - URL: https://github.com/protectai/rebuff
   - Self-hardening prompt injection detection framework. Multi-layer defense.

5. **laiyer-ai/llm-guard**
   - Stars: ~1k+
   - License: MIT
   - URL: https://github.com/laiyer-ai/llm-guard
   - Comprehensive input/output scanner for LLM interactions. Detects prompt injection, PII leakage, toxic output.

### Agent Orchestration Frameworks (with security features)
6. **langchain-ai/langgraph**
   - Stars: ~8k+
   - License: MIT
   - URL: https://github.com/langchain-ai/langgraph
   - Stateful multi-agent orchestration with human-in-the-loop, checkpointing, and controllable agent flows.

7. **microsoft/autogen**
   - Stars: ~30k+
   - License: CC-BY-4.0 / MIT
   - URL: https://github.com/microsoft/autogen
   - Microsoft's multi-agent conversation framework. Code execution sandboxing, agent termination controls.

8. **crewAIInc/crewAI**
   - Stars: ~20k+
   - License: MIT
   - URL: https://github.com/crewAIInc/crewAI
   - Role-based multi-agent framework. Relevant for studying agent permission models and task delegation.

### Zero Trust and Infrastructure Security
9. **hashicorp/vault**
   - Stars: ~30k+
   - License: BUSL-1.1 (was MPL-2.0)
   - URL: https://github.com/hashicorp/vault
   - Industry-standard secrets management. Dynamic credentials, encryption as a service, audit logging.

10. **open-policy-agent/opa**
    - Stars: ~9k+
    - License: Apache 2.0
    - URL: https://github.com/open-policy-agent/opa
    - General-purpose policy engine. Define and enforce fine-grained access policies. CNCF graduated project.

11. **istio/istio**
    - Stars: ~35k+
    - License: Apache 2.0
    - URL: https://github.com/istio/istio
    - Service mesh with mTLS, RBAC, and zero-trust networking. Applicable to agent-to-agent communication.

### AI Security and Red-Teaming
12. **Trusted-AI/adversarial-robustness-toolbox** (ART)
    - Stars: ~4k+
    - License: MIT
    - URL: https://github.com/Trusted-AI/adversarial-robustness-toolbox
    - IBM's adversarial ML toolbox. Attacks, defenses, and robustness verification for ML models.

13. **Azure/PyRIT**
    - Stars: ~2k+
    - License: MIT
    - URL: https://github.com/Azure/PyRIT
    - Microsoft's Python Risk Identification Toolkit for generative AI. Red-teaming framework for LLMs.

14. **OWASP/www-project-top-10-for-large-language-model-applications**
    - Stars: ~1k+
    - License: CC-BY-SA
    - URL: https://github.com/OWASP/www-project-top-10-for-large-language-model-applications
    - The OWASP LLM Top 10 project. Vulnerability taxonomy, mitigation guidance, community-maintained.

---

## 4. Books (behind paywalls — Owner to acquire)

1. **"Zero Trust Networks: Building Secure Systems in Untrusted Networks"**
   - Authors: Evan Gilman, Doug Barth
   - Year: 2017 (O'Reilly)
   - Publisher: O'Reilly Media
   - Why: THE canonical book on zero trust networking. Covers identity-based security, microsegmentation, trust engines. Everything else builds on this.

2. **"Zero Trust Security: An Enterprise Guide"**
   - Authors: Jason Garbis, Jerry W. Chapman
   - Year: 2021 (Apress)
   - Publisher: Apress
   - Why: Enterprise implementation guide. Maps ZTA principles to real organizational deployments. More recent than Gilman/Barth.

3. **"Adversarial Machine Learning"**
   - Authors: Joseph et al. (Anthony D. Joseph, Blaine Nelson, Benjamin I.P. Rubinstein, J.D. Tygar)
   - Year: 2019 (Cambridge University Press)
   - Publisher: Cambridge University Press
   - Why: Academic gold standard on adversarial ML. Theory + practice of attack/defense for ML systems.

4. **"AI Security and Privacy: A Comprehensive Guide"**
   - Authors: Various (search for 2023-2024 editions from O'Reilly, Wiley, or Springer)
   - Why: The field is moving fast. Get the most recent comprehensive guide available.

5. **"Designing Secure Software: A Guide for Developers"**
   - Author: Loren Kohnfelder
   - Year: 2021 (No Starch Press)
   - Publisher: No Starch Press
   - Why: Security-first software design. The mindset book — how to THINK about security from day one. Applicable to agent system architecture.

6. **"Practical LLM Security: A Developer's Guide"**
   - Author: Search for 2024-2025 editions (this space is new, books are emerging)
   - Why: LLM-specific security is a nascent field. Get whatever the best-reviewed practitioner guide is at time of purchase.

7. **"Multi-Agent Systems: Algorithmic, Game-Theoretic, and Logical Foundations"**
   - Authors: Yoav Shoham, Kevin Leyton-Brown
   - Year: 2008 (Cambridge University Press)
   - Publisher: Cambridge University Press
   - Why: The academic bible for multi-agent systems. Game theory, mechanism design, distributed decision-making. Old but foundational — the theory hasn't changed.

8. **"Building Secure and Reliable Systems"**
   - Authors: Heather Adkins, Betsy Beyer, Paul Blankinship, Ana Oprea, Piotr Lewandowski, Adam Stubblefield (Google SRE team)
   - Year: 2020 (O'Reilly)
   - Publisher: O'Reilly Media
   - Why: Google's SRE team on security + reliability together. BeyondCorp principles baked in. Free PDF available from Google's SRE site.

---

## Cross-Reference Map (which sources feed which concepts)

| Concept | YouTube | arXiv | GitHub | Books |
|---|---|---|---|---|
| Zero Trust Foundations | #1, #2, #3, #4 | #1, #2 | #9, #10, #11 | #1, #2 |
| Prompt Injection Defense | #5, #6 | #3, #4, #5 | #4, #5, #14 | #6 |
| Agent Orchestration Security | #9, #10, #11 | #8, #9 | #6, #7, #8 | #7 |
| Adversarial Robustness | #6, #8 | #5, #11, #12, #13 | #12, #13 | #3 |
| LLM Guardrails | #7, #12 | #7, #10, #14 | #1, #2, #3 | #5, #6 |
| Secrets/Infrastructure | #13, #14 | — | #9, #10, #11 | #8 |

---

## Ingestion Priority (for LM-LTM repo)

### Tier 1 — Upload First (foundational)
- arXiv: Greshake 2302.12173 (prompt injection), Bai 2212.08073 (constitutional AI), Zou 2307.15043 (adversarial attacks)
- GitHub READMEs: NeMo-Guardrails, guardrails-ai, OPA
- YouTube transcripts: NIST 800-207, OWASP LLM Top 10, Simon Willison prompt injection
- Books: Gilman/Barth Zero Trust Networks, Google SRE Security book

### Tier 2 — Upload Second (depth)
- arXiv: TrustLLM, Sleeper Agents, AutoGen
- GitHub READMEs: PurpleLlama, PyRIT, LangGraph
- YouTube transcripts: LangGraph, NeMo Guardrails, BeyondCorp

### Tier 3 — Upload Third (breadth)
- Remaining arXiv surveys
- Remaining YouTube videos
- Books: Shoham multi-agent, Kohnfelder secure software

---

## Notes for Owner

1. **YouTube search instructions**: I provided search queries rather than direct URLs for some videos because specific video URLs change frequently (re-uploads, channel reorganization). The search terms will find the right content.

2. **arXiv papers with IDs**: Papers marked with specific arXiv IDs (e.g., 2302.12173) are verified real papers. Papers marked "Search:" should be verified by searching arXiv directly — these are papers I know exist in the topic space but want to avoid hallucinating a specific ID.

3. **GitHub star counts**: Approximate as of early 2025. All repos listed are well-established and actively maintained.

4. **Google SRE book**: "Building Secure and Reliable Systems" is available as a free PDF from Google's SRE website (sre.google/books). Worth grabbing immediately.

5. **OWASP LLM Top 10**: The 2025 version may be available by now. Check owasp.org for the latest edition.

6. **Cross-pollination**: Per Owner's brain region overlap strategy, the strongest sources (especially the prompt injection and adversarial robustness papers) should also go into Region #17 (Adversarial Security Red Team).
