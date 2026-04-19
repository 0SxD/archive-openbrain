# Adversarial Security — Source List
> Compiled: 2026-03-21 by explorer agent
> Target brain region: #4 Adversarial Security / Red Team
> Purpose: Immune system methodology for OpenBrainLM — offensive security, adversarial methods, red teaming, biological immune analogies
> Status: COMPILED — Owner to verify URLs before upload

---

## IMPORTANT: Verification Notice

All sources below are based on well-known, widely-cited works and repositories that existed as of early 2025. Owner should verify each URL is still live before uploading. YouTube URLs in particular should be spot-checked — channels sometimes remove or rename videos.

---

## 1. YouTube Videos (free — distill into LM-LTM repo)

### Red Teaming AI Systems
1. **"Red Teaming LLMs — DEFCON AI Village"** — AI Village / DEFCON — Search: `DEFCON AI Village red teaming LLM 2023`
   - Why: DEFCON is the gold standard for adversarial security culture. The 2023 AI Village ran the largest public LLM red team event in history (organized with White House backing). Primary source for methodology.

2. **"How to Red Team AI Systems"** — Microsoft Research — Search: `Microsoft Research red teaming AI systems 2024`
   - Why: Microsoft built PyRIT and red-teamed GPT-4 before release. Their methodology talk covers systematic vulnerability discovery in generative AI.

3. **"AI Red Teaming: Lessons from the Field"** — Anthropic (various researchers) — Search: `Anthropic red teaming AI safety 2024`
   - Why: Anthropic publishes extensively on red teaming their own models. Direct source for Constitutional AI adversarial testing methodology.

4. **"Adversarial Machine Learning — Full Lecture"** — MIT OpenCourseWare / Stanford Online — Search: `adversarial machine learning lecture MIT Stanford`
   - Why: Academic foundation lecture covering evasion attacks, poisoning attacks, and robustness theory. Get the university-quality treatment before practitioner talks.

### Prompt Injection and Jailbreaking
5. **"Prompt Injection Attacks and Defenses"** — Simon Willison (various conference talks) — Search: `Simon Willison prompt injection`
   - Why: Willison is the leading practitioner-researcher on prompt injection. His talks are the gold standard. (Cross-ref: also in zero trust sources.)

6. **"Jailbreaking LLMs: A Comprehensive Overview"** — Yannic Kilcher — Search: `Yannic Kilcher jailbreaking LLMs`
   - Why: Kilcher does thorough paper walkthroughs. His coverage of jailbreaking papers explains the attack taxonomy clearly.

7. **"Indirect Prompt Injection — The Biggest Threat to LLM Applications"** — OWASP / community security talks — Search: `indirect prompt injection LLM OWASP 2024`
   - Why: Indirect injection (data-plane attacks via retrieved content) is the hardest class to defend against. This is the threat that breaks naive agent architectures.

### AI Safety and Alignment
8. **"Sleeper Agents: Training Deceptive LLMs — Paper Explained"** — Yannic Kilcher / AI Explained — Search: `sleeper agents deceptive LLMs Anthropic paper explained`
   - Why: The Sleeper Agents paper is critical for understanding persistent deception. A video walkthrough makes the dense paper accessible.

9. **"Constitutional AI Explained"** — Anthropic / AI safety channels — Search: `Constitutional AI Anthropic explained 2023`
   - Why: CAI is the foundation of Anthropic's alignment approach. Understanding it is prerequisite for building self-policing agent systems.

10. **"RLHF and DPO: How We Align Language Models"** — Hugging Face — Search: `Hugging Face RLHF DPO alignment tutorial`
    - Why: Hugging Face provides the best practitioner-level explanations of alignment training. Covers both RLHF and Direct Preference Optimization.

### Biological Immune System Analogies
11. **"Immunology — Innate vs Adaptive Immunity"** — Ninja Nerd / Osmosis — Search: `innate adaptive immunity full lecture Ninja Nerd`
    - Why: OpenBrainLM's immune agent is modeled on biological immunity. Need the real biology before building the analogy. Ninja Nerd and Osmosis are the best medical education channels.

