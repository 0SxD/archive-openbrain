# User Library Notes — Trading Bot 2026 Inventory
**Compiled:** 2026-03-24
**Agent:** Claude Sonnet 4.6 (research extraction pass)
**Sources read:**
- `module_atom_registry_v2_2026-03-15.md` (v2, 101 modules)
- `module_atom_registry.md` (v1, identical content — retained for history)
- `quant_pipeline_architecture_v5.3_2026-03-13.md` (active structural reference)
- `shadow_b_pipeline_b_project_report_2026-03-12.md` (full project status through lockdown)
- `quant_pipeline_architecture_v5.md` (v5.1, superseded by v5.3 but adds lineage context)
- `quant_pipeline_architecture_v4.md` (v4.0, DTMC architecture design)
- `codex techincal whitepaper for marcov chain build.md` (Phase 2 DTMC Markov engine plan)
- `Notebook_Audit_Austin_Gate_Shadow_B_Bot_pipe/SHADOW_B_PIPELINE_AUDIT_V2_COMPLETE.md`
- `strategy/indicator_hub.py` (live implementation — read directly)
- PDFs: **UNREADABLE** — `pdftoppm` not available in this environment. 5 PDFs not extracted:
  - `3.10.2026_Strategy_Module_Population_Draft_comments.docx.pdf`
  - `Additional Indicators for GA_Gene_Boolean_Run.pdf`
  - `DTMC_Phase2_Alignment_and_Rollout_Packet_2026-03-03.pdf`
  - `3.8.26_Pre_Phase3_PipelineA_&_ShadowB_Modular Evolution...pdf`
  - `Binance Data Pipeline Standardizatio_gemeni_research.pdf`

**IMPORTANT NOTE ON PDFs:** These 5 PDFs were not extractable. The PDF titled "Additional Indicators for GA_Gene_Boolean_Run.pdf" is especially likely to contain indicators not covered here. **Re-read these with a PDF-capable environment before treating this inventory as complete.**

---

## A. Indicators Mentioned

### A.1 Core Feature Set (SJM Regime Engine — 7 continuous features)

These are the `SHADOW_B_FEATURES` tensor fed to the SparseJumpModel. `relative_volume` was later excluded (see note).

| Feature Name | Description | Library/Source | Custom? |
|---|---|---|---|
| `price_fib_extend` | Price position relative to Fib channel: `(close - fib6_dn) / (fib6_up - fib6_dn)` | `indicator_hub.py` (custom formula) | **CUSTOM** |
| `bb_fib_extend` | BB basis position within Fib channel: `(bb_basis - fib6_dn) / (fib6_up - fib6_dn)` | `indicator_hub.py` (custom formula) | **CUSTOM** |
| `price_bb_extend` | Price position within BB channel: `(close - bb_lower) / (bb_upper - bb_lower)` | `indicator_hub.py` (custom formula) | **CUSTOM** |
| `chikou_fib_distance` | Chikou span distance from Fib6 bands (signed, uses 26-bar lag) | `indicator_hub.py` (custom formula) | **CUSTOM** |
| `price_slope_velocity` | 5-bar price rate of change: `(close - close[-5]) / (close[-5] * 5)` | `indicator_hub.py` (custom formula) | **CUSTOM** |
| `relative_volume` | `volume / volume_sma20` — **excluded from SJM tensor** (L1 weight < 0.02 across all configs), retained for internal module computations only | `indicator_hub.py` | **CUSTOM** |
| `obv` | On-Balance Volume (cumulative signed volume) | `indicator_hub.py` (standard formula, no external library) | Standard, custom impl |

### A.2 Primary Indicator Systems (Base Computations)

