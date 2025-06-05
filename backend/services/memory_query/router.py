from fastapi import APIRouter, Depends
from .schema import MemoryQueryRequest, MemoryQueryResponse
from .service import answer_query
from sqlalchemy.orm import Session
from alchemist.postgresql.resource import get_db
from services.auth.dependencies import get_current_user
from alchemist.postgresql.functions import User

router = APIRouter()

@router.post("/query", response_model=MemoryQueryResponse)
def query_memory(req: MemoryQueryRequest, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    return answer_query(db, req.query, current_user.id, req.source_type, req.title)