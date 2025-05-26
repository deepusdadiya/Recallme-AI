from sqlalchemy import Column, Integer, String, Text, ForeignKey, DateTime, Enum, Boolean
from sqlalchemy.orm import declarative_base
import uuid
import enum
import datetime
from sqlalchemy.dialects.postgresql import UUID, ARRAY
from pgvector.sqlalchemy import Vector

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
    created_at = Column(DateTime, default=datetime.datetime.now)


class MemoryChunk(Base):
    __tablename__ = "memory_chunks"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    memory_id = Column(UUID(as_uuid=True), ForeignKey("memories.id"), nullable=False)
    chunk_text = Column(Text, nullable=False)
    embedding = Column(Vector(768))
    created_at = Column(DateTime, default=datetime.datetime.now)


class User(Base):
    __tablename__ = "users"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    email = Column(String, unique=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    is_verified = Column(Boolean, default=False)
    otp_code = Column(String, nullable=True)
    otp_expiry = Column(DateTime, nullable=True)
    created_at = Column(DateTime, default=datetime.datetime.now)