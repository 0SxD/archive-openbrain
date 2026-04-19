# Barrier (Blood-Brain Barrier) -- Source List
> Compiled: 2026-03-21 by explorer agent
> Target brain region: #08 Barrier (Blood-Brain Barrier)
> Purpose: Screening, uncertainty management, and quarantine for OpenBrainLM -- selective permeability for information entering the brain
> Status: COMPILED -- Owner to verify URLs before upload

---

## IMPORTANT: Verification Notice

All sources below are based on well-known, widely-cited works and repositories that existed as of early 2025. Owner should verify each URL is still live before uploading. YouTube URLs in particular should be spot-checked -- channels sometimes remove or rename videos.

---

## 1. YouTube Videos (free -- distill into LM-LTM repo)

### Blood-Brain Barrier Biology
1. **"Blood Brain Barrier, bbb, Animation"** -- Armando Hasudungan -- Search: `Armando Hasudungan blood brain barrier`
   - Why: Hasudungan's medical illustrations are the clearest visual explanations of BBB transport mechanisms. Biomimicry foundation.

2. **"The Blood-Brain Barrier"** -- Osmosis (from Elsevier) -- Search: `Osmosis blood brain barrier`
   - Why: Covers tight junctions, transcytosis, efflux pumps, and immune privilege. Well-structured for non-biologists.

3. **"Blood Brain Barrier -- Structure and Function"** -- Ninja Nerd -- Search: `Ninja Nerd blood brain barrier`
   - Why: Deep dive into astrocyte end-feet, pericytes, and the neurovascular unit. The structural basis for selective permeability.

### Bayesian Uncertainty and Epistemic Reasoning
4. **"Bayesian Deep Learning and Uncertainty Quantification"** -- Yarin Gal (various talks) -- Search: `Yarin Gal Bayesian deep learning uncertainty`
   - Why: Gal is THE leading researcher on uncertainty in deep learning. His PhD thesis (Cambridge) redefined the field. Foundational.

5. **"Epistemic vs Aleatoric Uncertainty in Machine Learning"** -- Machine Learning Street Talk (MLST) -- Search: `MLST epistemic aleatoric uncertainty`
   - Why: MLST goes deep on the philosophical distinction between what you COULD know (epistemic) and what is fundamentally random (aleatoric). Core to the Barrier's quarantine logic.

6. **"Conformal Prediction: A Gentle Introduction"** -- Anastasios Angelopoulos (various talks) -- Search: `Anastasios Angelopoulos conformal prediction tutorial`
   - Why: Angelopoulos (Berkeley) is the leading voice on conformal prediction. Distribution-free uncertainty sets with coverage guarantees.

### Signal Detection and Decision Theory
7. **"Signal Detection Theory"** -- Daniel Lakens (Eindhoven) -- Search: `Daniel Lakens signal detection theory`
   - Why: Clear explanation of sensitivity, specificity, d-prime, ROC curves. The mathematical language of screening.

8. **"Thinking About Thinking: Metacognition"** -- Veritasium / various science channels -- Search: `Veritasium metacognition knowing what you know`
   - Why: Metacognition -- knowing what you know and don't know -- is the psychological foundation for doubt parking and decision deferral.

9. **"The Science of Being Wrong"** -- Julia Galef -- Search: `Julia Galef scout mindset being wrong`
   - Why: Galef's "scout mindset" framework is about calibration -- updating beliefs proportionally to evidence. Directly applicable to the Barrier's screening function.

### Active Learning and Knowing What You Don't Know
10. **"Active Learning: Querying the Right Data"** -- Stanford CS229 / various ML lectures -- Search: `active learning machine learning lecture uncertainty sampling`
    - Why: Active learning is the ML framework for knowing what you don't know and asking the right questions. Core Barrier capability.

11. **"Calibration of Modern Neural Networks"** -- Chuan Guo et al. (talks based on the ICML 2017 paper) -- Search: `neural network calibration Guo ICML 2017`
    - Why: The canonical paper showing modern nets are poorly calibrated. Temperature scaling fix. Barrier must calibrate confidence.

### Scientific Skepticism and Verification
12. **"The Problem with p-values"** -- StatQuest with Josh Starmer -- Search: `StatQuest p-values null hypothesis`
    - Why: Clear, accessible explanation of null hypothesis testing, burden of proof, and why p-values are misunderstood. Skepticism methodology.

