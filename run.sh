#!/bin/bash

# Change directory to the dspy-pipeline directory
cd dspy-pipeline || { echo "Failed to change directory to dspy-pipeline"; exit 1; }

if [ ! -f pyproject.toml ]; then
    echo "pyproject.toml not found. Please run this script from the repository root."
    exit 1
fi

echo "Building project..."
poetry build

echo "Uninstalling previous version (if any)..."
pip uninstall -y autodev-pipeline || true

echo "Installing package globally for current user..."
pip install --user --upgrade dist/autodev_pipeline-0.1.2-py3-none-any.whl

echo "Running CLI command..."
audev
