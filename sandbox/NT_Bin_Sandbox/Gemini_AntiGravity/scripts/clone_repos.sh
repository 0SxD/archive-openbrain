#!/usr/bin/env bash
# Clone required repositories for Option A (The Evolutionary Pipeline)

mkdir -p repos
cd repos

# 1. OPRO (Large Language Models as Optimizers - DeepMind)
echo "Cloning OPRO..."
git clone https://github.com/google-deepmind/opro.git || echo "OPRO already cloned"

# 2. ReEvo (Verbal Gradients for Evolution - AI4CO)
echo "Cloning ReEvo..."
git clone https://github.com/ai4co/reevo.git || echo "ReEvo already cloned"

# 3. feature-engine (For reference if needed, though installed via pip)
echo "Cloning feature_engine..."
git clone https://github.com/feature-engine/feature_engine.git || echo "feature_engine already cloned"

# 4. mRMR (smazzanti/mrmr - secondary option)
echo "Cloning mrmr..."
git clone https://github.com/smazzanti/mrmr.git || echo "mrmr already cloned"

echo "Repo acquisition complete."
