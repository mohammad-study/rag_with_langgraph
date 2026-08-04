import json
from state import GraphState
from prompts.direct_generate import direct_generation_prompt
from langchain_core.prompts import ChatPromptTemplate

from services.llm import llm
from models.direct_generation_response import DirectGenerationResponse



def direct_generate(state: GraphState):

    prompt = ChatPromptTemplate.from_template(
        direct_generation_prompt
    )

    direct_generation_chain = prompt | llm


    response = direct_generation_chain.invoke(
        {
            "question": state.standalone_question
        }
    )

    content = response.content.strip()
    
    try:
        # Parse JSON
        data = json.loads(content)

        # Validate with Pydantic
        result = DirectGenerationResponse.model_validate(data)

    except Exception as e:
        raise ValueError(
            f"Invalid GuardrailResponse from LLM:\n\n{content}"
        ) from e

    state.generation = result.answer
    state.cacheable = False

    return state