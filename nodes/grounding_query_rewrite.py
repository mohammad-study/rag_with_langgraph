from langchain_core.prompts import ChatPromptTemplate

from state import GraphState
from services.llm import llm
from prompts.grounding_query_rewrite import grounding_rewrite_prompt
from models.grounding_query_rewrite import GroundingRewriteResponse




def rewrite_for_grounding(state: GraphState):

    prompt = ChatPromptTemplate.from_template(
        grounding_rewrite_prompt
    )

    structured_llm = llm.with_structured_output(
        GroundingRewriteResponse
    )

    grounding_rewrite_chain = prompt | structured_llm

    response = grounding_rewrite_chain.invoke(
        {
            "question": state["standalone_question"],
            "answer": state["generation"],
            "hallucination_reason": state["hallucination_reason"],
            "chat_history": state["chat_history"],
        }
    )

    state["retrieved_documents"] = []

    state["grounding_rewrite_attempt"] += 1

    return state