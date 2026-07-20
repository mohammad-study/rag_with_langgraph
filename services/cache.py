import traceback
from uuid import uuid4

from redisvl.index import SearchIndex
from redisvl.query import VectorQuery

from services.embedding import embedding_service
from models.cache_schema import CACHE_SCHEMA

REDIS_URL = "redis://localhost:6379"

class CacheService:

    def __init__(self):

        self.index = SearchIndex.from_dict(
            CACHE_SCHEMA,
            redis_url=REDIS_URL
        )

        self.index.create(overwrite=True)

    def lookup(
        self,
        question: str,
        threshold: float = 0.90,
    ):

        embedding = embedding_service.embed(question)

        query = VectorQuery(
            vector=embedding,
            vector_field_name="embedding",
            return_fields=[
                "question",
                "answer"
            ],
            num_results=1
        )

        results = self.index.query(query)

        if len(results) == 0:
            return None

        result = results[0]

        distance = float(result["vector_distance"])

        if distance > (1 - threshold):
            return None

        return result["answer"]

    def save(self, question: str, answer: str):
        embedding = embedding_service.embed(question)

        doc = {
            "id": str(uuid4()),
            "question": question,
            "answer": answer,
            "embedding": embedding,
        }

        try:
            self.index.load([doc])
        except Exception as e:
            traceback.print_exc()
            print("Document:", doc)
            raise


cache_service = CacheService()