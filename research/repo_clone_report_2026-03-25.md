# Repo Clone Report — 2026-03-25
> Fresh GitHub clones into `<WORKSPACE>\_repos\trading\`
> All shallow clones (`--depth 1`) for read-only reference

## Clone Results

| Repo | Source URL | Clone Path | Status | Found In |
|---|---|---|---|---|
| nautilus_trader | https://github.com/nautechsystems/nautilus_trader | `_repos/trading/nautilus_trader/` | MOVED (was in `_repos/`) | P1 — execution framework |
| jump-models | https://github.com/Yizhan-Oliver-Shu/jump-models | `_repos/trading/jump-models/` | CLONED | requirements.txt + strategy/sjm_engine.py |
| hmmlearn | https://github.com/hmmlearn/hmmlearn | `_repos/trading/hmmlearn/` | CLONED | requirements.txt Phase 2 |
| dynamax | https://github.com/probml/dynamax | `_repos/trading/dynamax/` | CLONED | requirements.txt + strategy/fhmm_engine.py |
| factorial_hmm | https://github.com/regevs/factorial_hmm | `_repos/trading/factorial_hmm/` | CLONED | strategy/regime_adapters.py (TODO adapter, not pip-installable) |
| alphaevolve | https://github.com/google-deepmind/alphaevolve | — | FAILED | sandbox/03_alphaevolve_arm/. Repo not found — may be private, different org, or different name. |

## Key Findings from Scan

1. **mctx is NOT a DeepMind repo clone** — `mctx_module_registry` in trading bot is Creator's own local registry (MCTS pre-selection atomic sweeps). No external clone needed.

2. **alphaevolve URL is wrong** — `google-deepmind/alphaevolve` returns 404. The sandbox adapter references `git+https://github.com/google-deepmind/alphaevolve.git` but this repo doesn't exist publicly. Needs investigation — may be under a different name or still private.

3. **component_map_86_repos.md** — 86 repos across 14 categories. All are OpenBrainLM Phase 2+ candidates, NOT active trading deps. No clones needed from that file for trading work.

4. **All trading repos now in `_repos/trading/`** — organized per Creator's request.

## Comparison Notes (for NT framework evaluation)

| Repo | Why We Need Source Access |
|---|---|
| jump-models | THE alpha source for SJM regime detection. Unusual API (.fit(), .predict_online(), own preprocessors DataClipperStd/StandardScalerPD). 3 documented API corrections in long_term memory. |
| hmmlearn | CategoricalHMM + GaussianHMM backends. Known multi-feature shape bug (T,D) → (T*D,). Need source to verify behavior. |
| dynamax | JAX-accelerated FHMM backend. BROKEN with JAX 0.9.x. `most_likely_states(params, emissions)` is correct API (not `posterior_mode()`). Need source for version pinning. |
| factorial_hmm | Referenced in regime_adapters.py as TODO adapter. Not pip-installable — source clone is the only way to evaluate. |
| nautilus_trader | Execution framework. Source needed for Grep/Read of internals (wranglers.pyx, parquet.py, etc.) |
