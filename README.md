---
title: Medical RAG Agent
emoji: 🩺
colorFrom: blue
colorTo: red
sdk: docker
pinned: false
---

# 🩺 Medical Assistant RAG (Retrieval-Augmented Generation)

A production-grade, containerized Medical Assistant RAG application. The agent uses a local **Llama-3.2-3B-Instruct-GGUF** quantized model to process, index, and query medical documentation securely. Built with **FastAPI**, **LangChain**, and **ChromaDB**, and optimized for deployment to Hugging Face Spaces.

---

## 🚀 Key Features

*   **Local LLM Inference**: Powered by `llama-cpp-python` for highly efficient CPU execution.
*   **Vector Architecture**: Utilizes ChromaDB for persistent document vector indexing.
*   **Fast Integration Pipeline**: Fast dependency management and workspace setups using `uv`.
*   **Cloud Ready**: Fully Dockerized and configured directly for Hugging Face Spaces ecosystem limits.

---

## 📁 Repository Structure

```text
MEDICAL_ASSISTANT_RAG/
├── .venv/                 # Local isolated virtual environment
├── backend/
│   ├── __pycache__/
│   ├── __init__.py
│   └── app.py             # Core application routing logic
├── data/
│   └── medical.pdf        # Target medical reference (Tracked via Git LFS)
├── ui/                    # UI interface tier components
├── utils/                 # Extensible utility helper files
├── vector_db/             # Local database embeddings store
├── .env                   # Local infrastructure credentials
├── .gitattributes         # Git LFS file target maps
├── .gitignore             # Global repository omit maps
├── Dockerfile             # Multi-stage production container setup
├── main.py                # Global entrypoint script
├── pyproject.toml         # UV project configuration metadata
├── README.md              # Project documentation & space front-matter
└── uv.lock                # Deterministic dependency resolution lock
```

---

## 🛠️ Local Development Installation

### 1. Prerequisites
Ensure you have **Python 3.11**, **Git LFS**, and the **uv** package manager installed.

### 2. Clone and Setup Environment
```bash
# Clone the repository
git clone https://github.com/vinaykumarkv/Medical_Assistant_rag.git
cd Medical_Assistant_rag

# Initialize virtual environment and install dependencies
uv venv
uv pip install -r pyproject.toml
```

### 3. Initialize Git LFS (If modifying PDFs)
```bash
git lfs install
git lfs track "*.pdf"
```

### 4. Run the Application Localy
```bash
uvicorn main:app --host 0.0.0.0 --port 7860 --reload
```

---

## 🐳 Docker Container Compilation

To build and run the system locally exactly as it executes on Hugging Face Spaces:

```bash
# Build the container image
docker build -t medical-rag-agent .

# Run the container locally mapped to port 7860
docker run -p 7860:7860 medical-rag-agent
```

---

## 🌐 Continuous Deployment Pipelines

This project is configured to synchronize seamlessly with both GitHub and Hugging Face Spaces.

### Deploying Updates to Production

```bash
# Sync files to GitHub
git add .
git commit -m "Feature: Enhance RAG execution pipeline"
git push github main

# Deploy live directly to Hugging Face Spaces
git push hf main
```

---

## 🛡️ License
Distributed under the MIT License. See `LICENSE` for more information.
