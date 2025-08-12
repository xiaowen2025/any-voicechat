# Stage 1: Build the frontend
FROM node:20-slim as frontend-builder

WORKDIR /app/frontend

# Copy frontend package files
COPY frontend/package.json frontend/package-lock.json ./

# Install frontend dependencies
RUN npm install

# Copy the rest of the frontend source code
COPY frontend/ ./

# Build the frontend
RUN npm run build

# Stage 2: Build the backend
FROM python:3.11-slim

# Set the working directory in the container.
WORKDIR /app

# Install uv
RUN pip install uv

# Copy the dependency files.
COPY pyproject.toml uv.lock ./

# Install dependencies using uv.
RUN uv sync

# Copy the rest of the application code.
COPY . .

# Install the project in editable mode
RUN uv pip install -e . --system

# Copy the built frontend from the builder stage
COPY --from=frontend-builder /app/frontend/dist ./frontend/dist

# Expose the port that the API will run on.
EXPOSE 8000

# Command to run the application.
CMD ["uv", "run", "api"]
