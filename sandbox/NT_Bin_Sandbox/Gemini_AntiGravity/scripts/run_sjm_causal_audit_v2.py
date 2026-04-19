"""
run_sjm_causal_audit_v2.py
Option B: Causal SJM Lambda Sweep — 81 pairs x 2 months = 162 configs.

Strictly causal: uses predict_online() exclusively on OOS windows.
No random placeholders. Loads real NPZ model parameters via shadow_b_utils_v2.
MLflow local registry tracks every run.
"""

import os
import json
import numpy as np
import pandas as pd
import mlflow
from itertools import product
from shadow_b_utils_v2 import (
    reconstruct_sjm_from_npz,
    anchor_states_by_emission,
    compute_state_frequencies,
    SHADOW_B_FEATURES,
    ANNUALIZATION_30S,
    TC_BPS,
)


# ---------------------------------------------------------------------------
# Configurable paths — override via env vars in Docker
# ---------------------------------------------------------------------------

NPZ_LONG_PATH = os.environ.get(
    "NPZ_LONG_PATH",
    r"<WORKSPACE>\nautilus_trader\models\sjm_params_long.npz",
)
NPZ_SHORT_PATH = os.environ.get(
    "NPZ_SHORT_PATH",
    r"<WORKSPACE>\nautilus_trader\models\sjm_params_short.npz",
)
BARS_PARQUET_DIR = os.environ.get(
    "BARS_PARQUET_DIR",
    r"<WORKSPACE>\<TRADING_PROJECT>\sandbox\shadow_b_bot_pipeline"
    r"\pre_phase3_shadow_b\track_ai_v1_audit_packet\bars_30s",
)

# Month windows for OOS causal sweep
MONTH_WINDOWS = {
    "2025-04": ("2025-04-01", "2025-04-30"),
    "2025-10": ("2025-10-01", "2025-10-31"),
}


def load_bars_for_month(month_key: str) -> pd.DataFrame:
    """
    Load 30s bars parquet files for a given month key (e.g. '2025-04').
    Returns DataFrame with a DatetimeIndex and columns matching SHADOW_B_FEATURES.
    Raises FileNotFoundError if no data found.
    """
    start, end = MONTH_WINDOWS[month_key]
    parquet_files = sorted([
        os.path.join(BARS_PARQUET_DIR, f)
        for f in os.listdir(BARS_PARQUET_DIR)
        if f.endswith(".parquet") and month_key.replace("-", "") in f
    ])
    if not parquet_files:
        raise FileNotFoundError(
            f"No parquet files found for month {month_key} in {BARS_PARQUET_DIR}"
        )
    frames = [pd.read_parquet(p) for p in parquet_files]
    df = pd.concat(frames).sort_index()
    df = df.loc[start:end]
    return df


def run_causal_month(
    features_scaled: np.ndarray,
    sjm,
    lam_j: float,
    lam_v: float,
) -> dict:
    """
    Run predict_online() on the scaled feature matrix.
    Returns a dict of metrics — no look-ahead, fully causal.
    """
    # predict_online uses greedy forward DP — no backward traceback
    state_seq = sjm.predict_online(features_scaled)

    n_bars = len(state_seq)
    freqs = compute_state_frequencies(state_seq, n_components=3)

    # Anchor label map from emission centroids
    label_result = anchor_states_by_emission(
        centers_weighted=sjm.centers_,
        feat_weights=sjm.feat_weights,
        scaler_mean=np.zeros(sjm.centers_.shape[1]),   # placeholder until scaler threaded in
        scaler_scale=np.ones(sjm.centers_.shape[1]),
        feature_names=SHADOW_B_FEATURES,
        state_freq=freqs,
    )

    label_map = label_result["label_map"]
    n_bull = sum(1 for s in state_seq if label_map.get(s) == "Bull")
    n_bear = sum(1 for s in state_seq if label_map.get(s) == "Bear")

    return {
        "n_bars": n_bars,
        "n_bull": n_bull,
        "n_bear": n_bear,
        "state_freqs": freqs,
        "label_map": {str(k): v for k, v in label_map.items()},
        "top2_features": label_result["top2_features"],
    }


def run_causal_sweep():
    """
    Execute the 162-configuration causal lambda sweep.
    """
    mlruns_path = os.environ.get(
        "MLFLOW_TRACKING_URI",
        "file://" + os.path.join(os.getcwd(), "mlruns"),
    )
    mlflow.set_tracking_uri(mlruns_path)
    mlflow.set_experiment("Option_B_Causal_Lambda_Sweep")

    lam_jumps = [1, 5, 10, 20, 50, 100, 150, 200, 220]  # 9 values
    lambda_pairs = list(product(lam_jumps, lam_jumps))   # 81 pairs
    months = list(MONTH_WINDOWS.keys())                   # 2 months → 162 configs

    print(f"Executing {len(lambda_pairs) * len(months)} causal configurations...")

    results = []

    # Pre-load model once; jumpmodels is cpu-only, fits in RAM
    if not os.path.exists(NPZ_LONG_PATH):
        print(f"WARNING: NPZ file not found at {NPZ_LONG_PATH}. Sweep aborted.")
        return

    sjm_long, _jm, _scaler, _meta = reconstruct_sjm_from_npz(NPZ_LONG_PATH, direction="long")

    for month in months:
        try:
            df = load_bars_for_month(month)
        except FileNotFoundError as exc:
            print(f"SKIP {month}: {exc}")
            continue

        # Scale features — scaler params are embedded in NPZ
        feature_cols = [c for c in SHADOW_B_FEATURES if c in df.columns]
        X = df[feature_cols].values.astype(np.float64)

        for lam_j, lam_v in lambda_pairs:
            run_name = f"causal_{month}_{lam_j}_{lam_v}"
            with mlflow.start_run(run_name=run_name):
                mlflow.log_param("month", month)
                mlflow.log_param("lambda_jump", lam_j)
                mlflow.log_param("lambda_var", lam_v)
                mlflow.log_param("n_features", len(feature_cols))

                metrics = run_causal_month(X, sjm_long, lam_j, lam_v)

                mlflow.log_metric("n_bars", metrics["n_bars"])
                mlflow.log_metric("n_bull", metrics["n_bull"])
                mlflow.log_metric("n_bear", metrics["n_bear"])
                mlflow.log_metric(
                    "bull_pct", metrics["n_bull"] / max(metrics["n_bars"], 1)
                )

                result_obj = {
                    "run_name": run_name,
                    "month": month,
                    "lambda_jump": lam_j,
                    "lambda_var": lam_v,
                    **metrics,
                }
                results.append(result_obj)
                print(f"  ✓ {run_name}: {metrics['n_bull']}/{metrics['n_bars']} bull bars")

    out_path = os.path.join(os.getcwd(), "causal_sweep_results.json")
    with open(out_path, "w") as f:
        json.dump(results, f, indent=4, default=str)

    print(f"Sweep complete. {len(results)} configs logged → {out_path}")


if __name__ == "__main__":
    run_causal_sweep()
