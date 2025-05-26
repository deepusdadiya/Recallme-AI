from langchain_core.embeddings import Embeddings
from typing import List

class SentenceTransformerEmbeddings(Embeddings):
    def __init__(self, model_name='sentence-transformers/all-mpnet-base-v2'):
        from sentence_transformers import SentenceTransformer
        self.model = SentenceTransformer(model_name)

    def embed_documents(self, texts: List[str]) -> List[List[float]]:
        return self.model.encode(texts, convert_to_numpy=True).tolist()

    def embed_query(self, text: str) -> List[float]:
        return self.model.encode(text, convert_to_numpy=True).tolist()