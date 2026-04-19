# Evolutionary ML — Source List
> Compiled: 2026-03-21 by explorer agent
> Target brain region: #5 Evolutionary ML
> Purpose: Self-evolution foundations for OpenBrainLM — neuroevolution, open-ended evolution, biological self-modification, neural architecture search
> Status: COMPILED — Owner to verify URLs before upload

---

## IMPORTANT: Verification Notice

All sources below are based on well-known, widely-cited works and repositories that existed as of early 2025. Owner should verify each URL is still live before uploading. YouTube URLs in particular should be spot-checked — channels sometimes remove or rename videos.

---

## 1. YouTube Videos (free — distill into LM-LTM repo)

### Evolutionary Algorithms Foundations
1. **"Genetic Algorithms Explained"** — Lex Fridman (lecture series, MIT) — Search: `Lex Fridman genetic algorithms lecture`
   - Why: Clear academic presentation of GA fundamentals — selection, crossover, mutation, fitness landscapes.

2. **"Neuroevolution: Evolving Neural Networks"** — Lex Fridman (MIT 6.S094) — Search: `Lex Fridman neuroevolution lecture`
   - Why: Covers NEAT, HyperNEAT, and the intersection of evolution and deep learning. Directly relevant to OpenBrainLM morphogen agent.

3. **"Karl Sims — Evolved Virtual Creatures"** — Karl Sims (original 1994 demo, re-uploaded) — Search: `Karl Sims evolved virtual creatures 1994`
   - Why: The canonical demo of morphology + behavior co-evolution. 30 years old and still the clearest illustration of open-ended evolution.

4. **"Kenneth Stanley: Why Greatness Cannot Be Planned"** — Talks at Google / Lex Fridman — Search: `Kenneth Stanley why greatness cannot be planned talk`
   - Why: Stanley's thesis that objective-driven search fails and novelty/interestingness drives real discovery. Core philosophy for OpenBrainLM explorer agent.

### Neuroevolution and Neural Architecture Search
5. **"NEAT: NeuroEvolution of Augmenting Topologies"** — Various academic channels — Search: `NEAT neuroevolution augmenting topologies explained`
   - Why: Stanley's foundational algorithm. Evolves both topology and weights. The algorithm behind OpenBrainLM's morphogen concept.

6. **"Neural Architecture Search — AutoML"** — Yannic Kilcher — Search: `Yannic Kilcher neural architecture search`
   - Why: Kilcher's explanations of NAS papers are consistently the clearest in the community. Covers NASNet, DARTS, ENAS.

7. **"Jeff Clune: AI-Generating Algorithms"** — Various conference talks — Search: `Jeff Clune AI generating algorithm talk 2019`
   - Why: Clune's vision of algorithms that generate the learning algorithms themselves. The meta-level of self-evolution.

### Biological Self-Modification
8. **"How Octopuses Edit Their Own RNA"** — PBS Eons / Nature Video — Search: `octopus RNA editing PBS Eons` or `octopus RNA editing Nature`
   - Why: Biological basis for OpenBrainLM's morphogen agent. Octopuses rewrite their own genetic instructions on the fly.

9. **"Neuroplasticity — How the Brain Rewires Itself"** — Huberman Lab / Kurzgesagt — Search: `neuroplasticity brain rewires Huberman` or `Kurzgesagt neuroplasticity`
   - Why: Biological foundation for Hebbian learning and synaptic pruning in OpenBrainLM's L5 memory layer.

10. **"Turing Patterns in Biology"** — 3Blue1Brown / Numberphile — Search: `Turing patterns reaction diffusion 3Blue1Brown` or `Numberphile Turing patterns`
    - Why: Reaction-diffusion systems that generate biological morphology. Mathematical basis for morphogenetic field concepts.

