from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse, HTMLResponse
from pydantic import BaseModel
from langchain_community.vectorstores import Chroma
from langchain_huggingface import HuggingFaceEmbeddings
from llama_cpp import Llama
import json
import os

# Import your custom modules mapped to your project layout
from utils.llm_client import llm
from vector_db.embedding_gen import db

app = FastAPI()

# Allow your local HTML file to communicate with the FastAPI backend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class ChatRequest(BaseModel):
    message: str

# System prompt: defines the model's role and strict grounding rules.
# System prompt: wrapped in Llama 3.2 role formatting tokens
qna_system_message = """<|begin_of_text|><|start_header_id|>system<|end_header_id|>

You are a clinical decision-support assistant with access to the Merck Manual of Diagnosis and Therapy.

Instructions:
- Answer ONLY using information present in the provided context.
- Cite the relevant section if it can be identified from the context.
- If the answer cannot be derived from the context, respond exactly: "I don't know based on the provided context."
- Do NOT mention the context or the retrieval mechanism in your answer.
- Be concise, accurate, and clinically precise.<|eot_id|>"""

# User template: wrapped in Llama 3.2 user role tokens
qna_user_message_template = """<|start_header_id|>user<|end_header_id|>

###Context
Here are relevant passages retrieved from the Merck Manual:
{context}

###Question
{question}<|eot_id|>
<|start_header_id|>assistant<|end_header_id|>

"""


# New Route: Serves index.html from your /ui folder dynamically
@app.get("/", response_class=HTMLResponse)
async def serve_ui():
    # Dynamically find the absolute path to your project root and look inside /ui
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    ui_file_path = os.path.join(base_dir, "ui", "index.html")
    
    try:
        with open(ui_file_path, "r", encoding="utf-8") as f:
            return f.read()
    except FileNotFoundError:
        return f"<h3>Error: Could not find index.html at {ui_file_path}</h3>"

def generate_rag_response(user_query: str):
    # Retrieve context chunks from the local Vector DB
    docs = db.similarity_search(user_query, k=3)
    context = "\n\n".join([doc.page_content for doc in docs])
    
    global qna_system_message, qna_user_message_template
    
    # Construct a raw text prompt for Llama 3.2 Instruct format
    user_message = qna_user_message_template.replace('{context}', context)
    user_message = user_message.replace('{question}', user_query)

    prompt = qna_system_message + '\n' + user_message
    
    try:
        # Call the llama.cpp engine with streaming enabled
        response_stream = llm(
            prompt=prompt,
            max_tokens=512,
            stream=True,
            temperature=0.3
        )
        
        for chunk in response_stream:
            # FIX: Added [0] index to resolve dictionary mapping errors
            token_text = chunk["choices"][0]["text"]
            # Format as Server-Sent Events (SSE) standard data payload
            yield f"data: {json.dumps({'text': token_text})}\n\n"
            
    except Exception as e:
        yield f"data: {json.dumps({'error': str(e)})}\n\n"

@app.post("/api/chat")
async def chat_endpoint(request: ChatRequest):
    return StreamingResponse(generate_rag_response(request.message), media_type="text/event-stream")

if __name__ == "__main__":
    import uvicorn
    # Kept port 5000 style for easier local routing
    uvicorn.run(app, host="127.0.0.1", port=5000)
