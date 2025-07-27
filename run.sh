#!/bin/bash

# Exit on error
set -e

# Build frontend
echo "Building frontend..."
(cd frontend && npm install && npm run build)

# Run backend
echo "Launching backend..."
uv run interviewer
