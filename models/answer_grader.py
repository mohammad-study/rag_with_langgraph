from pydantic import BaseModel, Field


class AnswerGraderResponse(BaseModel):
    complete: bool = Field(
        description="Whether the generated answer fully answers the user's question."
    )

    reason: str = Field(
        description="Short explanation of the grading decision."
    )
