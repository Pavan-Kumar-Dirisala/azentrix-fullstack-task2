import os
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI

load_dotenv()

if not os.getenv("OPENAI_API_KEY"):
    raise ValueError("OPENAI_API_KEY not found in .env")

llm = ChatOpenAI(
    model="gpt-4o-mini",
    temperature=0
)

# print("LLM initialized successfully")