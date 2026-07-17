import os
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI

load_dotenv()


llm = ChatOpenAI(
    model="nvidia/nemotron-3-nano-omni-30b-a3b-reasoning:free",
    base_url="https://openrouter.ai/api/v1",
    api_key=os.getenv("OPENROUTER_API_KEY"),
)
