# SJM Parameter Extraction — Verification Report
> Date: 2026-03-26 | Agent: Opus (orchestrator verification) | Status: VERIFIED

## Verdict: Sage's Approach is CORRECT with Corrections

The "Decoupled Parameter Persistence" approach is the right pattern. However, the specific
attribute names Sage listed need correction based on the actual jumpmodels source code.

## Source: jumpmodels Library
- **Repo:** https://github.com/Yizhan-Oliver-Shu/jump-models
- **PyPI:** https://pypi.org/project/jumpmodels/
- **Author:** Yizhan Oliver Shu
- **API style:** scikit-learn compatible (BaseEstimator subclass)

## Verified Attribute Map

### SparseJumpModel (top-level fitted attributes)
| Attribute | Type | Shape | Description |
|-----------|------|-------|-------------|
| `w` | ndarray | (n_features,) | Feature weights from Lasso optimization |
| `feat_weights` | ndarray | (n_features,) | sqrt(w) — applied to input features |
| `centers_` | ndarray | (n_components, n_features) | Weighted cluster centers |
| `labels_` | ndarray | (n_samples,) | In-sample state assignments |
| `proba_` | ndarray | (n_samples, n_components) | In-sample probabilities |
| `n_features_all` | int | scalar | Total input features |
| `jm_ins` | JumpModel | object | Fitted inner JumpModel instance |

### JumpModel (inner model — jm_ins attributes)
| Attribute | Type | Shape | Description |
|-----------|------|-------|-------------|
| `centers_` | ndarray | (n_components, n_features) | Cluster centroids |
| `transmat_` | ndarray | (n_components, n_components) | Transition probability matrix |
| `labels_` | ndarray | (n_samples,) | Optimal label sequence |
| `proba_` | ndarray | (n_samples, n_components) | Probability matrix |
| `jump_penalty_mx` | ndarray | (n_components, n_components) | Jump penalty matrix |

### StandardScaler (sklearn)
| Attribute | Type | Shape | Description |
|-----------|------|-------|-------------|
| `mean_` | ndarray | (n_features,) | Per-feature mean |
| `scale_` | ndarray | (n_features,) | Per-feature std dev |
| `var_` | ndarray | (n_features,) | Per-feature variance |
| `n_features_in_` | int | scalar | Number of features seen |
| `n_samples_seen_` | int | scalar | Number of samples seen |

Source: https://scikit-learn.org/stable/modules/generated/sklearn.preprocessing.StandardScaler.html

## Corrections to Sage's Original Attribute List

Sage listed: `trans_mat_`, `means_`, `covars_`, `weights_`, `coef_`

**Corrected names:**
- `trans_mat_` → **`transmat_`** (no second underscore, on jm_ins)
- `means_` → **`centers_`** (jumpmodels uses "centers" not "means")
- `covars_` → **NOT PRESENT** (jumpmodels is NOT a GMM — no covariance matrices)
- `weights_` → **`w`** and **`feat_weights`** (on SparseJumpModel, not jm_ins)
- `coef_` → **NOT PRESENT** (this is a sklearn naming convention, not jumpmodels)

## Recommended Serialization Format

**.npz (numpy archive)** is correct and sufficient. Alternatives considered:
- JSON: works but requires .tolist() conversion, loses dtype precision
- safetensors: overkill for small parameter sets, adds HuggingFace dependency
- ONNX: designed for inference graphs, not raw parameter storage

.npz advantages: native numpy, zero dependencies, preserves dtypes, compact.

## What Must Be Extracted (Complete List)

```
# From SparseJumpModel:
sjm.w                          # (n_features,) feature weights
sjm.feat_weights               # (n_features,) sqrt(w)
sjm.centers_                   # (n_components, n_features) cluster centers
sjm.n_features_all             # int
sjm.jm_ins.centers_            # (n_components, n_features) inner centers
sjm.jm_ins.transmat_           # (n_components, n_components) transition matrix
sjm.jm_ins.jump_penalty_mx    # (n_components, n_components) penalty matrix

# From StandardScaler:
scaler.mean_                   # (n_features,)
scaler.scale_                  # (n_features,)
scaler.var_                    # (n_features,)
scaler.n_features_in_          # int
scaler.n_samples_seen_         # int

# Init params (needed to reconstruct):
sjm.n_components               # int
sjm.max_feats                  # float
sjm.jump_penalty               # float
sjm.cont                       # bool
```

## Reassembly Pattern (verified against sklearn docs)

StandardScaler reconstruction by setting attributes on a fresh instance is a
documented, supported pattern in scikit-learn. The jumpmodels library inherits
from BaseEstimator, which provides get_params()/set_params() — same pattern applies.

## 3-Step Airlock: CONFIRMED CORRECT

1. **Extract** (sandbox venv with torch): Load bundle.pkl, extract arrays, save as .npz
2. **Reassemble** (NT venv): Create fresh SJM + Scaler, inject parameters
3. **Wire** (NT strategy): Load .npz in Strategy.on_start(), run backtest

This pattern is standard MLOps practice for moving models between environments.
