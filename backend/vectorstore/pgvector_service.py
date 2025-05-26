import uuid
from sqlalchemy import text
from typing import List, Dict
from sqlalchemy.orm import Session
from langchain_core.documents import Document
from langchain.text_splitter import RecursiveCharacterTextSplitter
from vectorstore.wrapper import SentenceTransformerEmbeddings
from alchemist.postgresql.functions import MemoryChunk  # you'll create this table
import numpy as np

embedding_model = SentenceTransformerEmbeddings()
text_splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=100)

def store_text_pgvector(db: Session, text: str, metadata: Dict):
    if not text.strip():
        return
    chunks = text_splitter.split_text(text)
    if not chunks:
        return

    for chunk in chunks:
        embedding = embedding_model.embed_query(chunk)
        db_chunk = MemoryChunk(
            id=str(uuid.uuid4()),
            memory_id=metadata["memory_id"],
            chunk_text=chunk,
            embedding=embedding,
        )
        db.add(db_chunk)

    db.commit()

def search_memory_pgvector(db: Session, query: str, top_k: int = 5) -> List[Document]:
    query_embedding = embedding_model.embed_query(query)
    embedding_str = f"[{','.join(map(str, query_embedding))}]"

    sql = f"""
        SELECT chunk_text, memory_id
        FROM memory_chunks
        ORDER BY embedding <#> '{embedding_str}'
        LIMIT {top_k};
    """

    result = db.execute(text(sql))
    documents = [
        Document(
            page_content=row[0],
            metadata={"memory_id": row[1]}
        )
        for row in result.fetchall()
    ]
    return documents