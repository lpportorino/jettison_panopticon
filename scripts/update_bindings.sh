#!/bin/bash
# Script to ensure we have the latest Python bindings before building
# This script will update the submodule and commit if there are changes

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

# Fetch latest changes from submodule remote
echo "Fetching latest bindings from remote..."
git submodule update --remote --merge c_data_python_bindings

# Check if submodule has changes
if git diff --quiet --exit-code c_data_python_bindings; then
    echo "✓ Python bindings are up to date"
    exit 0
else
    echo "⚠ Python bindings have been updated"

    # Check if we're in CI environment
    if [ -n "$CI" ] || [ -n "$GITHUB_ACTIONS" ]; then
        echo "=== CI Environment Detected ==="
        echo "Creating automated commit and push..."

        # Configure git for CI
        git config user.name "GitHub Actions Bot"
        git config user.email "actions@github.com"

        # Add and commit the submodule update
        git add c_data_python_bindings
        git commit -m "chore: Update Python bindings submodule to latest

Auto-updated by CI build process to ensure latest bindings are used.
This commit was automatically generated." || {
            echo "Failed to commit changes"
            exit 1
        }

        # Push the changes
        if [ -n "$GITHUB_TOKEN" ]; then
            # Use GITHUB_TOKEN if available
            git push "https://${GITHUB_TOKEN}@github.com/${GITHUB_REPOSITORY}.git" HEAD:${GITHUB_REF#refs/heads/} || {
                echo "Failed to push changes with GITHUB_TOKEN"
                exit 1
            }
        else
            # Try regular push
            git push || {
                echo "Failed to push changes"
                exit 1
            }
        fi

        echo "✓ Successfully updated and pushed Python bindings"
        echo "⚠ IMPORTANT: Build cancelled - will restart with updated bindings"

        # Exit with special code to indicate build should be restarted
        exit 78  # Custom exit code to signal restart needed

    else
        echo "=== Local Environment Detected ==="
        echo ""
        echo "Python bindings have been updated. Please commit the changes:"
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
fi