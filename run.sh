#!/bin/bash

# Exit on error
set -e

# Build frontend
echo "Building frontend..."
(cd frontend && npm install && npm run build)

# Build backend image
echo "Building backend image..."
docker build -t interviewer-backend .

# Run backend container
echo "Launching backend..."
docker run --rm -p 8000:8000 interviewer-backend
