# Third-Party Repo Inventory — Creator's AI Workspace
> Date: 2026-03-25
> Scope: <TRADING_PROJECT>, nautilus_trader, OpenBrainLM
> Sources checked: memory files (long_term, short_term, connections), requirements.txt files,
>   strategy/*.py import statements, regime_adapters.py, fhmm_engine.py, sjm_engine.py,
>   sandbox/Research_ArM_shadowBBox_v1 imports, OpenBrainLM/research/component_map_86_repos.md

---

## Already Cloned (`<WORKSPACE>\_repos\`)

Only one repo found cloned:

| Repo | Clone Path |
|---|---|
| nautechsystems/nautilus_trader | `<WORKSPACE>\_repos\nautilus_trader\` |

---

## Full Inventory

### TIER 1 — Active / In-Use (pip-installed, imported in live code)

| Library | GitHub Repo | Used For | Already Cloned? | Priority |
|---|---|---|---|---|
| nautilus_trader | [nautechsystems/nautilus_trader](https://github.com/nautechsystems/nautilus_trader) | Backtesting engine, data pipeline, bar wranglers, live trading node — entire execution framework | YES (`_repos/nautilus_trader/`) | P1 |
| jumpmodels | [Yizhan-Oliver-Shu/jump-models](https://github.com/Yizhan-Oliver-Shu/jump-models) | SJM regime detection — THE alpha source. `.fit()`, `.predict_online()`, `DataClipperStd`, `StandardScalerPD`. Critical API corrections documented in long_term.md | NO | P1 |
| hmmlearn | [hmmlearn/hmmlearn](https://github.com/hmmlearn/hmmlearn) | CategoricalHMM + GaussianHMM backends in `regime_adapters.py` and `fhmm_engine.py`. Known multi-feature shape bug (T,D) → (T*D,) documented in memory | NO | P1 |
| dynamax | [probml/dynamax](https://github.com/probml/dynamax) | JAX-accelerated FHMM backend in `regime_adapters.py` and `fhmm_engine.py`. BROKEN with JAX 0.9.x — `most_likely_states(params, emissions)` is correct API (not `posterior_mode()`) | NO | P1 |
| polars | [pola-rs/polars](https://github.com/pola-rs/polars) | `data_loader.py` — primary parquet loader for bar data. `polars==1.38.1` pinned in requirements | NO | P2 |
| pandas | [pandas-dev/pandas](https://github.com/pandas-dev/pandas) | Used across every strategy file. `pandas==2.3.3` pinned | NO | P2 |
| numpy | [numpy/numpy](https://github.com/numpy/numpy) | Used across every strategy file. `numpy==2.4.2` pinned | NO | P2 |
| pyarrow | [apache/arrow](https://github.com/apache/arrow) | Parquet I/O with NT catalog. `pyarrow==23.0.1` pinned | NO | P2 |
| torch (PyTorch) | [pytorch/pytorch](https://github.com/pytorch/pytorch) | `model_server.py` + `rl_execution_agent.py` — behavior cloning policy network, BC execution agent | NO | P2 |
| fastapi | [tiangolo/fastapi](https://github.com/tiangolo/fastapi) | `model_server.py` — serves the BC policy network as a REST endpoint | NO | P2 |
| scipy | [scipy/scipy](https://github.com/scipy/scipy) | `markov_diagnostics.py` — `scipy.stats.chi2_contingency` for χ² independence testing on DTMC | NO | P2 |
| statsmodels | [statsmodels/statsmodels](https://github.com/statsmodels/statsmodels) | `regime_adapters.py` — `StatsmodelsMarkovAdapter` using `MarkovRegression` (econometric regime-switching) | NO | P2 |
| plotly | [plotly/plotly.py](https://github.com/plotly/plotly.py) | Dashboard visualization (`dashboard_v1_2026-03-19.py`, `plot_signals.py`). Also `cloud/requirements_cloud.txt` | NO | P2 |
| dash | [plotly/dash](https://github.com/plotly/dash) | Interactive HTML dashboard in sandbox visualization layer | NO | P2 |
| httpx | [encode/httpx](https://github.com/encode/httpx) | `live_message_bus.py` — async HTTP calls in live message bus | NO | P2 |
| google-genai | [googleapis/python-genai](https://github.com/googleapis/python-genai) | `run_treevo_llm_v1_2026-03-18.py` — `google.genai` SDK v1.66+. NOTE: `google.generativeai` is the OLD SDK. Memory correction: must use `google.genai`, NOT `google.generativeai` | NO | P2 |
| arxiv (Python client) | [lukasschwab/arxiv.py](https://github.com/lukasschwab/arxiv.py) | `arxiv_scraper_v1_2026-03-19.py` in sandbox — arXiv paper fetching for research agents | NO | P2 |
| pandas-ta | [twopirllc/pandas-ta](https://github.com/twopirllc/pandas-ta) | Listed in `nautilus_trader/requirements.txt` — technical analysis indicators for NT pipeline | NO | P2 |
| scikit-learn | [scikit-learn/scikit-learn](https://github.com/scikit-learn/scikit-learn) | Listed in `nautilus_trader/requirements.txt`. WARNING: DO NOT use sklearn preprocessors with jumpmodels — use jumpmodels' own `DataClipperStd`/`StandardScalerPD` only | NO | P2 |
| lightweight-charts | [tradingview/lightweight-charts](https://github.com/tradingview/lightweight-charts) | Listed in both requirements files — TradingView charting library for HTML dashboards | NO | P2 |
| duckdb | [duckdb/duckdb](https://github.com/duckdb/duckdb) | `duckdb==1.4.4` in requirements.txt — analytical SQL on parquet files | NO | P2 |
| msgspec | [jcrist/msgspec](https://github.com/jcrist/msgspec) | `msgspec==0.20.0` in requirements — fast serialization (used by NT internally) | NO | P2 |

---

### TIER 2 — Referenced / Phase 2+ (in requirements.txt or docs but not yet in active live code)

| Library | GitHub Repo | Used For | Already Cloned? | Priority |
|---|---|---|---|---|
| deap | [DEAP/deap](https://github.com/DEAP/deap) | In `requirements.txt` Phase 2 section + referenced in `test_phase3_eval_suite.py` as an evaluated framework for genetic algorithm TreEvo runs | NO | P3 |
| signatory | [patrick-kidger/signatory](https://github.com/patrick-kidger/signatory) | In `requirements.txt` Phase 2 section — path signature features for time series. Research use, not in active strategy code | NO | P3 |
| jax / jaxlib | [google/jax](https://github.com/google/jax) | Required by dynamax. BROKEN at 0.9.x with dynamax — version pinning needed | NO | P3 |
| quantstats | [ranaroussi/quantstats](https://github.com/ranaroussi/quantstats) | In `cloud/requirements_cloud.txt` — performance reporting (Sharpe, drawdown, etc.) for cloud run results | NO | P3 |
| hiplot | [facebookresearch/hiplot](https://github.com/facebookresearch/hiplot) | In `cloud/requirements_cloud.txt` — parallel coordinates visualization for hyperparameter sweep results | NO | P3 |
| plotly-resampler | [predict-idlab/plotly-resampler](https://github.com/predict-idlab/plotly-resampler) | In `cloud/requirements_cloud.txt` — downsampling for large time series in plotly | NO | P3 |
| python-dotenv | [theskumar/python-dotenv](https://github.com/theskumar/python-dotenv) | In `requirements.txt` Phase 2 section — `.env` file loading for API keys | NO | P3 |
| portion | [AlexandreDecan/portion](https://github.com/AlexandreDecan/portion) | In both requirements files — interval arithmetic (used by NT internally) | NO | P3 |

---

### TIER 3 — OpenBrainLM Phase 2+ Vision (evaluated, not installed)

These appear in `research/component_map_86_repos.md` (86 repos evaluated). None are installed or in active use. All are Phase 2+ candidates. Source: long_term.md correction 2026-03-23 — "the 86-repo component map references the FULL 8-layer vision. Current active use is Trinity + memory consolidation + brainstem. The rest is Phase 2+ dependencies."

| Library | GitHub Repo | Proposed Use | Already Cloned? | Priority |
|---|---|---|---|---|
| HippoRAG | [OSU-NLP-Group/HippoRAG](https://github.com/OSU-NLP-Group/HippoRAG) | Hippocampal memory indexing (NeurIPS 2024, ICML 2025). Highest-priority Phase 2 memory component | NO | P3 |
| semantic-router | [aurelio-labs/semantic-router](https://github.com/aurelio-labs/semantic-router) | L4 action selection routing via embedding cosine similarity (MIT, 3.3k stars) | NO | P3 |
| LangGraph | [langchain-ai/langgraph](https://github.com/langchain-ai/langgraph) | Orchestration backbone with cycles for dialectic loops (MIT, 26.2k stars) | NO | P3 |
| pymdp | [infer-actively/pymdp](https://github.com/infer-actively/pymdp) | Active inference / Expected Free Energy for action selection | NO | P3 |
| GraphRAG | [microsoft/graphrag](https://github.com/microsoft/graphrag) | Entity KG extraction, corpus-wide sensemaking queries (MIT, 30.9k stars) | NO | P3 |
| Kotaemon | [Cinnamon/kotaemon](https://github.com/Cinnamon/kotaemon) | Self-hosted NotebookLM alternative with citation grounding (Apache-2.0, 25.2k stars) | NO | P3 |
| NeMo Guardrails | [NVIDIA/NeMo-Guardrails](https://github.com/NVIDIA/NeMo-Guardrails) | Output rails / anti-hallucination enforcement (Apache-2.0) | NO | P3 |
| LightRAG | [HKUDS/LightRAG](https://github.com/HKUDS/LightRAG) | Dual-level graph RAG, lightweight local deployment (MIT, 29k stars) | NO | P3 |

---

## Summary: What Needs Cloning

### Clone NOW (P1 — we query source code, need grep/read access)

| Repo | Why | Clone Command |
|---|---|---|
| `nautechsystems/nautilus_trader` | Already cloned — verify it's up to date with v1.223.0 | — already at `_repos/nautilus_trader/` |
| `Yizhan-Oliver-Shu/jump-models` | THE alpha source. API is unusual (no `.fit_predict()`, own preprocessors). Memory has 3 documented API corrections. Need source to verify during rebuild | `git clone https://github.com/Yizhan-Oliver-Shu/jump-models.git` |
| `hmmlearn/hmmlearn` | Known multi-feature shape bug documented. Need source to verify CategoricalHMM behavior with (T,D) inputs | `git clone https://github.com/hmmlearn/hmmlearn.git` |
| `probml/dynamax` | BROKEN with JAX 0.9.x. Need source to understand version requirements and `most_likely_states` API | `git clone https://github.com/probml/dynamax.git` |

### Clone SOON (P2 — useful source reference for active pip dependencies)

Priority order based on how often we'll need to read the source:

1. `pola-rs/polars` — active data loader, Polars API changes fast
2. `twopirllc/pandas-ta` — NT pipeline dependency, need to verify indicator implementations
3. `pytorch/pytorch` — BC policy network, training loop reference
4. `ranaroussi/quantstats` — performance reporting, want to understand Sharpe/drawdown calculations
5. `statsmodels/statsmodels` — MarkovRegression API reference

Everything else in Tier 1/2 is standard enough that PyPI + official docs suffice.

### Do NOT Clone Yet (P3)

All OpenBrainLM Phase 2+ vision repos. Hold until Phase 2 work begins. Creator directive (2026-03-23): "ALL biology, biomimicry, 8-layer Python code is TABLED. Do NOT touch openbrainlm/*.py until current operational work is stable."

---

## Notes / Corrections

1. **`google-genai` vs `google-generativeai`**: The live trading bot sandbox uses `from google.genai import types as genai_types` (new SDK). The `utils/gemini_client.py` still uses `google.generativeai` (old SDK). Memory correction confirmed: use `google.genai` v1.66+, `gemini-2.5-flash` model. The old SDK reference in gemini_client.py should be flagged for update during rebuild.

2. **dynamax JAX compatibility**: Memory documents that dynamax is BROKEN with JAX 0.9.x. Source clone is needed to identify which JAX version dynamax supports. Do not attempt to use dynamax until version pinning is resolved.

3. **sklearn preprocessors + jumpmodels**: `scikit-learn` appears in `nautilus_trader/requirements.txt` but must NOT be used for jumpmodels preprocessing. The `SparseJumpAdapter` incident (documented in long_term.md) was caused by using sklearn instead of jumpmodels' own `DataClipperStd(mul=3.)` → `StandardScalerPD()`. This is a P1 correctness issue.

4. **`_repos/` is nearly empty**: Only `nautilus_trader/` is present. Every other dependency is pip-installed only. No source-level grep/read access to jumpmodels, hmmlearn, or dynamax currently exists.
