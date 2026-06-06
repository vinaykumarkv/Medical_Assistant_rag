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

# Copy project files into the container
COPY . /app

# Install application dependencies straight to system packages
RUN uv pip install --system fastapi uvicorn langchain langchain-community chromadb langchain-huggingface llama-cpp-python numpy pandas pydantic tiktoken sentence-transformers pymupdf

# Download the ACTUAL model binary from the Hugging Face repository 
# (Replace 'meta-llama/Llama-3.2-3B-Instruct' below with your target repo if needed)
RUN python -c " \
import urllib.request; \
urllib.request.urlretrieve('https://huggingface.co', 'llama-3.2-3b-instruct-q4_k_m.gguf') \
"

# Expose the mandatory Hugging Face port
EXPOSE 7860

# Fire up uvicorn directly targeting your main entrypoint file on port 7860
CMD ["uvicorn", "main.py:app", "--host", "0.0.0.0", "--port", "7860"]
