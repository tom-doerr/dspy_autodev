#!/bin/bash

# Change directory to the project root
cd "$(dirname "$0")"

# Install dependencies using poetry
poetry install

# Make run.sh executable
chmod +x run.sh

echo "Installation complete!"
