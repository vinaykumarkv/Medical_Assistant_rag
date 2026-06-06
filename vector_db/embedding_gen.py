from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import Chroma
from langchain_community.document_loaders import PyMuPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter

embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
out_dir = "./vector_db"
def embedding_pdf():
    file = "./data/medical.pdf"
    # Load the PDF and split it into chunks
    pdf_loader = PyMuPDFLoader(file)
    docs  = pdf_loader.load()
    text_splitter = RecursiveCharacterTextSplitter.from_tiktoken_encoder(
        encoding_name = 'cl100k_base',
        chunk_size    = 512,
        chunk_overlap = 50
    )
    docs = text_splitter.split_documents(docs)
    vectorstore = Chroma.from_documents(
        docs,
        embeddings,
        persist_directory = out_dir
    )



#embedding_pdf() # Run this once to create the vector database from the PDF. The resulting embeddings are saved to disk and can be reused without reprocessing the PDF.

db = Chroma(persist_directory="./vector_db", embedding_function=embeddings)
