#!/bin/bash
# Make sure PYTHONPATH includes the current directory
cd "$(dirname "$0")"
export PYTHONPATH=$PWD
export FLASK_APP=src/app.py
export FLASK_ENV=development
export PORT=8000
export NODE_ADDRESS=http://localhost:8000
export SEED_NODES=http://localhost:8001,http://localhost:8002
python3 -m src.app
