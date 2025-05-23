from fastapi import APIRouter
from .schema import MemoryQueryRequest, MemoryQueryResponse
from .service import answer_query

router = APIRouter()

@router.post("/query", response_model=MemoryQueryResponse)
def query_memory(req: MemoryQueryRequest):
    return answer_query(req.query)