| Indicator | Parameters | Library/Source | Custom? |
|---|---|---|---|
| Fibonacci Bands (midline) | EMA period=100 | `indicators/fibonacci_bands.py` | **CUSTOM** — TradingView Pine Script translation |
| Fibonacci Bands (fib1–fib6, up/down) | 6 levels: fib1–fib6 | `indicators/fibonacci_bands.py` | **CUSTOM** |
| Bollinger Bands (basis, upper, lower) | period=20, mult=2.0 | `fib_chikou_strategy.py:compute_bollinger()` | Standard formula, custom impl |
| Bollinger Bandwidth | `bb_upper - bb_lower` | `indicator_hub.py` | Standard derived |
| BB Width SMA20 | 20-bar rolling mean of bandwidth | `indicator_hub.py` | Standard derived |
| Ichimoku Conversion Line (Tenkan-sen) | period=9 | `fib_chikou_strategy.py:compute_ichimoku()` | Standard formula, custom impl |
| Ichimoku Base Line (Kijun-sen) | period=26 | same | Standard formula, custom impl |
| Ichimoku Leading Span A (Senkou A) | (conv+base)/2, plotted +26 | same | Standard formula, custom impl |
| Ichimoku Leading Span B (Senkou B) | period=52, plotted +26 | same | Standard formula, custom impl |
| Ichimoku Cloud (decision-aligned) | Shifted back 26 bars for causal use | `indicator_hub.py` | **CUSTOM** — decision-period alignment logic |
| Chikou Span (display only) | `close` shifted for display | `indicator_hub.py` | Standard |
| OBV (On-Balance Volume) | Cumulative signed volume | `indicator_hub.py` | Standard formula, custom impl |
| MFI / Money Flow RSI | period=14 | `indicator_hub.py` | Standard formula, custom impl |
| MFI Slope | `diff(5)` of MFI | `indicator_hub.py` | **CUSTOM** derived |
| Relative Volume | `volume / volume_sma20` | `indicator_hub.py` | Standard derived |

### A.3 Liquidity Bands (Group 6 — LMA + VWSD)

**FLAG: CUSTOM INDICATOR FAMILY**

| Feature | Description | Source | Custom? |
|---|---|---|---|
| `lma_20` | Liquidity-Weighted Mean Average: price weighted by `volume × true_range` over 20 bars | `indicator_hub.py` | **CUSTOM** |
| `vwsd_20` | Liquidity-Weighted Standard Deviation (VWSD) | `indicator_hub.py` | **CUSTOM** |
| `liq_band_upper` | `lma_20 + 2.0 × vwsd_20` | `indicator_hub.py` | **CUSTOM** |
| `liq_band_lower` | `lma_20 - 2.0 × vwsd_20` | `indicator_hub.py` | **CUSTOM** |
| `liq_bandwidth` | `(upper - lower) / lma_20 * 100` | `indicator_hub.py` | **CUSTOM** |

Design rationale (from source): weighting = `volume × true_range` (dollar-flow intensity proxy). High-volume wide-range bars get full weight; absorption churn bars (high vol, tight range) are downweighted relative to plain VWAP.

### A.4 Angular Slope Indicators (Group 8)

**FLAG: CUSTOM INDICATOR FAMILY**

Formula: `angular_slope = arctan(raw_slope × k) / (π/2)`, bounded [-1, +1].
`raw_slope = (feature[i] - feature[i-5]) / 5` (5-bar rate of change of the feature itself).

| Feature | k value | Description | Custom? |
|---|---|---|---|
| Angular slope of `price_fib_extend` | 50 | Momentum of price-in-fib indicator | **CUSTOM** |
| Angular slope of `price_bb_extend` | 50 | Momentum of price-in-BB indicator | **CUSTOM** |
| Angular slope of `chikou_fib_distance` | 1000 | Momentum of chikou distance (small values, large k) | **CUSTOM** |
| Angular slope of `bb_fib_extend` | 50 | Momentum of BB-in-fib indicator | **CUSTOM** |

Key design decision: k=1000 for chikou because chikou values are ~40x smaller than other features; k normalizes to comparable angular range.

### A.5 Advanced Quant Proxy Indicators (Group 10)

| Indicator | Description | Library | Custom? |
|---|---|---|---|
| Hurst VR Proxy | Variance ratio > 1.0 = trending regime | Custom proxy, no external lib cited | **CUSTOM PROXY** |
| Kang/Kalman Volume Shock | Volume shock detector based on Kang/Kalman methodology | No external lib cited | **CUSTOM PROXY** — flag for verification |

### A.6 Derived Distance / Conviction Features

