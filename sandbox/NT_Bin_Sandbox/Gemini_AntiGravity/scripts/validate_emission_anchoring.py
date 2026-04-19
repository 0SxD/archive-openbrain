"""
validate_emission_anchoring.py — Validates anchor_states_by_emission() label maps.

For each NPZ bundle (June + March/Oct), for both directions (long + short):
1. Reconstructs SJM from NPZ via reconstruct_sjm_from_npz()
2. Loads training bars, scales + weights features, runs JumpModel.predict()
3. Computes state frequencies from predictions
4. Calls anchor_states_by_emission() with model params + frequencies
5. Compares computed label_map against expected map from metadata.json

Output: output/anchor_validation_report.json
Exit 0 if overall_pass, exit 1 if not.
"""

from __future__ import annotations

import json
import sys
import os
from datetime import datetime, timezone
from pathlib import Path

import numpy as np
import pandas as pd

# Local import — same directory
sys.path.insert(0, str(Path(__file__).parent))
from shadow_b_utils_v2 import (
    SHADOW_B_FEATURES,
    anchor_states_by_emission,
    compute_state_frequencies,
    reconstruct_sjm_from_npz,
)

# ---------------------------------------------------------------------------
# Paths
# ---------------------------------------------------------------------------

JUNE_NPZ = (
    "<WORKSPACE>/<TRADING_PROJECT>/sandbox/shadow_b_bot_pipeline"
    "/pre_phase3_shadow_b/shadow_b_lockdown_2025/models"
    "/June_8day_locked_original/sjm_parameters_v1.npz"
)
JUNE_META = (
    "<WORKSPACE>/<TRADING_PROJECT>/sandbox/shadow_b_bot_pipeline"
    "/pre_phase3_shadow_b/shadow_b_lockdown_2025/models"
    "/June_8day_locked_original/metadata.json"
)

MAROC_NPZ = (
    "<WORKSPACE>/<TRADING_PROJECT>/sandbox/shadow_b_bot_pipeline"
    "/pre_phase3_shadow_b/shadow_b_lockdown_2025/models"
    "/March_October_2025_retrained_v1/sjm_parameters_v1.npz"
)
MAROC_META = (
    "<WORKSPACE>/<TRADING_PROJECT>/sandbox/shadow_b_bot_pipeline"
    "/pre_phase3_shadow_b/shadow_b_lockdown_2025/models"
    "/March_October_2025_retrained_v1/metadata.json"
)

BAR_DIR = (
    "<WORKSPACE>/<TRADING_PROJECT>/sandbox/shadow_b_bot_pipeline"
    "/pre_phase3_shadow_b/track_ai_v1_audit_packet/bars_30s"
)

OUTPUT_PATH = (
    "<WORKSPACE>/<TRADING_PROJECT>/sandbox/shadow_b_bot_pipeline"
    "/pre_phase3_shadow_b/codex_sjm_causal_audit_v2/output"
    "/anchor_validation_report.json"
)


# ---------------------------------------------------------------------------
# Bar loader
# ---------------------------------------------------------------------------


def load_training_bars(dates: list[str], bar_dir: str) -> pd.DataFrame:
    """
    Load parquet bar files for the given dates and extract SHADOW_B_FEATURES columns.

    Parameters
    ----------
    dates : list of "YYYY-MM-DD" strings
    bar_dir : directory containing BTCUSDT_30s_YYYY-MM-DD.parquet files

    Returns
    -------
    pd.DataFrame with columns = SHADOW_B_FEATURES, rows = all bars concatenated.
    """
    frames = []
    missing = []
    for date_str in dates:
        fpath = os.path.join(bar_dir, f"BTCUSDT_30s_{date_str}.parquet")
        if not os.path.isfile(fpath):
            missing.append(fpath)
            continue
        df = pd.read_parquet(fpath, columns=SHADOW_B_FEATURES)
        frames.append(df)

    if missing:
        print(f"  WARNING: {len(missing)} bar files not found (skipped):")
        for m in missing[:5]:
            print(f"    {m}")
        if len(missing) > 5:
            print(f"    ... and {len(missing) - 5} more")

    if not frames:
        raise FileNotFoundError(
            f"No bar files found for dates {dates[:3]}... in {bar_dir}"
        )

    combined = pd.concat(frames, ignore_index=True)
    # Drop rows with any NaN in feature columns
    before = len(combined)
    combined = combined.dropna(subset=SHADOW_B_FEATURES)
    after = len(combined)
    if before != after:
        print(f"  Dropped {before - after} NaN rows from {before} total")

    return combined[SHADOW_B_FEATURES]


# ---------------------------------------------------------------------------
# Bundle validator
# ---------------------------------------------------------------------------


