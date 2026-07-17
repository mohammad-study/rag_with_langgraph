from langchain_huggingface import HuggingFaceEmbeddings


class EmbeddingService:

    def __init__(self):

        self.embedding_model = HuggingFaceEmbeddings(
            model_name="BAAI/bge-small-en-v1.5"
        )

    def embed(self, text: str):

        return self.embedding_model.embed_query(text)


embedding_service = EmbeddingService()