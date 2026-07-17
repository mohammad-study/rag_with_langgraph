from services.llm import llm
from state import GraphState

from models.router import Router
from prompts.router import router_prompt

from langchain_core.prompts import ChatPromptTemplate


def route_query(state: GraphState):
    prompt = ChatPromptTemplate.from_template(router_prompt)

    llm_with_structured_response = llm.with_structured_output(Router)
    router_chain = prompt | llm_with_structured_response

    response = router_chain.invoke(
        {
            "question": state["standalone_question"]
        }
    )


    state["router"] = response.route

    return state