| Feature | Description | Custom? |
|---|---|---|
| `chikou_fib_distance_up` | Signed distance: close vs fib6_up[-26] | **CUSTOM** |
| `chikou_fib_distance_down` | Signed distance: close vs fib6_dn[-26] | **CUSTOM** |
| `price_slope_velocity_3` | 3-bar price slope | **CUSTOM** |
| `price_slope_velocity_10` | 10-bar price slope | **CUSTOM** |
| Distance beyond bands: weak (>10% BW beyond fib6) | Extension threshold gate | **CUSTOM** |
| Distance beyond bands: moderate (>30% BW) | Extension threshold gate | **CUSTOM** |
| Distance beyond bands: strong (>60% BW) | Extension threshold gate | **CUSTOM** |
| BB distance moderate (>30% BW beyond BB) | Extension threshold gate | **CUSTOM** |
| Conviction: dist>20% AND slope>0.20 | Strong aligned momentum composite | **CUSTOM** |
| Weakening: dist>20% BUT slope reversing | Momentum divergence composite | **CUSTOM** |
| Triple conviction: dist AND slope AND accel all aligned | Full conviction composite | **CUSTOM** |

### A.7 Volume / Microstructure Indicators (Group 2)

| Indicator | Description | Library | Custom? |
|---|---|---|---|
| OBV SMA cross | OBV crosses 20-bar SMA of OBV | Custom impl | Standard concept |
| CVD (Cumulative Volume Delta) | Bar delta crosses midline | Custom impl — no external lib cited | **CUSTOM PROXY** |
| VWAP (rolling 20-bar) | Price crosses 20-bar rolling VWAP | Custom impl | Standard concept, rolling variant |
| OFI (Order Flow Imbalance) | Bar proxy SMA cross | Custom impl — no external lib cited | **CUSTOM PROXY** — flag for verification |
| Volume surge | >2x avg in direction of candle body | Custom impl | **CUSTOM** logic |
| Amihud liquidity gate | Amihud ratio + fib6 breakout gate | Custom impl | Standard Amihud, custom gate |

### A.8 Placeholder / Scaffolded (Not Yet Implemented)

| Feature | Status |
|---|---|
| `buy_vol` | Hardcoded 0.0 — Phase 4 placeholder |
| `sell_vol` | Hardcoded 0.0 — Phase 4 placeholder |
| `imbalance` | Hardcoded 0.0 — Phase 4 placeholder |
| `spread_bps` | Hardcoded 0.0 — Phase 4 placeholder |

---

## B. Modules / Components Built

### B.1 Module Atom Registry (101 Boolean Signal Modules)

All 101 modules return `(long_entry_bool, short_entry_bool)` numpy bool arrays. Source: `scripts/mctx_module_registry.py`.

| Group Code | Group Name | Count | Key Signals | Status |
|---|---|---:|---|---|
| s1_* | Step 1 — Chikou x Fib6 buffer sweep | 5 | chikou vs fib6 with 5 buffer sizes (0–0.15%) | Built |
| s2_* | Step 2 — Fib lookback sweep | 20 | price crosses fib_up/dn, lookback 10–200 | Built |
| s3_* | Step 3 — Fib slope/expansion gate | 12 | band width threshold × slope ratio, 4×3 grid | Built |
| s4_* | Step 4 — Anticipatory short entries | 3 | slope contraction, band approach, midline cross | Built |
| M1.1 | G1 — Fib channel position | 8 | OTE zone, golden ratio, fib1/3/4/6 | Built |
| M1.2 | Pure Bollinger Band atoms | 3 | band cross, extend>1.0, squeeze release | Built |
| M1.3 | G3 — Ichimoku Cloud atoms | 8 | TK cross, cloud breakout, chikou confirm, full confluence | Built (added 2026-03-15) |
| M1.4 | G4 — Relational BB × Fib | 5 | BB basis vs fib6, double breakout, midpoint cross | Built |
| M1.5 | Phase 3b — Multi-system confluence | 8 | Fib+BB+Vol, chikou confirm, OBV, triple confluence | Built |
| M2.1 | G2 — Volume / microstructure | 7 | OBV, CVD, VWAP, OFI, vol surge, Amihud, VWAP+fib | Built |
| M6.1 | G6 — Liquidity Band atoms | 4 | LMA breakout, expansion, squeeze, cross | Built |
| M7.1 | G7 — Momentum oscillators | 1 | MFI 70/30 cross | Built |
| M8.1 | G8 — Angular slope of distance features | 4 | slopes of price_fib, price_bb, chikou, bb_fib | Built (added 2026-03-13) |
| M8.2 | G8 — Slope interaction atoms | 2 | dual slope confirmation | Built (added 2026-03-13) |
| M8.3 | G8 — Acceleration atoms | 2 | 2nd derivative of angular slope | Built (added 2026-03-15) |
| M9.1 | G9 — Distance Beyond Bands | 4 | mild/moderate/strong extension beyond fib6 + BB | Built (added 2026-03-15) |
| M10.1 | G10 — Advanced quant proxies | 2 | Hurst VR proxy, Kang/Kalman volume shock | Built |
| M11.1 | G11 — Conviction / Weakening | 3 | dist+slope, divergence, triple alignment | Built (added 2026-03-15) |
| **TOTAL** | | **101** | | |

