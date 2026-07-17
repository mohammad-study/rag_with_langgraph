from pydantic import BaseModel, Field
from typing import Optional

class GuardrailResponse(BaseModel):
    is_safe: bool = Field(
        description = "Either the prompt is safe or not safe"
    )
    reason: Optional[str] = Field(
        default = None,
        description="Reason is the input prompt is unsafe"
    )