from langchain_huggingface import HuggingFaceEmbeddings
from config import config


class EmbeddingService:

    def __init__(self):

        self.embedding_model = HuggingFaceEmbeddings(
            model_name=config["services"]["embedding_model_name"]
        )

    def embed(self, text: str):

        return self.embedding_model.embed_query(text)


embedding_service = EmbeddingService()