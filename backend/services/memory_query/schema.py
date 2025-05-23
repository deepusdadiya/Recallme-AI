from pydantic import BaseModel
from typing import List

class MemoryQueryRequest(BaseModel):
    query: str

class MemoryMatch(BaseModel):
    content: str
    metadata: dict

class MemoryQueryResponse(BaseModel):
    answer: str
    matches: List[MemoryMatch]