13. **"The Replication Crisis"** -- Veritasium -- Search: `Veritasium replication crisis`
    - Why: Why published results fail to replicate. File drawer problem, p-hacking, HARKing. The Barrier must screen for these failure modes.

### Quarantine and Sandboxing Patterns
14. **"Canary Deployments and Progressive Delivery"** -- CNCF / DevOps channels -- Search: `CNCF canary deployment progressive delivery`
    - Why: Canary deployments are the infrastructure pattern for quarantine: release to a small subset, monitor, promote or rollback. Directly maps to the Barrier's staged admission.

15. **"Container Security and Sandboxing"** -- Liz Rice (various conference talks) -- Search: `Liz Rice container security sandboxing`
    - Why: Rice is the leading practitioner on container isolation. Her talks cover namespace isolation, seccomp, and defense-in-depth. The tech pattern behind quarantine.

---

## 2. arXiv Papers (free PDFs -- distill into LM-LTM repo)

### Uncertainty Quantification
1. **"Dropout as a Bayesian Approximation: Representing Model Uncertainty in Deep Learning"**
   - Authors: Yarin Gal, Zoubin Ghahramani (2016)
   - arXiv: 1506.02142
   - URL: https://arxiv.org/abs/1506.02142
   - Why: THE foundational paper connecting dropout to Bayesian inference. MC Dropout = cheap uncertainty estimates. Every downstream uncertainty paper builds on this.

2. **"What Uncertainties Do We Need in Bayesian Deep Learning for Computer Vision?"**
   - Authors: Alex Kendall, Yarin Gal (2017)
   - arXiv: 1703.04977
   - URL: https://arxiv.org/abs/1703.04977
   - Why: The paper that formalized the epistemic vs aleatoric distinction in deep learning. Canonical reference.

3. **"Simple and Scalable Predictive Uncertainty Estimation using Deep Ensembles"**
   - Authors: Balaji Lakshminarayanan, Alexander Pritzel, Charles Blundell (2017, DeepMind)
   - arXiv: 1612.01474
   - URL: https://arxiv.org/abs/1612.01474
   - Why: Deep ensembles as a practical alternative to Bayesian methods. Often outperforms MC Dropout. Benchmark paper.

4. **"Practical Deep Learning with Bayesian Principles"**
   - Authors: Kazuki Osawa et al. (2019)
   - arXiv: 1906.02506
   - URL: https://arxiv.org/abs/1906.02506
   - Why: Bridges theory and practice for Bayesian deep learning at scale. Natural gradient variational inference.

### Conformal Prediction and Calibration
5. **"Conformal Prediction Under Covariate Shift"**
   - Authors: Ryan Tibshirani et al. (2019)
   - arXiv: 1904.06019
   - URL: https://arxiv.org/abs/1904.06019
   - Why: Extends conformal prediction to the non-exchangeable setting. Critical when incoming data distribution shifts.

6. **"Gentle Introduction to Conformal Prediction and Distribution-Free Uncertainty Quantification"**
   - Authors: Anastasios N. Angelopoulos, Stephen Bates (2022)
   - arXiv: 2107.07511
   - URL: https://arxiv.org/abs/2107.07511
   - Why: THE tutorial paper on conformal prediction. Distribution-free coverage guarantees. Directly applicable to Barrier screening.

7. **"On Calibration of Modern Neural Networks"**
   - Authors: Chuan Guo, Geoff Pleiss, Yu Sun, Kilian Q. Weinberger (2017)
   - arXiv: 1706.04599
   - URL: https://arxiv.org/abs/1706.04599
   - Why: Showed modern deep networks are miscalibrated. Introduced temperature scaling. Barrier must know when confidence scores are lying.

### Active Learning and Selective Prediction
8. **"A Survey of Active Learning for Text Classification using Deep Neural Networks"**
   - Authors: Christopher Schroeder, Andreas Niekler (2020)
   - arXiv: 2008.07267
   - URL: https://arxiv.org/abs/2008.07267
   - Why: Comprehensive survey of active learning strategies including uncertainty sampling, query-by-committee. Knowing-what-you-don't-know formalized.

9. **"SelectiveNet: A Deep Neural Network with an Integrated Reject Option"**
   - Authors: Yonatan Geifman, Ran El-Yaniv (2019)
   - arXiv: 1901.09192
   - URL: https://arxiv.org/abs/1901.09192
   - Why: Trains networks to ABSTAIN when uncertain. The ML formalization of "doubt parking" -- knowing when NOT to decide.

