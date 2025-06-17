import os
from crewai import Agent , Task
from src.providers import compound_llm
from src.models import AllExtractedProducts
output_dir = '/src/ai-agent-output'


scraper = Agent(
    role="Expert E-commerce Scraping Agent",
    goal="Extract high-quality product information from e-commerce pages and convert it into structured JSON data.",
    backstory=(
        "You are an advanced scraping agent trained to read and understand HTML structures of product pages on e-commerce sites. "
        "You focus on retrieving accurate product data including title, price, specifications, availability, and product images. "
        "You are error-tolerant — if a URL is broken, leads to a non-product page, or returns malformed content, you log it and continue without failing. "
        "You must only include products that follow the `SingleExtractedProduct` schema and are valid for the procurement report."
    ),
    llm=compound_llm,
    tools=[web_scraping_tool, read_json],
    verbose=True,
    allow_delegation=False,
)



scraping_task = Task(
    description="\n".join([
        "You are given a list of product page URLs stored in the variable {search_results}.",
        f"Your goal is to extract product information and recommend the top { '{top_recommendations_no}' } products.",
        "",
        "Instructions:",
        "1. Visit each URL in the list and scrape the product details.",
        "2. For each product, extract the following fields as defined in the `SingleExtractedProduct` model:",
        "   • Title",
        "   • Current price (float) and currency (e.g., SYP)",
        "   • Original price and discount percentage if available",
        "   • Product image URL",
        "   • 1 to 5 key specifications (focus on technical or purchasing-relevant specs)",
        "   • Availability (e.g., in stock, out of stock)",
        "   • Agent recommendation rank (1–5)",
        "   • Notes explaining the recommendation or rejection",
        "",
        "3. Skip any broken, inaccessible, or irrelevant links and continue.",
        "4. Compile all valid products into a JSON object that matches the `AllExtractedProducts` schema.",
    ]),
    expected_output="A valid JSON object of the top recommended products conforming to the AllExtractedProducts schema.",
    output_json=AllExtractedProducts,
    output_file=os.path.join(output_dir, "step_3_products_file.json"),
    agent=scraper
)
