from services.redis import history_service
from state import GraphState


def save_history(state: GraphState):

    history_service.save_conversation(

        session_id=state["session_id"],

        question=state["question"],

        answer=state["generation"]

    )

    return state