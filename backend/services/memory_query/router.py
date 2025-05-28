from fastapi import APIRouter, Depends
from .schema import MemoryQueryRequest, MemoryQueryResponse
from .service import answer_query
from sqlalchemy.orm import Session
from alchemist.postgresql.resource import get_db

router = APIRouter()

@router.post("/query", response_model=MemoryQueryResponse)
def query_memory(req: MemoryQueryRequest, db: Session = Depends(get_db)):
    return answer_query(db, req.query)