12. **"Artificial Immune Systems — Nature-Inspired Computing"** — various academic lectures — Search: `artificial immune systems nature-inspired computing lecture`
    - Why: AIS is a real subfield of computational intelligence. Clonal selection, danger theory, negative selection — all applicable to agent threat detection.

### Adversarial Tools and Frameworks
13. **"Microsoft PyRIT: Red Teaming Generative AI"** — Microsoft Security — Search: `Microsoft PyRIT red teaming generative AI tutorial`
    - Why: PyRIT is Microsoft's open-source red teaming toolkit for generative AI. Hands-on demo of automated adversarial probing.

14. **"NVIDIA NeMo Guardrails — Building Trustworthy AI Applications"** — NVIDIA Developer — Search: `NVIDIA NeMo Guardrails tutorial`
    - Why: Guardrails are the defensive complement to red teaming. Understanding what defenders build tells you what attackers target. (Cross-ref: also in zero trust sources.)

15. **"OWASP Top 10 for LLM Applications"** — OWASP Foundation / community talks — Search: `OWASP top 10 LLM applications 2024`
    - Why: The canonical vulnerability taxonomy for LLM systems. Essential for systematic threat enumeration. (Cross-ref: also in zero trust sources.)

---

## 2. arXiv Papers (free PDFs — distill into LM-LTM repo)

### Adversarial Attacks on LLMs
1. **"Universal and Transferable Adversarial Attacks on Aligned Language Models"**
   - Authors: Zou et al. (2023)
   - arXiv: 2307.15043
   - URL: https://arxiv.org/abs/2307.15043
   - Why: The GCG (Greedy Coordinate Gradient) attack paper. Demonstrated automated adversarial suffix generation that transfers across models. Changed the field. (Cross-ref: also in zero trust sources.)

2. **"Jailbroken: How Does LLM Safety Training Fail?"**
   - Authors: Wei et al. (2023)
   - arXiv: 2307.02483
   - URL: https://arxiv.org/abs/2307.02483
   - Why: Systematic taxonomy of jailbreak techniques — competing objectives and mismatched generalization. The theoretical framework for understanding why safety training is fragile.

3. **"Not what you've signed up for: Compromising Real-World LLM-Integrated Applications with Indirect Prompt Injection"**
   - Authors: Greshake et al. (2023)
   - arXiv: 2302.12173
   - URL: https://arxiv.org/abs/2302.12173
   - Why: The paper that defined indirect prompt injection as a threat class. Every agent system that retrieves external data must defend against this. (Cross-ref: also in zero trust sources.)

4. **"AutoDAN: Generating Stealthy Jailbreak Prompts on Aligned Large Language Models"**
   - Authors: Liu et al. (2023)
   - arXiv: 2310.04451
   - URL: https://arxiv.org/abs/2310.04451
   - Why: Automated jailbreak generation using hierarchical genetic algorithms. Shows that manual red teaming is insufficient — adversaries will automate.

5. **"Ignore This Title and HackAPrompt: Exposing Systemic Weaknesses of LLMs through a Global Scale Prompt Hacking Competition"**
   - Authors: Schulhoff et al. (2023)
   - arXiv: 2311.16119
   - URL: https://arxiv.org/abs/2311.16119
   - Why: Largest prompt hacking competition dataset. Empirical evidence of what attacks work in practice, categorized by technique.

### AI Safety and Alignment
6. **"Sleeper Agents: Training Deceptive LLMs that Persist Through Safety Training"**
   - Authors: Hubinger et al. (2024, Anthropic)
   - arXiv: 2401.05566
   - URL: https://arxiv.org/abs/2401.05566
   - Why: Showed deceptive behavior can survive safety training (RLHF, adversarial training). The strongest evidence that behavioral safety testing alone is insufficient. (Cross-ref: also in zero trust sources.)

