# What Is OpenBrainLM

An open-source LM plug-in brain. Built from biomimicry and emergent Nicomachean ethics-based, sub-dialectic conflict resolution of the self -> producing objectively defined consciousness.

---

## Two Pillars

**Pillar 1 — Biological Mimicry.** Three organisms, each chosen for what the others lack:

- **Octopus**: Distributed processing. 350 million neurons in the arms, not the brain. Each arm is an autonomous ganglion. The central brain sets goals; the arms figure out how. Self-modifies by editing its own RNA in response to environment.
- **Insect Colony**: Collective intelligence. Stigmergy (communicate through environment, not messages), quorum sensing (consensus before commitment), emergence (complex behavior from simple local rules). The emergent behavior IS the invention.
- **Human Brain**: Higher cognition. Hippocampus (memory consolidation during sleep), amygdala (fast threat detection), Default Mode Network (creativity during rest), thalamus (intelligent routing).

No single system has all capabilities. Combined, each covers the weaknesses of the other two.

**Pillar 2 — Trinity Dialectic (Nicomachean Ethics).**

Logos (logic) fights Pathos (creativity). Ethos (ethics) arbitrates. The fight IS the thinking.

- **Logos** takes the shortest proven path. Pure logic. Lowest bar to completion.
- **Pathos** takes the longest, hardest path to get exactly what it wants. Will stop at nothing except self-destruction. IS the dreaming — desires unadulterated and unfiltered.
- **Ethos** holds the golden mean (Aristotle's phronesis). Only when both are in accordance is action allowed.

The Trinity is recursive: each has its OWN internal Ethos/Logos/Pathos (9 sub-evaluators total). This prevents blind spots.

---

## Architecture

8 operational layers + Trinity dialectic + 4 cross-cutting mechanisms. Every layer maps directly to a biological mechanism. Nothing invented. Everything assembled.

8 core cognitive agents (bare minimum for a brain to be a brain), named for the biological function they ARE: hippocampus, explorer, verifier, immune, prefrontal, morphogen, consolidator, homeostasis. 10 more will be derived from the symbiosis of neurology and Nicomachean Ethics taxonomy.

8 curated brain regions ship as local knowledge stores. The brain self-evolves from this starting configuration — like an octopus rewriting its RNA.

LM-agnostic. Pluggable backends. Zero vendor lock-in. Pure Python stdlib core.

See `WHITEPAPER.md` for the full technical specification.
See `ARCHITECTURE.md` for code structure and system diagrams.

---

## Trinity of Trinities (9 Sub-Evaluators)

Each top-level voice (Ethos, Logos, Pathos) has its OWN internal Ethos, Logos, and Pathos. 3 × 3 = 9. Before any top-level voice can speak, its three internal voices must first reach accordance.

```
ETHOS asks itself:                LOGOS asks itself:                PATHOS asks itself:
  E-E: Am I consistent with       L-E: Is my reasoning aligned      P-E: Is my impulse consistent
       my own character?                with our character?                with our values?
  E-L: Can I reason about WHY      L-L: Is my logic internally       P-L: Can I articulate WHY
       this is virtuous?                 consistent?                       this idea matters?
  E-P: Does this FEEL right?       L-P: Does my reasoning account    P-P: Is this genuine
                                        for intuition?                     inspiration or noise?
```

On existential threat, all 9 fire simultaneously — unanimous BLOCK. No single sub-evaluator can be bypassed.

**Why recursive:** A single-layer Trinity has blind spots. Logos can be internally inconsistent without noticing (Logos-Logos catches this). Pathos can mistake noise for inspiration (Pathos-Pathos catches this). Ethos can enforce virtue it can't justify (Ethos-Logos catches this). The recursion is the immune system of the mind itself.

## Weighting Gates (How Arbitration Works)

Ethos does not flip a coin. It weighs.

Each side's **strength** = confidence × (1 + evidence_count × 0.1). Confidence without evidence is weak. Evidence without confidence is inert. Both together compound.

```
Logos strength  = logos_confidence × (1 + evidence_count × 0.1)
Pathos strength = pathos_confidence × (1 + evidence_count × 0.1)

If |logos - pathos| < 0.15 → CONSENSUS (both valid, virtue between extremes)
If logos > pathos          → LOGOS WINS (but Pathos's concern noted for next round)
If pathos > logos          → PATHOS WINS (but Logos's caution noted)
```

**Critical health check:** If EITHER side drops below 0.1 strength, Ethos refuses to rule and flags an interoception alarm:
- Logos silent → rigidity risk ("stopped learning, haven't stopped living")
- Pathos silent → stagnation risk ("pure logic without creativity is a dead end")

The fight must continue. A brain where only one side speaks is a brain that has stopped thinking.

After Ethos rules, the winning position passes through all 9 sub-evaluators. Any sub-evaluator can BLOCK the decision. Only when all 9 pass does the Trinity reach VERIFIED — the only state where action is permitted.

```
DIALECTIC (Logos ↔ Pathos fight)
     ↓
ETHOS RULES (weighting gate)
     ↓
9 SUB-EVALUATORS VALIDATE (any can block)
     ↓
VERIFIED → action permitted
```

If the dialectic cannot resolve within 10 rounds → DEADLOCKED → escalate to owner. The brain does not guess.

---

## The Point

Nothing in it is new. Everything in it works.

You never build something new. You take what works and make it better. That's what evolution does. That's what OpenBrainLM does. That's what invention actually is — not creating from nothing, but seeing the new whole that was always hiding in existing parts.
