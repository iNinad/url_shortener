# Use the official Python base image for Python 3.12
FROM python:3.12-slim

# Add metadata to the image
LABEL maintainer="Ninad Deshpande"
LABEL description="Docker image for the URL shortener application"
LABEL version="1.0"

# Set environment variables for MongoDB and Memcache
ENV MONGODB_URI="mongodb://mongodb-container:27017/" \
    MEMCACHE_URI="memcached-container:11211"

# Set working directory in the container
WORKDIR /app

# Copy only the requirements file to the working directory
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application files to the working directory
COPY . .

# Expose port 8000 for the FastAPI application
EXPOSE 8000

# Command to run the FastAPI application
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
