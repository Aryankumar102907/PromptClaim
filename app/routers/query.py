from fastapi import APIRouter, Depends
from core.security import get_current_user
from models.requests import QueryRequest
from utils.decision_engine import get_decision_for_document_and_query

router = APIRouter()

@router.post("/query")
async def query_document(request: QueryRequest, current_user: str = Depends(get_current_user)):
    return get_decision_for_document_and_query(request.policy_filename, request.user_query)
