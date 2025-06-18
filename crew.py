from src.Agents import (
    search_queries_recommendation, search_queries_recommendation_task,
    search_engine, search_engine_task,
    scraper, scraping_task,
    procurement_report, procurement_report_task
)
from crewai.knowledge.source.string_knowledge_source import StringKnowledgeSource
import agentops
from crewai import Crew, Process
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
agentops_api_key = os.getenv("Agentops_API_KEY")

# Initialize AgentOps (for tracking and monitoring agents)
agentops.init(
    api_key=agentops_api_key,
    skip_auto_end_session=True
)

# Company context (adapt this to your business)
company_context = StringKnowledgeSource(
    content="""
        SmartProcure Syria is a leading procurement firm specialized in sourcing technology products 
        for organizations and businesses in Syria, focusing on achieving the best value-for-money from regional e-commerce platforms.
    """
)

# Assemble the crew of agents and tasks for the procurement workflow
procurement_crew = Crew(
    agents=[
        search_queries_recommendation,
        search_engine,
        scraper,
        procurement_report
    ],
    tasks=[
        search_queries_recommendation_task,
        search_engine_task,
        scraping_task,
        procurement_report_task
    ],
    process=Process.sequential,    # Ensures agents execute in the right order
    knowledge_sources=[company_context],
    verbose=True,
)
