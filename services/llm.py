import os
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
load_dotenv()


llm = ChatOpenAI(
    model="Qwen/Qwen2.5-7B-Instruct",
    base_url="https://router.huggingface.co/v1",
    api_key=os.getenv("HF_TOKEN"),
)



'''
llm = ChatOpenAI(
    model="cohere/north-mini-code:free",
    base_url="https://openrouter.ai/api/v1",
    api_key=os.getenv("OPENROUTER_API_KEY"),
)

#print(llm.invoke("What is the capital of France?"))
'''