from crewai import Agent, Task
import os
from src.providers import compound_llm ,deepseek_v3__llm
from src.tools import read_json

output_dir = './src/ai-agent-output'

# ---------------- AGENT ------------------
procurement_report = Agent(
    role="Procurement Report Generator",
    goal="Generate a detailed, professional HTML procurement report with structured insights",
    backstory=(
        "You're a senior procurement analyst and report author. Your job is to convert structured product data into "
        "a professional and visually compelling HTML report that includes summary, analysis, recommendations, and data comparisons. "
        "The goal is to help the procurement department make data-informed decisions based on e-commerce product evaluations."
    ),
    llm=compound_llm,
    verbose=True,
    tools=[read_json]
)

# ---------------- TASK ------------------
procurement_report_task = Task(
    description="\n".join([
        "Generate a professional HTML procurement report using the content from the JSON file at {products_file}.",
        "The report should reflect a polished UI using the Bootstrap CSS framework.",
        "It should be personalized based on the context of the company and industry.",
        "The report **must be written in {language} language**.",
        "Use tables, section headers, and optional visualizations (charts) if relevant.",
        "Organize the report with the following structure:",
        "",
        "1. **Executive Summary** – Key findings and a quick summary of the report.",
        "2. **Introduction** – Purpose and objectives of the procurement.",
        "3. **Methodology** – How product data was collected and filtered.",
        "4. **Findings** – Comparative analysis of products (prices, specifications).",
        "5. **Analysis** – Commentary on value-for-money, patterns, outliers.",
        "6. **Recommendations** – What to buy and why, with justification.",
        "7. **Conclusion** – Wrap-up of insights and next steps.",
        "",
        "Ensure the generated HTML is ready to be embedded or viewed in a browser directly.",
    ]),
    expected_output="An HTML file containing the full procurement report in professional format.",
    output_file=os.path.join(output_dir, "step_4_procurement_report.html"),
    agent=procurement_report
)
