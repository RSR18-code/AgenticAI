import os
import re
import smtplib
import ssl
from email.message import EmailMessage


def is_valid_email_address(address: str) -> bool:
    """Return whether an address has a basic, safe email-address shape."""
    return bool(
        re.fullmatch(
            r"[^@\s]+@(?:[^@\s.]+\.)+[^@\s.]{2,}",
            address.strip(),
        )
    )


def send_result_email(
    topic: str,
    output: str,
    additional_recipient: str | None = None,
) -> bool:
    """Email the research output via Gmail when SMTP settings are configured."""
    required_settings = ("GMAIL_ADDRESS", "GMAIL_APP_PASSWORD", "EMAIL_RECIPIENT")
    settings = {name: os.environ.get(name, "").strip() for name in required_settings}
    configured_settings = [name for name, value in settings.items() if value]

    if not configured_settings:
        return False

    missing_settings = [name for name, value in settings.items() if not value]
    if missing_settings:
        missing = ", ".join(missing_settings)
        raise RuntimeError(f"Email configuration is incomplete. Set: {missing}.")

    recipients = [settings["EMAIL_RECIPIENT"]]
    if additional_recipient and additional_recipient.strip():
        extra_recipient = additional_recipient.strip()
        if not is_valid_email_address(extra_recipient):
            raise ValueError("The additional recipient email address is invalid.")
        if extra_recipient.casefold() not in {
            recipient.casefold() for recipient in recipients
        }:
            recipients.append(extra_recipient)

    message = EmailMessage()
    message["From"] = settings["GMAIL_ADDRESS"]
    message["To"] = ", ".join(recipients)
    safe_topic = " ".join(topic.splitlines()).strip()
    message["Subject"] = f"Research results: {safe_topic}"
    message.set_content(output)

    app_password = settings["GMAIL_APP_PASSWORD"].replace(" ", "")
    with smtplib.SMTP_SSL(
        "smtp.gmail.com",
        465,
        context=ssl.create_default_context(),
    ) as smtp:
        smtp.login(settings["GMAIL_ADDRESS"], app_password)
        refused_recipients = smtp.send_message(message, to_addrs=recipients)

    if refused_recipients:
        rejected = ", ".join(refused_recipients)
        raise RuntimeError(f"Gmail refused the message for: {rejected}.")

    return True
