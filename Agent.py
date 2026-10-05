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
topic = input("Enter the topic you want to research: ")

researcher = Agent(
    role="Senior Research Analyst",
    goal=f"Find latest key News about ({topic})",
    backstory="You are an expert analyst.",
    llm=llm,
)

writer = Agent(
    role="Expert Content Writer",
    goal=f"Turn research into a clear, short summary about ({topic})",
    backstory="You write simple, readable summaries.",
    llm=llm,
)

research_task = Task(
    description=f"Research the topic: {topic}. List the 5 most important points.",
    expected_output="A bullet list of 5 key points.",
    agent=researcher,
)

write_task = Task(
    description=f"Write a 150-word summary using the research on {topic}.",
    expected_output="A 150-word summary.",
    agent=writer,
    context=[research_task],
)

crew = Crew(
    agents=[researcher, writer],
    tasks=[research_task, write_task],
    process=Process.sequential,
)

result = crew.kickoff(inputs={"topic": topic})
print(result)
