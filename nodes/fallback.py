
from state import GraphState


def fallback_response(state: GraphState):

    state["generation"] = (
        "I couldn't generate a reliable answer because I couldn't find "
        "enough supporting information in the available documents."
    )

    state["cacheable"] = False

    return state