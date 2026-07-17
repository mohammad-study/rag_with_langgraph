from services.cache import cache_service


def update_cache(state):

    if state["grounded"] and state["cacheable"]:
        cache_service.save(
            question=state["standalone_question"],
            answer=state["generation"]
        )

    return state