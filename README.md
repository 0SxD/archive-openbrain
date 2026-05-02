> Status: R&D / scratchpad. Part of Sage / 0SxD's prompt-engineering research portfolio. Content may move, change, or be withdrawn. See LICENSE for terms.

# OctoBrian -> PUBLIC VERSION (coming...) "OctoBrian(?)_v1.01"

**A brain harness for large language models.**

LLMs have no memory. No discipline. No self-correction. OpenBrainLM gives them a brain — a harness that adds long-term memory, reasoning discipline, and self-learning to any LLM.

Built from real neuroscience. Not metaphors — mechanisms.

---

## What It Does

OctoBrian is a **brain-shaped harness** that wraps around any LLM and gives it:

### 1. A Brainstem (Hooks + Rules + Inhibition)
Every action passes through a brainstem — hooks that fire before and after tool use, rules that enforce discipline, inhibition-by-default (basal ganglia model: actions are *released*, not activated). The harness prevents the LLM from acting without thinking.

### 2. Long-Term Memory (Consolidation + Schema + Quarantine)
LLMs forget everything between sessions. OpenBrainLM gives them a hippocampal memory system:
- **Short-term memory** — session activity ledger
- **Long-term memory** — verified findings with schema: statement, confidence, source, status, last verified date
- **Quarantine layer** — new information is quarantined until verified. Nothing enters long-term memory unverified.
- **Consolidation cycle** — like biological sleep, the brain consolidates short-term into long-term at breakpoints

### 3. Trinity Dialectic (Scientific Reasoning Engine)
Inspired by Aristotle's Nicomachean Ethics. Three voices evaluate every significant decision:
- **Ethos** — the evidence corridor. Holds the verified evidence base AND the evaluation criteria. The shared ground truth both sides must work from.
- **Pathos** — the mission. Argues for the goal, the creative direction, the "why are we doing this." Weighted and configurable.
- **Logos** — the evaluation. Assesses whether the mission passes the criteria. Applies the evidence to judge the path forward. Weighted and configurable.

This isn't a pipeline — it's a dialectic. Pathos and Logos can be weighted (yes/no, scored, threshold-gated). Ethos holds the corridor they both operate within. The productive mechanism is the structured disagreement itself. Highly customizable — different domains, different weights, different evaluation criteria.

### 4. Self-Learning Loop (Research Corridors + Verification Gates)
The brain learns autonomously within strict boundaries:
- **Research corridors** — scoped investigation, not unlimited browsing
- **Verification gates** — claims must be verified against primary sources before promotion
- **The loop** — research → verify → apply → audit → refine. Every step builds on the last.

### 5. 8-Layer Biomimetic Architecture (The Full Vision)
Where this is going — a full cognitive architecture derived from real biological mechanisms:

| Layer | Name | Biology |
|---|---|---|
| L1 | Active Sensing | Octopus + Rat Whiskers |
| L2 | Ganglion | Octopus Arms |
| L3 | Stigmergy + Swarm | Insect Hive |
| L4 | Action Selection | Basal Ganglia + Thalamus |
| L5 | Memory (Hippocampus) | Hippocampus |
| L6 | Relevance Detection | Amygdala + Quorum |
| L7 | Chromatophore | Octopus Skin Display |
| L8 | Pathos | Human Default Mode Network |

Cross-cutting: Prediction Error, Hebbian Plasticity (STDP), Interoception, Cerebellum Timing.

The thesis: take what is in nature — fruit fly neural circuits, octopus arm autonomy, hippocampal consolidation, basal ganglia inhibition — and build the digital equivalent. Not artificial intelligence pretending to think. A harness that actually structures thought.

**The biomimetic memory consolidation layer** (short-term → long-term with sleep cycles, Hebbian strengthening, and immune-system verification) is the next major milestone. See the [whitepaper](WHITEPAPER.md) for the full roadmap.

---

## The Thesis

> If you give an LLM a research corridor, turn it into a scientist that can go back and forth and speak to itself, give it a strict harness, don't let it proceed until it meets criteria — criteria gates that it has to meet — and then give it very specific tools to work with... then it will really, really help.

