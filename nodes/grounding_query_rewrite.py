import json

from langchain_core.prompts import ChatPromptTemplate

from state import GraphState
from services.llm import llm

from prompts.grounding_query_rewrite import grounding_rewrite_prompt
from models.grounding_query_rewrite import GroundingRewriteResponse


def rewrite_for_grounding(state: GraphState):

    prompt = ChatPromptTemplate.from_template(
        grounding_rewrite_prompt
    )

    grounding_rewrite_chain = prompt | llm

    response = grounding_rewrite_chain.invoke(
        {
            "question": state.standalone_question,
            "answer": state.generation,
            "hallucination_reason": state.hallucination_reason,
            "chat_history": state.chat_history,
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
        result = GroundingRewriteResponse.model_validate(data)

    except json.JSONDecodeError as e:
        raise ValueError(
            f"LLM returned invalid JSON:\n\n{content}"
        ) from e

    except Exception as e:
        raise ValueError(
            f"LLM response does not match {GroundingRewriteResponse.__name__}:\n\n{content}"
        ) from e

    # Update state
    state.rewritten_question = result.rewritten_question
    state.retrieved_documents = []
    state.grounding_rewrite_attempt += 1

    return state