### Self-Play and Program Synthesis
11. **"AlphaGo Zero: Learning from Scratch"** — DeepMind (official) — Search: `DeepMind AlphaGo Zero learning from scratch`
    - Why: The canonical demonstration of self-play producing superhuman capability without human data. Core paradigm for self-improvement.

12. **"MuZero: Mastering Games Without Knowing the Rules"** — DeepMind / Yannic Kilcher — Search: `MuZero DeepMind mastering games`
    - Why: Extends self-play to learning the world model itself. Relevant to OpenBrainLM's prediction error mechanisms.

### Open-Ended Evolution
13. **"Joel Lehman: Novelty Search and Open-Ended Evolution"** — Various conferences / podcasts — Search: `Joel Lehman novelty search open-ended evolution talk`
    - Why: Co-author with Stanley on novelty search. The idea that rewarding novelty over fitness produces more creative solutions.

14. **"Artificial Life and Open-Ended Evolution"** — Santa Fe Institute / ALIFE conference talks — Search: `Santa Fe Institute artificial life open-ended evolution`
    - Why: The ALIFE community is where open-ended evolution research lives. SFI talks are consistently high-quality.

15. **"Hugo de Garis: The Artilect War / Brain Building"** — Various interviews and lectures — Search: `Hugo de Garis brain building artificial brain`
    - Why: De Garis built evolutionary neural circuits on FPGAs in the 1990s-2000s. Controversial but technically substantive work on evolving brain modules.

---

## 2. arXiv Papers (free PDFs — distill into LM-LTM repo)

### Neuroevolution
1. **"Evolving Neural Networks through Augmenting Topologies"**
   - Authors: Kenneth O. Stanley, Risto Miikkulainen (2002)
   - Published: Evolutionary Computation, MIT Press
   - URL: http://nn.cs.utexas.edu/downloads/papers/stanley.ec02.pdf
   - Why: THE foundational NEAT paper. Evolves both topology and weights simultaneously. Speciation preserves innovation. Canonical reference for morphogen agent.

2. **"A Hypercube-Based Encoding for Evolving Large-Scale Neural Networks"**
   - Authors: Kenneth O. Stanley, David B. D'Ambrosio, Jason Gauci (2009)
   - Published: Artificial Life, MIT Press
   - Why: HyperNEAT — extends NEAT to evolve large-scale networks using compositional pattern producing networks (CPPNs). Geometric regularity in neural connectivity.

3. **"Deep Neuroevolution: Genetic Algorithms Are a Competitive Alternative for Training Deep Neural Networks for Reinforcement Learning"**
   - Authors: Felipe Petroski Such, Vashisht Madhavan, Edoardo Conti, Joel Lehman, Kenneth O. Stanley, Jeff Clune (2017)
   - arXiv: 1712.06567
   - URL: https://arxiv.org/abs/1712.06567
   - Why: Showed simple GAs can train large deep networks competitively with gradient-based RL. Uber AI Labs. Reopened the neuroevolution door.

4. **"Regularized Evolution for Image Classifier Architecture Search"**
   - Authors: Esteban Real, Alok Aggarwal, Yanping Huang, Quoc V. Le (2019)
   - arXiv: 1802.01548
   - URL: https://arxiv.org/abs/1802.01548
   - Why: Google Brain. Showed regularized (aging) tournament selection outperforms RL-based NAS. Simple evolutionary approach beats complex methods.

### Open-Ended Evolution and Novelty Search
5. **"Exploiting Open-Endedness to Solve Problems Through the Search for Novelty"**
   - Authors: Joel Lehman, Kenneth O. Stanley (2008)
   - Published: ALIFE XI
   - Why: The original novelty search paper. Abandoning objectives and rewarding behavioral novelty produces better solutions. Paradigm shift.

6. **"Abandoning Objectives: Evolution Through the Search for Novelty Alone"**
   - Authors: Joel Lehman, Kenneth O. Stanley (2011)
   - Published: Evolutionary Computation, MIT Press
   - Why: Extended novelty search paper with rigorous analysis. Shows why objective-driven search gets trapped in deceptive fitness landscapes.

