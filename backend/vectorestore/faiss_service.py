import os
import uuid
from typing import List, Dict
from langchain.vectorstores import FAISS
from langchain.embeddings import OpenAIEmbeddings
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.docstore.document import Document

# Path to store FAISS index
FAISS_INDEX_PATH = "vectorstore/faiss_index"

# Embedding model setup (you can swap with Groq, Krutrim, etc.)
embedding_model = OpenAIEmbeddings()  # Replace with your wrapper if needed

# Chunking setup
text_splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=100)


def _load_or_create_vectorstore() -> FAISS:
    """Load FAISS index from disk, or create a new one if it doesn't exist."""
    if os.path.exists(FAISS_INDEX_PATH):
        return FAISS.load_local(FAISS_INDEX_PATH, embeddings=embedding_model)
    else:
        return FAISS.from_documents([], embedding_model)


def store_text(text: str, metadata: Dict):
    """
    Splits input text, embeds it, and stores into FAISS with metadata.

    Args:
        text (str): raw text from memory (e.g., OCR, transcript)
        metadata (dict): e.g., { "memory_id": "...", "title": "..." }
    """
    vectorstore = _load_or_create_vectorstore()

    chunks = text_splitter.split_text(text)
    docs = [
        Document(page_content=chunk, metadata={**metadata, "chunk_id": str(uuid.uuid4())})
        for chunk in chunks
    ]

    vectorstore.add_documents(docs)
    vectorstore.save_local(FAISS_INDEX_PATH)


def search_memory(query: str, top_k: int = 5) -> List[Document]:
    """
    Perform semantic search on stored memory chunks.

    Args:
        query (str): user question/input
        top_k (int): number of results to return

    Returns:
        List of matching Document objects (with .page_content and .metadata)
    """
    vectorstore = _load_or_create_vectorstore()
    return vectorstore.similarity_search(query, k=top_k)