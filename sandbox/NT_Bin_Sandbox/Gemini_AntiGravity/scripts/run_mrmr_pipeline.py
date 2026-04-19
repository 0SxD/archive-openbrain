"""
run_mrmr_pipeline.py
Option A: Evolutionary Indicator Pipeline Feature Screener

Screens 101 Boolean indicator columns down to 15-20 orthogonal features.
Pipeline: VarianceThreshold -> feature_engine.selection.MRMR
Configured per official trainindata.com docs:
    method="MIQ", max_features=20, regression=False

ZCR-verified: fit_transform returns numpy array; feature names retrieved
explicitly from the MRMR transformer's .selected_features_ attribute.
"""

import pandas as pd
import numpy as np
from sklearn.feature_selection import VarianceThreshold
from feature_engine.selection import MRMR


def run_mrmr_selection(X: pd.DataFrame, y: pd.Series):
    """
    Run the feature selection pipeline.

    Parameters
    ----------
    X : pd.DataFrame
        Input DataFrame of Boolean (0/1) indicator columns.
    y : pd.Series
        Target labels (e.g., Bull=1 / Bear=0) aligned to X's index.

    Returns
    -------
    X_selected : pd.DataFrame
        Reduced DataFrame containing only the mRMR-selected columns.
    final_features : list[str]
        Names of the selected features, in selection order.
    """
    print(f"Input shape: {X.shape}")

    # Step 1: Variance filter — drop any constant Boolean columns first.
    vt = VarianceThreshold(threshold=0.0)
    X_vt = pd.DataFrame(
        vt.fit_transform(X),
        columns=X.columns[vt.get_support()],
        index=X.index,
    )
    print(f"After VarianceThreshold: {X_vt.shape}")

    # Step 2: mRMR — selects up to 20 maximally relevant, minimally redundant features.
    # method="MIQ" = Mutual Information Quotient (relevance/redundancy ratio).
    # regression=False = classification mode (discrete targets).
    mrmr = MRMR(
        method="MIQ",
        max_features=20,
        regression=False,
    )
    mrmr.fit(X_vt, y)

    # selected_features_ is the canonical Feature-engine attribute listing kept columns.
    final_features = mrmr.selected_features_
    X_selected = mrmr.transform(X_vt)  # returns pd.DataFrame (feature-engine preserves it)

    print(f"Output shape: {X_selected.shape}")
    print(f"Selected {len(final_features)} features:")
    for feat in final_features:
        print(f"  - {feat}")

    return X_selected, final_features


if __name__ == "__main__":
    np.random.seed(42)
    n_samples, n_features = 1000, 101

    X_mock = pd.DataFrame(
        np.random.randint(0, 2, size=(n_samples, n_features)),
        columns=[f"ind_{i}" for i in range(1, n_features + 1)],
    )
    y_mock = pd.Series(np.random.randint(0, 2, size=n_samples), name="target")

    print("Running Option A mock screen (101 Boolean indicators → ≤20 selected)...")
    X_out, features = run_mrmr_selection(X_mock, y_mock)
    print(f"\nFinal selected features: {features}")
