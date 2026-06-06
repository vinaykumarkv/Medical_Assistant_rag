# Use an optimized Python image
FROM python:3.11-slim

# Install system dependencies required to build llama-cpp-python binaries
RUN apt-get update && apt-get install -y \
    build-essential \
    cmake \
    git \
    && rm -rf /var/lib/apt/lists/*

# Install uv globally inside the container
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

# Set work directory
WORKDIR /app

# Copy lockfiles/dependency maps first to leverage Docker caching layers
COPY . /app

# Install application dependencies directly into the system environment using uv
RUN uv pip install --system fastapi uvicorn langchain langchain-community chromadb langchain-huggingface llama-cpp-python numpy pandas pydantic tiktoken sentence-transformers pymupdf

# Download the model directly into the image layer from Hugging Face during build
# This ensures the space boots instantly without downloading models on startup
RUN uv run python -c " \
import urllib.request; \
urllib.request.urlretrieve('https://huggingface.co', 'llama-3.2-3b-instruct-q4_k_m.gguf') \
"

# Expose the mandatory Hugging Face port
EXPOSE 7860

# Fire up the production ASGI production cluster pointing to port 7860
CMD ["uv", "run", "uvicorn", "backend.app:app", "--host", "0.0.0.0", "--port", "7860"]
