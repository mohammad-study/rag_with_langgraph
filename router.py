from langgraph.graph import END
from state import GraphState


def guardrail_router(state: GraphState):

    if state["is_valid"]:
        return "load_history"

    return "Input_Validation_Failed"

def cache_router(state):

    if state["cache_hit"]:
        return "answer_from_cache"

    return "cache_miss"

def query_router(state: GraphState):

    return state["router"]


MAX_REWRITE_ATTEMPTS = 3

def document_router(state: GraphState):

    if state["documents_relevant"]:
        return "generate_response"
    
    if state.get("document_rewrite_attempt", 0) >= MAX_REWRITE_ATTEMPTS:
        return "fallback"

    return "rewrite"

def hallucination_router(state: GraphState):

    if state["grounded"]:
        return "save_history"
    
    if state.get("grounding_rewrite_attempt", 0) >= MAX_REWRITE_ATTEMPTS:
        return "fallback"

    return "retrieve_again"