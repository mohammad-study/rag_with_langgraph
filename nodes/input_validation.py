import json

from langchain_core.prompts import ChatPromptTemplate

from services.llm import llm
from state import GraphState
from models.guardrail_response import GuardrailResponse
from prompts.input_guardrails import input_guardrail_prompt
from services.redis import history_service


def input_guardrails(state: GraphState):
    prompt = ChatPromptTemplate.from_template(
        input_guardrail_prompt
    )

    chain = prompt | llm

    response = chain.invoke(
        {
            "question": state.question,
        }
    )

    content = response.content.strip()

    # Remove markdown code fences if the model adds them
    if content.startswith("```"):
        content = (
            content.replace("```json", "")
            .replace("```", "")
            .strip()
        )

    try:
        data = json.loads(content)
        result = GuardrailResponse.model_validate(data)

    except json.JSONDecodeError as e:
        raise ValueError(
            f"LLM returned invalid JSON:\n\n{content}"
        ) from e

    except Exception as e:
        raise ValueError(
            f"LLM response does not match {GuardrailResponse.__name__}:\n\n{content}"
        ) from e

    history_service.add_user_message(
        state.session_id,
        state.question,
    )

    state.is_valid = result.is_safe
    state.validation_error = result.reason

    return state