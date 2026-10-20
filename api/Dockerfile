# Use Python 3.13-slim as base image (alpine is smaller, but longer to build and less compatible)
FROM python:3.13-slim
# Copy latest uv binary from official image
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

# Python environment variables:
# PYTHONDONTWRITEBYTECODE=1: Prevents Python from writing .pyc files (speeds up development and reduces container size)
# PYTHONUNBUFFERED=1: Prevents Python from buffering stdout/stderr (ensures log messages are output immediately)
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

# Copy the project into the image
ADD . /app

# Set work directory and install dependencies in a new environment
WORKDIR /app
# Sync the project, asserting the lockfile is up to date
RUN uv sync --locked

# Document that the container listens on port 8000
EXPOSE 8000

# Start the application using gunicorn
CMD uv run gunicorn --bind 0.0.0.0:8000 --workers 1 --worker-class uvicorn.workers.UvicornWorker main:app
