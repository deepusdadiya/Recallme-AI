from pydantic import BaseModel
from typing import List, Optional

class MemoryQueryRequest(BaseModel):
    query: str
    source_type: Optional[str] = None  # e.g. 'pdf', 'image', etc.
    title: Optional[str] = None  

class MemoryMatch(BaseModel):
    content: str
    metadata: dict

class MemoryQueryResponse(BaseModel):
    answer: str
    matches: List[MemoryMatch]