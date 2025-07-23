from fastapi import APIRouter
from models.requests import QueryRequest
from utils.decision_engine import get_decision_for_document_and_query

router = APIRouter()

@router.post("/query")
async def query_document(request: QueryRequest):
    return get_decision_for_document_and_query(request.policy_filename, request.user_query)
