#!/bin/bash
cd "$(dirname "$0")"
export PYTHONPATH=$PWD
export FLASK_APP=src/app.py
export FLASK_ENV=development
export PORT=8001
export NODE_ADDRESS=http://localhost:8001
export SEED_NODES=http://localhost:8000,http://localhost:8002
python3 -m src.app
