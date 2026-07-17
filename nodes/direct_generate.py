from state import GraphState
from prompts.direct_generate import direct_generation_prompt
from langchain_core.prompts import ChatPromptTemplate

from services.llm import llm
from models.direct_generation_response import DirectGenerationResponse



def direct_generate(state: GraphState):

    prompt = ChatPromptTemplate.from_template(
        direct_generation_prompt
    )

    structured_llm = llm.with_structured_output(
        DirectGenerationResponse
    )

    direct_generation_chain = prompt | structured_llm


    response = direct_generation_chain.invoke(
        {
            "question": state["standalone_question"]
        }
    )

    state["generation"] = response.answer
    state["cacheable"] = False

    return state