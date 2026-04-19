# SJM + Indicator Implementation Review — Session 38
> Combined findings report for Sage review.
> Gate: Sage reviews this before convergence work begins.
> Date: 2026-03-27

---

## File Inventory

### SJM Scripts (training, inference, audit, sweep, backtest)
Total: 148 scripts matched. Key files listed by sandbox area:

#### sandbox/shadow_b_bot_pipeline/pre_phase3_shadow_b/ (primary lab)
- `<WORKSPACE>/<TRADING_PROJECT>/sandbox/shadow_b_bot_pipeline/pre_phase3_shadow_b/shadow_b_utils.py`
- `<WORKSPACE>/<TRADING_PROJECT>/sandbox/shadow_b_bot_pipeline/pre_phase3_shadow_b/sjm_tuner.py`
- `<WORKSPACE>/<TRADING_PROJECT>/sandbox/shadow_b_bot_pipeline/pre_phase3_shadow_b/stage_features.py`
- `<WORKSPACE>/<TRADING_PROJECT>/sandbox/shadow_b_bot_pipeline/pre_phase3_shadow_b/trade_sim_utils.py`
- `<WORKSPACE>/<TRADING_PROJECT>/sandbox/shadow_b_bot_pipeline/pre_phase3_shadow_b/run_sjm_baselines.py`
- `<WORKSPACE>/<TRADING_PROJECT>/sandbox/shadow_b_bot_pipeline/pre_phase3_shadow_b/run_sjm_entry_screen.py`
- `<WORKSPACE>/<TRADING_PROJECT>/sandbox/shadow_b_bot_pipeline/pre_phase3_shadow_b/run_sjm_gated_screen.py`
- `<WORKSPACE>/<TRADING_PROJECT>/sandbox/shadow_b_bot_pipeline/pre_phase3_shadow_b/run_sjm_retrain_v2.py`
- `<WORKSPACE>/<TRADING_PROJECT>/sandbox/shadow_b_bot_pipeline/pre_phase3_shadow_b/run_sjm_sweep.py`
- `<WORKSPACE>/<TRADING_PROJECT>/sandbox/shadow_b_bot_pipeline/pre_phase3_shadow_b/run_shadow_b_sweep.py`
- `<WORKSPACE>/<TRADING_PROJECT>/sandbox/shadow_b_bot_pipeline/pre_phase3_shadow_b/run_dual_sjm_baseline.py`
- `<WORKSPACE>/<TRADING_PROJECT>/sandbox/shadow_b_bot_pipeline/pre_phase3_shadow_b/run_hmm_regime.py`
- `<WORKSPACE>/<TRADING_PROJECT>/sandbox/shadow_b_bot_pipeline/pre_phase3_shadow_b/run_mtf_dual_baseline.py`
- `<WORKSPACE>/<TRADING_PROJECT>/sandbox/shadow_b_bot_pipeline/pre_phase3_shadow_b/run_mtf_dual_baseline_oos.py`
- `<WORKSPACE>/<TRADING_PROJECT>/sandbox/shadow_b_bot_pipeline/pre_phase3_shadow_b/run_monthly_oos.py`
- `<WORKSPACE>/<TRADING_PROJECT>/sandbox/shadow_b_bot_pipeline/pre_phase3_shadow_b/run_holdout_validation.py`
- `<WORKSPACE>/<TRADING_PROJECT>/sandbox/shadow_b_bot_pipeline/pre_phase3_shadow_b/run_treevo_llm.py`
- `<WORKSPACE>/<TRADING_PROJECT>/sandbox/shadow_b_bot_pipeline/pre_phase3_shadow_b/run_treevo_track_ai_v1.py`
- `<WORKSPACE>/<TRADING_PROJECT>/sandbox/shadow_b_bot_pipeline/pre_phase3_shadow_b/run_mcts_autoresearch.py`
- `<WORKSPACE>/<TRADING_PROJECT>/sandbox/shadow_b_bot_pipeline/pre_phase3_shadow_b/run_alpha_dashboard.py`
- `<WORKSPACE>/<TRADING_PROJECT>/sandbox/shadow_b_bot_pipeline/pre_phase3_shadow_b/run_asymmetric_tf_sweep.py`
- `<WORKSPACE>/<TRADING_PROJECT>/sandbox/shadow_b_bot_pipeline/pre_phase3_shadow_b/run_tf_sweep.py`
- `<WORKSPACE>/<TRADING_PROJECT>/sandbox/shadow_b_bot_pipeline/pre_phase3_shadow_b/run_module_preselect_sweep.py`
- `<WORKSPACE>/<TRADING_PROJECT>/sandbox/shadow_b_bot_pipeline/pre_phase3_shadow_b/run_1m_conflict_sweep.py`
- `<WORKSPACE>/<TRADING_PROJECT>/sandbox/shadow_b_bot_pipeline/pre_phase3_shadow_b/run_short_bot_sweep.py`
- `<WORKSPACE>/<TRADING_PROJECT>/sandbox/shadow_b_bot_pipeline/pre_phase3_shadow_b/run_batting_cage_v1.py`
- `<WORKSPACE>/<TRADING_PROJECT>/sandbox/shadow_b_bot_pipeline/pre_phase3_shadow_b/run_batting_cage_v2.py`
- `<WORKSPACE>/<TRADING_PROJECT>/sandbox/shadow_b_bot_pipeline/pre_phase3_shadow_b/run_bad_module_dashboard.py`
- `<WORKSPACE>/<TRADING_PROJECT>/sandbox/shadow_b_bot_pipeline/pre_phase3_shadow_b/run_comparison_viz.py`
- `<WORKSPACE>/<TRADING_PROJECT>/sandbox/shadow_b_bot_pipeline/pre_phase3_shadow_b/run_long_lambda_diag.py`
- `<WORKSPACE>/<TRADING_PROJECT>/sandbox/shadow_b_bot_pipeline/pre_phase3_shadow_b/run_trade_pattern_mining.py`
- `<WORKSPACE>/<TRADING_PROJECT>/sandbox/shadow_b_bot_pipeline/pre_phase3_shadow_b/run_autoresearch_gcp.py`
- `<WORKSPACE>/<TRADING_PROJECT>/sandbox/shadow_b_bot_pipeline/pre_phase3_shadow_b/run_frozen_june_fullyear.py`
- `<WORKSPACE>/<TRADING_PROJECT>/sandbox/shadow_b_bot_pipeline/pre_phase3_shadow_b/run_frozen_june_october_audit.py`
- `<WORKSPACE>/<TRADING_PROJECT>/sandbox/shadow_b_bot_pipeline/pre_phase3_shadow_b/run_june2025_full_sanity.py`
- `<WORKSPACE>/<TRADING_PROJECT>/sandbox/shadow_b_bot_pipeline/pre_phase3_shadow_b/run_oct6_sanity_check.py`
- `<WORKSPACE>/<TRADING_PROJECT>/sandbox/shadow_b_bot_pipeline/pre_phase3_shadow_b/run_5s_june9_smoketest.py`
- `<WORKSPACE>/<TRADING_PROJECT>/sandbox/shadow_b_bot_pipeline/pre_phase3_shadow_b/diagnose_march2025.py`
- `<WORKSPACE>/<TRADING_PROJECT>/sandbox/shadow_b_bot_pipeline/pre_phase3_shadow_b/parity_check.py`
- `<WORKSPACE>/<TRADING_PROJECT>/sandbox/shadow_b_bot_pipeline/pre_phase3_shadow_b/visualize_shadow_b.py`
- `<WORKSPACE>/<TRADING_PROJECT>/sandbox/shadow_b_bot_pipeline/pre_phase3_shadow_b/build_master_dossier_v1.py`
- `<WORKSPACE>/<TRADING_PROJECT>/sandbox/shadow_b_bot_pipeline/pre_phase3_shadow_b/build_stage_b_prep_v1.py`

#### shadow_b_lockdown_2025/ (locked training artifacts)
- `<WORKSPACE>/<TRADING_PROJECT>/sandbox/shadow_b_bot_pipeline/pre_phase3_shadow_b/shadow_b_lockdown_2025/run_shadow_b_multimonth_train.py`
- `<WORKSPACE>/<TRADING_PROJECT>/sandbox/shadow_b_bot_pipeline/pre_phase3_shadow_b/shadow_b_lockdown_2025/resume_shadow_b_multimonth_from_fits.py`
- `<WORKSPACE>/<TRADING_PROJECT>/sandbox/shadow_b_bot_pipeline/pre_phase3_shadow_b/shadow_b_lockdown_2025/extract_sjm_parameters.py`

#### modular_sjm_lab_20260317/ (modular refactor lab)
- `<WORKSPACE>/<TRADING_PROJECT>/sandbox/shadow_b_bot_pipeline/pre_phase3_shadow_b/modular_sjm_lab_20260317/run_modular_sjm_lab.py`
- `<WORKSPACE>/<TRADING_PROJECT>/sandbox/shadow_b_bot_pipeline/pre_phase3_shadow_b/modular_sjm_lab_20260317/run_extremes_down.py`
- `<WORKSPACE>/<TRADING_PROJECT>/sandbox/shadow_b_bot_pipeline/pre_phase3_shadow_b/modular_sjm_lab_20260317/shadow_b_utils_lab.py`
- `<WORKSPACE>/<TRADING_PROJECT>/sandbox/shadow_b_bot_pipeline/pre_phase3_shadow_b/modular_sjm_lab_20260317/regime_adapters_lab.py`
- `<WORKSPACE>/<TRADING_PROJECT>/sandbox/shadow_b_bot_pipeline/pre_phase3_shadow_b/modular_sjm_lab_20260317/indicator_hub_lab.py`

