from fastapi import APIRouter
from pydantic import BaseModel

from app.dependencies import retrieval_service, ai_service

router = APIRouter(prefix="/api/ai", tags=["AI"])


class QueryRequest(BaseModel):
    query: str
    document_id: str | None = None


@router.post("/query")
def query_ai(request: QueryRequest):
    chunks = retrieval_service.retrieve(
        query=request.query,
        document_id=request.document_id
    )

    response = ai_service.answer(
        query=request.query,
        retrieved_chunks=chunks
    )

    return response