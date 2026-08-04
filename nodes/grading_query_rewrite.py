import json

from langchain_core.prompts import ChatPromptTemplate

from state import GraphState
from prompts.grading_query_rewrite import query_rewrite_prompt
from models.grading_query_rewrite import QueryRewriteResponse
from services.llm import llm


def rewrite_query(state: GraphState):

    prompt = ChatPromptTemplate.from_template(
        query_rewrite_prompt
    )

    query_rewrite_chain = prompt | llm

    response = query_rewrite_chain.invoke(
        {
            "chat_history": state.chat_history,
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
        result = QueryRewriteResponse.model_validate(data)

    except json.JSONDecodeError as e:
        raise ValueError(
            f"LLM returned invalid JSON:\n\n{content}"
        ) from e

    except Exception as e:
        raise ValueError(
            f"LLM response does not match {QueryRewriteResponse.__name__}:\n\n{content}"
        ) from e

    state.rewritten_question = result.rewritten_question
    state.retrieved_documents = []
    state.document_rewrite_attempt += 1

    return state