import json

from langchain_core.prompts import ChatPromptTemplate

from services.llm import llm
from state import GraphState

from models.router import Router
from prompts.router import router_prompt


def route_query(state: GraphState):

    prompt = ChatPromptTemplate.from_template(
        router_prompt
    )

    router_chain = prompt | llm

    response = router_chain.invoke(
        {
            "question": state.standalone_question,
        }
    )

    content = response.content.strip()

    # Remove markdown code fences
    if content.startswith("```"):
        content = (
            content.replace("```json", "")
            .replace("```", "")
            .strip()
        )

    try:
        data = json.loads(content)
        result = Router.model_validate(data)

    except json.JSONDecodeError as e:
        raise ValueError(
            f"LLM returned invalid JSON:\n\n{content}"
        ) from e

    except Exception as e:
        raise ValueError(
            f"LLM response does not match {Router.__name__}:\n\n{content}"
        ) from e

    state.router = result.route

    return state