from pydantic import BaseModel, Field


class QueryRewriteResponse(BaseModel):

    rewritten_question: str = Field(
        description="A rewritten version of the user's question optimized for document retrieval."
    )