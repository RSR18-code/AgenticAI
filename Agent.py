import os
from pathlib import Path

from crewai import Agent, Crew, LLM, Process, Task
from dotenv import load_dotenv

from email_output import send_result_email

load_dotenv(dotenv_path=Path(__file__).with_name(".env"), override=False)

api_key = os.environ.get("GEMINI_API_KEY")
if not api_key:
    raise RuntimeError(
        "Set the GEMINI_API_KEY environment variable or create a .env file next to Agent.py before running this script."
    )

llm = LLM(model="gemini-3.5-flash-lite", api_key=api_key)

# Enter the topic
topic = input("Enter the topic you want to research: ")

researcher = Agent(
    role="Senior Research Analyst",
    goal=f"Find latest key News about ({topic})",
    backstory="You are an expert analyst.",
    llm=llm,
)

writer = Agent(
    role="Expert Content Writer",
    goal=f"Turn research into a clear, short summary about ({topic}) ",
    backstory="You write simple, readable summaries.",
    llm=llm,
)

research_task = Task(
    description=f"Research the topic: {topic}. List down all the important and latest news about it",
    expected_output="Get the latest news and key points about the topic.",
    agent=researcher,
)

write_task = Task(
    description=f"Write a 150-word summary using the research on {topic}.",
    expected_output="A bullet list of 5 key points for each side (pros and cons).",
    agent=writer,
    context=[research_task],
)

crew = Crew(
    agents=[researcher, writer],
    tasks=[research_task, write_task],
    process=Process.sequential,
)

result = crew.kickoff(inputs={"topic": topic})
result_text = str(result)
print(result_text)

if send_result_email(topic, result_text):
    print(f"Research results emailed to {os.environ['EMAIL_RECIPIENT']}.")
else:
    print("Email not configured; skipping email delivery.")
