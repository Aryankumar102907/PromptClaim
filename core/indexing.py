import os
import pickle
from pathlib import Path
import faiss
from sentence_transformers import SentenceTransformer

from utils.semantic_search import build_faiss_index_from_embeddings
from utils.file_ops import extract_text_from_document
from utils.chunking import recursive_chunk_text

from core.config import DOCUMENTS_DIR, INDEX_DIR, SENTENCE_TRANSFORMER_MODEL, MAX_CHUNK_SIZE, OVERLAP

class GlobalModel:
    def __init__(self):
        self.model = None

    def set_model(self, model_name: str):
        if self.model is None:
            self.model = SentenceTransformer(model_name)

class GlobalFaissIndex:
    def __init__(self):
        self.index = None

    def set_index(self, faiss_index):
        self.index = faiss_index

class GlobalChunksData:
    def __init__(self):
        self.data = {"texts": [], "metadata": []}

    def set_data(self, chunks_data):
        self.data = chunks_data

global_model = GlobalModel()
global_faiss_index = GlobalFaissIndex()
global_all_chunks_data = GlobalChunksData()

def load_global_index_and_chunks():
    index_path = os.path.join(INDEX_DIR, "faiss_index.bin")
    chunks_path = os.path.join(INDEX_DIR, "chunks.pkl")

    global_index = None
    all_chunks_data = {"texts": [], "metadata": []}

    if os.path.exists(index_path) and os.path.exists(chunks_path):
        try:
            with open(index_path, "rb") as f:
                global_index = pickle.load(f)
            with open(chunks_path, "rb") as f:
                all_chunks_data = pickle.load(f)
        except Exception as e:
            print(f"Error loading existing index or chunks: {e}")
    return global_index, all_chunks_data

def save_global_index_and_chunks(index, chunks_data):
    index_path = os.path.join(INDEX_DIR, "faiss_index.bin")
    chunks_path = os.path.join(INDEX_DIR, "chunks.pkl")
    
    os.makedirs(INDEX_DIR, exist_ok=True) # Ensure directory exists

    with open(index_path, "wb") as f:
        pickle.dump(index, f)
    with open(chunks_path, "wb") as f:
        pickle.dump(chunks_data, f)
    print(f"FAISS index saved to {index_path}")
    print(f"Chunks data saved to {chunks_path}")