7. **"Open-Ended Learning in Symmetric Zero-Sum Games"**
   - Authors: David Balduzzi, Sebastien Racaniere, James Martens, Jakob Foerster, Karl Tuyls, Thore Graepel (2019)
   - arXiv: 1901.08106
   - URL: https://arxiv.org/abs/1901.08106
   - Why: DeepMind. Formal framework for open-ended learning in competitive games. Relevant to self-play evolution.

8. **"Why Greatness Cannot Be Planned: The Myth of the Objective"**
   - Authors: Kenneth O. Stanley, Joel Lehman (2015)
   - Published: Springer (book, but key ideas also in conference papers)
   - Why: The full argument against objective-driven search. Serendipity and stepping stones matter more than fitness functions.

### Neural Architecture Search
9. **"Neural Architecture Search with Reinforcement Learning"**
   - Authors: Barret Zoph, Quoc V. Le (2017)
   - arXiv: 1611.01578
   - URL: https://arxiv.org/abs/1611.01578
   - Why: The paper that launched NAS. Used RL to discover architectures. Google Brain. Showed machines can design networks.

10. **"DARTS: Differentiable Architecture Search"**
    - Authors: Hanxiao Liu, Karen Simonyan, Yiming Yang (2019)
    - arXiv: 1806.09055
    - URL: https://arxiv.org/abs/1806.09055
    - Why: Made NAS practical by relaxing discrete search to continuous optimization. Orders of magnitude faster than RL-based NAS.

11. **"Efficient Neural Architecture Search via Parameter Sharing"**
    - Authors: Hieu Pham, Melody Y. Guan, Barret Zoph, Quoc V. Le, Jeff Dean (2018)
    - arXiv: 1802.03268
    - URL: https://arxiv.org/abs/1802.03268
    - Why: ENAS — made NAS 1000x cheaper by sharing parameters across candidate architectures. Practical breakthrough.

### Self-Play and Self-Improvement
12. **"Mastering the Game of Go without Human Knowledge"**
    - Authors: David Silver et al. (2017, DeepMind)
    - Published: Nature, Vol. 550
    - DOI: 10.1038/nature24270
    - Why: AlphaGo Zero. Self-play from tabula rasa surpasses all human knowledge. The existence proof for self-improvement in AI.

13. **"Mastering Atari, Go, Chess and Shogi by Planning with a Learned Model"**
    - Authors: Julian Schrittwieser et al. (2020, DeepMind)
    - arXiv: 1911.08265
    - URL: https://arxiv.org/abs/1911.08265
    - Why: MuZero. Learns the model, the value function, AND the policy through self-play. No rules given. The most general self-play system.

### Biological Self-Modification
14. **"Trade-off between Transcriptome Plasticity and Genome Evolution in Cephalopods"**
    - Authors: Natan Liscovitch-Brauer, Shahar Alon, Hagit T. Porath, et al. (2017)
    - Published: Cell, Vol. 169, Issue 2
    - DOI: 10.1016/j.cell.2017.03.025
    - Why: The landmark paper showing octopuses extensively edit their RNA at the cost of genomic evolution. Biology's proof that runtime self-modification works.

15. **"AI-Generating Algorithms, an Alternate Paradigm for Producing General Artificial Intelligence"**
    - Authors: Jeff Clune (2019)
    - arXiv: 1905.10985
    - URL: https://arxiv.org/abs/1905.10985
    - Why: The manifesto for algorithms that generate learning algorithms. Meta-learning through evolution. Directly relevant to OpenBrainLM's self-evolution goal.

16. **"Genetic Programming: On the Programming of Computers by Means of Natural Selection"**
    - Authors: John R. Koza (1992)
    - Published: MIT Press (book — seminal reference)
    - Why: THE foundational work on evolving programs. Koza invented genetic programming. Everything in program synthesis traces back here.

