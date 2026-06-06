from huggingface_hub import hf_hub_download
from llama_cpp import Llama


model_name_or_path = "Qwen/Qwen2.5-3B-Instruct-GGUF"
model_basename    = "qwen2.5-3b-instruct-q4_k_m.gguf"

# hf_hub_download fetches the file from Hugging Face and caches it locally.
# Returns the local file path where the model was saved.
model_path = hf_hub_download(
    repo_id  = model_name_or_path,
    filename = model_basename
)

llm = Llama(
    model_path=model_path,
    n_ctx=4096,
    n_gpu_layers  = 38,
    n_batch       = 512,
    verbose=False
)