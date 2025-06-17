from pydantic import  ValidationError
from typing import List, Dict, Any
from scrapegraph_py import Client
from crewai.tools import tool
import os
from dotenv import load_dotenv
import logging
import time
import json
from src.models import  AllExtractedProducts_sec ,SingleExtractedProduct_sec
# Load API key
load_dotenv()
scrape_client = Client(api_key=os.getenv("scrapegraph"))

# Logging setup (optional but recommended)
logging.basicConfig(level=logging.INFO)




# ---------- Tool ----------
@tool
def web_scraping_tool(page_url: str) -> Dict[str, Any]:
    """
    Smart web scraping tool that extracts product details from an e-commerce product page
    and validates them against a structured schema.
    """
    start_time = time.time()
    logging.info(f"[SCRAPER] Starting extraction from: {page_url}")

    schema_str = json.dumps(SingleExtractedProduct_sec.schema(), indent=2)

    try:
        response = scrape_client.smartscraper(
            website_url=page_url,
            user_prompt=(
                f"Extract a valid JSON object that matches the following Pydantic schema:\n"
                f"```json\n{schema_str}\n```"
            )
        )

        if isinstance(response, str):
            response = json.loads(response)

        details = response.get("details", response)

        validated = SingleExtractedProduct_sec(**details)
        logging.info(f"[SCRAPER] Successfully extracted and validated product: {validated.product_title}")

        return {
            "page_url": page_url,
            "status": "success",
            "duration_sec": round(time.time() - start_time, 2),
            "product": validated.dict()
        }

    except (ValidationError, KeyError, json.JSONDecodeError) as e:
        logging.warning(f"[SCRAPER] Validation or extraction failed for: {page_url} – {str(e)}")

        return {
            "page_url": page_url,
            "status": "failed",
            "error": str(e),
            "duration_sec": round(time.time() - start_time, 2),
            "product": None
        }
