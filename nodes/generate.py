import json
from langchain_core.prompts import ChatPromptTemplate

from prompts.generate import generation_prompt
from models.response_model import GenerationResponse
from services.llm import llm

from state import GraphState


def generate_answer(state: GraphState):

    prompt = ChatPromptTemplate.from_template(
        generation_prompt
    )

    generation_chain = prompt | llm

    context = "\n\n".join(
        f"""
    Section: {doc.section}

    Subsection: {doc.subsection}

    Content:
    {doc.chunk}
    """
            for doc in state.retrieved_documents
        )

    response = generation_chain.invoke(
        {
            "chat_history": state.chat_history,
            "context": context,
            "question": state.standalone_question,
        }
    )

    content = response.content.strip()

    # Remove markdown fences if present
    if content.startswith("```"):
        content = (
            content.replace("```json", "")
            .replace("```", "")
            .strip()
        )

    try:
        data = json.loads(content)
        result = GenerationResponse.model_validate(data)

    except json.JSONDecodeError as e:
        raise ValueError(
            f"LLM returned invalid JSON:\n\n{content}"
        ) from e

    except Exception as e:
        raise ValueError(
            f"LLM response does not match {GenerationResponse.__name__}:\n\n{content}"
        ) from e



    state.generation = result.answer

    return state