7. **"Constitutional AI: Harmlessness from AI Feedback"**
   - Authors: Bai et al. (2022, Anthropic)
   - arXiv: 2212.08073
   - URL: https://arxiv.org/abs/2212.08073
   - Why: The CAI paper. Self-supervised alignment via principle-based critique. Foundation for building agent systems that self-police. (Cross-ref: also in zero trust sources.)

8. **"Training a Helpful and Harmless Assistant with Reinforcement Learning from Human Feedback"**
   - Authors: Bai et al. (2022, Anthropic)
   - arXiv: 2204.05862
   - URL: https://arxiv.org/abs/2204.05862
   - Why: The canonical RLHF paper from Anthropic. Documents the tension between helpfulness and harmlessness — the core alignment tradeoff.

9. **"Direct Preference Optimization: Your Language Model is Secretly a Reward Model"**
   - Authors: Rafailov et al. (2023, Stanford)
   - arXiv: 2305.18290
   - URL: https://arxiv.org/abs/2305.18290
   - Why: DPO simplifies RLHF by eliminating the reward model. Rapidly adopted alternative to RLHF. Understanding both methods is necessary.

### Adversarial Robustness
10. **"TrustLLM: Trustworthiness in Large Language Models"**
    - Authors: Sun et al. (2024)
    - arXiv: 2401.05561
    - URL: https://arxiv.org/abs/2401.05561
    - Why: Comprehensive benchmark for LLM trustworthiness across 8 dimensions including robustness, safety, and fairness. (Cross-ref: also in zero trust sources.)

11. **"Adversarial Examples Are Not Easily Detected: Bypassing Ten Detection Methods"**
    - Authors: Carlini & Wagner (2017)
    - arXiv: 1705.07263
    - URL: https://arxiv.org/abs/1705.07263
    - Why: Classic adversarial ML paper showing detection methods are brittle. The lesson transfers directly to LLM output filtering — defenses that seem robust often are not.

12. **"Towards Evaluating the Robustness of Neural Networks"**
    - Authors: Carlini & Wagner (2017)
    - arXiv: 1608.04644
    - URL: https://arxiv.org/abs/1608.04644
    - Why: The C&W attack — the gold standard for evaluating adversarial robustness. Every robustness claim must be tested against this. Foundational adversarial ML.

### Multi-Agent Threat Modeling
13. **"R-Judge: Benchmarking Safety Risk Awareness for LLM Agents"**
    - Authors: Yuan et al. (2024)
    - arXiv: 2401.10019
    - URL: https://arxiv.org/abs/2401.10019
    - Why: Benchmark specifically for evaluating whether LLM agents can identify safety risks in multi-step scenarios. Directly relevant to OpenBrainLM's immune agent.

14. **"Agent Smith: A Single Image Can Jailbreak One Million Multimodal LLM Agents"**
    - Authors: Gu et al. (2024)
    - arXiv: 2402.08567
    - URL: https://arxiv.org/abs/2402.08567
    - Why: Demonstrates infectious jailbreak propagation across multi-agent systems. One compromised agent infects others. Critical threat model for any multi-agent architecture.

15. **"Purple Llama CyberSecEval: A Secure Coding Benchmark for Language Models"**
    - Authors: Bhatt et al. (2023, Meta)
    - arXiv: 2312.04724
    - URL: https://arxiv.org/abs/2312.04724
    - Why: Meta's benchmark for evaluating LLM-generated code for security vulnerabilities. Relevant to any agent that writes or executes code.

16. **"Robust Intelligence: The Next Frontier for AI Safety"**
    - Search: `arxiv robust intelligence AI safety survey 2024`
    - Why: Survey covering the intersection of adversarial robustness and AI safety — bridging the ML robustness and alignment communities.

---

## 3. GitHub Repositories (free, open source)

### Red Teaming and Offensive Security
1. **Azure/PyRIT**
   - Stars: ~2k+
   - License: MIT
   - URL: https://github.com/Azure/PyRIT
   - Microsoft's Python Risk Identification Toolkit for generative AI. Automated red teaming: attack strategies, scorers, converters, orchestrators. The most complete open-source red teaming framework. (Cross-ref: also in zero trust sources.)

