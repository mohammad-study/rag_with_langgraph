from langchain_core.prompts import ChatPromptTemplate

from state import GraphState
from prompts.grading_query_rewrite import query_rewrite_prompt
from models.grading_query_rewrite import QueryRewriteResponse
from services.llm import llm


def rewrite_query(state: GraphState):

    prompt = ChatPromptTemplate.from_template(query_rewrite_prompt)

    structured_llm = llm.with_structured_output(
        QueryRewriteResponse
    )

    query_rewrite_chain = prompt | structured_llm

    response = query_rewrite_chain.invoke(
        {
            "chat_history": state.chat_history,
            "question": state.standalone_question,
        }
    )

    state.rewritten_question = response.rewritten_question
    state.retrieved_documents = []

    state.document_rewrite_attempt += 1

    return state