from crewai import LLM
import os
from dotenv import load_dotenv
load_dotenv()

open_router_api_key = os.getenv("OPEN_ROUTER_API_KEY")
os.environ["OPENAI_API_KEY"] =  os.getenv("OPENAI_API_KEY")
os.environ['GROQ_API_KEY']  = os.getenv("GROQ_API_KEY")

compound_llm = groq  = LLM(
    model="groq/compound-beta",
    temperature=0
)


deepseek_v3__llm= LLM(
    model="openrouter/deepseek/deepseek-chat-v3-0324:free",
    base_url="https://openrouter.ai/api/v1",
    api_key=open_router_api_key,
    temperature=0
)

mistral_small_llm = LLM(
    model="openrouter/mistralai/mistral-small-3.1-24b-instruct:free",
    base_url="https://openrouter.ai/api/v1",
    api_key=open_router_api_key,
    temperature=0
)


gpt_4o_mini = LLM(model="gpt-4o-mini-2024-07-18", temperature=0 )