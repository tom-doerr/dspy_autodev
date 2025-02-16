#!/bin/bash
cd dspy-pipeline || { echo "Failed to change directory to dspy-pipeline"; exit 1; }
if [ ! -f pyproject.toml ]; then
    echo "pyproject.toml not found. Please run this script from the repository root."
    exit 1
fi
echo "Building project..."
poetry build
echo "Installing package globally for current user..."
pip install --user dist/autodev-pipeline-0.1.0-py3-none-any.whl
echo "Running CLI command..."
audev
