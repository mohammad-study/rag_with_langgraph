from services.llm import llm
from state import GraphState

from models.guardrail_response import GuardrailResponse
from prompts.input_guardrails import input_guardrail_prompt

from services.redis import history_service

from langchain_core.prompts import ChatPromptTemplate


def input_guardrails(state: GraphState):    
    prompt = ChatPromptTemplate.from_template(input_guardrail_prompt)

    llm_with_structured_response = llm.with_structured_output(GuardrailResponse)
    guardrail_chain = prompt | llm_with_structured_response

    response = guardrail_chain.invoke(
        {
            "question": state.question,
        }
    )

    history_service.add_user_message(
         state.session_id,
         state.question
    )

    state.is_valid = response.is_safe
    state.validation_error = response.reason

    return state


