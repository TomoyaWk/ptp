FROM python:3.11-slim

WORKDIR /app

# Install uv
COPY --from=ghcr.io/astral-sh/uv:latest /uv /usr/local/bin/uv

# Set environment variables for uv
ENV UV_SYSTEM_PYTHON=1

# Copy dependency files and app directory
COPY pyproject.toml ./
COPY ./app ./app
COPY ./tests ./tests
COPY ./pytest.ini ./pytest.ini

# Install dependencies using uv (including dev dependencies for testing)
RUN uv sync

# Expose port
EXPOSE 8000

# Activate virtual environment and run the application
CMD [".venv/bin/uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