### B.2 Regime Engine Components

| Component | Purpose | Library | Status |
|---|---|---|---|
| `SparseJumpAdapter` / `SparseJumpModel` | Probabilistic macro regime gate (K=3: Bull/Bear/Neutral) | `jumpmodels` v0.1.1 (`jumpmodels.sparse_jump`) | Working — June 8-day locked SJM is active benchmark |
| DTMC (Discrete-Time Markov Chain) | 9-state regime engine from `price_bb_extend × bb_fib_extend` | Custom (`markov_engine.py`) | Built but superseded — destroys edge via 1500-8000+ transitions/window |
| FHMM (Factorial HMM) | Parallel 3-chain shadow model | `strategy/fhmm_engine.py` | Built as shadow model — not primary |
| SJM Long Bot | Independent SJM for Bull regime, λ=220 | `jumpmodels` | Working |
| SJM Short Bot | Independent SJM for Bear regime, λ=100 | `jumpmodels` | Working |

### B.3 Discovery / Optimization Components

| Component | Purpose | Library | Status |
|---|---|---|---|
| MCTS seed generation | Broad module screening for entry candidates | `mctx` | Working — produced top50 long/short JSON artifacts |
| TreEvo v1 (invalidated) | LLM-guided formula evolution — first attempt | Custom | **INVALIDATED** — overlapping entry model, mathematically invalid |
| TreEvo tandem (accepted) | Proxy IC discovery → SJM-gated holdout validation | Custom | **Working** — produced locked formulas |
| Optuna TPE parameter locking | Continuous parameter optimization on winning formulas | `optuna` | Working — Phase 4a locked formulas |
| GA / DEAP / mealpy / pymoo | Earlier Phase 3 tactical evolution approaches (Pipeline A era) | `DEAP`, `mealpy`, `pymoo` | Historical — superseded by MCTS + TreEvo path |

### B.4 Exit / Execution Components

| Component | Purpose | Library | Status |
|---|---|---|---|
| Hawkes dynamic exit | Microstructural exit policy (micro floor) | `HawkesPyLib` | Working — validated; replaced `tick` (environment conflict) |
| Static 0.3% trailing stop | Comparator baseline | Custom | Tested and explicitly rejected as inferior |
| SJM regime flip exit | Macro ceiling exit | `jumpmodels` | Working |
| Behavior-cloned execution agent | Policy model trained via imitation learning | PyTorch | Working — BC metrics: val accuracy 1.000, HOLD recall 1.000 |
| FastAPI model server | Inference API for BC policy | `FastAPI`, Docker | Working — locally and GCP validated |
| Async message bus | Live execution bridge | `strategy/live_message_bus.py` | Built |

### B.5 Data Pipeline Components

| Component | Purpose | Library | Status |
|---|---|---|---|
| `build_bars_from_parquet.py` | aggTrades → 30s/1m bars via Polars `group_by_dynamic()` | `polars` | Working |
| `strategy/data_loader.py` | Polars-based parquet bar loader | `polars` | Working (known issues in NT context) |
| `strategy/indicator_hub.py` | 70+ indicator columns computed on bar DataFrame | `pandas`, `numpy` | Working |
| `indicators/fibonacci_bands.py` | Clean TradingView Pine Script Fib bands translation | `numpy` | Working |
| Bar data (365 files, 541M rows, full 2025) | Raw aggTrades for BTCUSDT | Binance | Exists — SHA256 byte-identical across 3 builds |

