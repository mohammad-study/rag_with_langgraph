from langchain_core.prompts import ChatPromptTemplate

from prompts.generate import generation_prompt
from models.response_model import GenerationResponse
from services.llm import llm

from state import GraphState


def generate_answer(state: GraphState):

    prompt = ChatPromptTemplate.from_template(
        generation_prompt
    )

    structured_llm = llm.with_structured_output(
        GenerationResponse
    )

    generation_chain = prompt | structured_llm

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

    state.generation = response.answer

    return state