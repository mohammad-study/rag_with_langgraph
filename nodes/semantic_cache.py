from services.cache import cache_service


def semantic_cache(state):

    answer = cache_service.lookup(
        state.standalone_question
    )

    if answer:

        state.cache_hit = True
        state.cached_response = answer
        state.generation = answer

    else:

        state.cache_hit = False
        state.cached_response = None
        state.generation = None

    return state