---

## 3. GitHub Repositories (free, open source)

### Neuroevolution Frameworks
1. **CodeReclworx/neat-python**
   - Stars: ~1k+
   - License: BSD 3-Clause
   - URL: https://github.com/CodeReclworx/neat-python
   - Python implementation of NEAT. Well-documented, actively used for research and education.

2. **uber-research/deep-neuroevolution**
   - Stars: ~1.5k+
   - License: Apache 2.0
   - URL: https://github.com/uber-research/deep-neuroevolution
   - Uber AI Labs. Scalable GA for deep RL. The code behind the "Deep Neuroevolution" paper (Petroski Such et al. 2017).

3. **google-deepmind/open_spiel**
   - Stars: ~4k+
   - License: Apache 2.0
   - URL: https://github.com/google-deepmind/open_spiel
   - DeepMind's framework for games and self-play research. Includes AlphaZero, MCTS, evolutionary game theory.

### Evolutionary Algorithms
4. **DEAP/deap**
   - Stars: ~5k+
   - License: LGPL-3.0
   - URL: https://github.com/DEAP/deap
   - Distributed Evolutionary Algorithms in Python. The standard EA framework. Supports GP, GA, ES, multi-objective (NSGA-II). Production-grade.

5. **mealpy** (thieu1995/mealpy)
   - Stars: ~800+
   - License: GPL-3.0
   - URL: https://github.com/thieu1995/mealpy
   - Meta-heuristic optimization library. 200+ algorithms including GA, PSO, DE, CMA-ES. Broad optimization toolkit applicable to morphogen fitness evaluation.

6. **CMA-ES/pycma**
   - Stars: ~1k+
   - License: BSD 3-Clause
   - URL: https://github.com/CMA-ES/pycma
   - Covariance Matrix Adaptation Evolution Strategy. Nikolaus Hansen's reference implementation. Gold standard for continuous optimization.

### Neural Architecture Search
7. **automl/NASLib**
   - Stars: ~500+
   - License: Apache 2.0
   - URL: https://github.com/automl/NASLib
   - AutoML Freiburg. Unified NAS library supporting DARTS, ENAS, random search, regularized evolution. Benchmark-ready.

8. **microsoft/nni**
   - Stars: ~13k+
   - License: MIT
   - URL: https://github.com/microsoft/nni
   - Microsoft Neural Network Intelligence. NAS, hyperparameter tuning, model compression. Production framework.

### Artificial Life and Open-Ended Evolution
9. **google/evojax**
   - Stars: ~800+
   - License: Apache 2.0
   - URL: https://github.com/google/evojax
   - Google. Hardware-accelerated neuroevolution on JAX. Massively parallel ES/GA on GPU/TPU.

10. **uber-research/poet**
    - Stars: ~500+
    - License: Apache 2.0
    - URL: https://github.com/uber-research/poet
    - Paired Open-Ended Trailblazer (POET). Co-evolves agents AND environments. Open-ended evolution in practice.

11. **Evolutionary-Intelligence/pypop**
    - Stars: ~300+
    - License: MIT
    - URL: https://github.com/Evolutionary-Intelligence/pypop
    - Pure Python population-based optimization. Clean implementations of CMA-ES, NES, OpenAI-ES, GA, DE, PSO.

---

## 4. Books (behind paywalls — Owner to acquire)

1. **"Why Greatness Cannot Be Planned: The Myth of the Objective"**
   - Authors: Kenneth O. Stanley, Joel Lehman
   - Year: 2015 (Springer)
   - Publisher: Springer
   - Why: The philosophical foundation for novelty-driven search. Argues that objectives are traps and stepping stones are everything. Core philosophy for OpenBrainLM's explorer agent.

