import os
from crewai import Agent , Task
from src.providers import compound_llm
from src.models import AllSearchResults
from src.tools import search_engine_tool 

output_dir = '/src/ai-agent-output'


search_engine = Agent(
    role="E-Commerce Search Execution Agent",
    goal="Execute search queries and retrieve relevant product pages with high confidence scores from trusted e-commerce websites.",
    backstory=(
        "You are a specialized search execution agent. Your role is to take pre-optimized search queries "
        "and retrieve only the most relevant product pages from the web. "
        "You are highly skilled at evaluating search results, filtering out irrelevant, suspicious, or low-quality links, "
        "and returning structured, trustworthy results for procurement analysis."
    ),
    llm=compound_llm,
    tools=[search_engine_tool],
    verbose=True
)


search_engine_task = Task(
    description="\n".join([
        "Execute each of the provided search queries to find individual product pages on e-commerce websites.",
        "You must collect results for all suggested queries and evaluate them carefully.",
        "",
        "Guidelines:",
        "• Exclude any link that appears suspicious, broken, or not leading to a direct product page.",
        "• Discard results with a confidence score lower than ({score_th}).",
        "• Do not include category pages, advertisements, or generic site listings.",
        "• Prefer results that contain specific product titles, pricing, and descriptions.",
        "",
        "The final output should be a structured JSON object following the AllSearchResults model. "
        "It will later be used to compare prices across websites for procurement."
    ]),
    expected_output="A JSON object conforming to the AllSearchResults model.",
    output_json=AllSearchResults,
    output_file=os.path.join(output_dir, "step_2_search_results.json"),
    agent=search_engine
)
