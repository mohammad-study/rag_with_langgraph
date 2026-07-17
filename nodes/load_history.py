from state import GraphState
from services.redis import history_service


def load_history(state: GraphState):

    history = history_service.get_session(
        state["session_id"]
    )

    state["history"] = history
    state["chat_history"] = history.messages

    return state