---

## C. Approaches / Architectures Tried

| Approach | What It Was | Did It Work? |
|---|---|---|
| **DTMC 9-state** (`price_bb_extend × bb_fib_extend`) | Discrete-Time Markov Chain regime gate, 3×3 state grid, binned at ±0.5 | Produces gross signal BUT fails standalone: 1,500–8,000+ transitions per window destroys all edge via transaction costs. Net Sharpe -21 to -220 across all tested months/pairs. |
| **DTMC 27-state (3-feature)** | Expanded Cramér's V–selected feature triple | Phase 2.1 pilot: 20 of 27 states empty on 30s data, N<30 gate fail — dimensionality wall. |
| **TreEvo v1 (overlapping entries)** | LLM-guided formula evolution with all-entry evaluation contract | **INVALIDATED** — mathematically invalid (overlapping entries not comparable to baseline). Explicitly quarantined. |
| **TreEvo tandem (masked proxy IC)** | LLM proposer uses proxy metrics for search; SJM gate applied only at holdout validation | **WORKED** — produced valid directional formulas. Holdout SHORT Sharpe 19.6 vs baseline 17.8; LONG 6.5 vs baseline 5.2. |
| **SJM probabilistic gate** | Sparse Jump Model, K=3 states, L1 penalty for stickiness | **WORKING** — real, reproducible alpha. June sanity check: Sharpe +17.750. |
| **Multimonth SJM retrain** (Mar+Oct 2025) | Attempt to generalize June SJM to broader market | **REJECTED** — collapsed Long side (Sharpe 0.000). Original June 8-day SJM retained. |
| **Hawkes dynamic exit** | `HawkesPyLib` microstructural stop/TP policy | **WORKING** — SHORT dynamic Sharpe 18.9 vs static 9.9; LONG 3.1 vs static -2.7. |
| **Static 0.3% trailing stop** | Simple percentage trailing stop baseline | **EXPLICITLY REJECTED** as inferior to Hawkes exit. |
| **Behavior cloning** | Imitation learning on demonstration buffer, PyTorch policy model | **WORKING** — val accuracy 1.000 on 1885-sample buffer. |
| **MCTS atom discovery** | Broad 66-module/101-module Boolean atom screening | **WORKING** — produced valid seed shortlist for TreEvo. |
| **Optuna TPE Phase 4a** | Parameter locking on structural formula winners | **WORKING** — produced locked formulas (SHORT lookback 22, bias 0.955643; LONG lookback 10, weight 0.648160). |
| **FHMM (Factorial HMM)** | 3-parallel-chain shadow model | Built as tandem challenger — not elevated to primary. |
| **Phase 4b alpha runtime** | `strategy/phase4b_alpha_runtime.py` | Exists in codebase — status unclear from notes. |
| **Lambda regime-dependent tuning** | Per-month retraining with adaptive lambda selection | Finding: lambda IS regime-dependent. June L=220/S=100 works April but fails October. Per-month adaptive lambda required for production. |

---

## D. Things Explicitly Marked as Working / Validated

### D.1 Locked Entry Formulas (Phase 4a — Optuna TPE optimized)

```
SHORT: s1_buf_0100 * (ts_mean(price_fib_extend, 22) / relative_volume) - 0.955643
LONG:  m2_1_3a * (ts_mean(m2_1_3a, 10) - 0.648160 * obv)
```

Holdout validation (March+April 2025, SJM-gated):
- SHORT average Sharpe: **19.622** vs baseline 17.814
- LONG average Sharpe: **6.466** vs baseline 5.224

Phase 5 dynamic exit applied:
- SHORT dynamic Sharpe: **18.901** vs static trailing 9.910
- LONG dynamic Sharpe: **3.120** vs static trailing -2.701

### D.2 Regime Engine — June 8-day SJM Benchmark

| Metric | Value |
|---|---|
| Sharpe (June 9-24 eval) | +17.750 |
| Total Return | +33.86% |
| Max Drawdown | 3.18% |
| Long Time-in-Market | 56.0% |
| Short Time-in-Market | 1.1% |
| Cash | 42.9% |
| Transitions | 69 |
| TC Drag | 6.9% |

