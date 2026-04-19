"""
shadow_b_utils_v2.py — Emission-centroid anchoring utilities for SJM state labeling.

PURPOSE
-------
Provides deterministic, model-parameter-only state labeling for SparseJumpModel (SJM)
regimes — no price data required at label-assignment time.

ALGORITHM: emission_centroid_top2
---------------------------------
1. Recover unweighted centroids from SJM's weighted centers_ (centers_weighted / feat_weights).
2. Identify top-2 features by abs(feat_weights) magnitude.
3. Score each non-degenerate state by summing its top-2 centroid values (z-score space).
4. Highest score → Bull, lowest score → Bear, remainder → Neutral.
5. Degenerate states (below frequency threshold) → Neutral unconditionally.

VERIFICATION TARGETS
--------------------
These label maps come from metadata.json files and must be reproducible by
anchor_states_by_emission() given the correct model parameters:

  June long model:
    label_map = {0: "Bull", 1: "Bear", 2: "Neutral"}
    (state 2 is degenerate — frequency < 2%)

  March/Oct long model:
    label_map = {0: "Neutral", 1: "Bear", 2: "Bull"}

CONSTRAINTS
-----------
- numpy only at module level (no jumpmodels, no sklearn)
- json imported only inside reconstruct_sjm_from_npz()
- All functions have complete type hints
"""

from __future__ import annotations

import numpy as np

__all__ = [
    "SHADOW_B_FEATURES",
    "ANNUALIZATION_30S",
    "TC_BPS",
    "anchor_states_by_emission",
    "compute_state_frequencies",
    "reconstruct_sjm_from_npz",
]

# ---------------------------------------------------------------------------
# Constants (copied from shadow_b_utils.py, extended with obv_osc and TC_BPS)
# ---------------------------------------------------------------------------

SHADOW_B_FEATURES: list[str] = [
    "price_fib_extend",
    "bb_fib_extend",
    "price_bb_extend",
    "chikou_fib_distance",
    "price_slope_velocity",
    "obv",
    "obv_osc",
]

ANNUALIZATION_30S: float = (365 * 2880) ** 0.5  # ~1024.69 (30-second bars)
TC_BPS: float = 0.001  # 10 bps per transition (one-way)


# ---------------------------------------------------------------------------
# Core labeling function
# ---------------------------------------------------------------------------


def anchor_states_by_emission(
    centers_weighted: np.ndarray,    # (K, n_features) — SparseJumpModel.centers_
    feat_weights: np.ndarray,        # (n_features,) — SparseJumpModel.feat_weights
    scaler_mean: np.ndarray,         # (n_features,) — StandardScaler.mean_
    scaler_scale: np.ndarray,        # (n_features,) — StandardScaler.scale_
    feature_names: list[str],        # ordered feature names matching columns
    state_freq: dict[int, float],    # {state_int: fraction_of_training_bars}
    degenerate_threshold: float = 0.02,  # states below this freq → Neutral
) -> dict:
    """
    Label SJM states from model emission parameters alone (no price data).

    Parameters
    ----------
    centers_weighted : (K, n_features) ndarray
        SparseJumpModel.centers_ — weighted centroids in z-score space.
    feat_weights : (n_features,) ndarray
        SparseJumpModel.feat_weights — per-feature weights from sparse penalty.
    scaler_mean : (n_features,) ndarray
        StandardScaler.mean_ — passed through for caller reference; not used in scoring.
    scaler_scale : (n_features,) ndarray
        StandardScaler.scale_ — passed through for caller reference; not used in scoring.
    feature_names : list[str]
        Ordered feature names aligned to the column axis of centers_weighted.
    state_freq : dict[int, float]
        Fraction of training bars assigned to each state k.
    degenerate_threshold : float
        States with freq < this value are labeled "Neutral" unconditionally.

    Returns
    -------
    dict with keys:
        label_map        : {int: str}   — e.g. {0: "Bull", 1: "Bear", 2: "Neutral"}
        top2_features    : [str, str]   — names of top-2 features by |feat_weight|
        top2_indices     : [int, int]   — column indices of those features
        state_scores     : {int: float} — sum of top-2 unweighted centroid values per active state
        degenerate_states: [int]        — states below frequency threshold
        method           : str          — "emission_centroid_top2"
    """
    centers_weighted = np.asarray(centers_weighted, dtype=np.float64)
    feat_weights = np.asarray(feat_weights, dtype=np.float64)

    K = centers_weighted.shape[0]
    n_features = centers_weighted.shape[1]

    if len(feat_weights) != n_features:
        raise ValueError(
            f"feat_weights length {len(feat_weights)} does not match "
            f"centers_weighted n_features {n_features}"
        )
    if len(feature_names) != n_features:
        raise ValueError(
            f"feature_names length {len(feature_names)} does not match "
            f"centers_weighted n_features {n_features}"
        )

    # ------------------------------------------------------------------
    # Step 1: Identify degenerate states
    # ------------------------------------------------------------------
    degenerate_states: list[int] = []
    active_states: list[int] = []
    for k in range(K):
        freq = float(state_freq.get(k, 0.0))
        if freq < degenerate_threshold:
            degenerate_states.append(k)
        else:
            active_states.append(k)

    # ------------------------------------------------------------------
    # Step 2: Recover unweighted centroids (centers_weighted / feat_weights)
    # Handle division by zero: treat near-zero weights as 0 centroid.
    # ------------------------------------------------------------------
    safe_weights = feat_weights.copy()
    near_zero_mask = np.abs(safe_weights) < 1e-10
    safe_weights[near_zero_mask] = 1.0  # avoid division by zero

    centers_unweighted = centers_weighted / safe_weights[np.newaxis, :]
    # Zero out centroid values for near-zero-weight features
    centers_unweighted[:, near_zero_mask] = 0.0

    # ------------------------------------------------------------------
    # Step 3: Top-2 features by abs(feat_weights) magnitude
    # ------------------------------------------------------------------
    abs_weights = np.abs(feat_weights)
    sorted_indices = np.argsort(abs_weights)[::-1]  # descending
    top2_indices: list[int] = [int(sorted_indices[0]), int(sorted_indices[1])]
    top2_features: list[str] = [feature_names[i] for i in top2_indices]

    # ------------------------------------------------------------------
    # Step 4: Score each active state (sum of top-2 unweighted centroid values)
    # ------------------------------------------------------------------
    state_scores: dict[int, float] = {}
    for k in active_states:
        score = float(
            centers_unweighted[k, top2_indices[0]]
            + centers_unweighted[k, top2_indices[1]]
        )
        state_scores[k] = score

    # ------------------------------------------------------------------
    # Steps 5, 6, 7: Assign labels
    # ------------------------------------------------------------------
    label_map: dict[int, str] = {}

    # Degenerate states always get Neutral
    for k in degenerate_states:
        label_map[k] = "Neutral"

    n_active = len(active_states)

    if n_active == 0:
        # Step 7: No active states — all Neutral (already handled above)
        pass
    elif n_active == 1:
        # Step 6: Only 1 active state — can't determine direction → Neutral
        label_map[active_states[0]] = "Neutral"
    else:
        # Step 5: Sort active states by score descending
        sorted_active = sorted(active_states, key=lambda k: state_scores[k], reverse=True)
        label_map[sorted_active[0]] = "Bull"    # highest score
        label_map[sorted_active[-1]] = "Bear"   # lowest score
        for k in sorted_active[1:-1]:            # middle states
            label_map[k] = "Neutral"

    return {
        "label_map": label_map,
        "top2_features": top2_features,
        "top2_indices": top2_indices,
        "state_scores": state_scores,
        "degenerate_states": degenerate_states,
        "method": "emission_centroid_top2",
    }


