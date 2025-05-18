from pydantic import BaseModel
from enum import Enum
from uuid import UUID
from datetime import datetime

class SourceType(str, Enum):
    text = "text"
    image = "image"
    audio = "audio"
    pdf = "pdf"

class MemoryIn(BaseModel):
    title: str
    source_type: SourceType
    raw_text: str

class MemoryOut(MemoryIn):
    id: UUID
    created_at: datetime