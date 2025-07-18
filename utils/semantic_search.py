from sentence_transformers import SentenceTransformer
import faiss
import numpy as np

def build_faiss_index(text_chunks, model_name='all-MiniLM-L6-v2'):
    model = SentenceTransformer(model_name)
    embeddings = model.encode(text_chunks)
    index = faiss.IndexFlatL2(embeddings.shape[1])
    index.add(np.array(embeddings))
    return model, index, embeddings

def build_faiss_index_from_embeddings(embeddings):
    """Builds a FAISS index from pre-computed embeddings."""
    index = faiss.IndexFlatL2(embeddings.shape[1])
    index.add(np.array(embeddings))
    return index

def search_topk(query, model, index, text_chunks, k=5):
    q_vec = model.encode([query])
    scores, ids = index.search(np.array(q_vec), k)
    return [text_chunks[i] for i in ids[0]]
