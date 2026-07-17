from pydantic import BaseModel, Field


class DocumentGrade(BaseModel):

    relevant: bool = Field(
        description="Whether the retrieved documents are sufficient to answer the question."
    )

    reason: str = Field(
        description="Short explanation."
    )