# src/Dockerfile
FROM python:3.11-slim

WORKDIR /opt/app

# Install required packages
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy all Python source files
COPY . .

# Run data generator by default
CMD ["python", "data_generator.py"]
