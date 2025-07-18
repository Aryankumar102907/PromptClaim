import os
from contextlib import asynccontextmanager
from pathlib import Path
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from core.config import DOCUMENTS_DIR, INDEX_DIR, PROMPT_PATH, GOOGLE_CLIENT_ID, GOOGLE_CLIENT_SECRET, GOOGLE_REDIRECT_URI, SECRET_KEY, ALGORITHM, ACCESS_TOKEN_EXPIRE_MINUTES
from core.indexing import global_model, global_faiss_index, global_all_chunks_data, load_global_index_and_chunks, save_global_index_and_chunks, build_faiss_index_from_embeddings

from app.routers import auth, documents, query

# Ensure directories exist
os.makedirs(DOCUMENTS_DIR, exist_ok=True)
os.makedirs(INDEX_DIR, exist_ok=True)

if not all([GOOGLE_CLIENT_ID, GOOGLE_CLIENT_SECRET, GOOGLE_REDIRECT_URI, SECRET_KEY]):
    raise ValueError("Missing one or more Google OAuth or JWT environment variables.")

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup event
    print("Loading SentenceTransformer model...")
    global_model.set_model('all-MiniLM-L6-v2') # Initialize the model
    
    print("Loading global FAISS index and chunks...")
    loaded_index, loaded_chunks_data = load_global_index_and_chunks()
    global_faiss_index.set_index(loaded_index)
    global_all_chunks_data.set_data(loaded_chunks_data)

    # Get list of files currently in the index
    indexed_files = {metadata["source"] for metadata in global_all_chunks_data.data["metadata"]}

    # Scan documents directory for new/updated files
    documents_path = Path(DOCUMENTS_DIR)
    all_document_files = []
    for ext in ["*.pdf", "*.docx", "*.txt"]:
        all_document_files.extend(documents_path.glob(ext))

    new_documents_found = False
    for doc_file_path in all_document_files:
        if doc_file_path.name not in indexed_files:
            print(f"Found new document: {doc_file_path.name}. Processing...")
            new_documents_found = True
            try:
                text = extract_text_from_document(str(doc_file_path))
                if text:
                    chunks = recursive_chunk_text(text, max_chunk_size=1024, overlap=100)
                    for chunk in chunks:
                        global_all_chunks_data.data["texts"].append(chunk)
                        global_all_chunks_data.data["metadata"].append({"source": doc_file_path.name})
                else:
                    print(f"Warning: Could not extract text from {doc_file_path.name}.")
            except Exception as e:
                print(f"Error processing {doc_file_path.name} during startup: {e}")

    if new_documents_found or global_faiss_index.index is None and global_all_chunks_data.data["texts"]:
        print("Rebuilding FAISS index with all documents...")
        if global_all_chunks_data.data["texts"]:
            embeddings = global_model.model.encode(global_all_chunks_data.data["texts"])
            global_faiss_index.set_index(build_faiss_index_from_embeddings(embeddings))
            save_global_index_and_chunks(global_faiss_index.index, global_all_chunks_data.data)
        else:
            print("No documents to index after scanning.")
            global_faiss_index.set_index(None)
            global_all_chunks_data.set_data({"texts": [], "metadata": []})
            # Clean up index files if no documents are present
            if os.path.exists(os.path.join(INDEX_DIR, "faiss_index.bin")):
                os.remove(os.path.join(INDEX_DIR, "faiss_index.bin"))
            if os.path.exists(os.path.join(INDEX_DIR, "chunks.pkl")):
                os.remove(os.path.join(INDEX_DIR, "chunks.pkl"))
    elif global_faiss_index.index is None:
        print("No existing index or documents found. Starting fresh.")

    yield

    # Shutdown event (optional)
    print("Application shutting down.")

app = FastAPI(lifespan=lifespan)

# Add CORS middleware to allow requests from the frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)

# Include routers
app.include_router(auth.router, prefix="/auth", tags=["auth"])
app.include_router(documents.router, tags=["documents"])
app.include_router(query.router, tags=["query"])

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
