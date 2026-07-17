from typing import TypedDict, Optional

from langchain_redis import RedisChatMessageHistory
from langchain_core.messages import BaseMessage

from models.retrieved_document import RetrievedDocument

class GraphState(TypedDict):
    session_id: str
    #Input Validation
    question: str
    is_valid: bool
    validation_error: Optional[str]

    # Chat History
    history: RedisChatMessageHistory
    chat_history: list[BaseMessage]

    standalone_question: str
    rewritten_question: Optional[str]
    document_rewrite_attempt: int

    # Cache
    cache_hit: bool
    cached_response: str
    cacheable: bool = True

    # Generation
    generation: Optional[str]

    # Router
    router: str

    #Retrieval
    retrieved_documents: list[RetrievedDocument]
    documents_found: bool

    # Relevance
    documents_relevant: bool

    # Hallucination Check
    grounded: bool
    hallucination_reason: str
    grounding_rewrite_attempt: int