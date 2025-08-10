#!/bin/bash

# Exit on error
set -e

# Build frontend
echo "Building frontend..."
(cd frontend && npm install && npm run build)

# Build backend image
echo "Building backend image..."
docker build --no-cache -t api .

# Run backend container
echo "Launching backend..."
docker run --rm -p 8000:8000 api