def validate_bundle(
    npz_path: str,
    meta_path: str,
    bundle_name: str,
) -> dict:
    """
    Validate both directions for one NPZ bundle.

    Returns a dict with keys "long" and "short", each containing:
        expected_map, computed_map, match, top2_features,
        state_freq, state_scores, degenerate_states
    """
    print(f"\n=== Bundle: {bundle_name} ===")

    # Load metadata to get train_dates and expected label maps
    with open(meta_path, "r") as f:
        metadata = json.load(f)

    train_dates: list[str] = metadata["train_dates"]
    print(f"  Train dates: {len(train_dates)} days ({train_dates[0]} .. {train_dates[-1]})")

    # Load training bars once (shared across directions — same scaler)
    print(f"  Loading {len(train_dates)} bar files ...")
    bars_df = load_training_bars(train_dates, BAR_DIR)
    X_raw = bars_df.values  # (N, 7) float64
    print(f"  Loaded {len(X_raw)} bars")

    results: dict = {}

    for direction in ("long", "short"):
        print(f"\n  Direction: {direction}")

        # --- Reconstruct model params ---
        sjm, jm, scaler_params, _ = reconstruct_sjm_from_npz(
            npz_path, metadata_path=None, direction=direction
        )

        scaler_mean = scaler_params["mean_"]    # (7,)
        scaler_scale = scaler_params["scale_"]  # (7,)
        feat_weights = sjm.feat_weights          # (7,)

        # --- Scale + weight features ---
        X_scaled = (X_raw - scaler_mean) / scaler_scale   # (N, 7)
        X_weighted = X_scaled * feat_weights               # (N, 7)

        # --- Run JumpModel.predict() on training data ---
        from jumpmodels import JumpModel  # noqa: PLC0415

        n_components = jm.centers_.shape[0]  # K=3

        jm_model = JumpModel(n_components=n_components, jump_penalty=0.0)
        jm_model.centers_ = jm.centers_
        jm_model.transmat_ = jm.transmat_
        jm_model.jump_penalty_mx = jm.jump_penalty_mx

        print(f"    Running JumpModel.predict() on {len(X_weighted)} weighted bars ...")
        states = jm_model.predict(X_weighted)  # (N,) int array

        # --- Compute state frequencies ---
        state_freq = compute_state_frequencies(
            np.asarray(states, dtype=int), n_components=n_components
        )
        freq_display = {k: f"{v:.3f}" for k, v in state_freq.items()}
        print(f"    State frequencies: {freq_display}")

        # --- Anchor states by emission ---
        result = anchor_states_by_emission(
            centers_weighted=sjm.centers_,
            feat_weights=feat_weights,
            scaler_mean=scaler_mean,
            scaler_scale=scaler_scale,
            feature_names=SHADOW_B_FEATURES,
            state_freq=state_freq,
        )

        computed_map: dict[int, str] = result["label_map"]

        # --- Get expected map from metadata ---
        raw_expected: dict[str, str] = metadata["diagnostics"][direction]["train_label_map"]
        expected_map: dict[int, str] = {int(k): v for k, v in raw_expected.items()}

        # --- Compare ---
        match = computed_map == expected_map
        status = "PASS" if match else "FAIL"
        print(f"    Expected : {expected_map}")
        print(f"    Computed : {computed_map}")
        print(f"    Result   : {status}")

        results[direction] = {
            "expected_map": {str(k): v for k, v in expected_map.items()},
            "computed_map": {str(k): v for k, v in computed_map.items()},
            "match": match,
            "top2_features": result["top2_features"],
            "state_freq": {str(k): round(v, 6) for k, v in state_freq.items()},
            "state_scores": {str(k): round(v, 6) for k, v in result["state_scores"].items()},
            "degenerate_states": result["degenerate_states"],
        }

    return results


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------


def main() -> None:
    print("validate_emission_anchoring.py — starting")
    print(f"Timestamp: {datetime.now(timezone.utc).isoformat()}")

    all_results: dict = {}

    # --- June bundle ---
    june_results = validate_bundle(
        npz_path=JUNE_NPZ,
        meta_path=JUNE_META,
        bundle_name="June_8day_locked_original",
    )
    all_results["June_8day_locked_original"] = june_results

    # --- March/Oct bundle ---
    maroc_results = validate_bundle(
        npz_path=MAROC_NPZ,
        meta_path=MAROC_META,
        bundle_name="March_October_2025_retrained_v1",
    )
    all_results["March_October_2025_retrained_v1"] = maroc_results

    # --- Overall pass ---
    all_matches = [
        all_results[bundle][direction]["match"]
        for bundle in all_results
        for direction in all_results[bundle]
    ]
    overall_pass = all(all_matches)

    # --- Build output ---
    report = {
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "bundles": all_results,
        "overall_pass": overall_pass,
    }

    # --- Write report ---
    out_path = Path(OUTPUT_PATH)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    with open(out_path, "w") as f:
        json.dump(report, f, indent=2)

    print("\n=== SUMMARY ===")
    for bundle, dirs in all_results.items():
        for direction, res in dirs.items():
            status = "PASS" if res["match"] else "FAIL"
            print(f"  {bundle} / {direction}: {status}")
    print(f"\nOverall: {'PASS' if overall_pass else 'FAIL'}")
    print(f"Report written to: {OUTPUT_PATH}")

    sys.exit(0 if overall_pass else 1)


if __name__ == "__main__":
    main()
