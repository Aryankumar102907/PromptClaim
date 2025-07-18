from pydantic import BaseModel

class QueryRequest(BaseModel):
    policy_filename: str
    user_query: str
