from pydantic import BaseModel, Field


class ContextualizedQuestion(BaseModel):

    standalone_question: str = Field(
        description="A standalone version of the user's latest question."
    )