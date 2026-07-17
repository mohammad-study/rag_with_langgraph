from pydantic import BaseModel


class DirectGenerationResponse(BaseModel):
    answer: str