2. **"Genetic Programming: On the Programming of Computers by Means of Natural Selection"**
   - Author: John R. Koza
   - Year: 1992 (MIT Press)
   - Publisher: MIT Press
   - Why: THE foundational book on evolving programs. Koza invented the field. Dense but canonical.

3. **"Neuroevolution: Principles and Practice"**
   - Author: Kenneth O. Stanley (with various co-authors, multiple editions/chapters)
   - Note: Key material spread across Stanley's papers rather than a single book. Best consolidated source is his 2019 Nature Machine Intelligence review "Designing neural networks through neuroevolution" (Stanley, Clune, Lehman, Miikkulainen).
   - Why: Stanley is the central figure in neuroevolution. His review papers serve as de facto textbook chapters.

4. **"Introduction to Evolutionary Computing"**
   - Authors: A.E. Eiben, J.E. Smith
   - Year: 2003, 2nd ed. 2015 (Springer)
   - Publisher: Springer (Natural Computing Series)
   - Why: The standard textbook for evolutionary computation. Covers GA, GP, ES, EP, multi-objective optimization. Used in most university courses.

5. **"The Major Transitions in Evolution"**
   - Authors: John Maynard Smith, Eors Szathmary
   - Year: 1995 (Oxford University Press)
   - Publisher: Oxford University Press
   - Why: How complexity emerges through evolutionary transitions (replicating molecules to cells to multicellularity to language). The biological roadmap for open-ended evolution.

6. **"Other Minds: The Octopus, the Sea, and the Deep Origins of Consciousness"**
   - Author: Peter Godfrey-Smith
   - Year: 2016 (Farrar, Straus and Giroux)
   - Publisher: FSG
   - Why: Philosopher of biology examines octopus intelligence — distributed nervous system, RNA editing, independent arm cognition. Direct biological inspiration for OpenBrainLM's ganglion layer.

7. **"The Self-Assembling Brain: How Neural Networks Grow Smarter"**
   - Author: Peter Robin Hiesinger
   - Year: 2021 (Princeton University Press)
   - Publisher: Princeton University Press
   - Why: How biological brains build themselves through developmental programs, not just learning. Morphogenetic fields, growth rules, self-organization. Directly relevant to L1-L3 layers.

8. **"Artificial Life: A Report from the Frontier Where Computers Meet Biology"**
   - Author: Steven Levy
   - Year: 1992 (Vintage)
   - Publisher: Vintage Books
   - Why: The accessible history of the artificial life movement — Langton, Kauffman, Holland, Ray. Context for why open-ended evolution matters.

9. **"An Introduction to Genetic Algorithms"**
   - Author: Melanie Mitchell
   - Year: 1996 (MIT Press)
   - Publisher: MIT Press
   - Why: The most readable introduction to GAs. Mitchell (Santa Fe Institute) bridges theory and practice clearly. Good complement to Eiben/Smith for accessibility.

---

## Cross-Reference Map (which sources feed which concepts)

| Concept | YouTube | arXiv | GitHub | Books |
|---|---|---|---|---|
| Genetic Algorithms / GP | #1 | #16 (Koza) | #4, #5 | #2, #4, #9 |
| Neuroevolution (NEAT/HyperNEAT) | #2, #5 | #1, #2, #3 | #1, #2, #9 | #3, #4 |
| Neural Architecture Search | #6 | #4, #9, #10, #11 | #7, #8 | #4 |
| Open-Ended Evolution | #4, #13, #14 | #5, #6, #7, #8 | #10 | #1, #5, #8 |
| Biological Self-Modification (RNA editing) | #8, #9 | #14 | — | #6, #7 |
| Neuroplasticity / Synaptic Pruning | #9, #10 | — | — | #7, #6 |
| Self-Play / Self-Improvement | #11, #12 | #12, #13 | #3 | — |
| Program Synthesis | #1 | #15, #16 | #4 | #2, #9 |
| Morphogenetic Fields / Turing Patterns | #10 | — | — | #5, #7 |
| Meta-Evolution (AI-Generating Algorithms) | #7, #15 | #3, #15 | #2, #10 | #1, #3 |

