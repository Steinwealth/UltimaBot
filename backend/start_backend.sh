#!/bin/bash

# Ensure virtual environment is active
if [ ! -d ".venv" ]; then
  echo "Creating virtual environment..."
  python3.11 -m venv .venv
fi
source .venv/bin/activate

# Install dependencies if needed
pip install --upgrade pip
pip install -r requirements.txt

# Launch the backend with PYTHONPATH so 'app' is resolvable
PYTHONPATH=backend uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
