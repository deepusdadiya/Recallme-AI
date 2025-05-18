from sqlalchemy import Column, Integer, String, Text, ForeignKey, DateTime, Enum
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import declarative_base
import uuid
import enum
import datetime

Base = declarative_base()

class SourceType(str, enum.Enum):
    text = "text"
    image = "image"
    audio = "audio"
    pdf = "pdf"

class Memory(Base):
    __tablename__ = "memories"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(Integer, nullable=False)
    title = Column(String(255))
    source_type = Column(Enum(SourceType))
    raw_text = Column(Text)
    summary = Column(Text)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)