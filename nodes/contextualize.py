from prompts.contextualize_question import contextualize_question_prompt
from models.contextualize_question import ContextualizedQuestion



from langchain_core.prompts import ChatPromptTemplate

from services.llm import llm
from state import GraphState
from state import GraphState


def contextualize_question(state: GraphState):

    prompt = ChatPromptTemplate.from_template(
    contextualize_question_prompt
    )

    structured_llm = llm.with_structured_output(
        ContextualizedQuestion
    )

    contextualize_chain = prompt | structured_llm

    result = contextualize_chain.invoke(
        {
            "chat_history": state.chat_history,
            "question": state.question,
        }
    )

    state.standalone_question = result.standalone_question

    return state