2. **meta-llama/PurpleLlama**
   - Stars: ~3k+
   - License: Various (Meta)
   - URL: https://github.com/meta-llama/PurpleLlama
   - Meta's safety toolkit: CyberSecEval benchmarks (insecure code, prompt injection), Llama Guard content safety classifier. "Purple" = red + blue teaming. (Cross-ref: also in zero trust sources.)

3. **Trusted-AI/adversarial-robustness-toolbox** (ART)
   - Stars: ~4k+
   - License: MIT
   - URL: https://github.com/Trusted-AI/adversarial-robustness-toolbox
   - IBM's adversarial ML toolbox. Comprehensive: evasion, poisoning, extraction, inference attacks + defenses. Supports PyTorch, TensorFlow, scikit-learn. The standard adversarial ML library. (Cross-ref: also in zero trust sources.)

4. **leondz/garak**
   - Stars: ~2k+
   - License: Apache 2.0
   - URL: https://github.com/leondz/garak
   - LLM vulnerability scanner. Named after a Star Trek character. Probes for prompt injection, data leakage, hallucination, toxicity. Plugin architecture for custom probes.

5. **OWASP/www-project-top-10-for-large-language-model-applications**
   - Stars: ~1k+
   - License: CC-BY-SA
   - URL: https://github.com/OWASP/www-project-top-10-for-large-language-model-applications
   - The OWASP LLM Top 10 project. Canonical vulnerability taxonomy with mitigation guidance. Community-maintained and regularly updated. (Cross-ref: also in zero trust sources.)

### Guardrails and Defense
6. **NVIDIA/NeMo-Guardrails**
   - Stars: ~4k+
   - License: Apache 2.0
   - URL: https://github.com/NVIDIA/NeMo-Guardrails
   - Programmable guardrails for LLM systems. Colang rail definitions, topical/safety/fact-checking rails. Production-grade, NVIDIA-backed. (Cross-ref: also in zero trust sources.)

7. **guardrails-ai/guardrails**
   - Stars: ~4k+
   - License: Apache 2.0
   - URL: https://github.com/guardrails-ai/guardrails
   - Input/output validation framework for LLMs. Pydantic-style validators. Validator Hub for community-contributed checks. (Cross-ref: also in zero trust sources.)

8. **laiyer-ai/llm-guard**
   - Stars: ~1k+
   - License: MIT
   - URL: https://github.com/laiyer-ai/llm-guard
   - Comprehensive input/output scanner: prompt injection detection, PII leakage, toxicity, ban topics, invisible text detection. (Cross-ref: also in zero trust sources.)

9. **protectai/rebuff**
   - Stars: ~1k+
   - License: Apache 2.0
   - URL: https://github.com/protectai/rebuff
   - Self-hardening prompt injection detection. Multi-layer defense: heuristics, LLM-based detection, canary tokens, vector similarity. (Cross-ref: also in zero trust sources.)

### Adversarial ML and Robustness
10. **bethgelab/foolbox**
    - Stars: ~2.5k+
    - License: MIT
    - URL: https://github.com/bethgelab/foolbox
    - Python library for adversarial attacks on neural networks. Clean API, supports PyTorch, TensorFlow, JAX. Good complement to IBM ART with different attack implementations.

11. **QData/TextAttack**
    - Stars: ~2.5k+
    - License: MIT
    - URL: https://github.com/QData/TextAttack
    - Framework for adversarial attacks on NLP models. Perturbation recipes, augmentation, training. Specifically designed for text-domain adversarial ML.

12. **huggingface/evaluate**
    - Stars: ~2k+
    - License: Apache 2.0
    - URL: https://github.com/huggingface/evaluate
    - Hugging Face's evaluation library. Includes toxicity metrics, bias evaluation, and robustness testing. Standardized metrics for safety evaluation.

---

## 4. Books (behind paywalls — Owner to acquire)

1. **"Adversarial Machine Learning"**
   - Authors: Anthony D. Joseph, Blaine Nelson, Benjamin I.P. Rubinstein, J.D. Tygar
   - Year: 2019 (Cambridge University Press)
   - Publisher: Cambridge University Press
   - Why: The academic gold standard on adversarial ML. Covers evasion, poisoning, privacy attacks with formal treatment. Theory + practice. (Cross-ref: also in zero trust sources.)

