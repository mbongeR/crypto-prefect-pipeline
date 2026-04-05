# Use the official Python image
FROM python:3.12-slim

# Install system dependencies (git)
RUN apt-get update && apt-get install -y git && rm -rf /var/lib/apt/lists/*

# Set the working directory
WORKDIR /app

# FORCING the installation directly so Docker cannot ignore it
RUN pip install --no-cache-dir prefect prefect-email httpx

# Start the worker
CMD ["prefect", "worker", "start", "--pool", "my-local-pool"]