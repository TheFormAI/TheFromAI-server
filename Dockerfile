FROM python:3.12-slim

# Install required tools
RUN apt-get update && apt-get install -y curl build-essential && \
    rm -rf /var/lib/apt/lists/*

# Install uv to user space
RUN curl -LsSf https://astral.sh/uv/install.sh | sh

# Make sure uv is on PATH
ENV PATH="/root/.local/bin/:$PATH"

# Optional: Verify uv works
RUN uv --version

# Set workdir
WORKDIR /app

# Copy files
COPY . .

# Install Python packages with uv
RUN uv sync

RUN uv add uvicorn

# Expose FastAPI port
EXPOSE 8000


# Run the app
CMD [".venv/bin/uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
