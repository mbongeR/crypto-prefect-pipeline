# Use the official Python image (matching your 3.12 environment)
FROM python:3.12-slim

# Set the working directory inside the container
WORKDIR /app

# Copy the requirements file into the container
COPY requirements.txt .

# Install the required packages
RUN pip install --no-cache-dir -r requirements.txt

# The command to start the worker when the container boots up
CMD ["prefect", "worker", "start", "--pool", "my-local-pool"]