OpenBrainLM is that harness.

---

## LLM-Agnostic

OpenBrainLM works with any LLM backend. The harness is the brain — the LLM is the raw intelligence being harnessed.

- **Claude Code** — fully implemented (hooks, rules, brainstem, memory)
- **Gemini** — adapter planned
- **Codex / other** — adapter planned
- **Pluggable bridge** — `openbrainlm/bridge.py` is the spinal cord. Swap backends without changing the brain.

---

## Quick Start

```bash
# Clone
git clone https://github.com/0SxD/OpenBrainLM.git
cd OpenBrainLM

# Install (editable)
pip install -e .

# Run CLI
python -m openbrainlm

# Run tests
pytest tests/ -v
```

---

## Key Documents

| Document | What It Covers |
|---|---|
| [`WHAT_IS_OPENBRAIN.md`](WHAT_IS_OPENBRAIN.md) | Philosophy — why this exists |
| [`WHITEPAPER.md`](WHITEPAPER.md) | Technical whitepaper — the full architecture |
| [`ARCHITECTURE.md`](ARCHITECTURE.md) | Technical spec + system diagrams |
| [`OPERATIONAL_LAYERS.md`](OPERATIONAL_LAYERS.md) | 8-layer biology spec |
| [`OPEN_BRAIN.md`](OPEN_BRAIN.md) | Core principles (append-only) |

**Concept Papers:**
1. [The Dialectic Loop](docs/concept_papers/01_THE_DIALECTIC_LOOP.md) — adversarial debate as decision mechanism
2. [The Trinity & Memory](docs/concept_papers/02_THE_TRINITY_AND_MEMORY.md) — recursive self-checking + consolidation
3. [The Self-Learning Brain](docs/concept_papers/03_THE_SELF_LEARNING_BRAIN.md) — evolution, fitness, knowledge promotion
4. [The 8-Layer Brain](docs/concept_papers/04_THE_8_LAYER_BRAIN.md) — full biomimetic architecture

---

## Design Principles

1. **Harness first.** The brain is a harness — hooks, rules, inhibition, memory. Without the harness, the LLM is raw potential with no structure.
2. **Biomimicry, not metaphor.** Every component derives from a real biological mechanism. Nothing invented. Everything assembled from nature.
3. **Inhibition-by-default.** Default state = all actions suppressed. Actions are *released*, not activated. (Basal ganglia model.)
4. **Trinity is a dialectic, not a pipeline.** Ethos holds the evidence corridor. Pathos argues the mission. Logos evaluates against criteria. The structured disagreement is the productive mechanism.
5. **Quarantine before promotion.** New information enters quarantine. Verified by immune challenge. Only then promoted to long-term memory.
6. **Append-only knowledge.** Never delete from brain memory. Overflow to long-term storage.

---

## Status

**Alpha** — brainstem hooks deployed, memory consolidation working, Trinity dialectic engine built, 135 tests passing. The harness works. The 8-layer biomimetic architecture is the roadmap.

This is research becoming infrastructure. Use it, learn from it, build on it.

---

## Origin

This project started as a question: *can you derive a functional brain architecture for LLMs from real biology — not metaphors, but actual mechanisms?*

The answer turned out to be yes. The biological patterns are clear. The harness works. The memory consolidation works. The dialectic reasoning works.

What's here is a process — take what is in nature, build the digital equivalent, teach it, give it human traits (Aristotle's Nicomachean Ethics). It's not how most people are approaching AI cognition. But it works.

---

## Acknowledgments

Inspired by [OB1 (Open Brain)](https://github.com/NateBJones-Projects/OB1) by Nate B. Jones — the idea that AI needs a real brain, not just a context window. OpenBrainLM is an independent project with different architecture and purpose.

Built with insights from the research community: SPAUN 2.0 (Eliasmith), free energy principle (Friston), Drosophila connectome (Scheffer et al.), octopus arm autonomy (Sumbre et al.), and the Anthropic agent patterns.

---

## Contributing

This is early. If the concept resonates, open an issue or fork it. The vision is bigger than one person — the community decides where this goes.

---

## License

[MIT](LICENSE)
