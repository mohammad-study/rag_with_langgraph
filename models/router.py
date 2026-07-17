from pydantic import BaseModel, Field
from typing import Optional

class Router(BaseModel):
    route: str = Field(
        description = "LLM if the query should be routed to LLM otherwise RAG"
    )