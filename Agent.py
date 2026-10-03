import os
from pathlib import Path

from crewai import Agent, Crew, LLM, Process, Task
from dotenv import load_dotenv

load_dotenv(dotenv_path=Path(__file__).with_name(".env"), override=False)

api_key = os.environ.get("GEMINI_API_KEY")
if not api_key:
    raise RuntimeError(
        "Set the GEMINI_API_KEY environment variable or create a .env file next to Agent.py before running this script."
    )

llm = LLM(model="gemini-3.5-flash-lite", api_key=api_key)

researcher = Agent(
    role="Research Analyst",
    goal="Find key facts about India",
    backstory="You are a careful analyst.",
    llm=llm,
)

writer = Agent(
    role="Content Writer",
    goal="Turn research into a clear, short summary",
    backstory="You write simple, readable summaries.",
    llm=llm,
)

research_task = Task(
    description="Research the topic: India. List the 5 most important points.",
    expected_output="A bullet list of 5 key points.",
    agent=researcher,
)

write_task = Task(
    description="Write a 150-word summary using the research.",
    expected_output="A 150-word summary.",
    agent=writer,
    context=[research_task],
)

crew = Crew(
    agents=[researcher, writer],
    tasks=[research_task, write_task],
    process=Process.sequential,
)

result = crew.kickoff(inputs={"topic": "India"})
print(result)
