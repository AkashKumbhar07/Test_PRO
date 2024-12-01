# Quick Start Guide

This guide will help you get the distributed key-value store up and running quickly.

## Single Node Setup (5 minutes)

1. Prerequisites:
```bash
# Install Python 3.9 or higher
python --version  # Should show 3.9 or higher

# Install pip
pip --version
```

2. Clone and setup:
```bash
# Clone repository
git clone https://github.com/your-username/distributed-kv-store.git
cd distributed-kv-store

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

3. Run single node:
```bash
export FLASK_APP=run.py
export FLASK_ENV=development
export PORT=8000
flask run --port 8000
```

4. Test it works:
```bash
# In a new terminal:

# Create key-value
curl -X PUT -H "Content-Type: application/json" -d '{"value": "test123"}' http://localhost:8000/kv/mykey

# Read value
curl http://localhost:8000/kv/mykey

# Delete key
curl -X DELETE http://localhost:8000/kv/mykey
```

## Multi-Node Setup (10 minutes)

1. Prerequisites:
```bash
# Install Docker
docker --version
docker-compose --version
```

2. Start multi-node cluster:
```bash
cd docker
docker-compose up --build
```

3. Test cluster:
```bash
# Create on node 1
curl -X PUT -H "Content-Type: application/json" -d '{"value": "test123"}' http://localhost:8000/kv/mykey

# Read from node 2
curl http://localhost:8001/kv/mykey

# Delete from node 3
curl -X DELETE http://localhost:8002/kv/mykey
```

## Common Issues and Solutions

1. Port already in use:
   - Change port in environment variables or docker-compose.yml

2. Import errors:
   - Make sure you're in the virtual environment
   - Check your Python path

3. Docker issues:
   - Ensure Docker daemon is running
   - Try restarting Docker

## Next Steps

- Run the benchmark tool to test performance
- Check the main README for full API documentation
- Explore the test suite for example usage
- Review architecture documentation for system design details

For more detailed information, refer to the main README.md file.
