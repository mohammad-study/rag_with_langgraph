import json

from langchain_core.prompts import ChatPromptTemplate

from state import GraphState
from services.llm import llm

from models.hallucination_check import HallucinationCheck
from prompts.hallucination_grader import hallucination_check_prompt


def hallucination_check(state: GraphState):

    prompt = ChatPromptTemplate.from_template(
        hallucination_check_prompt
    )

    hallucination_chain = prompt | llm

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
        result = HallucinationCheck.model_validate(data)

    except json.JSONDecodeError as e:
        raise ValueError(
            f"LLM returned invalid JSON:\n\n{content}"
        ) from e

    except Exception as e:
        raise ValueError(
            f"LLM response does not match {HallucinationCheck.__name__}:\n\n{content}"
        ) from e

    state.grounded = result.grounded
    state.hallucination_reason = result.reason

    return state