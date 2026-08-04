import json
from state import GraphState
from services.llm import llm

from models.document_grade import DocumentGrade
from prompts.document_grader import document_grader_prompt

from langchain_core.prompts import ChatPromptTemplate


def grade_documents(state: GraphState):

    prompt = ChatPromptTemplate.from_template(
        document_grader_prompt
    )
    document_grader_chain = prompt | llm

    docs = "\n\n".join(
        doc.chunk
        for doc in state.retrieved_documents
    )

    response = document_grader_chain.invoke(
        {
            "question": state.standalone_question,
            "documents": docs,
        }
    )

    # Extract response text
    content = response.content.strip()

    # Remove markdown fences if present
    if content.startswith("```"):
        content = content.replace("```json", "").replace("```", "").strip()

    try:
        # Parse JSON
        data = json.loads(content)

        # Validate with Pydantic
        result = DocumentGrade.model_validate(data)

    except Exception as e:
        raise ValueError(
            f"Invalid GuardrailResponse from LLM:\n\n{content}"
        ) from e


    if result.relevant:
        state.documents_relevant = result.relevant

    else:
        state.documents_relevant = result.relevant
        state.grounded = False
        state.hallucination_reason = None

    return state