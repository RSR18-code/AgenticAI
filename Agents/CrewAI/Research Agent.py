import os
from pathlib import Path

from crewai import Agent, LLM
from dotenv import load_dotenv

load_dotenv(Path(__file__).with_name(".env"))

if not os.environ.get("GEMINI_API_KEY"):
    raise RuntimeError("Set the GEMINI_API_KEY environment variable before running this script.")

llm = LLM(model="gemini/gemini-2.0-flash")

researcher = Agent(
    role="Research Analyst",
    goal="Find key facts about india",
    backstory="You are a careful analyst.",
    llm=llm,
)