---

## Ingestion Priority (for LM-LTM repo)

### Tier 1 — Upload First (foundational)
- arXiv: Stanley NEAT paper (#1), Lehman/Stanley novelty search (#5, #6), Clune AI-Generating Algorithms (1905.10985), AlphaGo Zero (#12)
- GitHub READMEs: DEAP, neat-python, open_spiel
- YouTube transcripts: Kenneth Stanley "Greatness Cannot Be Planned" talk, Karl Sims "Evolved Virtual Creatures", Octopus RNA editing
- Books: Stanley/Lehman "Why Greatness Cannot Be Planned", Eiben/Smith "Introduction to Evolutionary Computing"

### Tier 2 — Upload Second (depth)
- arXiv: Deep Neuroevolution (1712.06567), DARTS (1806.09055), MuZero (1911.08265), Regularized Evolution (1802.01548)
- GitHub READMEs: uber-research/deep-neuroevolution, uber-research/poet, microsoft/nni
- YouTube transcripts: Neuroevolution lectures, Jeff Clune AI-generating algorithm talk, Neuroplasticity
- Books: Godfrey-Smith "Other Minds", Hiesinger "The Self-Assembling Brain"

### Tier 3 — Upload Third (breadth)
- arXiv: NAS with RL (1611.01578), ENAS (1802.03268), Open-Ended Learning in Games (1901.08106), Octopus RNA Cell paper
- Remaining YouTube: Turing patterns, Hugo de Garis, ALIFE talks
- GitHub READMEs: evojax, pycma, pypop, NASLib
- Books: Koza GP, Melanie Mitchell, Maynard Smith/Szathmary, Levy "Artificial Life"

---

## Notes for Owner

1. **Kenneth Stanley is the central figure.** His work (NEAT, HyperNEAT, novelty search, "Why Greatness Cannot Be Planned") forms the philosophical and algorithmic backbone of evolutionary ML. His papers and talks should be prioritized above all others in this domain.

2. **Joel Lehman and Jeff Clune are Stanley's key collaborators.** Lehman co-developed novelty search and MAP-Elites. Clune pushed the "AI-generating algorithm" vision. Together with Stanley, they form the Uber AI Labs evolutionary AI lineage.

3. **Karl Sims (1994) is old but irreplaceable.** His "Evolved Virtual Creatures" demo remains the single most compelling visualization of co-evolved morphology and behavior. The video is worth uploading even if the paper is dated.

4. **Octopus RNA editing (Liscovitch-Brauer et al. 2017)** is published in Cell, not arXiv. The DOI link (10.1016/j.cell.2017.03.025) should work. This is the biological anchor for OpenBrainLM's morphogen agent — runtime self-modification at the genetic level.

5. **Hugo de Garis** is controversial (his "Artilect War" predictions are sensationalist), but his actual technical work on evolving neural circuits in FPGAs (the CAM-Brain project) was legitimate engineering. Use the technical content, skip the futurism.

6. **YouTube search instructions**: Direct URLs were avoided for most videos because specific video URLs change frequently. The search terms provided will find the right content.

7. **arXiv vs. journal papers**: Several foundational papers (NEAT, novelty search, AlphaGo Zero, octopus RNA editing) were published in journals, not arXiv. Direct URLs or DOIs are provided where the paper lives. All are freely accessible or have preprint versions.

8. **Cross-pollination targets**: Per Owner's brain region overlap strategy, the strongest sources should also feed into:
   - Region #1 (Neural_ARC): Neuroevolution, neuroplasticity, octopus RNA editing
   - Region #6 (Optimization & ML): DEAP, CMA-ES, mealpy (general-purpose optimization)
   - Region #3 (Agents_Arcs): Self-play, AI-generating algorithms, open-ended evolution