Verdict from hostile audit: PASS_WITH_AMENDMENT. Signal is real and reproducible. Locked at `sandbox/pre_phase3_shadow_b/shadow_b_lockdown_2025/models/June_8day_locked_original`.

### D.3 Indicator Implementation

From hostile audit v2:
- **Indicator integrity:** PRODUCTION READY (TV parity verified, no future-looking bias, computation chain correct)
- **Zero-fudging:** PASS — `ddof=0, adjust=False` confirmed in `fibonacci_bands.py` + `fib_chikou_strategy.py`
- **Anti-smoothing:** PASS — no `interpolate/ffill/smooth` found
- **Bar data:** SHA256 byte-identical across 3 independent builds (365 files, 541M rows)
- **Trade sequentiality:** PASS — 259 rows, 6 groups, 0 violations

### D.4 Single Module Standout

From batting cage (April 1m level_hold1): `s1_buf_1000` long = Sharpe **+3.66** (only positive module without SJM gating).

**Critical finding:** All 101 modules produce negative Sharpe without SJM regime gating. Modules are entry timing signals within regime windows — not regime detectors.

### D.5 Behavior Cloning Metrics (Shadow B Lockdown Run)

| Metric | Value |
|---|---|
| Dataset size | 1885 samples |
| Active samples | 377 |
| HOLD samples | 1508 |
| Best epoch | 31 |
| Validation accuracy | 1.000000 |
| HOLD recall | 1.000000 |
| Classification loss | 0.009142 |
| Total loss | 0.991600 |

---

## E. Visual Tools / Outputs Liked

| Output | Location / Script | Format | Notes |
|---|---|---|---|
| Trade clustering analysis | `output/sandbox/trade_clustering_analysis.html` | HTML | Phase 4a vetting artifact |
| Forensic dashboard | `scripts/gen_forensic_dashboard_v2.py` | HTML (implied) | Math forensic visual; `.bak.20260317` backup exists |
| Regime sandbox visuals | `scripts/regime_sandbox_visuals.py` | Unknown | Script exists |
| Module comparison table | `scripts/gen_module_comparison_table.py` | Unknown | Module sweep comparison |
| Module dashboard | `scripts/gen_module_dashboard.py` | Unknown | Module-level dashboard |
| TPM network plot | `scripts/plot_tpm_network.py` | Unknown | Transition probability matrix network |
| Markov heatmap summary | `output/backtests/Module_1/markov_phase2/.../markov_heatmap_summary.md` | Markdown | DTMC era — phase 2 plan artifact |
| Sweep charts (canonical) | `output/charts/` | Implied chart files | Copied from sweep runs |
| Phase 4a HTML clustering | `output/sandbox/trade_clustering_analysis.html` | HTML | Explicitly mentioned in Phase 4a vetting |

---

## F. Custom Indicator Flag Summary

The following indicators have **no named external library source** and are fully custom implementations. These should be verified against any institutional re-implementation plan:

| Indicator | Risk Level | Notes |
|---|---|---|
| Fibonacci Bands (all levels) | HIGH — foundation of entire system | TradingView Pine Script translation. Verify fib ratios and EMA base. |
| `price_fib_extend` | HIGH — used in locked entry formula | Depends on correct fib band computation |
| `bb_fib_extend` | HIGH — used in SJM feature tensor | |
| `price_bb_extend` | HIGH — used in SJM feature tensor | |
| `chikou_fib_distance` | HIGH — used in SJM feature tensor | 26-bar decision-period alignment is non-standard |
| Liquidity Bands (LMA + VWSD) | MEDIUM | vol×TR weighting is non-standard; no published reference cited |
| Angular slope normalized | MEDIUM | arctan normalization with k values is custom; threshold 0.15 = 8.6° is empirically derived |
| Acceleration atoms (2nd derivative) | MEDIUM | Second derivative of angular slope — compounded custom |
| Conviction/Weakening composites | MEDIUM | dist + slope + accel threshold logic is fully custom |
| CVD (Cumulative Volume Delta) | LOW-MEDIUM | Standard concept but implementation is custom proxy |
| OFI (Order Flow Imbalance) | MEDIUM | "bar proxy SMA cross" — likely simplified proxy, not true OFI from L2 data. Flag. |
| Kang/Kalman volume shock | HIGH | "Kang/Kalman" reference not verified against any published paper. Flag for citation check. |
| Hurst VR proxy | MEDIUM | "variance ratio > 1.0" is a simplified proxy for Hurst exponent, not the full Hurst calculation |
| Decision-aligned Ichimoku cloud | LOW | Standard Ichimoku with explicit shift(26) for causal alignment — sound but non-default |

