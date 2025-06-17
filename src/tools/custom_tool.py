import os
import json
from dotenv import load_dotenv
from crewai.tools import tool
from tavily import TavilyClient

# Load environment variables from .env
load_dotenv()

# Initialize the search client
search_client = TavilyClient(api_key=os.getenv("TVLY_SEARCH_API_KEY"))


@tool
def read_json(file_path: str) -> dict:
    """
    Reads a JSON file from the specified path and returns its content as a Python dictionary.
    Handles both UTF-8 and Latin-1 encoded files gracefully.

    Parameters:
        file_path (str): Path to the JSON file.

    Returns:
        dict: Parsed content of the JSON file.
    """
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    except UnicodeDecodeError:
        with open(file_path, 'r', encoding='latin1') as f:
            return json.load(f)
    except FileNotFoundError:
        return {"error": f"File not found: {file_path}"}
    except json.JSONDecodeError:
        return {"error": "Invalid JSON format."}


@tool
def search_engine_tool(query: str) -> dict:
    """
    Performs a web search using the Tavily search client for a given query string.

    Parameters:
        query (str): The search query to execute.

    Returns:
        dict: Search results containing titles, URLs, content snippets, and confidence scores.
    """
    try:
        return search_client.search(query)
    except Exception as e:
        return {
            "error": str(e),
            "message": "Search failed. Please check your API key or query."
        }
