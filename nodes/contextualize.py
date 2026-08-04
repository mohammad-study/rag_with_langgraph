import json

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

    contextualize_chain = prompt | llm

    response = contextualize_chain.invoke(
        {
            "chat_history": state.chat_history,
            "question": state.question,
        }
    )

    content = response.content.strip()

    try:
        # Parse JSON
        data = json.loads(content)

        # Validate with Pydantic
        result = ContextualizedQuestion.model_validate(data)

    except Exception as e:
        raise ValueError(
            f"Invalid GuardrailResponse from LLM:\n\n{content}"
        ) from e

    state.standalone_question = result.standalone_question

    return state