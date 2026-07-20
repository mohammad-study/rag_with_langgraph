from state import GraphState
from services.llm import llm

from models.document_grade import DocumentGrade
from prompts.document_grader import document_grader_prompt

from langchain_core.prompts import ChatPromptTemplate


def grade_documents(state: GraphState):

    prompt = ChatPromptTemplate.from_template(
        document_grader_prompt
    )

    llm_with_output = llm.with_structured_output(
        DocumentGrade
    )

    document_grader_chain = prompt | llm_with_output

    docs = "\n\n".join(
        doc.chunk
        for doc in state.retrieved_documents
    )

    response = document_grader_chain.invoke(
        {
            "question": state.standalone_question,
            "documents": docs,
        }
    )

    if response.relevant:
        state.documents_relevant = response.relevant

    else:
        state.documents_relevant = response.relevant
        state.grounded = False
        state.hallucination_reason = None

    return state