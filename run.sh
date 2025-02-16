#!/bin/bash
cd dspy-pipeline || { echo "Failed to change directory to dspy-pipeline"; exit 1; }
poetry run dspy-pipeline
