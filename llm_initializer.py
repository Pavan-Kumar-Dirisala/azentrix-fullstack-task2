import os
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI

load_dotenv()

if not os.getenv("OPENAI_API_KEY"):
    raise ValueError("OPENAI_API_KEY not found in .env")

llm_mini = ChatOpenAI(
    model="gpt-5-mini",
    temperature=0
)
llm = ChatOpenAI(
    model = "gpt-5",
    temperature = 0
)
# print("LLM initialized successfully")