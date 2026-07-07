from pydantic import BaseModel

class RetrievalRequest(BaseModel):
    query: str

class RetrievalResponse(BaseModel):
    context: str