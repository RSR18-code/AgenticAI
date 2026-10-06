import os
from pathlib import Path

from dotenv import load_dotenv

from email_output import send_result_email
from research import run_research


def main() -> None:
    load_dotenv(dotenv_path=Path(__file__).with_name(".env"), override=False)

    topic = input("Enter the topic you want to research: ").strip()
    if not topic:
        raise ValueError("The research topic cannot be empty.")

    result = run_research(topic)
    print(result)

    if send_result_email(topic, result):
        print(f"Research results emailed to {os.environ['EMAIL_RECIPIENT']}.")
    else:
        print("Email not configured; skipping email delivery.")


if __name__ == "__main__":
    main()
