from sentence_transformers import SentenceTransformer
import chromadb

from .utils import query_knowledge_base
from .chroma import collection
from config import config

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

        retrieval_config = config["retrieval"]

        return query_knowledge_base(
            query=question,
            model=self.model,
            collection=self.collection,
            alpha=0.8,
            semantic_top_k=retrieval_config["semantic_top_k"],
            keyword_top_k=retrieval_config["keyword_top_k"],
            top_k=top_k,
        )
    



retrieval_service = RetrievalService(
    model=SentenceTransformer(config["retrieval"]["model_name"]),
    collection=collection
)