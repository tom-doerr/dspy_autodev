#!/bin/bash

# Change directory to the dspy-pipeline directory (where pyproject.toml is located)
#DSPY_PIPELINE_DIR="$(dirname "$0")/dspy-pipeline"
DSPY_PIPELINE_DIR="dspy-pipeline"

# Install dependencies using poetry
cd "$DSPY_PIPELINE_DIR" || { echo "Failed to change directory to dspy-pipeline"; exit 1; }
poetry install

# Build the project
echo "Building project..."
poetry build

# Uninstall previous version (if any)...
pip uninstall -y autodev-pipeline || true

# Install package globally for current user...
pip install --user --upgrade "dist/autodev_pipeline-0.1.2-py3-none-any.whl"

# Add the user's local bin directory to PATH if it's not already there
export PATH="$PATH:$HOME/.local/bin"

if ! echo "$PATH" | grep -q "$HOME/.local/bin"; then
  echo "Adding $HOME/.local/bin to PATH"
  export PATH="$PATH:$HOME/.local/bin"
fi

# Change back to repository root
cd .. || { echo "Failed to change directory back to repository root"; exit 1; }

# Make run.sh executable
chmod +x run.sh

echo "Installation complete!"
