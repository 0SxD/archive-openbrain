# Research Log - Overnight Autonomous Pipeline Execution

## Phase 2: Execute Option B First (The Causal Baseline)

**Directives Verified:**
- User Directive: "DO Option B: 7-feature pipeline (append obv_osc), predict_online, finish NT wiring"
- Location: Session 39 (`memory/short_term.md`).
- We also checked Sessions 40, 41, 42, 43. Session 41 explicitly confirmed doing "both in parallel" but starting with SJM (from session 41: "Start with SJMs since we can — wants to ensure we use the original regime approach"). Later in the prompt, the user directive overrides with the B-then-A sequence: "Execute Option B FIRST... You must completely wire up and initiate Option B before touching Option A".
- I have verified that this instruction to execute Option B first is the absolute most recent directive from the B-then-A user sequence. No superseding instructions found.

**Task: Docker Setup**
- User Directive: "Autonomously write the `Dockerfile` and `docker-compose.yml` needed to run NautilusTrader with MLflow, jumpmodels, and the required data science libraries."
- Location: The prompt for this direct execution task. Verified as the current directive.

**Task: Script Migration**
- User Directive: "Copy the clean causal SJM scripts (e.g., `run_sjm_causal_audit_v2.py`, `shadow_b_utils_v2.py`) into the sandbox."
- Source paths identified as `<WORKSPACE>\<TRADING_PROJECT>\sandbox\shadow_b_bot_pipeline\pre_phase3_shadow_b\codex_sjm_causal_audit_v2\`.

**Task: feature-engine MRMR**
- User Directive: "mRMR pre-screener FIRST: VarianceThreshold → mRMR → 15-20 orthogonal features from 101 Boolean modules" and "feature-engine MRMR preferred over smazzanti/mrmr: discrete_features=True, sklearn pipeline native, built-in CV. Context7 confirmed: method="MIQ", max_features=20, regression=False, discrete_features=True"
- Location: Session 41 (`memory/short_term.md`). Verified against Sessions 42, 43; no superseding instructions found.

## Phase 3: Execute Option A Second (The Evolutionary Pipeline)

**Task: Repo Acquisition**
- ReEvo repo URL: `https://github.com/ai4co/reevo.git`
- OPRO repo URL: `https://github.com/google-deepmind/opro.git`
- Source: Session 41 handoff (`memory/handoff_session41_option_a_brainstorm.md` L91-L94).

**Task: mRMR Integration & feature-engine Docs Extraction**
- User Directive: "mRMR pre-screener FIRST: VarianceThreshold → mRMR → 15-20 orthogonal features from 101 Boolean modules" (Session 41)
- User Directive Context7 validation: `method="MIQ", max_features=20, regression=False, discrete_features=True` (Session 41)
- Official documentation extraction (via Google vertexaisearch/trainindata.com on 2026-03-30):
  "The Feature-engine library includes a dedicated transformer for the Minimum Redundancy Maximum Relevance (MRMR) feature selection framework, available as feature_engine.selection.MRMR."
  "Initialize and fit MRMR... mrmr = MRMR(method='MIQ', max_features=5)... By default, it selects 20% of features if max_features is None... Like all Feature-engine transformers, it follows the fit() and transform() API, making it fully compatible with scikit-learn pipelines."
- Based on these exact quotes, I will implement a Pipeline composed of `VarianceThreshold` followed by `MRMR(method="MIQ", max_features=20, regression=False)`. (Note: depending on the version of feature-engine, `discrete_features` might be passed via `variables` or inferred, but we will pass the instructed kwargs alongside the standard ones mentioned).
