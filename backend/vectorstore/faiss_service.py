import os
import uuid
from typing import List, Dict
# from sentence_transformers import SentenceTransformer
from langchain_community.vectorstores import FAISS
from langchain_core.documents import Document
from langchain.text_splitter import RecursiveCharacterTextSplitter
from vectorstore.wrapper import SentenceTransformerEmbeddings

embedding_model = SentenceTransformerEmbeddings()
text_splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=100)

# FAISS storage path
FAISS_INDEX_PATH = "vectorstore/faiss_index"

def _load_or_create_vectorstore() -> FAISS:
    if os.path.exists(f"{FAISS_INDEX_PATH}/index.faiss"):
        return FAISS.load_local(FAISS_INDEX_PATH, embeddings=embedding_model, allow_dangerous_deserialization=True)
    else:
        return FAISS.from_documents([], embedding_model)

def store_text(text: str, metadata: Dict):
    vectorstore = _load_or_create_vectorstore()
    chunks = text_splitter.split_text(text)
    docs = [Document(page_content=chunk, metadata={**metadata, "chunk_id": str(uuid.uuid4())}) for chunk in chunks]
    vectorstore.add_documents(docs)
    vectorstore.save_local(FAISS_INDEX_PATH)

def search_memory(query: str, top_k: int = 5) -> List[Document]:
    vectorstore = _load_or_create_vectorstore()
    return vectorstore.similarity_search(query, k=top_k)
