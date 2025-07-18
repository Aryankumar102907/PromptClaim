import os
from pathlib import Path
from fastapi import APIRouter, Depends, UploadFile, File, HTTPException

from core.config import DOCUMENTS_DIR, INDEX_DIR, MAX_CHUNK_SIZE, OVERLAP
from core.indexing import global_model, global_faiss_index, global_all_chunks_data, save_global_index_and_chunks
from core.security import get_current_user

from utils.file_ops import extract_text_from_document
from utils.chunking import recursive_chunk_text
from utils.semantic_search import build_faiss_index_from_embeddings

router = APIRouter()

@router.get("/documents")
async def list_documents(current_user: str = Depends(get_current_user)):
    """Lists all the available documents."""
    documents = os.listdir(DOCUMENTS_DIR)
    return {"documents": documents}

@router.post("/upload_document")
async def upload_document(file: UploadFile = File(...), current_user: str = Depends(get_current_user)):
    global global_faiss_index, global_all_chunks_data, global_model

    if not global_model.model:
        raise HTTPException(status_code=500, detail="SentenceTransformer model not loaded.")

    file_location = Path(DOCUMENTS_DIR) / file.filename
    os.makedirs(DOCUMENTS_DIR, exist_ok=True)
    try:
        with open(file_location, "wb+") as file_object:
            file_object.write(await file.read())
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Could not save file: {e}")

    try:
        text = extract_text_from_document(str(file_location))
        if not text:
            raise HTTPException(status_code=400, detail="Could not extract text from document.")

        chunks = recursive_chunk_text(text, max_chunk_size=MAX_CHUNK_SIZE, overlap=OVERLAP)
        if not chunks:
            raise HTTPException(status_code=400, detail="No chunks generated from document.")

        new_chunks_data = {"texts": [], "metadata": []}
        for chunk in chunks:
            new_chunks_data["texts"].append(chunk)
            new_chunks_data["metadata"].append({"source": file.filename})

        # Combine old and new chunks
        combined_texts = global_all_chunks_data.data["texts"] + new_chunks_data["texts"]
        combined_metadata = global_all_chunks_data.data["metadata"] + new_chunks_data["metadata"]

        # Rebuild FAISS index with combined data
        if combined_texts:
            embeddings = global_model.model.encode(combined_texts)
            global_faiss_index.set_index(build_faiss_index_from_embeddings(embeddings))
            global_all_chunks_data.set_data({"texts": combined_texts, "metadata": combined_metadata})
            save_global_index_and_chunks(global_faiss_index.index, global_all_chunks_data.data)
        else:
            global_faiss_index.set_index(None)
            global_all_chunks_data.set_data({"texts": [], "metadata": []})
            # Optionally delete index files if no chunks remain
            if os.path.exists(os.path.join(INDEX_DIR, "faiss_index.bin")):
                os.remove(os.path.join(INDEX_DIR, "faiss_index.bin"))
            if os.path.exists(os.path.join(INDEX_DIR, "chunks.pkl")):
                os.remove(os.path.join(INDEX_DIR, "chunks.pkl"))

        return {"message": f"Document {file.filename} uploaded and processed successfully."}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing document: {e}")

@router.delete("/documents/{filename}")
async def delete_document(filename: str, current_user: str = Depends(get_current_user)):
    global global_faiss_index, global_all_chunks_data, global_model

    file_location = Path(DOCUMENTS_DIR) / filename

    if not file_location.exists():
        raise HTTPException(status_code=404, detail=f"Document '{filename}' not found.")

    try:
        os.remove(file_location)

        # Remove chunks related to the deleted file
        new_texts = []
        new_metadata = []
        for i, meta in enumerate(global_all_chunks_data.data["metadata"]):
            if meta["source"] != filename:
                new_texts.append(global_all_chunks_data.data["texts"][i])
                new_metadata.append(meta)
        
        global_all_chunks_data.set_data({"texts": new_texts, "metadata": new_metadata})

        # Rebuild FAISS index with remaining data
        if global_all_chunks_data.data["texts"]:
            embeddings = global_model.model.encode(global_all_chunks_data.data["texts"])
            global_faiss_index.set_index(build_faiss_index_from_embeddings(embeddings))
            save_global_index_and_chunks(global_faiss_index.index, global_all_chunks_data.data)
        else:
            global_faiss_index.set_index(None)
            # Clean up index files if no chunks remain
            if os.path.exists(os.path.join(INDEX_DIR, "faiss_index.bin")):
                os.remove(os.path.join(INDEX_DIR, "faiss_index.bin"))
            if os.path.exists(os.path.join(INDEX_DIR, "chunks.pkl")):
                os.remove(os.path.join(INDEX_DIR, "chunks.pkl"))

        return {"message": f"Document '{filename}' deleted and index updated successfully."}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error deleting or re-indexing document: {e}")
