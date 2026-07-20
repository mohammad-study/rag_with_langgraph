from services.cache import cache_service
from state import GraphState


def update_cache(state: GraphState):

    if state.grounded and state.cacheable:
        cache_service.save(
            question=state.standalone_question,
            answer=state.generation
        )

    return state