---

## G. Architecture Decisions That Are Overridable (Per Brief)

These are historical decisions — **not binding constraints** per the research brief instructions:

| Decision | What Was Decided | Overridable? |
|---|---|---|
| Phase 3 locked to Boolean AND/OR, MAX_DEPTH=4 | Prevents GPU OOM and overfitting | Yes — "deferred to Phase 4/v2" for continuous dials |
| `relative_volume` excluded from SJM tensor | L1 weight <0.02 across all tested configs | Yes — evidence-based exclusion but testable on new data |
| Original June 8-day SJM as benchmark | Mar+Oct retrain collapsed Long side | Yes — the retrain failure was a data prep bug (54/62 days silently skipped) — worth retesting with correct data |
| Hawkes exit over static trailing | Hawkes 2× better Sharpe | Yes — other dynamic exit approaches untested |
| Lambda regime-dependent (no single lambda) | Per-month adaptive lambda required | Design constraint, not arbitrary decision |
| Short Bot fires ~1% at 30s (λ=100) | Expected for high stickiness | Lambda is tunable |

---

## H. Key File Locations

| Artifact | Path |
|---|---|
| Module registry (live) | `<TRADING_PROJECT>/scripts/mctx_module_registry.py` |
| Indicator hub (live) | `<TRADING_PROJECT>/strategy/indicator_hub.py` |
| Fibonacci bands | `<TRADING_PROJECT>/indicators/fibonacci_bands.py` |
| June SJM locked model | `sandbox/pre_phase3_shadow_b/shadow_b_lockdown_2025/models/June_8day_locked_original` |
| BC model checkpoint | `sandbox/pre_phase3_shadow_b/shadow_b_lockdown_2025/output/behavior_cloning/rl_execution_agent_bc.pt` |
| Locked entry formula report | `sandbox/pre_phase3_shadow_b/Phase4a_Vetting_Report.md` |
| Dynamic vs static exit report | `<TRADING_PROJECT>/phase5_dynamic_vs_static_report.md` |
| TreEvo tandem final review | `sandbox/pre_phase3_shadow_b/TREEVO_TANDEM_FINAL_REVIEW_2026-03-12.md` |
| Multimonth train report | `sandbox/pre_phase3_shadow_b/shadow_b_lockdown_2025/shadow_b_multimonth_train_report.md` |
| Hostile audit v2 (complete) | `user_lib_notes_trading_2026_READONLY/Notebook_Audit_Austin_Gate_Shadow_B_Bot_pipe/SHADOW_B_PIPELINE_AUDIT_V2_COMPLETE.md` |

---

## I. Open Questions / Gaps

1. **5 PDFs unread** — especially "Additional Indicators for GA_Gene_Boolean_Run.pdf" likely contains indicator candidates not in this inventory. Re-run with PDF-capable environment.
2. **CVD implementation** — described as "bar delta crosses midline" but no library source. Is this a true CVD or a proxy using bar-level OHLCV only?
3. **OFI implementation** — described as "bar proxy SMA cross" — true OFI requires tick-level bid/ask. This is almost certainly a proxy. Needs verification.
4. **Kang/Kalman volume shock** — no paper or library cited. Needs citation check.
5. **Hurst VR proxy** — "variance ratio > 1.0" is a simplified heuristic; Lo-MacKinlay variance ratio test is the standard reference.
6. **FHMM engine status** — `strategy/fhmm_engine.py` exists but no performance results documented in these notes.
7. **`derived_phase3_features.py`** — file exists but not inventoried here.
8. **`dynamic_exits.py`** — file exists; likely Hawkes integration but not confirmed from notes.
9. **April+November 2025 offline OOS async simulation** — explicitly documented as NOT yet done. This is the next major unresolved validation gate.
10. **`predict_online` NotImplementedError** in `regime_adapters.py` — live inference is broken as of 2026-03-24 per project CLAUDE.md.