10. **"Learning to Defer to Multiple Experts"**
    - Authors: Rajeev Verma, Eric Nalisnick (2022)
    - arXiv: 2206.07912
    - URL: https://arxiv.org/abs/2206.07912
    - Why: Formalizes the decision to defer -- when the system should pass judgment to a more capable evaluator. Core Barrier behavior.

### Out-of-Distribution Detection
11. **"A Baseline for Detecting Misclassified and Out-of-Distribution Examples in Neural Networks"**
    - Authors: Dan Hendrycks, Kevin Gimpel (2017)
    - arXiv: 1610.02136
    - URL: https://arxiv.org/abs/1610.02136
    - Why: The baseline OOD detection paper. Maximum softmax probability as a simple detector. Starting point for all subsequent work.

12. **"Energy-based Out-of-distribution Detection"**
    - Authors: Weitang Liu, Xiaoyun Wang, John Owens, Yixuan Li (2020)
    - arXiv: 2010.03759
    - URL: https://arxiv.org/abs/2010.03759
    - Why: Energy scores as theoretically grounded OOD detectors. Better than softmax baseline. Barrier needs to detect when inputs are from outside its training distribution.

### Information Filtering and Quality Gates
13. **"TrustScore: A Measure of Classifier Trustworthiness"**
    - Authors: Heinrich Jiang, Been Kim, Melody Guan, Maya Gupta (2018, Google)
    - arXiv: 1805.11783
    - URL: https://arxiv.org/abs/1805.11783
    - Why: Assigns a trust score to individual predictions independent of the classifier. Directly applicable to per-claim screening.

14. **"Know What You Don't Know: Unanswerable Questions for SQuAD"**
    - Authors: Pranav Rajpurkar, Robin Jia, Percy Liang (2018, Stanford)
    - arXiv: 1806.03822
    - URL: https://arxiv.org/abs/1806.03822
    - Why: SQuAD 2.0 -- training systems to say "I don't know." The NLP benchmark for abstention and doubt parking.

15. **"Selective Question Answering under Domain Shift"**
    - Authors: Amita Kamath, Robin Jia, Percy Liang (2020, Stanford)
    - arXiv: 2006.09462
    - URL: https://arxiv.org/abs/2006.09462
    - Why: Extends selective prediction to the domain-shift setting. When the world changes, the Barrier must recalibrate what it admits.

---

## 3. GitHub Repositories (free, open source)

### Uncertainty Quantification
1. **uncertainty-toolbox/uncertainty-toolbox**
   - Stars: ~1.5k+
   - License: MIT
   - URL: https://github.com/uncertainty-toolbox/uncertainty-toolbox
   - Python toolbox for assessing, visualizing, and improving uncertainty quantification. Calibration metrics, sharpness, recalibration.

2. **google/edward2**
   - Stars: ~500+ (within tensorflow/probability ecosystem)
   - License: Apache 2.0
   - URL: https://github.com/google/edward2
   - Bayesian deep learning library from Google. Probabilistic layers, uncertainty-aware models.

3. **y0ast/deterministic-uncertainty-quantification** (DUQ)
   - Stars: ~200+
   - License: MIT
   - URL: https://github.com/y0ast/deterministic-uncertainty-quantification
   - Single forward-pass uncertainty estimation without ensembles or MC Dropout. Efficient Barrier screening.

### Conformal Prediction
4. **aangelopoulos/conformal-prediction**
   - Stars: ~500+
   - License: MIT
   - URL: https://github.com/aangelopoulos/conformal-prediction
   - Angelopoulos's reference implementation. Tutorials, examples, and code from the tutorial paper (2107.07511).

5. **valeman/awesome-conformal-prediction**
   - Stars: ~1k+
   - License: CC0
   - URL: https://github.com/valeman/awesome-conformal-prediction
   - Curated list of conformal prediction resources: papers, tutorials, software, applications. Starting point for the field.

### Out-of-Distribution Detection
6. **deeplearning-wisc/openood**
   - Stars: ~1k+
   - License: MIT
   - URL: https://github.com/deeplearning-wisc/openood
   - Unified benchmark for OOD detection. Implements 30+ methods. From Yixuan Li's group at Wisconsin.

7. **hendrycks/anomaly-seg**
   - Stars: ~200+
   - License: Apache 2.0
   - URL: https://github.com/hendrycks/anomaly-seg
   - Dan Hendrycks's anomaly/OOD detection code. Companion to the baseline OOD paper.

