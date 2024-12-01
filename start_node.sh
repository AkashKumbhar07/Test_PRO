#!/bin/bash

# Function to export environment variables
setup_env() {
    export PYTHONPATH=$PWD
    export FLASK_APP=src/app.py
    export FLASK_ENV=development
    export PORT=$1
    export NODE_ADDRESS="http://localhost:$1"
    export SEED_NODES=$2
}

# Check if port number is provided
if [ -z "$1" ]; then
    echo "Please provide a port number (8000, 8001, or 8002)"
    exit 1
fi

case $1 in
    8000)
        setup_env 8000 "http://localhost:8001,http://localhost:8002"
        ;;
    8001)
        setup_env 8001 "http://localhost:8000,http://localhost:8002"
        ;;
    8002)
        setup_env 8002 "http://localhost:8000,http://localhost:8001"
        ;;
    *)
        echo "Invalid port. Please use 8000, 8001, or 8002"
        exit 1
        ;;
esac

# Activate virtual environment if it exists
if [ -d "venv" ]; then
    source venv/bin/activate
fi

# Start the application
python src/app.py
