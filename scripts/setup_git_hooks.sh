#!/bin/bash
# =============================================================================
# Setup Git Hooks — Install pre-commit hook from tracked template
# =============================================================================
# Purpose: Copies the tracked pre-commit template into .git/hooks/ and sets
#          the executable bit. Safe to run multiple times (idempotent).
#
# Usage:
#   bash scripts/setup_git_hooks.sh
#
# Run this once after cloning the repo, or after updating the template.
# =============================================================================

set -euo pipefail

# ---------------------------------------------------------------------------
# Resolve repo root (works from any subdirectory)
# ---------------------------------------------------------------------------
REPO_ROOT="$(git rev-parse --show-toplevel)"
TEMPLATE="$REPO_ROOT/docs/templates/pre-commit"
HOOK_DIR="$REPO_ROOT/.git/hooks"
HOOK_DEST="$HOOK_DIR/pre-commit"

# ---------------------------------------------------------------------------
# Verify the template exists
# ---------------------------------------------------------------------------
if [[ ! -f "$TEMPLATE" ]]; then
  echo "ERROR: Template not found at $TEMPLATE" >&2
  echo "  → Ensure docs/templates/pre-commit is tracked in the repository." >&2
  exit 1
fi

# ---------------------------------------------------------------------------
# Ensure .git/hooks directory exists (it always should, but be safe)
# ---------------------------------------------------------------------------
mkdir -p "$HOOK_DIR"

# ---------------------------------------------------------------------------
# Backup existing hook if present, then copy template
# ---------------------------------------------------------------------------
if [[ -f "$HOOK_DEST" ]]; then
    BACKUP_PATH="${HOOK_DEST}.bak.$(date +%s)"
    cp "$HOOK_DEST" "$BACKUP_PATH"
    echo "  Backed up existing hook to $BACKUP_PATH"
fi
cp "$TEMPLATE" "$HOOK_DEST"

# ---------------------------------------------------------------------------
# Set executable permission
# ---------------------------------------------------------------------------
chmod +x "$HOOK_DEST"

# ---------------------------------------------------------------------------
# Confirm
# ---------------------------------------------------------------------------
echo "Git hook installed successfully:"
echo "  Source:      $TEMPLATE"
echo "  Destination: $HOOK_DEST"
echo "  Permissions: $(ls -la "$HOOK_DEST" | awk '{print $1, $3, $4}')"
echo ""
echo "The audit gate pre-commit hook is now active."
echo "To reinstall after updating the template, run this script again."
