FROM python:3.11-slim

WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Add current directory to Python path
ENV PYTHONPATH=/app

# Copy application code
COPY . .

# Run the application
CMD ["python", "src/app.py"]
