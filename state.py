from typing import Optional, Annotated, Any

from pydantic import BaseModel, Field

from langchain_core.messages import BaseMessage
from langchain_redis import RedisChatMessageHistory
from langgraph.graph.message import add_messages
from langchain_core.messages import AnyMessage

from models.retrieved_document import RetrievedDocument


class GraphState(BaseModel):
    # Session
    session_id: str

    # Input Validation
    question: str
    is_valid: bool = True
    validation_error: Optional[str] = None

    # Chat History
    chat_history: Annotated[
        list[AnyMessage],
        add_messages
    ] = Field(default_factory=list)

    # Question Processing
    standalone_question: str = ""
    rewritten_question: Optional[str] = None
    document_rewrite_attempt: int = 0

    # Cache
    cache_hit: bool = False
    cached_response: Optional[str] = None
    cacheable: bool = True

    # Generation
    generation: Optional[str] = None

    # Router
    router: Optional[str] = None

    # Retrieval
    retrieved_documents: list[RetrievedDocument] = Field(default_factory=list)
    documents_found: bool = False

    # Relevance
    documents_relevant: bool = False

    # Hallucination Check
    grounded: bool = False
    hallucination_reason: Optional[str] = None
    grounding_rewrite_attempt: int = 0