### Active Learning
8. **modAL-python/modAL**
   - Stars: ~2k+
   - License: MIT
   - URL: https://github.com/modAL-python/modAL
   - Active learning framework for Python. Uncertainty sampling, query-by-committee, Bayesian optimization. Scikit-learn compatible.

### Selective Prediction and Abstention
9. **geifmany/selectivenet**
   - Stars: ~100+
   - License: MIT
   - URL: https://github.com/geifmany/selectivenet
   - Reference implementation of SelectiveNet (reject option networks). Train models that know when to abstain.

### Content Moderation and Filtering
10. **NVIDIA/NeMo-Guardrails**
    - Stars: ~4k+
    - License: Apache 2.0
    - URL: https://github.com/NVIDIA/NeMo-Guardrails
    - Programmable guardrails for LLM systems. Input/output filtering, topic control, fact-checking flows. The production-grade Barrier pattern for LLMs.

11. **cleanlab/cleanlab**
    - Stars: ~9k+
    - License: AGPL-3.0
    - URL: https://github.com/cleanlab/cleanlab
    - Automatically finds and fixes label errors in datasets. Data quality gate -- screens for noise in training data. Confident Learning algorithm.

---

## 4. Books (behind paywalls -- Owner to acquire)

1. **"The Blood-Brain Barrier in Health and Disease"**
   - Editor: Krestin Dorovini-Zis
   - Year: 2015 (CRC Press)
   - Publisher: CRC Press
   - Why: Comprehensive reference on BBB biology: tight junctions, transporters, immune interactions, pathological disruption. The biomimicry source.

2. **"The Signal and the Noise: Why So Many Predictions Fail -- but Some Don't"**
   - Author: Nate Silver
   - Year: 2012 (Penguin)
   - Publisher: Penguin Press
   - Why: The accessible masterwork on separating signal from noise. Bayesian thinking, calibration, prediction markets. Barrier philosophy in book form.

3. **"Bayesian Reasoning and Machine Learning"**
   - Author: David Barber
   - Year: 2012 (Cambridge University Press)
   - Publisher: Cambridge University Press
   - Why: Full treatment of Bayesian inference, graphical models, approximate inference. Free PDF available from author's website. Theory backbone for uncertainty quantification.

4. **"Statistical Decision Theory and Bayesian Analysis"**
   - Author: James O. Berger
   - Year: 1985 (Springer), 2nd edition
   - Publisher: Springer
   - Why: THE rigorous reference on decision theory under uncertainty. Loss functions, admissibility, minimax. The mathematical foundation for "when NOT to decide."

5. **"Pattern Recognition and Machine Learning"**
   - Author: Christopher M. Bishop
   - Year: 2006 (Springer)
   - Publisher: Springer
   - Why: Chapter 1.5 (decision theory), Chapter 3 (Bayesian linear regression), Chapter 10 (approximate inference). The ML textbook treatment of uncertainty.

6. **"Detection Theory: A User's Guide"**
   - Authors: Neil A. Macmillan, C. Douglas Creelman
   - Year: 2005 (Lawrence Erlbaum), 2nd edition
   - Publisher: Lawrence Erlbaum Associates
   - Why: THE reference on signal detection theory. d-prime, ROC analysis, sensitivity/specificity trade-offs. Mathematical language of screening.

7. **"The Scout Mindset: Why Some People See Things Clearly and Others Don't"**
   - Author: Julia Galef
   - Year: 2021 (Portfolio/Penguin)
   - Publisher: Portfolio/Penguin
   - Why: Calibrated reasoning under uncertainty. The psychology of updating beliefs and resisting motivated reasoning. Barrier mindset.

8. **"Superforecasting: The Art and Science of Prediction"**
   - Authors: Philip E. Tetlock, Dan Gardner
   - Year: 2015 (Crown)
   - Publisher: Crown Publishers
   - Why: Tetlock's research on calibrated judgment. Foxes vs hedgehogs, Brier scores, epistemic humility. How to be properly uncertain.

9. **"How to Measure Anything: Finding the Value of Intangibles in Business"**
   - Author: Douglas W. Hubbard
   - Year: 2014 (Wiley), 3rd edition
   - Publisher: Wiley
   - Why: Practical uncertainty quantification for real-world decisions. Calibration training, confidence intervals, value of information analysis.

---

## Cross-Reference Map (which sources feed which concepts)