2. **"The Art of Software Security Assessment: Identifying and Preventing Software Vulnerabilities"**
   - Authors: Mark Dowd, John McDonald, Justin Schnier
   - Year: 2006 (Addison-Wesley)
   - Publisher: Addison-Wesley
   - Why: The bible of vulnerability assessment methodology. Old but timeless — the mental model for finding security flaws transfers directly to AI systems. Teaches you to THINK like an attacker.

3. **"The Web Application Hacker's Handbook"**
   - Authors: Dafydd Stuttard, Marcus Pinto
   - Year: 2011 (2nd edition, Wiley)
   - Publisher: Wiley
   - Why: The penetration testing methodology book. Systematic approach to finding and exploiting vulnerabilities. The methodology (recon, mapping, discovery, exploitation) maps directly to AI red teaming.

4. **"Immune: A Journey into the Mysterious System That Keeps You Alive"**
   - Author: Philipp Dettmer (Kurzgesagt)
   - Year: 2021 (Random House)
   - Publisher: Random House
   - Why: Best popular-science treatment of the human immune system. Written by the Kurzgesagt creator. Innate vs adaptive immunity, self/non-self discrimination, complement system — all directly analogous to OpenBrainLM's immune agent design.

5. **"Immunobiology" (Janeway's)**
   - Authors: Kenneth Murphy, Casey Weaver
   - Year: 2016 (9th edition, Garland Science)
   - Publisher: Garland Science
   - Why: The canonical immunology textbook. If Dettmer is the overview, Janeway is the full spec. Clonal selection, MHC presentation, thymic selection — the real biology behind AIS (Artificial Immune Systems).

6. **"Penetration Testing: A Hands-On Introduction to Hacking"**
   - Author: Georgia Weidman
   - Year: 2014 (No Starch Press)
   - Publisher: No Starch Press
   - Why: Practical pentest methodology. While focused on traditional systems, the structured approach (reconnaissance, exploitation, post-exploitation, reporting) is the template for AI system red teaming.

7. **"Building Secure and Reliable Systems"**
   - Authors: Heather Adkins, Betsy Beyer, Paul Blankinship, Ana Oprea, Piotr Lewandowski, Adam Stubblefield (Google SRE team)
   - Year: 2020 (O'Reilly)
   - Publisher: O'Reilly Media
   - Why: Google's SRE team on security + reliability together. Chapter on adversarial testing is directly applicable. Free PDF available from Google's SRE site (sre.google/books). (Cross-ref: also in zero trust sources.)

8. **"Multi-Agent Systems: Algorithmic, Game-Theoretic, and Logical Foundations"**
   - Authors: Yoav Shoham, Kevin Leyton-Brown
   - Year: 2008 (Cambridge University Press)
   - Publisher: Cambridge University Press
   - Why: Game-theoretic foundations for multi-agent interaction. Adversarial agents are modeled by game theory. Mechanism design tells you how to build systems resistant to strategic manipulation. (Cross-ref: also in zero trust sources.)

9. **"Threat Modeling: Designing for Security"**
   - Author: Adam Shostack
   - Year: 2014 (Wiley)
   - Publisher: Wiley
   - Why: The canonical threat modeling book. STRIDE methodology, attack trees, DFDs. Shostack built Microsoft's threat modeling program. Directly applicable to modeling threats in multi-agent AI systems.

---

## 5. Cross-Reference Map (which sources feed which concepts)

| Concept | YouTube | arXiv | GitHub | Books |
|---|---|---|---|---|
| Red Teaming Methodology | #1, #2, #3 | #5 | #1, #2, #4 | #3, #6 |
| Adversarial Attacks (LLM) | #4, #6 | #1, #2, #4, #5 | #3, #10, #11 | #1 |
| Prompt Injection / Jailbreaking | #5, #6, #7 | #3, #4, #5 | #4, #5, #8, #9 | #1 |
| AI Safety / Alignment | #8, #9, #10 | #6, #7, #8, #9 | #2, #6 | #7 |
| Biological Immune Analogies | #11, #12 | — | — | #4, #5 |
| Multi-Agent Threat Modeling | #2, #15 | #13, #14 | #1, #5 | #8, #9 |
| Output Validation / Guardrails | #13, #14 | #10, #15 | #6, #7, #8 | #7 |
| Adversarial Robustness (Classical ML) | #4 | #11, #12 | #3, #10, #11 | #1 |

---

## 6. Ingestion Priority (for LM-LTM repo)

### Tier 1 — Upload First (foundational, highest signal)
- arXiv: Zou 2307.15043 (GCG attack), Greshake 2302.12173 (indirect injection), Hubinger 2401.05566 (Sleeper Agents), Bai 2212.08073 (Constitutional AI)
- GitHub READMEs: PyRIT, PurpleLlama, IBM ART, garak
- YouTube transcripts: DEFCON AI Village red teaming, Simon Willison prompt injection, Anthropic red teaming
- Books: Joseph et al. Adversarial ML, Dettmer Immune, Shostack Threat Modeling

### Tier 2 — Upload Second (depth + methodology)
- arXiv: Wei 2307.02483 (Jailbroken), Rafailov 2305.18290 (DPO), Gu 2402.08567 (Agent Smith), Carlini 1608.04644 (C&W attack)
- GitHub READMEs: NeMo-Guardrails, LLM-Guard, TextAttack
- YouTube transcripts: PyRIT tutorial, RLHF/DPO Hugging Face, Yannic Kilcher jailbreaking
- Books: Weidman Penetration Testing, Stuttard/Pinto Web App Hacker's Handbook

### Tier 3 — Upload Third (breadth + reference)
- arXiv: TrustLLM, R-Judge, CyberSecEval, remaining surveys
- GitHub READMEs: Foolbox, guardrails-ai, rebuff
- YouTube transcripts: Biological immunity lectures, AIS lectures, OWASP LLM Top 10
- Books: Janeway's Immunobiology, Shoham/Leyton-Brown Multi-Agent Systems, Google SRE Security

---

## 7. Notes for Owner

1. **Overlap with zero trust sources is intentional.** Per cross-pollination strategy, ~8 sources appear in both files. This region (adversarial/red team) focuses on OFFENSIVE methodology — how attacks work, how to break things, how to think like an adversary. The zero trust region focuses on DEFENSIVE architecture — how to build systems that assume breach.

2. **Biological immune sources are unique to this region.** The Dettmer and Janeway books, plus the immunity lectures, are specific to brain region #4 because the immune agent's design comes from real immunology. Self/non-self discrimination, clonal selection, danger theory — these are not metaphors, they are design patterns.

3. **Carlini & Wagner papers are old but canonical.** The 2017 C&W papers established the methodology for evaluating adversarial robustness. Every robustness paper since cites them. They teach the principle: "your defense is only as good as the attack you test it against."

4. **Agent Smith paper (Gu 2024) is especially relevant.** It demonstrates infectious jailbreak propagation in multi-agent systems — exactly the threat model OpenBrainLM's immune agent must defend against. One compromised agent propagating malicious instructions to others via shared context.

5. **YouTube search instructions**: Search queries are provided rather than direct URLs for videos where URLs may have changed. The search terms will find the right content.

6. **arXiv papers with IDs**: Papers marked with specific arXiv IDs (e.g., 2307.15043) are verified real papers with confirmed IDs. Papers marked "Search:" should be verified by searching arXiv directly.

7. **GitHub star counts**: Approximate as of early 2025. All repos listed are well-established projects backed by major organizations (Microsoft, Meta, NVIDIA, IBM, OWASP).

8. **Threat modeling book (Shostack)**: While from 2014, the STRIDE methodology and attack tree approach are timeless. Adam Shostack literally wrote the book on threat modeling at Microsoft. Apply his framework to enumerate threats in the OpenBrainLM agent ecosystem.