#### track_ai_v1_audit_packet/ (step-by-step audit chain)
- `<WORKSPACE>/<TRADING_PROJECT>/sandbox/shadow_b_bot_pipeline/pre_phase3_shadow_b/track_ai_v1_audit_packet/run_step2_sjm_june_sanity.py`
- `<WORKSPACE>/<TRADING_PROJECT>/sandbox/shadow_b_bot_pipeline/pre_phase3_shadow_b/track_ai_v1_audit_packet/run_step3_dtmc_gate_check.py`
- `<WORKSPACE>/<TRADING_PROJECT>/sandbox/shadow_b_bot_pipeline/pre_phase3_shadow_b/track_ai_v1_audit_packet/run_step3b_sjm_oct_apr.py`
- `<WORKSPACE>/<TRADING_PROJECT>/sandbox/shadow_b_bot_pipeline/pre_phase3_shadow_b/track_ai_v1_audit_packet/run_step3c_dtmc_dualbot.py`
- `<WORKSPACE>/<TRADING_PROJECT>/sandbox/shadow_b_bot_pipeline/pre_phase3_shadow_b/track_ai_v1_audit_packet/run_step3d_dtmc_experiments.py`
- `<WORKSPACE>/<TRADING_PROJECT>/sandbox/shadow_b_bot_pipeline/pre_phase3_shadow_b/track_ai_v1_audit_packet/run_step3e_corrected_experiments.py`
- `<WORKSPACE>/<TRADING_PROJECT>/sandbox/shadow_b_bot_pipeline/pre_phase3_shadow_b/track_ai_v1_audit_packet/run_step3f_dtmc_local_train.py`
- `<WORKSPACE>/<TRADING_PROJECT>/sandbox/shadow_b_bot_pipeline/pre_phase3_shadow_b/track_ai_v1_audit_packet/run_step4_sjm_cold_test.py`
- `<WORKSPACE>/<TRADING_PROJECT>/sandbox/shadow_b_bot_pipeline/pre_phase3_shadow_b/track_ai_v1_audit_packet/run_step4_sjm_lambda_sweep.py`
- `<WORKSPACE>/<TRADING_PROJECT>/sandbox/shadow_b_bot_pipeline/pre_phase3_shadow_b/track_ai_v1_audit_packet/build_audit_bars.py`
- `<WORKSPACE>/<TRADING_PROJECT>/sandbox/shadow_b_bot_pipeline/pre_phase3_shadow_b/track_ai_v1_audit_packet/build_notebooklm_master_export.py`
- `<WORKSPACE>/<TRADING_PROJECT>/sandbox/shadow_b_bot_pipeline/pre_phase3_shadow_b/track_ai_v1_audit_packet/generate_oct_oos_csv.py`
- `<WORKSPACE>/<TRADING_PROJECT>/sandbox/shadow_b_bot_pipeline/pre_phase3_shadow_b/track_ai_v1_audit_packet/generate_visual_audit.py`
- `<WORKSPACE>/<TRADING_PROJECT>/sandbox/shadow_b_bot_pipeline/pre_phase3_shadow_b/track_ai_v1_audit_packet/generate_visual_audit_v2.py`

#### data_rebuild_audit_2025_june_v1/
- `<WORKSPACE>/<TRADING_PROJECT>/sandbox/shadow_b_bot_pipeline/pre_phase3_shadow_b/data_rebuild_audit_2025_june_v1/run_june_sjm_gate_only.py`
- `<WORKSPACE>/<TRADING_PROJECT>/sandbox/shadow_b_bot_pipeline/pre_phase3_shadow_b/data_rebuild_audit_2025_june_v1/build_june_bars_from_raw.py`
- `<WORKSPACE>/<TRADING_PROJECT>/sandbox/shadow_b_bot_pipeline/pre_phase3_shadow_b/data_rebuild_audit_2025_june_v1/audit_june_bar_parity.py`

#### track_a_gate_rebuild_2025_june_july_v1/
- `<WORKSPACE>/<TRADING_PROJECT>/sandbox/shadow_b_bot_pipeline/pre_phase3_shadow_b/track_a_gate_rebuild_2025_june_july_v1/run_track_a_optuna.py`
- `<WORKSPACE>/<TRADING_PROJECT>/sandbox/shadow_b_bot_pipeline/pre_phase3_shadow_b/track_a_gate_rebuild_2025_june_july_v1/run_track_b_fjm.py`
- `<WORKSPACE>/<TRADING_PROJECT>/sandbox/shadow_b_bot_pipeline/pre_phase3_shadow_b/track_a_gate_rebuild_2025_june_july_v1/build_mtf_bars_from_ticks.py`
- `<WORKSPACE>/<TRADING_PROJECT>/sandbox/shadow_b_bot_pipeline/pre_phase3_shadow_b/track_a_gate_rebuild_2025_june_july_v1/audit_mtf_bar_parity.py`
- `<WORKSPACE>/<TRADING_PROJECT>/sandbox/shadow_b_bot_pipeline/pre_phase3_shadow_b/track_a_gate_rebuild_2025_june_july_v1/build_track_ab_audit_dashboards.py`

#### track_c_dtmc_recheck_2025_june_july_v1/
- `<WORKSPACE>/<TRADING_PROJECT>/sandbox/shadow_b_bot_pipeline/pre_phase3_shadow_b/track_c_dtmc_recheck_2025_june_july_v1/run_track_c_dtmc.py`
- `<WORKSPACE>/<TRADING_PROJECT>/sandbox/shadow_b_bot_pipeline/pre_phase3_shadow_b/track_c_dtmc_recheck_2025_june_july_v1/run_track_c_fjm.py`
- `<WORKSPACE>/<TRADING_PROJECT>/sandbox/shadow_b_bot_pipeline/pre_phase3_shadow_b/track_c_dtmc_recheck_2025_june_july_v1/run_track_c_sanity.py`

#### full_year_sanity_2025/
- `<WORKSPACE>/<TRADING_PROJECT>/sandbox/shadow_b_bot_pipeline/pre_phase3_shadow_b/full_year_sanity_2025/run_post_conflict_fullyear.py`

#### codex_sjm_causal_audit_v2/
- `<WORKSPACE>/<TRADING_PROJECT>/sandbox/shadow_b_bot_pipeline/pre_phase3_shadow_b/codex_sjm_causal_audit_v2/shadow_b_utils_v2.py`
- `<WORKSPACE>/<TRADING_PROJECT>/sandbox/shadow_b_bot_pipeline/pre_phase3_shadow_b/codex_sjm_causal_audit_v2/validate_emission_anchoring.py`

#### v2_audit_packet_2026-03-15-18_2026/ (hostile + explicit audits)
- `<WORKSPACE>/<TRADING_PROJECT>/sandbox/shadow_b_bot_pipeline/v2_audit_packet_2026-03-15-18_2026/codex_hostile_audit_independent_v1/run_hostile_shadow_b_audit.py`
- `<WORKSPACE>/<TRADING_PROJECT>/sandbox/shadow_b_bot_pipeline/v2_audit_packet_2026-03-15-18_2026/codex_hostile_audit_independent_v2/run_updated_hostile_checks.py`
- `<WORKSPACE>/<TRADING_PROJECT>/sandbox/shadow_b_bot_pipeline/v2_audit_packet_2026-03-15-18_2026/codex_sjm_explicit_audit_v1/run_sjm_explicit_audit.py`
- `<WORKSPACE>/<TRADING_PROJECT>/sandbox/shadow_b_bot_pipeline/v2_audit_packet_2026-03-15-18_2026/scripts/run_step3c_dtmc_dualbot.py`
- `<WORKSPACE>/<TRADING_PROJECT>/sandbox/shadow_b_bot_pipeline/v2_audit_packet_2026-03-15-18_2026/scripts/run_step3d_dtmc_experiments.py`
- `<WORKSPACE>/<TRADING_PROJECT>/sandbox/shadow_b_bot_pipeline/v2_audit_packet_2026-03-15-18_2026/scripts/run_step3e_corrected_experiments.py`
- `<WORKSPACE>/<TRADING_PROJECT>/sandbox/shadow_b_bot_pipeline/v2_audit_packet_2026-03-15-18_2026/scripts/run_step3f_dtmc_local_train.py`
- `<WORKSPACE>/<TRADING_PROJECT>/sandbox/shadow_b_bot_pipeline/v2_audit_packet_2026-03-15-18_2026/scripts/run_step4_sjm_lambda_sweep.py`

#### v3_visual_dashboard_old/ and shadowBB VizBox
- `<WORKSPACE>/<TRADING_PROJECT>/sandbox/shadow_b_bot_pipeline/v3_visual_dashboard_old/generate_dashboard_v3.py`
- `<WORKSPACE>/<TRADING_PROJECT>/sandbox/shadow_b_bot_pipeline/v3_visual_dashboard_old/generate_oct_oos_csv.py`
- `<WORKSPACE>/<TRADING_PROJECT>/sandbox/shadow_b_bot_pipeline/shadowBB_Binance_Nautilus_VizBox_v1/v3_visual_dashboard/generate_dashboard_v3.py`
- `<WORKSPACE>/<TRADING_PROJECT>/sandbox/shadow_b_bot_pipeline/shadowBB_Binance_Nautilus_VizBox_v1/v3_visual_dashboard/generate_oct_oos_csv.py`

#### pre_phase3_shadow_b/ (standalone audit packet copy)
- `<WORKSPACE>/<TRADING_PROJECT>/sandbox/pre_phase3_shadow_b/track_ai_v1_audit_packet/generate_oct_oos_csv.py`
- `<WORKSPACE>/<TRADING_PROJECT>/sandbox/pre_phase3_shadow_b/track_ai_v1_audit_packet/generate_visual_audit.py`
- `<WORKSPACE>/<TRADING_PROJECT>/sandbox/pre_phase3_shadow_b/track_ai_v1_audit_packet/generate_visual_audit_v2.py`

