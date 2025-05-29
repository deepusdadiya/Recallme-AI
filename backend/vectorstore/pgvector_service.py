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
            title=metadata.get("title"),
            source_type=metadata.get("source_type"),
        )
        db.add(db_chunk)

    db.commit()

def search_memory_pgvector(db: Session, query: str, top_k: int = 5, filter_by: Dict = None) -> List[Document]:
    query_embedding = embedding_model.embed_query(query)
    embedding_str = f"[{','.join(map(str, query_embedding))}]"
    # Build WHERE clause dynamically
    where_clauses = []
    if filter_by:
        if "source_type" in filter_by:
            where_clauses.append(f"source_type = :source_type")
        if "title" in filter_by:
            where_clauses.append(f"title ILIKE :title")

    where_sql = f"WHERE {' AND '.join(where_clauses)}" if where_clauses else ""

    sql = f"""
        SELECT chunk_text, memory_id, title, source_type
        FROM memory_chunks
        {where_sql}
        ORDER BY embedding <#> '{embedding_str}'
        LIMIT {top_k};
    """

        # Build params dictionary for SQL query
    params = {}
    if filter_by:
        if "source_type" in filter_by:
            params["source_type"] = filter_by["source_type"]
        if "title" in filter_by:
            params["title"] = f"%{filter_by['title']}%"

    result = db.execute(text(sql), params)
    documents = [
        Document(
            page_content=row[0],
            metadata={
                "memory_id": row[1],
                "title": row[2],
                "source_type": row[3]
            }
        )
        for row in result.fetchall()
    ]
    return documents