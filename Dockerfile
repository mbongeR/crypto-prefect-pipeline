# Use the official Python image
FROM python:3.12-slim

# Install system dependencies 
RUN apt-get update && apt-get install -y git && rm -rf /var/lib/apt/lists/*

# Set the working directory inside the container
WORKDIR /app

# Copy the requirements file into the container
COPY requirements.txt .

# Install the required packages with a longer timeout
RUN pip install --default-timeout=100 --no-cache-dir -r requirements.txt

# The command to start the worker when the container boots up
CMD ["prefect", "worker", "start", "--pool", "my-local-pool"]