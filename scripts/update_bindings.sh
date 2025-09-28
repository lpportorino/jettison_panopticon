#!/bin/bash
# Script to check and update Python bindings for local development
# For CI environments, the workflow handles updates directly

set -e

echo "=== Checking for Python Bindings Updates ==="

# Store current directory
REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$REPO_ROOT"

# Check if we're in a git repository
if ! git rev-parse --git-dir > /dev/null 2>&1; then
    echo "Error: Not in a git repository"
    exit 1
fi

# Store current commit
cd c_data_python_bindings
CURRENT_COMMIT=$(git rev-parse HEAD)
cd ..

# Fetch latest changes from submodule remote
echo "Fetching latest bindings from remote..."
git submodule update --remote --merge c_data_python_bindings

# Check new commit
cd c_data_python_bindings
NEW_COMMIT=$(git rev-parse HEAD)
cd ..

# Check if submodule was updated
if [ "$CURRENT_COMMIT" = "$NEW_COMMIT" ]; then
    echo "✓ Python bindings are up to date"
    exit 0
else
    echo "⚠ Python bindings have been updated"
    echo "  From: $CURRENT_COMMIT"
    echo "  To:   $NEW_COMMIT"
    echo ""
    echo "Please commit the changes:"
    echo ""
    echo "  git add c_data_python_bindings"
    echo "  git commit -m \"chore: Update Python bindings submodule to latest\""
    echo "  git push"
    echo ""
    echo "Then run the build again."

    # Show what changed
    echo ""
    echo "Changes detected:"
    git diff --submodule c_data_python_bindings

    exit 1
fi