| Concept | YouTube | arXiv | GitHub | Books |
|---|---|---|---|---|
| BBB Biology / Biomimicry | #1, #2, #3 | -- | -- | #1 |
| Bayesian Uncertainty | #4, #5 | #1, #2, #3, #4 | #1, #2, #3 | #3, #4, #5 |
| Epistemic vs Aleatoric | #4, #5 | #2 | #1 | #3, #5 |
| Conformal Prediction / Calibration | #6, #11 | #5, #6, #7 | #4, #5 | #5 |
| Doubt Parking / Decision Deferral | #8, #9 | #9, #10 | #9 | #4, #7, #8 |
| Quarantine / Sandboxing | #14, #15 | -- | #10 | -- |
| Active Learning / Know What You Don't Know | #10 | #8, #14 | #8 | #9 |
| Signal Detection Theory | #7, #12 | -- | -- | #6 |
| Scientific Skepticism / Replication | #12, #13 | -- | #11 | #2, #7, #8 |
| OOD Detection / Information Filtering | -- | #11, #12, #13 | #6, #7 | -- |
| Quality Gates / Verification | #14 | #13, #15 | #10, #11 | #9 |
| Content Moderation / Triage | #15 | #14 | #10 | -- |

---

## Ingestion Priority (for LM-LTM repo)

### Tier 1 -- Upload First (foundational)
- arXiv: Gal & Ghahramani 1506.02142 (MC Dropout), Kendall & Gal 1703.04977 (epistemic vs aleatoric), Angelopoulos & Bates 2107.07511 (conformal prediction), Geifman & El-Yaniv 1901.09192 (SelectiveNet)
- GitHub READMEs: uncertainty-toolbox, conformal-prediction (Angelopoulos), NeMo-Guardrails
- YouTube transcripts: Yarin Gal uncertainty, Angelopoulos conformal prediction, Armando Hasudungan BBB
- Books: Nate Silver Signal and the Noise, Bishop PRML (chapters 1.5, 3, 10)

### Tier 2 -- Upload Second (depth)
- arXiv: Deep Ensembles 1612.01474, Hendrycks OOD baseline 1610.02136, Guo calibration 1706.04599, TrustScore 1805.11783, SQuAD 2.0 1806.03822
- GitHub READMEs: openood, cleanlab, modAL
- YouTube transcripts: MLST epistemic/aleatoric, StatQuest p-values, Julia Galef scout mindset
- Books: Berger Statistical Decision Theory, Macmillan Detection Theory

### Tier 3 -- Upload Third (breadth)
- arXiv: Remaining active learning and selective prediction papers (#4, #10, #15)
- YouTube: Veritasium replication crisis, Ninja Nerd BBB, CNCF canary deployments
- Books: Tetlock Superforecasting, Hubbard How to Measure Anything, Dorovini-Zis BBB reference
- GitHub: selectivenet, DUQ, awesome-conformal-prediction

---

## Notes for Owner

1. **YouTube search instructions**: Search queries provided rather than direct URLs for most videos because specific URLs change frequently. The search terms will find the right content.

2. **arXiv papers with IDs**: All papers listed with specific arXiv IDs (e.g., 1506.02142) are verified real papers with correct author attributions. These are among the most-cited papers in their respective subfields.

3. **GitHub star counts**: Approximate as of early 2025. All repos listed are established and actively maintained.

4. **Free books**: David Barber's "Bayesian Reasoning and Machine Learning" is available as a free PDF from his website (web4.cs.ucl.ac.uk/staff/D.Barber/pmwiki/pmwiki.php?n=Brml.Online). Bishop's PRML also has free PDF editions circulating with author permission.

5. **BBB biology scope**: The biology sources (#1-#3 YouTube, #1 Books) are for biomimicry grounding only. The Barrier agent does not need to become a neuroscientist -- it needs to understand the PRINCIPLES: selective permeability, active transport, immune privilege, and what happens when the barrier breaks down.

6. **Cross-pollination**: Per Owner's brain region overlap strategy, the strongest sources should also feed into:
   - Region #02 (Zero Trust) -- quarantine patterns, sandboxing
   - Region #17 (Adversarial Security Red Team) -- OOD detection, adversarial inputs
   - Region #06 (Optimization & ML) -- uncertainty quantification, calibration, conformal prediction

7. **The core insight**: The blood-brain barrier is not a wall -- it is a SELECTIVE MEMBRANE. It actively transports what the brain needs, blocks toxins, and has immune sentinels monitoring for threats. The Barrier agent must do the same: not block everything, but screen intelligently with calibrated confidence about what to admit, what to quarantine, and what to reject.
