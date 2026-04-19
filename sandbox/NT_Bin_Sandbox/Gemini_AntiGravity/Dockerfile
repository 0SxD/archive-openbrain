FROM python:3.11-slim

# System dependencies: build tools + git for pip VCS installs
RUN apt-get update && apt-get install -y \
    build-essential \
    git \
    && rm -rf /var/lib/apt/lists/*

# Core scientific stack — pinned to verified production versions
RUN pip install --no-cache-dir \
    numpy \
    pandas \
    scikit-learn \
    scipy \
    mlflow==3.10.1 \
    joblib==1.5.3 \
    feature-engine==1.9.4 \
    xgboost==3.2.0 \
    shap==0.51.0

# jumpmodels — correct repo: Yizhan-Oliver-Shu/jump-models (verified 2026-03-30)
# predict_online() is confirmed present in this repo (PyPI: jumpmodels)
RUN pip install --no-cache-dir git+https://github.com/Yizhan-Oliver-Shu/jump-models.git

# NautilusTrader — large binary, installed last to maximise layer cache reuse
RUN pip install --no-cache-dir nautilus_trader

WORKDIR /workspace
