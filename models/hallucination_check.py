from pydantic import BaseModel, Field


class HallucinationCheck(BaseModel):

    grounded: bool = Field(
        description="Whether the generated answer is fully supported by the retrieved documents."
    )

    reason: str = Field(
        description="Short explanation."
    )