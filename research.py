import os
from pathlib import Path

from crewai import Agent, Crew, LLM, Process, Task
from dotenv import load_dotenv


def run_research(topic: str) -> str:
    """Run the research crew for a topic and return its result as text."""
    normalized_topic = topic.strip()
    if not normalized_topic:
        raise ValueError("The research topic cannot be empty.")

    load_dotenv(dotenv_path=Path(__file__).with_name(".env"), override=False)

    api_key = os.environ.get("GEMINI_API_KEY")
    if not api_key:
        raise RuntimeError(
            "Set GEMINI_API_KEY in the environment or in a .env file next to the app."
        )

    llm = LLM(model="gemini-3.5-flash-lite", api_key=api_key)

    researcher = Agent(
        role="Senior Research Analyst",
        goal=f"Find the latest key news about {normalized_topic}",
        backstory="You are an expert analyst.",
        llm=llm,
    )

    writer = Agent(
        role="Expert Content Writer",
        goal=f"Turn research into a clear, actionable summary about {normalized_topic}",
        backstory="You write actionable, readable summaries.",
        llm=llm,
    )

    research_task = Task(
        description=(
            f"Research the topic: {normalized_topic}. "
            "List the important and latest news about it."
        ),
        expected_output="The latest news and key points about the topic.",
        agent=researcher,
    )

    write_task = Task(
        description=(
            f"Write a 300-word summary using the research on {normalized_topic}."
        ),
        expected_output="A concise summary highlighting key points and pros and cons.",
        agent=writer,
        context=[research_task],
    )

    crew = Crew(
        agents=[researcher, writer],
        tasks=[research_task, write_task],
        process=Process.sequential,
    )
    result = crew.kickoff(inputs={"topic": normalized_topic})
    return str(result)