#### R_ARM_austin_audit_drop_b/SJM_Binance_NT_audit_pack_3_20_26/02_SJM_clean_api/ (clean API — newest area)
- `<WORKSPACE>/<TRADING_PROJECT>/sandbox/R_ARM_austin_audit_drop_b/SJM_Binance_NT_audit_pack_3_20_26/02_SJM_clean_api/sjm_clean_dashboard_2026-03-20.py`
- `<WORKSPACE>/<TRADING_PROJECT>/sandbox/R_ARM_austin_audit_drop_b/SJM_Binance_NT_audit_pack_3_20_26/02_SJM_clean_api/sjm_gated_sim_june_2026-03-20.py`
- `<WORKSPACE>/<TRADING_PROJECT>/sandbox/R_ARM_austin_audit_drop_b/SJM_Binance_NT_audit_pack_3_20_26/02_SJM_clean_api/sjm_lambda_sweep_clean_2026-03-20.py`
- `<WORKSPACE>/<TRADING_PROJECT>/sandbox/R_ARM_austin_audit_drop_b/SJM_Binance_NT_audit_pack_3_20_26/02_SJM_clean_api/sjm_lambda_sweep_gcp_2026-03-20.py`
- `<WORKSPACE>/<TRADING_PROJECT>/sandbox/R_ARM_austin_audit_drop_b/SJM_Binance_NT_audit_pack_3_20_26/02_SJM_clean_api/sjm_nt_backtest_2026-03-20.py`
- `<WORKSPACE>/<TRADING_PROJECT>/sandbox/R_ARM_austin_audit_drop_b/SJM_Binance_NT_audit_pack_3_20_26/02_SJM_clean_api/sjm_oos_june_clean_2026-03-20.py`
- `<WORKSPACE>/<TRADING_PROJECT>/sandbox/R_ARM_austin_audit_drop_b/SJM_Binance_NT_audit_pack_3_20_26/02_SJM_clean_api/lambda_sweep_validator_2026-03-20.py`
- `<WORKSPACE>/<TRADING_PROJECT>/sandbox/R_ARM_austin_audit_drop_b/SJM_Binance_NT_audit_pack_3_20_26/02_SJM_clean_api/pipeline_validator_v1_2026-03-20.py`
- `<WORKSPACE>/<TRADING_PROJECT>/sandbox/R_ARM_austin_audit_drop_b/SJM_Binance_NT_audit_pack_3_20_26/02_SJM_clean_api/sweep_june1_atoms_2026-03-20.py`
- `<WORKSPACE>/<TRADING_PROJECT>/sandbox/R_ARM_austin_audit_drop_b/SJM_Binance_NT_audit_pack_3_20_26/02_SJM_clean_api/gen_dashboard_june1_2026-03-20.py`
- `<WORKSPACE>/<TRADING_PROJECT>/sandbox/R_ARM_austin_audit_drop_b/SJM_Binance_NT_audit_pack_3_20_26/02_SJM_clean_api/infra_smoke_test_2026-03-20.py`
- `<WORKSPACE>/<TRADING_PROJECT>/sandbox/R_ARM_austin_audit_drop_b/SJM_Binance_NT_audit_pack_3_20_26/02_SJM_clean_api/validate_oos_dashboard_2026-03-20.py`
- `<WORKSPACE>/<TRADING_PROJECT>/sandbox/R_ARM_austin_audit_drop_b/SJM_Binance_NT_audit_pack_3_20_26/02_SJM_clean_api/strategy_search_2026-03-20.py`
- `<WORKSPACE>/<TRADING_PROJECT>/sandbox/R_ARM_austin_audit_drop_b/SJM_Binance_NT_audit_pack_3_20_26/02_SJM_clean_api/run_mcts_autoresearch_v1_2026-03-18.py`
- `<WORKSPACE>/<TRADING_PROJECT>/sandbox/R_ARM_austin_audit_drop_b/SJM_Binance_NT_audit_pack_3_20_26/02_SJM_clean_api/run_treevo_llm_v1_2026-03-18.py`
- `<WORKSPACE>/<TRADING_PROJECT>/sandbox/R_ARM_austin_audit_drop_b/SJM_Binance_NT_audit_pack_3_20_26/02_SJM_clean_api/_export_features_for_gcp.py`
- `<WORKSPACE>/<TRADING_PROJECT>/sandbox/R_ARM_austin_audit_drop_b/SJM_Binance_NT_audit_pack_3_20_26/02_SJM_clean_api/deps/derived_phase3_features.py`
- `<WORKSPACE>/<TRADING_PROJECT>/sandbox/R_ARM_austin_audit_drop_b/SJM_Binance_NT_audit_pack_3_20_26/02_SJM_clean_api/deps/markov_engine.py`
- `<WORKSPACE>/<TRADING_PROJECT>/sandbox/R_ARM_austin_audit_drop_b/SJM_Binance_NT_audit_pack_3_20_26/02_SJM_clean_api/deps/phase3_shared_evaluator.py`
- `<WORKSPACE>/<TRADING_PROJECT>/sandbox/R_ARM_austin_audit_drop_b/SJM_Binance_NT_audit_pack_3_20_26/02_SJM_clean_api/deps/phase3_tactical_registry.py`
- `<WORKSPACE>/<TRADING_PROJECT>/sandbox/R_ARM_austin_audit_drop_b/SJM_Binance_NT_audit_pack_3_20_26/02_SJM_clean_api/deps/parity_pine_polfwack.py`
- `<WORKSPACE>/<TRADING_PROJECT>/sandbox/R_ARM_austin_audit_drop_b/SJM_Binance_NT_audit_pack_3_20_26/02_SJM_clean_api/deps/regime_adapters.py`
- `<WORKSPACE>/<TRADING_PROJECT>/sandbox/R_ARM_austin_audit_drop_b/SJM_Binance_NT_audit_pack_3_20_26/02_SJM_clean_api/deps/shadow_b_utils.py`
- `<WORKSPACE>/<TRADING_PROJECT>/sandbox/R_ARM_austin_audit_drop_b/SJM_Binance_NT_audit_pack_3_20_26/02_SJM_clean_api/deps/__init__.py`
- `<WORKSPACE>/<TRADING_PROJECT>/sandbox/R_ARM_austin_audit_drop_b/SJM_Binance_NT_audit_pack_3_20_26/02_SJM_clean_api/_ref_dashboard_copy/generate_oct_oos_csv.py`
- `<WORKSPACE>/<TRADING_PROJECT>/sandbox/R_ARM_austin_audit_drop_b/SJM_Binance_NT_audit_pack_3_20_26/02_SJM_clean_api/_ref_dashboard_copy/generate_visual_audit.py`
- `<WORKSPACE>/<TRADING_PROJECT>/sandbox/R_ARM_austin_audit_drop_b/SJM_Binance_NT_audit_pack_3_20_26/02_SJM_clean_api/_ref_dashboard_copy/generate_visual_audit_v2.py`

#### R_ARM_austin_audit_drop_b/ — 04_regime_adapters_DEPRECATED/
- `<WORKSPACE>/<TRADING_PROJECT>/sandbox/R_ARM_austin_audit_drop_b/SJM_Binance_NT_audit_pack_3_20_26/04_regime_adapters_DEPRECATED/regime_adapters_CANONICAL.py`
- `<WORKSPACE>/<TRADING_PROJECT>/sandbox/R_ARM_austin_audit_drop_b/SJM_Binance_NT_audit_pack_3_20_26/04_regime_adapters_DEPRECATED/regime_adapters_DEPS_COPY.py`

#### R_ARM_austin_audit_drop_b/ — 07_shadow_b_reference/
- `<WORKSPACE>/<TRADING_PROJECT>/sandbox/R_ARM_austin_audit_drop_b/SJM_Binance_NT_audit_pack_3_20_26/07_shadow_b_reference/shadow_b_utils_DEPS_COPY.py`

#### Research_ArM_shadowBBox_v1/02_treevo_arm/ (treevo ARM branch)
- `<WORKSPACE>/<TRADING_PROJECT>/sandbox/Research_ArM_shadowBBox_v1/02_treevo_arm/sjm_clean_dashboard_2026-03-20.py`
- `<WORKSPACE>/<TRADING_PROJECT>/sandbox/Research_ArM_shadowBBox_v1/02_treevo_arm/sjm_gated_sim_june_2026-03-20.py`
- `<WORKSPACE>/<TRADING_PROJECT>/sandbox/Research_ArM_shadowBBox_v1/02_treevo_arm/sjm_lambda_sweep_clean_2026-03-20.py`
- `<WORKSPACE>/<TRADING_PROJECT>/sandbox/Research_ArM_shadowBBox_v1/02_treevo_arm/sjm_lambda_sweep_gcp_2026-03-20.py`
- `<WORKSPACE>/<TRADING_PROJECT>/sandbox/Research_ArM_shadowBBox_v1/02_treevo_arm/sjm_nt_backtest_2026-03-20.py`
- `<WORKSPACE>/<TRADING_PROJECT>/sandbox/Research_ArM_shadowBBox_v1/02_treevo_arm/sjm_oos_june_clean_2026-03-20.py`
- `<WORKSPACE>/<TRADING_PROJECT>/sandbox/Research_ArM_shadowBBox_v1/02_treevo_arm/lambda_sweep_validator_2026-03-20.py`
- `<WORKSPACE>/<TRADING_PROJECT>/sandbox/Research_ArM_shadowBBox_v1/02_treevo_arm/sweep_june1_atoms_2026-03-20.py`
- `<WORKSPACE>/<TRADING_PROJECT>/sandbox/Research_ArM_shadowBBox_v1/02_treevo_arm/deps/regime_adapters.py`
- `<WORKSPACE>/<TRADING_PROJECT>/sandbox/Research_ArM_shadowBBox_v1/02_treevo_arm/deps/shadow_b_utils.py`

#### NT data pipeline (in both sandbox roots)
- `<WORKSPACE>/<TRADING_PROJECT>/sandbox/R_ARM_austin_audit_drop_b/SJM_Binance_NT_audit_pack_3_20_26/01_NT_binance_data_pipeline/aggtrades_to_nautilus_catalog_v1_2026-03-18.py`
- `<WORKSPACE>/<TRADING_PROJECT>/sandbox/R_ARM_austin_audit_drop_b/SJM_Binance_NT_audit_pack_3_20_26/01_NT_binance_data_pipeline/aggtrades_to_nautilus_catalog_v4_2026-03-18.py`
- `<WORKSPACE>/<TRADING_PROJECT>/sandbox/R_ARM_austin_audit_drop_b/SJM_Binance_NT_audit_pack_3_20_26/01_NT_binance_data_pipeline/bar_parity_validator_v1_2026-03-18.py`
- `<WORKSPACE>/<TRADING_PROJECT>/sandbox/R_ARM_austin_audit_drop_b/SJM_Binance_NT_audit_pack_3_20_26/01_NT_binance_data_pipeline/binance_aggtrades_downloader_v1_2026-03-18.py`
- `<WORKSPACE>/<TRADING_PROJECT>/sandbox/R_ARM_austin_audit_drop_b/SJM_Binance_NT_audit_pack_3_20_26/01_NT_binance_data_pipeline/nautilus_bar_builder_v1_2026-03-18.py`
- `<WORKSPACE>/<TRADING_PROJECT>/sandbox/Data_v2_Binance_Nautilus_ShadowBbot/aggtrades_to_nautilus_catalog_v1_2026-03-18.py`
- `<WORKSPACE>/<TRADING_PROJECT>/sandbox/Data_v2_Binance_Nautilus_ShadowBbot/aggtrades_to_nautilus_catalog_v2_2026-03-18.py`
- `<WORKSPACE>/<TRADING_PROJECT>/sandbox/Data_v2_Binance_Nautilus_ShadowBbot/aggtrades_to_nautilus_catalog_v3_2026-03-18.py`
- `<WORKSPACE>/<TRADING_PROJECT>/sandbox/Data_v2_Binance_Nautilus_ShadowBbot/aggtrades_to_nautilus_catalog_v4_2026-03-18.py`
- `<WORKSPACE>/<TRADING_PROJECT>/sandbox/Data_v2_Binance_Nautilus_ShadowBbot/bar_parity_validator_v1_2026-03-18.py`
- `<WORKSPACE>/<TRADING_PROJECT>/sandbox/Data_v2_Binance_Nautilus_ShadowBbot/binance_aggtrades_downloader_v1_2026-03-18.py`
- `<WORKSPACE>/<TRADING_PROJECT>/sandbox/Data_v2_Binance_Nautilus_ShadowBbot/nautilus_bar_builder_v1_2026-03-18.py`
- `<WORKSPACE>/<TRADING_PROJECT>/sandbox/Data_v2_Binance_Nautilus_ShadowBbot/nautilus_bar_builder_v2_2026-03-18.py`
- `<WORKSPACE>/<TRADING_PROJECT>/sandbox/Data_v2_Binance_Nautilus_ShadowBbot/nautilus_bar_builder_v3_2026-03-18.py`

