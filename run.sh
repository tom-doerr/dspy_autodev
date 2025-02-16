#!/bin/bash
cd dspy-pipeline || { echo "Failed to change directory to dspy-pipeline"; exit 1; }
if [ ! -f pyproject.toml ]; then
    echo "pyproject.toml not found. Please run this script from the repository root."
    exit 1
fi
echo "Installing project dependencies..."
poetry install
echo "Running CLI command..."
poetry run dspy-pipeline
