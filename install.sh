#!/bin/bash

# Change directory to the dspy-pipeline directory (where pyproject.toml is located)
cd "$(dirname "$0")/dspy-pipeline" || { echo "Failed to change directory to dspy-pipeline"; exit 1; }

# Install dependencies using poetry
poetry install

# Install dependencies using poetry
poetry install

# Change back to repository root
cd .. || { echo "Failed to change directory back to repository root"; exit 1; }

# Make run.sh executable
chmod +x run.sh

echo "Installation complete!"
