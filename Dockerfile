# Use the official Python image.
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

# Expose the port that the API will run on.
EXPOSE 8000



# Command to run the application.
CMD ["uv", "run", "api"]