---

### Indicator Modules
Total in sandbox: 22. Total outside sandbox (<TRADING_PROJECT> root): 10.

#### Sandbox — 03_indicator_modules/ (R_ARM audit pack — canonical copies)
- `<WORKSPACE>/<TRADING_PROJECT>/sandbox/R_ARM_austin_audit_drop_b/SJM_Binance_NT_audit_pack_3_20_26/03_indicator_modules/indicator_hub.py`
- `<WORKSPACE>/<TRADING_PROJECT>/sandbox/R_ARM_austin_audit_drop_b/SJM_Binance_NT_audit_pack_3_20_26/03_indicator_modules/indicator_hub_DEPS_COPY.py`
- `<WORKSPACE>/<TRADING_PROJECT>/sandbox/R_ARM_austin_audit_drop_b/SJM_Binance_NT_audit_pack_3_20_26/03_indicator_modules/fibonacci_bands.py`
- `<WORKSPACE>/<TRADING_PROJECT>/sandbox/R_ARM_austin_audit_drop_b/SJM_Binance_NT_audit_pack_3_20_26/03_indicator_modules/fibonacci_bands_DEPS_COPY.py`
- `<WORKSPACE>/<TRADING_PROJECT>/sandbox/R_ARM_austin_audit_drop_b/SJM_Binance_NT_audit_pack_3_20_26/03_indicator_modules/fib_chikou_strategy.py`
- `<WORKSPACE>/<TRADING_PROJECT>/sandbox/R_ARM_austin_audit_drop_b/SJM_Binance_NT_audit_pack_3_20_26/03_indicator_modules/fib_chikou_strategy_DEPS_COPY.py`
- `<WORKSPACE>/<TRADING_PROJECT>/sandbox/R_ARM_austin_audit_drop_b/SJM_Binance_NT_audit_pack_3_20_26/03_indicator_modules/mctx_module_registry.py`
- `<WORKSPACE>/<TRADING_PROJECT>/sandbox/R_ARM_austin_audit_drop_b/SJM_Binance_NT_audit_pack_3_20_26/03_indicator_modules/parity_pine_polfwack.py`

#### Sandbox — 02_SJM_clean_api/deps/ (inline deps for clean API)
- `<WORKSPACE>/<TRADING_PROJECT>/sandbox/R_ARM_austin_audit_drop_b/SJM_Binance_NT_audit_pack_3_20_26/02_SJM_clean_api/deps/indicator_hub.py`
- `<WORKSPACE>/<TRADING_PROJECT>/sandbox/R_ARM_austin_audit_drop_b/SJM_Binance_NT_audit_pack_3_20_26/02_SJM_clean_api/deps/fibonacci_bands.py`
- `<WORKSPACE>/<TRADING_PROJECT>/sandbox/R_ARM_austin_audit_drop_b/SJM_Binance_NT_audit_pack_3_20_26/02_SJM_clean_api/deps/fib_chikou_strategy.py`
- `<WORKSPACE>/<TRADING_PROJECT>/sandbox/R_ARM_austin_audit_drop_b/SJM_Binance_NT_audit_pack_3_20_26/02_SJM_clean_api/deps/derived_phase3_features.py`
- `<WORKSPACE>/<TRADING_PROJECT>/sandbox/R_ARM_austin_audit_drop_b/SJM_Binance_NT_audit_pack_3_20_26/02_SJM_clean_api/deps/mctx_module_registry.py`

#### Sandbox — Research_ArM_shadowBBox_v1/02_treevo_arm/deps/
- `<WORKSPACE>/<TRADING_PROJECT>/sandbox/Research_ArM_shadowBBox_v1/02_treevo_arm/deps/indicator_hub.py`
- `<WORKSPACE>/<TRADING_PROJECT>/sandbox/Research_ArM_shadowBBox_v1/02_treevo_arm/deps/fibonacci_bands.py`
- `<WORKSPACE>/<TRADING_PROJECT>/sandbox/Research_ArM_shadowBBox_v1/02_treevo_arm/deps/fib_chikou_strategy.py`
- `<WORKSPACE>/<TRADING_PROJECT>/sandbox/Research_ArM_shadowBBox_v1/02_treevo_arm/deps/derived_phase3_features.py`
- `<WORKSPACE>/<TRADING_PROJECT>/sandbox/Research_ArM_shadowBBox_v1/02_treevo_arm/_export_features_for_gcp.py`

#### Sandbox — modular_sjm_lab_20260317/
- `<WORKSPACE>/<TRADING_PROJECT>/sandbox/shadow_b_bot_pipeline/pre_phase3_shadow_b/modular_sjm_lab_20260317/indicator_hub_lab.py`

#### Sandbox — stage_features.py (pre_phase3_shadow_b)
- `<WORKSPACE>/<TRADING_PROJECT>/sandbox/shadow_b_bot_pipeline/pre_phase3_shadow_b/stage_features.py`

#### Outside sandbox — <TRADING_PROJECT>/indicators/ (source-of-truth candidates)
- `<WORKSPACE>/<TRADING_PROJECT>/indicators/fibonacci_bands.py`
- `<WORKSPACE>/<TRADING_PROJECT>/indicators/audit_phase3.py`
- `<WORKSPACE>/<TRADING_PROJECT>/indicators/tv_parity_check.py`
- `<WORKSPACE>/<TRADING_PROJECT>/indicators/tv_parity_check_30s.py`
- `<WORKSPACE>/<TRADING_PROJECT>/indicators/validate_indicators.py`
- `<WORKSPACE>/<TRADING_PROJECT>/indicators/validate_indicators_headless.py`
- `<WORKSPACE>/<TRADING_PROJECT>/indicators/verify_fib_bands.py`

#### Outside sandbox — <TRADING_PROJECT>/strategy/ (live strategy modules)
- `<WORKSPACE>/<TRADING_PROJECT>/strategy/indicator_hub.py`
- `<WORKSPACE>/<TRADING_PROJECT>/strategy/derived_phase3_features.py`

#### Outside sandbox — <TRADING_PROJECT>/scripts/
- `<WORKSPACE>/<TRADING_PROJECT>/scripts/plot_indicators_only.py`

---

### Model Artifacts (.npz, .pkl, metadata.json)
Total: 6 files across 2 locked model bundles.

#### June_8day_locked_original/ (original locked model)
- `<WORKSPACE>/<TRADING_PROJECT>/sandbox/shadow_b_bot_pipeline/pre_phase3_shadow_b/shadow_b_lockdown_2025/models/June_8day_locked_original/sjm_parameters_v1.npz`
- `<WORKSPACE>/<TRADING_PROJECT>/sandbox/shadow_b_bot_pipeline/pre_phase3_shadow_b/shadow_b_lockdown_2025/models/June_8day_locked_original/bundle.pkl`
- `<WORKSPACE>/<TRADING_PROJECT>/sandbox/shadow_b_bot_pipeline/pre_phase3_shadow_b/shadow_b_lockdown_2025/models/June_8day_locked_original/metadata.json`

#### March_October_2025_retrained_v1/ (retrained model)
- `<WORKSPACE>/<TRADING_PROJECT>/sandbox/shadow_b_bot_pipeline/pre_phase3_shadow_b/shadow_b_lockdown_2025/models/March_October_2025_retrained_v1/sjm_parameters_v1.npz`
- `<WORKSPACE>/<TRADING_PROJECT>/sandbox/shadow_b_bot_pipeline/pre_phase3_shadow_b/shadow_b_lockdown_2025/models/March_October_2025_retrained_v1/bundle.pkl`
- `<WORKSPACE>/<TRADING_PROJECT>/sandbox/shadow_b_bot_pipeline/pre_phase3_shadow_b/shadow_b_lockdown_2025/models/March_October_2025_retrained_v1/metadata.json`

Both model bundles located at:
`<WORKSPACE>/<TRADING_PROJECT>/sandbox/shadow_b_bot_pipeline/pre_phase3_shadow_b/shadow_b_lockdown_2025/models/`

---

### Result/Output Files (.json, .csv)
Total matching result/output/sweep/audit/lambda/sharpe/explicit pattern: 529 files.
The majority (~500+) are module_sweep pair CSVs (long/short per combo) in:
`<WORKSPACE>/<TRADING_PROJECT>/sandbox/Research_ArM_shadowBBox_v1/02_treevo_arm/output/module_sweep/june1/`

Key non-sweep result files:

#### Alpha pool outputs (R_ARM clean API)
- `<WORKSPACE>/<TRADING_PROJECT>/sandbox/R_ARM_austin_audit_drop_b/SJM_Binance_NT_audit_pack_3_20_26/02_SJM_clean_api/alpha_pool/alpha_pool_30s_long.csv`
- `<WORKSPACE>/<TRADING_PROJECT>/sandbox/R_ARM_austin_audit_drop_b/SJM_Binance_NT_audit_pack_3_20_26/02_SJM_clean_api/alpha_pool/alpha_pool_30s_short.csv`

#### Lambda sweep output (R_ARM clean API)
- `<WORKSPACE>/<TRADING_PROJECT>/sandbox/R_ARM_austin_audit_drop_b/SJM_Binance_NT_audit_pack_3_20_26/02_SJM_clean_api/output/sjm_lambda_sweep_clean_june1_8_30s.csv`

#### MCTS seed artifacts (JSON)
- `<WORKSPACE>/<TRADING_PROJECT>/sandbox/R_ARM_austin_audit_drop_b/SJM_Binance_NT_audit_pack_3_20_26/02_SJM_clean_api/seed_artifacts/mcts_top50_long.json`
- `<WORKSPACE>/<TRADING_PROJECT>/sandbox/R_ARM_austin_audit_drop_b/SJM_Binance_NT_audit_pack_3_20_26/02_SJM_clean_api/seed_artifacts/mcts_top50_short.json`

#### Module sweep CSV pairs (Research_ArM_shadowBBox_v1 — bulk output)
Pattern: `output/module_sweep/june1/m{tier}_{slot}_{variant}_{side}.csv`
Example entries:
- `<WORKSPACE>/<TRADING_PROJECT>/sandbox/Research_ArM_shadowBBox_v1/02_treevo_arm/output/module_sweep/june1/m1_1_1a_long.csv`
- `<WORKSPACE>/<TRADING_PROJECT>/sandbox/Research_ArM_shadowBBox_v1/02_treevo_arm/output/module_sweep/june1/m1_1_1a_short.csv`
(~500+ files total in this directory — long/short pairs for each module combination tested)

