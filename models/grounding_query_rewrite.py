from pydantic import BaseModel, Field


class GroundingRewriteResponse(BaseModel):

    rewritten_question: str = Field(
        description="A rewritten question that will retrieve documents needed to verify or support the generated answer."
    )