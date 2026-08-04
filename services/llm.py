import os
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from config import config

load_dotenv()

llm_config = config["llm"]["alternative"]

llm = ChatOpenAI(
    model=llm_config["model"],
    base_url=llm_config["base_url"],
    api_key=os.getenv(llm_config["api_key_env"]),
)