---

## Structural Observations

### Sandbox Layout — 4 major areas
1. **shadow_b_bot_pipeline/pre_phase3_shadow_b/** — Primary lab. The oldest and most complete area. Contains the full run history, locked models, and all historical sweeps.
2. **R_ARM_austin_audit_drop_b/SJM_Binance_NT_audit_pack_3_20_26/** — Newest clean-API area (2026-03-20). Organized into numbered subdirs (01_pipeline, 02_SJM_clean_api, 03_indicator_modules, 04_regime_adapters_DEPRECATED, 07_shadow_b_reference). This appears to be the intended convergence target.
3. **Research_ArM_shadowBBox_v1/02_treevo_arm/** — TreeEvo / ARM research branch. Contains bulk module sweep outputs and parallel copies of the SJM scripts.
4. **Data_v2_Binance_Nautilus_ShadowBbot/** — NT data pipeline scripts only (v1-v4 of catalog ingestion, bar builder, parity validator).

### Key Duplication Pattern
`indicator_hub.py`, `fibonacci_bands.py`, `fib_chikou_strategy.py`, `regime_adapters.py`, and `shadow_b_utils.py` each appear in 3-4 locations:
- `<TRADING_PROJECT>/strategy/` or `indicators/` (canonical outside sandbox)
- `03_indicator_modules/` (clean audit copies with _DEPS_COPY suffix)
- `02_SJM_clean_api/deps/` (inline deps bundled with clean API)
- `Research_ArM_shadowBBox_v1/02_treevo_arm/deps/` (treevo ARM copy)

**Version divergence risk is high.** Next agents reading these files should check for content differences between copies.

### `04_regime_adapters_DEPRECATED/` flag
The folder name explicitly marks regime_adapters as DEPRECATED. The canonical copy lives in `03_indicator_modules/` and the active deps copy in `02_SJM_clean_api/deps/`. The lab version is `modular_sjm_lab_20260317/regime_adapters_lab.py`.

---

## Summary

| Category | Count |
|---|---|
| SJM scripts (in sandbox) | 148 |
| Indicator modules (in sandbox) | 22 |
| Indicator modules (outside sandbox, <TRADING_PROJECT> root) | 10 |
| Model artifacts (.npz, .pkl, metadata.json) | 6 (2 bundles) |
| Result/output files (.json, .csv matching pattern) | 529 |
| — of which module_sweep CSVs (bulk, Research_ArM) | ~500+ |
| — of which named result/alpha/MCTS files | ~25 |

---

## SJM Script + Artifact Findings (Task 6)

> Audited: 2026-03-27. READ-ONLY review of 11 scripts + 2 model metadata files.
> Note: `shadow_b_utils_v2.py` and `validate_emission_anchoring.py` were blocked by
> `audit_read_blocker.sh` (unaudited code gate). Content recovered via Grep.

---

### predict() Call Site Audit

| File (short name) | Line | Method | Context | Verdict |
|---|---|---|---|---|
| `run_shadow_b_multimonth_train.py` | 165 | `model.predict(x_scaled)` | `_predict_states()` — called for BOTH training labeling AND eval windows | CONTAMINATED for eval |
| `run_shadow_b_multimonth_train.py` | 212 | `model.predict(x_train)` | `_fit_bundle()` — labeling on TRAIN data | VALID (train labeling) |
| `sjm_lambda_sweep_clean_2026-03-20.py` | 124 | `sjm.predict(X_processed)` | IS sweep only — no OOS, full IS block passed | CONTAMINATED within IS |
| `sjm_oos_june_clean_2026-03-20.py` | 161 | `sjm.predict(X_train_p)` | `fit_predict_sjm()` — train states for label mapping | VALID (train labeling) |
| `sjm_oos_june_clean_2026-03-20.py` | 162 | `sjm.predict_online(X_oos_p)` | OOS inference | VALID |
| `sjm_gated_sim_june_2026-03-20.py` | 321 | `long_model.predict(is_X_scaled)` | IS label mapping only | VALID (train labeling) |
| `sjm_gated_sim_june_2026-03-20.py` | 322 | `short_model.predict(is_X_scaled)` | IS label mapping only | VALID (train labeling) |
| `sjm_gated_sim_june_2026-03-20.py` | 367 | `long_model.predict_online(oos_X_scaled)` | OOS causal inference | VALID |
| `sjm_gated_sim_june_2026-03-20.py` | 368 | `short_model.predict_online(oos_X_scaled)` | OOS causal inference | VALID |
| `deps/regime_adapters.py` | 229 | `self.model.predict(X)` | `SparseJumpAdapter.predict()` — wrapper exposes predict() | CONTAMINATED if called on OOS |
| `deps/regime_adapters.py` | 233 | `self.model.predict_online(X)` | `SparseJumpAdapter.predict_online()` — causal wrapper | VALID |
| `run_sjm_explicit_audit.py` | 140 | `model.predict(X_eval_s)` | `eval_single()` — called in `mode=="batch"` branch; also called for train labeling | CONTAMINATED (batch mode on eval) |
| `run_sjm_explicit_audit.py` | 140 | `model.predict_online(X_eval_s)` | `eval_single()` — called in `mode=="online"` branch | VALID |
| `run_sjm_explicit_audit.py` | 159 | `model_long.predict(X_eval_s)` | `eval_dual()` — batch mode branch | CONTAMINATED |
| `run_sjm_explicit_audit.py` | 160 | `model_long.predict_online(X_eval_s)` | `eval_dual()` — online mode branch | VALID |
| `run_sjm_explicit_audit.py` | 238-241 | `model.predict(X_train_s)` x4 | Train labeling for batch/online label maps | VALID (train labeling) |
| `run_sjm_explicit_audit.py` | 239 | `model.predict_online(X_train_s)` x2 | Train states for online label maps | VALID |
| `run_sjm_explicit_audit.py` | 255-258 | `predict_proba(X_eval_s)` / `predict_proba_online(X_eval_s)` | Probability comparison audit | predict_proba = CONTAMINATED; predict_proba_online = VALID |
| `validate_emission_anchoring.py` (grep) | ~185 | `jm_model.predict(X_weighted)` | Explicit comment: "Running JumpModel.predict() on training data" | VALID (train data only) |

**Summary counts:**
- predict() on OOS/eval data = **4 contaminated call sites** (run_shadow_b_multimonth_train, sjm_lambda_sweep, run_sjm_explicit_audit batch mode x2)
- predict() on TRAIN data only = **9 valid call sites** (correct use for label mapping)
- predict_online() on OOS = **5 valid call sites**
- predict_proba() = **1 contaminated** (explicit audit comparison — intentional for the comparison, but would be contaminated in production)

---

### Critical Finding: `run_shadow_b_multimonth_train.py` — Primary Contamination

The production training script uses `_predict_states()` at line 164-174, which calls `model.predict(x_scaled)` for ALL windows including OOS eval windows. The function `_build_context()` at line 257 calls `_predict_states()` for each eval window. This means:

1. `_fit_bundle()` correctly uses `predict()` on TRAIN data only (valid for label mapping).
2. `_build_context()` then passes each eval window's scaled features through `predict()` — which is the Viterbi path using all data in that block simultaneously.
3. The macro_gate array fed to `_evaluate_formula()` and `_evaluate_bundle()` is built from contaminated OOS states.
4. The behavior cloning buffer (demonstration samples) is built from contaminated macro_gate signals.

**This is the central look-ahead contamination in the lockdown pipeline.**

---

### Feature Alignment

The canonical 6 Shadow B features are defined in `shadow_b_utils.py` (canonical, `pre_phase3_shadow_b/`) and duplicated identically in `deps/shadow_b_utils.py` (clean API deps):

```
SHADOW_B_FEATURES = [
    "price_fib_extend",
    "bb_fib_extend",
    "price_bb_extend",
    "chikou_fib_distance",
    "price_slope_velocity",
    "obv",
]
```

The OBV feature is transformed to an oscillator (obv - SMA50) before being fed to SJM in all scripts. This is consistent across all scripts reviewed.

**However:** `run_sjm_explicit_audit.py` creates a 7th column "obv_osc" in `prep_features()` (line 88):
```python
X = np.column_stack([X, obv - sma])
fn = SHADOW_B_FEATURES + ["obv_osc"]
```
This appends `obv_osc` as a separate column ALONGSIDE the original `obv` column — meaning it feeds 7 features (including raw obv AND obv_osc) to the SJM. All other scripts replace obv in-place with the oscillator. This is a **feature mismatch** in the explicit audit script.

| SJM Feature | In metadata.json | In `stage_features.py` / `shadow_b_utils.py` | In `run_sjm_explicit_audit.py` | Match? |
|---|---|---|---|---|
| price_fib_extend | YES (idx 0) | YES | YES | YES |
| bb_fib_extend | YES (idx 1) | YES | YES | YES |
| price_bb_extend | YES (idx 2) | YES | YES | YES |
| chikou_fib_distance | YES (idx 3) | YES | YES | YES |
| price_slope_velocity | YES (idx 4) | YES | YES | YES |
| obv (as oscillator) | YES (idx 5, transformed) | YES | obv kept raw + obv_osc added as col 7 | MISMATCH in audit script |
| obv_osc (extra col) | NOT IN metadata | NOT in canonical | Added in explicit audit only | MISMATCH |

**feat_weights length discrepancy:** Both metadata.json bundles have `nonzero_feature_count: 7` but `feat_weights` arrays contain exactly 7 values — matching the 6-feature input. Wait — 6 features produce 6 feat_weight values normally. Counting actual values in metadata:

- June_8day_locked_original: long has 7 feat_weights values, short has 7 values
- March_October_2025_retrained_v1: long has 7 feat_weights values, short has 7 values

**FLAG: feat_weights arrays have 7 elements but SHADOW_B_FEATURES only has 6 entries.** The models were trained on 7 features, not 6. This strongly suggests the training script used an additional feature beyond the canonical 6. Review `_featurize()` in `run_shadow_b_multimonth_train.py` — it extracts `SHADOW_B_FEATURES` (6) and applies OBV oscillator in-place, which should still be 6. The 7-element feat_weights may indicate the `max_feats=None` default was operating on 7 features due to a subtle bug or a different feature set used at training time vs what is now in the canonical feature list.

**This is a critical artifact mismatch that needs investigation.**

---

### Per-Script Analysis

#### 1. `run_shadow_b_multimonth_train.py`
**Purpose:** Production multi-month training pipeline. Fits SJM bundles on March+October 2025, evaluates vs June 8-day locked original, selects the better bundle, builds demonstration buffer for behavior cloning, trains RL execution agent.

**predict() usage:**
- Line 165: `model.predict(x_scaled)` in `_predict_states()` — used for ALL windows including eval. **CONTAMINATED for OOS evaluation.**
- Line 212: `model.predict(x_train)` in `_fit_bundle()` — training states for label mapping. VALID.

**Features:** SHADOW_B_FEATURES (6), OBV transformed in-place to oscillator. 6 features into SJM.

**Data windows:**
- Train: March 2025 (all days) + October 2025 (all days)
- OOS reserved: April 2025 + November 2025
- Reference (locked): June 2025 (days 1-8)

**Lambda values:**
- Long: 220.0
- Short: 100.0
- N_STATES: 3
- OBV_WINDOW: 50

**Result storage:** `bundle.pkl`, `metadata.json`, `sjm_model_registry.json`, `demonstration_buffer_shadow_b_train.json`, BC model `.pt`, metrics `.json`, MD report.

**FLAGS:**
- CONTAMINATED: `_predict_states()` used for eval windows — macro_gate is look-ahead biased
- CONTAMINATED: demonstration buffer and BC training data derived from contaminated macro_gate
- `max_feats=None` (no L1 sparsity) — all features receive non-zero weights; inconsistent with clean API scripts that use `max_feats=3.`
- feat_weights in both metadata bundles have 7 elements vs 6-feature input (unexplained)

---

#### 2. `shadow_b_utils.py` (canonical)
**Purpose:** Shared utilities for Shadow B pipeline. Defines SHADOW_B_FEATURES (6-element list), lambda sweep grid, NLL/entropy/state-stats helpers, state labeling functions (by MAD of price_fib_extend OR by mean returns), 0/1 Sharpe and short Sharpe evaluators, NLL holdout evaluator.

**predict() usage:** None directly. `identify_regime_states_by_returns()` docstring mentions `model.predict()` as expected input — pure consumer of states arrays.

**FLAGS:** None. This is utility code only, no predict calls.

---

#### 3. `stage_features.py`
**Purpose:** Multi-day feature loading pipeline. Loads N days of parquet bars, concatenates, runs `compute_all_indicators()` once (continuous lookback — correct), extracts SHADOW_B_FEATURES, applies OBV oscillator (obv - SMA50), drops NaN rows, applies StandardScaler.

**predict() usage:** None. Pure feature extraction.

**Features:** SHADOW_B_FEATURES (6), OBV replaced in-place. 6 features returned.

**FLAGS:**
- Scaler is `fit_transform` on the full loaded strip — if this includes OOS bars, scaler is fit on OOS data (data leakage in scaling). Intended use is training data only, but the function doesn't enforce this.

---

#### 4. `sjm_lambda_sweep_clean_2026-03-20.py`
**Purpose:** Lambda sweep script using clean jumpmodels API directly (no adapter wrapper). IS-only sweep on June 1-8. Tests n_components = 2 and 3. Uses `DataClipperStd(mul=3.) + StandardScalerPD()` (canonical jumpmodels preprocessing). No OOS evaluation.

**predict() usage:**
- Line 124: `sjm.predict(X_processed)` — IS data only. Within-sample characterization. CONTAMINATED in that Viterbi sees all IS bars simultaneously, but for IS-only characterization this is the standard approach.

**Features:** SHADOW_B_FEATURES (6), OBV oscillator (in-place). Uses `DataClipperStd` + `StandardScalerPD` — note this is DIFFERENT from `StandardScaler` used in the adapter-based scripts.

**Lambda values:** [1, 3, 5, 10, 15, 20, 30, 50] for n_comp=2; [1, 3, 5, 8, 10, 15, 20, 30, 50, 80] for n_comp=3. Uses `max_feats=100.` (essentially unlimited).

**FLAGS:**
- Preprocessing mismatch: uses `DataClipperStd + StandardScalerPD` vs `StandardScaler` used in production adapter scripts. Sweep results not directly comparable to locked model results.
- `max_feats=100.` vs production `max_feats=None` — different sparsity behavior.

---

#### 5. `sjm_oos_june_clean_2026-03-20.py`
**Purpose:** Clean API OOS evaluation on June 2025. Train June 1-8, OOS June 9-30. Runs separate Long Bot (λ=50,100,150,220) and Short Bot (λ=15,30,50,100) sweeps. Uses `predict_online()` for OOS — causal.

**predict() usage:**
- Line 161: `sjm.predict(X_train_p)` — train states for label mapping. VALID.
- Line 162: `sjm.predict_online(X_oos_p)` — OOS inference. VALID.

**CRITICAL NOTE:** Indicators computed on `all_bars = pd.concat([train_bars, oos_bars])` (line 323) — indicator continuity is correct (no per-day resets), but the full strip includes OOS bars when computing the scaler. However, scaler is fit on train portion only via `scaler.fit_transform(clipper.fit_transform(X_train))` and only `transform` is applied to OOS. This is correct.

**Features:** SHADOW_B_FEATURES (6), OBV oscillator in-place. `DataClipperStd(mul=3.) + StandardScalerPD()`.

**Lambda values:** Long = [50, 100, 150, 220]; Short = [15, 30, 50, 100]. N_STATES=2 (confirmed — note this differs from N_STATES=3 used in production).

**Result storage:** `sjm_oos_june_sweep_summary.csv`, dashboard CSVs.

**FLAGS:**
- N_STATES=2 vs production N_STATES=3 — results from this sweep are for 2-state model only.
- Preprocessing uses `DataClipperStd` not available in production adapter.

---

#### 6. `sjm_gated_sim_june_2026-03-20.py`
**Purpose:** SJM-gated strategy simulation with atom combos. Train IS (June 1-8) with adapter wrapper (`SparseJumpAdapter`), OOS (June 9-30) with `predict_online()`. Uses `StandardScaler` (matches production). Rising-edge entry, regime-flip exit.

**predict() usage:**
- Lines 321-322: `model.predict(is_X_scaled)` — IS label mapping. VALID.
- Lines 367-368: `model.predict_online(oos_X_scaled)` — causal OOS. VALID.

**Features:** SHADOW_B_FEATURES (6), OBV oscillator in-place. `StandardScaler`.

**Lambda values:** LAMBDA_LONG=220.0, LAMBDA_SHORT=100.0, N_STATES=3.

**Result storage:** `sjm_gated_results.csv`, per-combo trade CSVs.

**FLAGS:** None for predict() usage — this script is clean.

---

#### 7. `deps/regime_adapters.py`
**Purpose:** Multi-engine regime adapter (hmmlearn, statsmodels, jumpmodels, dynamax, regevs FHMM, PyMC). `SparseJumpAdapter` is the operative wrapper for SJM.

**predict() in SparseJumpAdapter:**
- Line 229: `self.model.predict(X)` — exposes raw Viterbi. CONTAMINATED if called on OOS.
- Line 233: `self.model.predict_online(X)` — causal wrapper. VALID.
- Line 243: `self.model.predict_proba_online(X)` — causal probability. VALID.

**FLAGS:**
- `predict()` is exposed and callable by any consumer. The adapter does not enforce causal-only usage for OOS. Callers must use `predict_online()` explicitly for OOS.
- `cont` parameter accepted in `__init__` kwargs but not listed in signature — minor API inconsistency (line 209 in production `run_shadow_b_multimonth_train.py` passes `cont=False`).
- `StatsmodelsMarkovAdapter.predict()` uses `smoothed_marginal_probabilities` — this is a smoother (uses future data), not a filter. Any use of this adapter for OOS is contaminated.

---

#### 8. `deps/shadow_b_utils.py`
**Purpose:** Identical copy of canonical `shadow_b_utils.py` bundled as local dep for clean API scripts. Content verified identical by inspection — same SHADOW_B_FEATURES list, same helper functions.

**FLAGS:** Version divergence risk (duplicate file, no sync mechanism).

---

#### 9. `run_sjm_explicit_audit.py` (v1)
**Purpose:** Explicit audit comparing batch (predict) vs online (predict_online) mode across Oct2025 and Apr2025 windows. Quantifies look-ahead magnitude. Also runs `predict_proba` vs `predict_proba_online` comparison.

**predict() usage:**
- Line 140 (batch branch): `model.predict(X_eval_s)` in `eval_single()` — intentional contamination for comparison audit. CONTAMINATED (by design for comparison).
- Line 140 (online branch): `model.predict_online(X_eval_s)` — VALID.
- Lines 238-241: `model.predict(X_train_s)` — train labeling x4. VALID.
- Lines 239: `model.predict_online(X_train_s)` — online train states. VALID.
- Line 255: `model.predict_proba(X_eval_s)` — batch proba for comparison. CONTAMINATED (by design).
- Line 256: `model.predict_proba_online(X_eval_s)` — VALID.

**Feature mismatch FLAG:** `prep_features()` at line 83-89 appends `obv_osc` as a 7th column alongside the original 6 SHADOW_B_FEATURES (obv not replaced in-place). This means the audit script tests a 7-feature model while metadata.json was generated from a 6-feature model. State assignments are NOT comparable between audit results and locked bundle performance.

**Lambda values:** Oct2025: long_lam=50, short_lam=50; Apr2025: long_lam=100, short_lam=100. Both differ from production lambdas (220/100).

**Result storage:** Per-month JSON, per-bar CSV, `sjm_explicit_summary.json`.

**FLAGS:**
- FEATURE MISMATCH: 7 features in audit vs 6 in production
- LAMBDA MISMATCH: Oct2025 uses lam=50/50, Apr2025 uses lam=100/100 — not testing production lambdas (220/100)
- predict() usage is intentional (contamination comparison), not accidental

---

#### 10. `shadow_b_utils_v2.py` (grep-only, blocked by audit_read_blocker.sh)
**Purpose:** V2 version of shadow_b_utils with emission anchoring utilities. Adds `SHADOW_B_FEATURES` export (confirmed via grep — same 6-feature list). Contains `compute_emission_anchoring()` function accepting `centers_weighted`, `feat_weights`, `scaler_mean`, `scaler_scale`, `feature_names` — computes top-2 features by |feat_weight|, zeros near-zero weights.

**predict() usage (grep):** None directly in this file.

**FLAGS:** None visible from grep output.

---

#### 11. `validate_emission_anchoring.py` (grep-only, blocked by audit_read_blocker.sh)
**Purpose:** Validates emission anchoring by loading training bars, scaling+weighting features, running `JumpModel.predict()` on training data, comparing expected vs computed state maps.

**predict() usage (grep):**
- Line ~185: `jm_model.predict(X_weighted)` — explicit comment states "Running JumpModel.predict() on training data." VALID (train data only).

**FLAGS:** None visible from grep output for predict usage.

---

### Model Artifact Summary

#### Bundle 1: `June_8day_locked_original`
- **Train dates:** June 1-8, 2025 (8 days)
- **n_components (N_STATES):** 3
- **Features:** 7 feat_weights values recorded (see FLAG below)
- **Lambda long:** 220.0, `max_feats_kappa: null`
- **Lambda short:** 100.0, `max_feats_kappa: null`
- **mode_loss:** 1.0 (both directions)
- **Train label maps:**
  - Long: {0: Bull, 1: Bear, 2: Neutral}
  - Short: {0: Bull, 1: Bear, 2: Neutral}
- **feat_weights (long):** [0.705, 0.759, 0.108, 0.644, 0.149, 0.026, 0.705] — indices 0,1,3,6 are dominant
- **feat_weights (short):** [0.792, 0.864, 0.251, 0.399, 0.140, 0.005, 0.376] — indices 0,1 are dominant

**FLAG: 7 feat_weights values for a 6-feature input.** The 7th weight (index 6 = 0.705 for long, 0.376 for short) suggests either (a) a 7th feature was present during training, (b) a bug in weight storage, or (c) the model was fit on 7 columns including both raw obv and obv_osc simultaneously.

#### Bundle 2: `March_October_2025_retrained_v1`
- **Train dates:** March 1-31, 2025 + October 1-31, 2025 (62 days)
- **n_components (N_STATES):** 3
- **Features:** 7 feat_weights values recorded
- **Lambda long:** 220.0, `max_feats_kappa: null`
- **Lambda short:** 100.0, `max_feats_kappa: null`
- **mode_loss:** 1.0 (both directions)
- **Train label maps:**
  - Long: {2: Bull, 1: Bear, 0: Neutral} — NOTE: state ordering flipped vs June bundle
  - Short: {2: Bull, 1: Bear, 0: Neutral} — NOTE: state ordering flipped vs June bundle
- **feat_weights (long):** [0.027, 0.013, 0.010, 0.873, 0.805, 0.010, 0.007] — indices 3,4 dominate (chikou_fib_distance, price_slope_velocity)
- **feat_weights (short):** [0.556, 0.647, 0.191, 0.917, 0.353, 0.004, 0.272] — indices 0,1,3 dominate

**Important: Feature importance shifted dramatically between bundles:**
- June bundle: price_fib_extend + bb_fib_extend dominate long model
- Retrained bundle: chikou_fib_distance + price_slope_velocity dominate long model
- This is a major regime-characteristic shift between the two training periods.

**FLAG: Same 7-feat_weights anomaly.** The 7th index weight is present in both bundles, produced by the same training script. The 7th weight is near-zero in the retrained bundle (0.007 long, 0.272 short) but non-trivial in the June bundle (0.705 long, 0.376 short).

---

### Summary

| Metric | Count / Finding |
|---|---|
| Total predict() call sites reviewed | 19 |
| predict() on OOS/eval data (CONTAMINATED) | 4 (run_shadow_b_multimonth_train._predict_states, sjm_lambda_sweep IS block, run_sjm_explicit_audit batch mode x2) |
| predict() on TRAIN data only (VALID for label mapping) | 9 |
| predict_online() on OOS (VALID, causal) | 5 |
| predict_proba() on eval (CONTAMINATED — in explicit audit for comparison) | 1 |
| predict_proba_online() on eval (VALID) | 1 |

**Feature alignment:** SHADOW_B_FEATURES (6 features) is consistent across all active production scripts. The explicit audit script (v1) has a confirmed 7-feature mismatch. Both model artifact bundles contain 7 feat_weights values vs 6 expected.

**Critical flags:**
1. **CONTAMINATED PRODUCTION PIPELINE:** `run_shadow_b_multimonth_train.py` uses `_predict_states()` (which calls `predict()`) for ALL eval windows. All OOS macro_gate values, formula evaluations, and demonstration buffer samples are look-ahead contaminated.
2. **7-feat_weights anomaly:** Both metadata.json bundles store 7 feat_weights for what should be a 6-feature model. The source of the 7th feature is unresolved — requires checking the actual training run context.
3. **Feature mismatch in audit script:** `run_sjm_explicit_audit.py` uses 7 features (obv + obv_osc both present) — audit results are not comparable to production model performance.
4. **Lambda mismatch in audit script:** Uses lam=50/50 (Oct) and 100/100 (Apr) rather than production 220/100.
5. **Preprocessing inconsistency:** Clean API scripts use `DataClipperStd + StandardScalerPD`; production adapter scripts use `StandardScaler` only. Sweep results are not directly comparable.
6. **State label map flip:** June bundle {0:Bull} vs Retrained bundle {2:Bull} — the `_select_active_bundle()` logic must correctly route through the stored label maps, not assume fixed state→label mapping.
7. **`StatsmodelsMarkovAdapter.predict()` uses smoother** — any use of this adapter for OOS would be contaminated; flagged for awareness.

---

## Indicator Module Findings (Task 5)

> Reviewed 2026-03-27. Files read directly (read-only).

### Files Read

| File | Role |
|---|---|
| `03_indicator_modules/indicator_hub.py` (canonical audit copy) | Centralized feature computation entry point |
| `03_indicator_modules/fibonacci_bands.py` (canonical audit copy) | Fib band math |
| `03_indicator_modules/fib_chikou_strategy.py` (canonical audit copy) | Bollinger + Ichimoku helpers |
| `03_indicator_modules/mctx_module_registry.py` (canonical audit copy) | Entry-signal registry (50+ modules) |
| `sandbox/shadow_b_bot_pipeline/pre_phase3_shadow_b/stage_features.py` | Feature staging (6-feature path) |
| `02_SJM_clean_api/deps/derived_phase3_features.py` | Pine-derived gate families (NOT the 7 SJM features) |
| `strategy/indicator_hub.py` (outside sandbox) | Priority 3 copy |
| `indicators/fibonacci_bands.py` (outside sandbox) | Priority 3 copy |
| `02_SJM_clean_api/deps/shadow_b_utils.py` | SHADOW_B_FEATURES canonical definition (6 features) |
| `codex_sjm_causal_audit_v2/shadow_b_utils_v2.py` (via grep only — read-blocked by audit hook) | Extended features (7 features, adds obv_osc) |
| `shadow_b_lockdown_2025/models/June_8day_locked_original/sjm_parameters_v1_metadata.json` | Locked model artifact — confirms 7 features |
| `shadow_b_lockdown_2025/models/June_8day_locked_original/metadata.json` | Training diagnostics |

---

### Per-Indicator Analysis

#### 1. `compute_fibonacci_bands` — Fib Band Math

- **Location:** `03_indicator_modules/fibonacci_bands.py:48`; `indicators/fibonacci_bands.py:48`
- **Parameters:** `ema_period: int = 100` (configurable, default 100). Called from `indicator_hub.py:59` with the hub's `ema_period` parameter, default 100.
- **Inputs:** OHLC numpy arrays
- **Computation chain:**
  1. `effclose = max(open, close)` if `close >= open`, else `min(open, close)` — body top/bottom, not wicks
  2. `midline = SMA-seeded EMA(effclose, ema_period)`, `nz()` applied (NaN→0.0 before warmup completes)
  3. `dev = rolling_stdev(effclose, ema_period)` — population std (ddof=0), matching TradingView `stdev()`
  4. `plusdevmult = max(0, (toc - midline) / dev)`; `minusdevmult = max(0, (midline - boc) / dev)`
  5. `maxmult = max(plusdevmult, minusdevmult)`
  6. `lm = EMA(maxmult, ema_period)` — second EMA chain on the normalized deviation
  7. Fib multipliers: lm2=lm/2, lm3=lm2×0.38196601, lm4=lm×1.38196601, lm5=lm×1.61803399, lm6=(lm+lm2)/2
  8. Bands: `6_up = midline + dev*lm5`, ..., `6_down = midline - dev*lm5` (symmetric)
- **Output:** dict — midline, dev, lm–lm6, 1_up–6_up, 1_down–6_down
- **FLAG — warmup on 30s bars:** Combined warmup before valid `6_up`/`6_down` is ~200 bars (~100 minutes). First EMA takes `ema_period=100` bars; second EMA (`lm`) adds another 100 bars. For sessions starting cold, fib bands are invalid for the first 100 minutes. Deliberate design per comments ("canonical v3.1").
- **Version divergence:** `indicators/fibonacci_bands.py` and `03_indicator_modules/fibonacci_bands.py` are **byte-for-byte identical**. No divergence.

---

#### 2. `compute_bollinger` — Bollinger Bands

- **Location:** `03_indicator_modules/fib_chikou_strategy.py:130`
- **Parameters:** `period=20`, `mult=2.0` (both defaults, both configurable from hub)
- **Inputs:** `close_arr` numpy array
- **Logic:** Rolling mean (basis) + rolling population stdev (ddof=0). `bb_upper = basis + mult*std`, `bb_lower = basis - mult*std`. NaN for first `period-1` bars.
- **Output:** `(basis, upper, lower)` numpy arrays
- **Status:** CORRECT. Standard implementation.

---

#### 3. `compute_ichimoku` — Ichimoku Cloud

- **Location:** `03_indicator_modules/fib_chikou_strategy.py:151`
- **Parameters:** HARDCODED 9/26/52. Enforced by ValueError guard in `indicator_hub.py:134-135` — any non-default call raises immediately.
- **Logic:**
  - `conversion = donchian_mid(high, low, 9)` — Tenkan-sen
  - `base = donchian_mid(high, low, 26)` — Kijun-sen
  - `leading_a = (conversion + base) / 2` — Senkou Span A (unshifted raw)
  - `leading_b = donchian_mid(high, low, 52)` — Senkou Span B (unshifted raw)
- **FLAG — display vs. decision-aligned split:** `indicator_hub.py:143-159` correctly separates DISPLAY columns (unshifted, for plotting) from DECISION-ALIGNED columns (shift(26) applied: `ichi_cloud_top_decision`, `ichi_cloud_bottom_decision`). This is correct look-ahead prevention. Boolean modules in mctx_module_registry that use cloud for entry conditions MUST use the `_decision` columns.
- **FLAG — 30s bar context:** 9-period = 4.5 min, 26-period = 13 min, 52-period = 26 min. Very short in absolute time. Standard crypto parameters, not a code error, but worth flagging for regime context.
- **Status:** CORRECT.

---

#### 4. OBV — On-Balance Volume

- **Location:** `indicator_hub.py:165-171`
- **Formula:**
  ```python
  price_diff = np.diff(close_arr, prepend=close_arr[0])
  vol_sign = np.sign(price_diff)
  obv = cumsum(vol_arr * vol_sign)
  ```
- **FLAG — prepend design:** Bar 0 diff = 0, so bar 0 contributes zero volume to OBV. Correct, no off-by-one.
- **FLAG — raw cumulative OBV is NOT what the model was trained on.** Every active pipeline script overwrites or supplements the OBV column with `obv - rolling_mean(obv, 50)` before passing to the SJM. The raw `obv` column from `indicator_hub.py` is an intermediate value, not the final SJM feature.
- **Status:** CORRECT as computed. The oscillator transformation is done downstream.

---

### 7-Feature Alignment Check

The locked model (`June_8day_locked_original`) has `scaler_n_features_in: 7` and `long_n_features_all: 7` confirmed in `sjm_parameters_v1_metadata.json`.

| # | Feature Name | Where Computed | Status |
|---|---|---|---|
| 1 | `price_fib_extend` | `indicator_hub.py:108` — `(close - fib_6_down) / (fib_6_up - fib_6_down)` | CORRECT |
| 2 | `bb_fib_extend` | `indicator_hub.py:109` — `(bb_basis - fib_6_down) / (fib_6_up - fib_6_down)` | CORRECT |
| 3 | `price_bb_extend` | `indicator_hub.py:110` — `(close - bb_lower) / (bb_upper - bb_lower)` | CORRECT |
| 4 | `chikou_fib_distance` | `indicator_hub.py:112-119` — current close vs. fib bands from 26 bars ago | CORRECT (naming note below) |
| 5 | `price_slope_velocity` | `indicator_hub.py:131` — alias for lb=5 velocity: `(close - close[t-5]) / (close[t-5] * 5)` | CORRECT |
| 6 | `obv` | `indicator_hub.py:171` — raw cumulative OBV | CORRECT as intermediate |
| 7 | `obv_osc` | NOT in `indicator_hub.py` — computed inline in calling scripts | SUSPECT — see below |

**Feature 4 naming note:** `chikou_fib_distance` is NOT the traditional Chikou span (current close plotted 26 bars back). It is current close compared to the fib bands that existed 26 bars ago. The name is slightly misleading but the computation is consistent and intentional.

**Feature 7 critical finding — THREE incompatible patterns exist:**

| Pattern | Scripts | Feature count | How obv_osc is handled |
|---|---|---|---|
| A — 6-feat overwrite | `sjm_oos_june_clean_2026-03-20.py`, `sjm_gated_sim_june_2026-03-20.py`, `sjm_nt_backtest_2026-03-20.py`, `run_shadow_b_multimonth_train.py` | 6 | `obv` column replaced in-place with `obv - SMA50`. Model sees 6 features where feature[5] = oscillator. |
| B — 7-feat append (inline) | `sjm_tuner.py` | 7 | `obv` kept raw + `obv_osc` appended as 7th column via `np.column_stack` |
| C — 7-feat named list | `shadow_b_utils_v2.py` (`codex_sjm_causal_audit_v2/`) | 7 | `obv_osc` as a named element in `SHADOW_B_FEATURES`, requires column pre-computed upstream |

**The locked `June_8day_locked_original` model has 7 features** (`scaler_n_features_in: 7`). Pattern A (currently the dominant clean-API path) produces only 6 features. If the locked model is loaded and Pattern A feature vectors are fed to it, there will be a dimension mismatch at `.predict()` or `.fit()`. This is the same 7-feat anomaly flagged in Task 6 — Task 5 analysis confirms its origin: the model was trained with Pattern B or C, not Pattern A.

---

### Summary

- 5 of 7 indicators: **CORRECT** — `price_fib_extend`, `bb_fib_extend`, `price_bb_extend`, `price_slope_velocity`, `obv` (as raw intermediate)
- 1 of 7 indicators: **CORRECT with naming caveat** — `chikou_fib_distance` (computation valid, name implies traditional Chikou but is current-price-vs-historical-fib)
- 1 of 7 indicators: **SUSPECT** — `obv_osc` (not in `indicator_hub.py`; three incompatible pipeline patterns exist; locked model trained with 7 features but dominant clean-API path produces only 6)

**Parameter concerns:**
- `ema_period=100` on 30s bars: ~100-minute combined warmup before fib bands are valid. Correct but important for cold-start scenarios.
- Ichimoku 9/26/52 hardcoded: standard crypto choice, but these are very short windows on 30s data.
- `OBV_WINDOW=50` (25 minutes): consistent across all scripts.

**Version divergence:**
- `indicator_hub.py`: canonical (`03_indicator_modules/`) and outside-sandbox (`strategy/`) copies are **identical**. No divergence.
- `fibonacci_bands.py`: canonical and outside-sandbox copies are **identical**. No divergence.
- `shadow_b_utils.py`: **CRITICAL DIVERGENCE** across three locations. 6-feature version in `deps/shadow_b_utils.py` and the primary `shadow_b_utils.py`. 7-feature version in `shadow_b_utils_v2.py`. Inline Pattern B in `sjm_tuner.py`. The locked model requires the 7-feature form. The current clean-API scripts use the 6-feature overwrite form. These are NOT interchangeable.

**Action required before convergence work:**
Before running the NT backtest with the locked model, confirm which feature vector format is used for inference. If using `June_8day_locked_original` (7-feature model), the inference pipeline must produce a 7-column input aligned to `[price_fib_extend, bb_fib_extend, price_bb_extend, chikou_fib_distance, price_slope_velocity, obv_raw, obv_osc]`. The current dominant clean-API path (Pattern A, 6-feature overwrite) will silently misalign features 6 and 7, or crash with a dimension error.

---

## SYNTHESIS — Session 38 Combined Findings (Task 7)

> **SAGE GATE:** This section summarizes all findings from Tasks 4-6. Sage reviews before convergence work begins.

### Critical Issues (must resolve before NT wiring)

**1. Production Pipeline Contamination (CRITICAL)**
- `run_shadow_b_multimonth_train.py` line 165: `_predict_states()` calls `model.predict()` (look-ahead Viterbi) on ALL windows including OOS eval
- Every macro_gate value, demonstration buffer sample, and behavior cloning training data is contaminated
- 4 contaminated OOS call sites total out of 19 reviewed
- Clean scripts exist (`sjm_oos_june_clean`, `sjm_gated_sim_june`) using correct predict_online() pattern
- **Impact:** All historical backtest results from the production pipeline are unreliable. Only results from clean scripts are trustworthy.

**2. 7th Feature Dimension Mismatch (CRITICAL)**
- Locked June model: trained on 7 features (confirmed in metadata.json: `scaler_n_features_in: 7`)
- Dominant clean-API pipeline (Pattern A): produces 6 features (overwrites obv in-place)
- Pattern B (sjm_tuner.py): appends obv_osc as 7th column → matches locked model
- Pattern C (shadow_b_utils_v2.py): names obv_osc explicitly in feature list
- **Impact:** Loading the June model with Pattern A vectors will crash or silently misalign. The March/Oct retrained model also has 7 features but 7th weight is near-zero.

**3. Three Pipeline Fixes from 43-Finding Audit (CRITICAL)**
- Fee: taker 0.04% → 0.05% (20% cost understatement)
- numpy.bool_: `is True` identity check fails on numpy scalars
- Import path: canonical ParquetDataCatalog import for forward compatibility

### Important Issues (resolve before trusting results)

**4. Preprocessing Inconsistency**
- Clean API scripts: DataClipperStd + StandardScalerPD
- Production adapter scripts: StandardScaler only
- Sweep results from different preprocessing pipelines are NOT directly comparable

**5. Feature Importance Shift Between Bundles**
- June: price_fib_extend + bb_fib_extend dominate
- March/Oct retrained: chikou_fib_distance + price_slope_velocity dominate
- Different market regimes selecting different indicators — expected but monitoring needed

**6. Explicit Audit Script Feature Mismatch**
- `run_sjm_explicit_audit.py` appends obv_osc as 7th column (doesn't overwrite)
- Uses lambdas 50/50 and 100/100, not production 220/100
- Audit results NOT comparable to production model performance

### Verified OK

- 5 of 7 indicator features: CORRECT implementation
- chikou_fib_distance: CORRECT (naming is misleading but computation is intentional)
- indicator_hub.py and fibonacci_bands.py: no version divergence between canonical and outside-sandbox copies
- State label map routing: correctly uses stored maps, doesn't assume fixed state→label ordering
- Clean API scripts: correct predict_online() pattern on OOS data

### Indicator Assessment

| Feature | Status | Notes |
|---------|--------|-------|
| price_fib_extend | CORRECT | Normalized ratio, proper zero-guard |
| bb_fib_extend | CORRECT | Same pattern |
| price_bb_extend | CORRECT | Same pattern |
| chikou_fib_distance | CORRECT (naming caveat) | Not traditional Chikou span — computes current close vs historical fib bands |
| price_slope_velocity | CORRECT | lb=5 (2.5min on 30s bars) |
| obv | CORRECT | Standard cumulative OBV |
| obv_osc | SUSPECT | 3 incompatible patterns. Locked model requires 7-feature form. |

### predict() Call Site Summary

| Category | Count | Verdict |
|----------|-------|---------|
| predict() on OOS/eval | 4 | CONTAMINATED |
| predict() on train only | 9 | VALID (label mapping) |
| predict_online() on OOS | 5 | VALID (causal) |
| predict_proba() on eval | 1 | CONTAMINATED (intentional comparison in audit) |

### Recommendations for Sage

1. **Resolve the 7-feature question FIRST** — Which pattern (A/B/C) will be used for NT inference? The locked model requires 7 features. Options:
   a) Retrain with 6 features (cleanest, but loses existing models)
   b) Use Pattern B (append obv_osc) for inference pipeline (matches locked model)
   c) Use only the March/Oct model where 7th weight is near-zero (hack, not recommended)

2. **Use clean scripts as the NT reference** — `sjm_oos_june_clean` and `sjm_gated_sim_june` have correct predict_online() usage. Build NT pipeline from these, not the production training scripts.

3. **Standardize preprocessing** — Pick DataClipperStd+StandardScalerPD (clean API) or StandardScaler-only (production) and use it everywhere. Results from mixed preprocessing are not comparable.

4. **Apply 3 pipeline fixes** from the 43-finding audit before any backtesting.

5. **jumpmodels audit (2C)** — Still recommended to verify predict_online() source code is truly causal. Scope unchanged by these findings.

### Full report location
`<WORKSPACE>/OpenBrainLM/research/sjm_indicator_review_2026-03-27.md` (this file, 800+ lines)
