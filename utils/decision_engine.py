import os
import pickle
import re
import json
from pathlib import Path
from fastapi import HTTPException

from core.config import DOCUMENTS_DIR, PROMPT_PATH
from core.indexing import global_model, global_faiss_index, global_all_chunks_data

from utils.semantic_search import search_topk, build_faiss_index_from_embeddings
from utils.gemini_client import client

def read_prompt():
    with open(PROMPT_PATH, "r") as f:
        return f.read()

def parse_query_with_regex(query: str) -> dict:
    """
    Extracts entities from a structured query using regular expressions.
    Returns a dictionary of the extracted parts.
    """
    pattern = re.compile(r"(\d+)\s*([MF]),\s*(.*?),\s*(.*?),\s*(\d+)\s*-month policy", re.IGNORECASE)
    match = pattern.search(query)
    
    if not match:
        return {"raw_query": query, "structured": {}}

    age, gender, procedure, city, duration = match.groups()
    
    structured_query = {
        "age": int(age),
        "gender": gender.upper(),
        "procedure": procedure.strip(),
        "city": city.strip(),
        "policy_duration_months": int(duration),
    }
    return {"raw_query": query, "structured": structured_query}

def run_decision_engine(parsed_query, model, doc_index, doc_chunks):
    """Runs the decision engine using a document-specific FAISS index."""
    top_clauses = search_topk(parsed_query["raw_query"], model, doc_index, doc_chunks)
    
    clause_context = "\n".join(top_clauses)
    structured_query_str = json.dumps(parsed_query["structured"], indent=2)

    reasoning_prompt = f"""
{read_prompt()}

User Query (structured): {structured_query_str}
User Query (raw): {parsed_query["raw_query"]}

Relevant Clauses:
{clause_context}
"""
    response = client.generate_content(reasoning_prompt, generation_config={"temperature": 0.1})
    # Clean up the response to ensure it's valid JSON
    cleaned_response = response.text.strip().replace("```json", "").replace("```", "")
    return cleaned_response

from core.indexing import load_global_index_and_chunks

def get_decision_for_document_and_query(policy_filename: str, user_query: str):
    if not global_model.model:
        global_model.set_model('all-MiniLM-L6-v2')
    
    if not global_faiss_index.index or not global_all_chunks_data.data["texts"]:
        loaded_index, loaded_chunks_data = load_global_index_and_chunks()
        global_faiss_index.set_index(loaded_index)
        global_all_chunks_data.set_data(loaded_chunks_data)

    if not global_model.model:
        return {"error": "SentenceTransformer model not loaded."}
    if not global_faiss_index.index:
        return {"error": "FAISS index not loaded or built. Run preprocess.py."}

    if not Path(DOCUMENTS_DIR, policy_filename).exists():
        return {"error": f"Document '{policy_filename}' not found in '{DOCUMENTS_DIR}' directory."}

    doc_chunks = [chunk for i, chunk in enumerate(global_all_chunks_data.data["texts"]) if global_all_chunks_data.data["metadata"][i]["source"] == policy_filename]
    
    if not doc_chunks:
        return {"error": f"No chunks found for document '{policy_filename}'. Did you run preprocess.py or upload it?"}

    doc_embeddings = global_model.model.encode(doc_chunks)
    doc_index = build_faiss_index_from_embeddings(doc_embeddings)

    parsed_query = parse_query_with_regex(user_query)
    decision_json_str = run_decision_engine(parsed_query, global_model.model, doc_index, doc_chunks)
    
    try:
        decision_dict = json.loads(decision_json_str)
        return decision_dict
    except json.JSONDecodeError:
        return {"error": "Could not parse the output as JSON.", "raw_output": decision_json_str}

