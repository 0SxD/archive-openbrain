#!/usr/bin/env bash
# SessionStart: Save-Point Injection
# ====================================
# Fires the exact millisecond a new agent session boots.
# Reads external state files and injects them into the fresh context.
# This is the "resume from save point" mechanism for episodic operation.
#
# Source: Anthropic long-running agent patterns, Ralph loop, OAP.
# By injecting progress.txt and features.json on boot, the fresh agent
# orients from external state — not from conversation history.

# --- Candidate project roots (check cwd first, then known projects) ---
PROJECT_ROOTS=(
    "$(pwd)"
    "<WORKSPACE>/OpenBrainLM"
    "<WORKSPACE>/nautilus_trader"
    "<WORKSPACE>/<TRADING_PROJECT>"
)

FOUND_FEATURES=""
FOUND_PROGRESS=""

for ROOT in "${PROJECT_ROOTS[@]}"; do
    [ -z "$ROOT" ] && continue

    if [ -f "$ROOT/features.json" ] && [ -z "$FOUND_FEATURES" ]; then
        FOUND_FEATURES="$ROOT/features.json"
    fi

    if [ -f "$ROOT/progress.txt" ] && [ -z "$FOUND_PROGRESS" ]; then
        FOUND_PROGRESS="$ROOT/progress.txt"
    fi
done

# --- Build injection context ---
OUTPUT=""

if [ -n "$FOUND_FEATURES" ]; then
    # Extract only failing/pending features (not the whole file)
    FAILING=$(python3 -c "
import json, sys
try:
    with open('$FOUND_FEATURES') as f:
        data = json.load(f)
    items = []
    for feat in data.get('features', []):
        status = feat.get('status', '')
        if status in ('failing', 'pending'):
            blocker = feat.get('blocker', '')
            line = f\"  [{feat['id']}] {feat['name']} — {status.upper()}\"
            if blocker:
                line += f\" (BLOCKER: {blocker})\"
            items.append(line)
    if items:
        print('TASK BACKLOG (failing/pending):')
        print('\n'.join(items))
    else:
        print('TASK BACKLOG: All features passing.')
except Exception as e:
    print(f'TASK BACKLOG: Error reading features.json: {e}')
" 2>/dev/null)
    OUTPUT="${OUTPUT}${FAILING}\n\n"
fi

if [ -n "$FOUND_PROGRESS" ]; then
    # Inject last 20 lines of progress.txt (most recent events)
    RECENT=$(tail -20 "$FOUND_PROGRESS" 2>/dev/null)
    if [ -n "$RECENT" ]; then
        OUTPUT="${OUTPUT}RECENT PROGRESS (last 20 lines of progress.txt):\n${RECENT}\n\n"
    fi
fi

# --- Inject session state snapshot if it exists ---
STATE_FILE="<WORKSPACE>/OpenBrainLM/memory/.harness/session_state.json"
if [ -f "$STATE_FILE" ]; then
    STATE=$(cat "$STATE_FILE" 2>/dev/null)
    OUTPUT="${OUTPUT}LAST SESSION STATE: ${STATE}\n"
fi

# --- Output to stdout (injected into agent context by SessionStart hook) ---
if [ -n "$OUTPUT" ]; then
    echo -e "SAVE-POINT INJECTION (SessionStart hook)\n========================================\n${OUTPUT}"
    echo "BOOT-UP PROTOCOL: Read this context. Do NOT guess what happened previously."
    echo "Pick ONE failing/pending task from the backlog. Execute. Update progress.txt. Ask Sage for context."
fi
