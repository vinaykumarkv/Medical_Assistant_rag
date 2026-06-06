# Use an optimized Python image
FROM python:3.11-slim

# Install light system dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    git \
    && rm -rf /var/lib/apt/lists/*

# Install uv globally inside the container
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

# Set work directory
WORKDIR /app

# Copy project files into the container
COPY . /app

# Install dependencies using pre-compiled wheels for llama-cpp to bypass high-RAM compilation
RUN PIP_EXTRA_INDEX_URL=https://github.io \
    uv pip install --system fastapi uvicorn langchain langchain-community chromadb langchain-huggingface llama-cpp-python numpy pandas pydantic tiktoken sentence-transformers pymupdf

# Expose the mandatory Hugging Face port
EXPOSE 7860

# Launch uvicorn directly
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "7860"]
