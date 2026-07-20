from sentence_transformers import SentenceTransformer
import chromadb

from .utils import query_knowledge_base
from .chroma import collection

class RetrievalService:

    def __init__(
        self,
        model: SentenceTransformer,
        collection: chromadb.Collection,
    ):

        self.model = model
        self.collection = collection

    def retrieve(
        self,
        question: str,
        top_k: int = 5,
    ):

        return query_knowledge_base(
            query=question,
            model=self.model,
            collection=self.collection,
            alpha=0.8,
            semantic_top_k=20,
            keyword_top_k=20,
            top_k=top_k,
        )
    



retrieval_service = RetrievalService(
    model=SentenceTransformer("all-MiniLM-L6-v2"),
    collection=collection
)