# ---------------------------------------------------------------------------
# Helper: compute state frequencies from a state-assignment array
# ---------------------------------------------------------------------------


def compute_state_frequencies(
    state_sequence: np.ndarray,
    n_components: int,
) -> dict[int, float]:
    """
    Compute fraction of bars assigned to each state.

    Parameters
    ----------
    state_sequence : 1D integer array
        State assignments from model.predict() or similar.
    n_components : int
        Total number of states K (ensures all states appear in output).

    Returns
    -------
    dict[int, float]
        {state_index: fraction_of_total_bars} for k in range(n_components).
    """
    counts = np.bincount(state_sequence.astype(int), minlength=n_components)
    total = int(counts.sum())
    if total == 0:
        return {k: 0.0 for k in range(n_components)}
    return {k: float(counts[k]) / float(total) for k in range(n_components)}


# ---------------------------------------------------------------------------
# Helper: reconstruct SJM + JM + scaler from saved .npz parameters
# ---------------------------------------------------------------------------


def reconstruct_sjm_from_npz(
    npz_path: str,
    metadata_path: str | None = None,
    direction: str = "long",
):
    """
    Reconstruct SparseJumpModel, JumpModel, and StandardScaler from .npz params.

    The .npz file is expected to contain direction-prefixed arrays:
      long_*  or  short_*  (controlled by the `direction` parameter)
    and shared scaler arrays (no direction prefix).

    Key mapping
    -----------
    direction="long":
        sjm  <- long_centers, long_feat_weights, long_w
        jm   <- long_jm_centers, long_jm_transmat, long_jm_jump_penalty_mx
    direction="short":
        sjm  <- short_centers, short_feat_weights, short_w
        jm   <- short_jm_centers, short_jm_transmat, short_jm_jump_penalty_mx
    scaler (shared, no direction prefix):
        scaler_mean, scaler_scale, scaler_var

    Parameters
    ----------
    npz_path : str
        Path to the .npz parameter archive.
    metadata_path : str or None
        Optional path to a JSON metadata file. If provided, loaded and returned.
    direction : str
        "long" or "short" — selects which set of prefixed keys to load.

    Returns
    -------
    tuple: (sjm, jm, scaler_params, metadata)
        sjm          : SimpleNamespace with centers_, feat_weights, w
        jm           : SimpleNamespace with centers_, transmat_, jump_penalty_mx
        scaler_params: dict with mean_, scale_, var_ arrays
        metadata     : dict from JSON file, or None
    """
    import json
    from types import SimpleNamespace

    if direction not in ("long", "short"):
        raise ValueError(f"direction must be 'long' or 'short', got {direction!r}")

    prefix = direction + "_"
    data = np.load(npz_path, allow_pickle=False)

    sjm = SimpleNamespace(
        centers_=data[f"{prefix}centers"],
        feat_weights=data[f"{prefix}feat_weights"],
        w=data[f"{prefix}w"],
    )

    jm = SimpleNamespace(
        centers_=data[f"{prefix}jm_centers"],
        transmat_=data[f"{prefix}jm_transmat"],
        jump_penalty_mx=data[f"{prefix}jm_jump_penalty_mx"],
    )

    scaler_params: dict[str, np.ndarray] = {
        "mean_": data["scaler_mean"],
        "scale_": data["scaler_scale"],
        "var_": data["scaler_var"],
    }

    metadata = None
    if metadata_path is not None:
        with open(metadata_path, "r") as f:
            metadata = json.load(f)

    return sjm, jm, scaler_params, metadata
