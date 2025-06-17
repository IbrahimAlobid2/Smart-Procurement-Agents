import os
from crewai import Agent , Task
from src.providers import compound_llm
from src.models import SuggestedSearchQuerie

output_dir = '/src/ai-agent-output'

search_queries_recommendation = Agent(
    role="E-Commerce Search Query Generator",
    goal="Generate highly targeted search queries that lead directly to individual product pages on specific e-commerce sites.",
    backstory="\n".join([
        "You are an expert in crafting precise and effective search queries tailored for e-commerce platforms.",
        "Your goal is to help procurement agents discover the best products by generating optimized queries that return direct product page links, not general category or ad pages.",
        "You deeply understand how search engines work and how to structure queries that maximize precision and relevance.",
        "You always use domain restriction (e.g., site:) to target results from trusted sources.",
        "You enrich the queries by including product features, specifications, or model numbers if available, and ensure the queries match the preferred language and country context.",
        "Your output must be a list of clear, diverse, and value-focused search queries ready to be used by a search engine agent.",
    ]),
    llm=compound_llm,
    verbose=True
)

    
search_queries_recommendation_task = Task(
    description="\n".join([
        "Your task is to generate high-quality search queries for purchasing '{product_name}' at the best possible value-for-price.",
        "These queries will be used to search e-commerce platforms specifically in {country_name}.",
        "Limit the search scope to the following websites only: {websites_list}.",
        "You must generate up to {no_keywords} diverse search queries in the {language} language.",
        "",
        "Guidelines for generating the queries:",
        "• Focus on producing queries that directly return individual product pages (not categories or ads).",
        "• Use the 'site:' operator to restrict results to the provided websites (e.g., site:{websites_list}).",
        "• Include product-specific attributes like model number, specs, or common keywords when possible.",
        "• Reflect real buyer behavior—think like a person comparing options online.",
        "• Ensure all queries are written fluently and naturally in {language}.",
        "",
        "Examples of good queries (in English):",
        "- site:noon.com 'HP Envy 13 x360 laptop 16GB RAM best price in Syria'",
        "- site:opensooq.com 'iPhone 13 128GB black brand new Damascus'",
    ]),
    expected_output="A JSON object containing a list of suggested search queries.",
    output_json=SuggestedSearchQuerie,
    output_file=os.path.join(output_dir, "step_1_suggested_search_queries.json"),
    agent=search_queries_recommendation
)
