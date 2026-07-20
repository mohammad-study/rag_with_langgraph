from state import GraphState
from services.llm import llm

from models.hallucination_check import HallucinationCheck
from prompts.hallucination_grader import hallucination_check_prompt

from langchain_core.prompts import ChatPromptTemplate


def hallucination_check(state: GraphState):

    prompt = ChatPromptTemplate.from_template(
        hallucination_check_prompt
    )

    structured_llm = llm.with_structured_output(
        HallucinationCheck
    )

    hallucination_chain = prompt | structured_llm

    documents = "\n\n".join(
        doc.chunk
        for doc in state.retrieved_documents
    )

    response = hallucination_chain.invoke(
        {
            "question": state.standalone_question,
            "documents": documents,
            "answer": state.generation,
        }
    )

    state.grounded = response.grounded
    state.hallucination_reason = response.reason

    return state