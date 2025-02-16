#!/bin/bash

# Change directory to the dspy-pipeline directory (where pyproject.toml is located)
cd "$(dirname "$0")/dspy-pipeline" || { echo "Failed to change directory to dspy-pipeline"; exit 1; }

# Install dependencies using poetry
poetry install

# Install dependencies using poetry
poetry install

# Change back to repository root
cd .. || { echo "Failed to change directory back to repository root"; exit 1; }

# Install package globally for current user...
pip install --user --upgrade dist/autodev_pipeline-0.1.1-py3-none-any.whl

# Add the user's local bin directory to PATH if it's not already there
export PATH="$PATH:$HOME/.local/bin"

if ! echo "$PATH" | grep -q "$HOME/.local/bin"; then
  echo "Adding $HOME/.local/bin to PATH"
  export PATH="$PATH:$HOME/.local/bin"
fi

# Make run.sh executable
chmod +x run.sh

echo "Installation complete!"
