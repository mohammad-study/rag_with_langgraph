# Langraph
from langgraph.graph import StateGraph, END, START

from state import GraphState

#Nodes
from nodes.input_validation import input_guardrails
from nodes.load_history import load_history
from nodes.contextualize import contextualize_question
from nodes.semantic_cache import semantic_cache
from nodes.save_history import save_history
from nodes.router import route_query
from nodes.direct_generate import direct_generate
from nodes.retriever import retrieve_documents
from nodes.document_grade import grade_documents
from nodes.generate import generate_answer
from nodes.hallucination import hallucination_check
from nodes.update_cache import update_cache
from nodes.grading_query_rewrite import rewrite_query
from nodes.grounding_query_rewrite import rewrite_for_grounding
from nodes.fallback import fallback_response


# Router
from router import guardrail_router, cache_router, query_router, document_router,hallucination_router



rag_workflow = StateGraph(GraphState)

# Add node
rag_workflow.add_node("input_guardrail", input_guardrails)
rag_workflow.add_node("load_history", load_history)
rag_workflow.add_node("contextualize_question", contextualize_question)
rag_workflow.add_node("semantic_cache", semantic_cache)
rag_workflow.add_node("save_history", save_history)
rag_workflow.add_node("route_query", route_query)
rag_workflow.add_node("direct_generate", direct_generate)
rag_workflow.add_node("retrieve_documents", retrieve_documents)
rag_workflow.add_node("grade_documents", grade_documents)
rag_workflow.add_node("rewrite_query", rewrite_query)
rag_workflow.add_node("generate_answer", generate_answer)
rag_workflow.add_node("hallucination_check", hallucination_check)
rag_workflow.add_node("rewrite_for_grounding", rewrite_for_grounding)
rag_workflow.add_node("fallback", fallback_response)
rag_workflow.add_node("update_cache", update_cache)



# Edge
rag_workflow.add_edge(START,"input_guardrail")

rag_workflow.add_conditional_edges(
    "input_guardrail",
    guardrail_router,
    {
        "load_history" : "load_history",
        "Input_Validation_Failed": END
    },

)

rag_workflow.add_edge("load_history", "contextualize_question")
rag_workflow.add_edge("contextualize_question", "semantic_cache")


rag_workflow.add_conditional_edges(
    "semantic_cache",
    cache_router,
    {
        "answer_from_cache": "save_history",
        "cache_miss": "route_query"
    }
)

rag_workflow.add_conditional_edges(
    "route_query",
    query_router,
    {
        "LLM": "direct_generate",
        "RAG": "retrieve_documents"
    }
)


rag_workflow.add_edge("direct_generate", "save_history")
rag_workflow.add_edge("retrieve_documents", "grade_documents")

rag_workflow.add_conditional_edges(
    "grade_documents",
    document_router,
    {
        "generate_response": "generate_answer",
        "rewrite": "rewrite_query",
        "fallback": "fallback"
    }
)

rag_workflow.add_edge("rewrite_query", "retrieve_documents")

rag_workflow.add_edge("generate_answer", "hallucination_check")

rag_workflow.add_conditional_edges(
    "hallucination_check",
    hallucination_router,
    {
        "save_history": "save_history",
        "fallback": "fallback",
        "retrieve_again": "rewrite_for_grounding"
    }
)

rag_workflow.add_edge("rewrite_for_grounding", "retrieve_documents")
rag_workflow.add_edge("fallback", "save_history")

rag_workflow.add_edge("save_history", "update_cache")
rag_workflow.add_edge("update_cache", END)

graph = rag_workflow.compile()

result = graph.invoke({
    "question": "What is company policy about workplace respect",
    "session_id": "8"
})

print(result)

