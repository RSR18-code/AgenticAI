import os
import smtplib
from pathlib import Path

import streamlit as st
from dotenv import load_dotenv

from email_output import is_valid_email_address, send_result_email
from research import run_research

load_dotenv(dotenv_path=Path(__file__).with_name(".env"), override=False)

st.set_page_config(
    page_title="Research Desk",
    page_icon="✳",
    layout="centered",
)

st.markdown(
    """
    <style>
    :root {
        color-scheme: light;
    }
    .stApp {
        background:
            radial-gradient(ellipse at 12% 0%, #e4f4ee 0, transparent 36rem),
            #f7f9f8;
    }
    .block-container {
        max-width: 820px;
        padding-top: 4rem;
        padding-bottom: 4rem;
    }
    .eyebrow {
        color: #147d64;
        font-size: 0.78rem;
        font-weight: 700;
        letter-spacing: 0.13em;
        text-transform: uppercase;
    }
    h1 {
        color: #152b27;
        letter-spacing: -0.045em;
        line-height: 1.08;
    }
    .intro {
        color: #53645f;
        font-size: 1.08rem;
        line-height: 1.65;
        max-width: 42rem;
    }
    div[data-testid="stForm"] {
        background: #ffffff;
        border: 1px solid #dce7e2;
        border-radius: 18px;
        padding: 1.5rem;
        box-shadow: 0 16px 48px rgba(24, 54, 45, 0.07);
    }
    div.stButton > button[kind="primary"],
    div[data-testid="stFormSubmitButton"] > button {
        background: #147d64;
        border: 1px solid #147d64;
        border-radius: 10px;
        color: #ffffff;
        min-height: 3rem;
        font-weight: 650;
    }
    div.stButton > button[kind="primary"]:hover,
    div[data-testid="stFormSubmitButton"] > button:hover {
        background: #0f6853;
        border-color: #0f6853;
    }
    div[data-testid="stFormSubmitButton"] > button:focus-visible {
        outline: 3px solid #84cdb7;
        outline-offset: 2px;
    }
    div[data-testid="stVerticalBlockBorderWrapper"] {
        background: #ffffff;
        border-color: #dce7e2;
        border-radius: 16px;
    }
    @media (max-width: 640px) {
        .block-container {
            padding: 2rem 1rem;
        }
        div[data-testid="stForm"] {
            padding: 1rem;
        }
    }
    </style>
    """,
    unsafe_allow_html=True,
)

st.markdown('<p class="eyebrow">RSR AI Solutions · Research assistant</p>', unsafe_allow_html=True)
st.title("Turn a topic into a clear briefing.")
st.markdown(
    '<p class="intro">Enter a subject and the research team will gather current '
    "coverage, then shape it into a concise, readable summary.</p>",
    unsafe_allow_html=True,
)

email_ready = all(
    os.environ.get(setting, "").strip()
    for setting in ("GMAIL_ADDRESS", "GMAIL_APP_PASSWORD", "EMAIL_RECIPIENT")
)

with st.form("research_form"):
    topic = st.text_input(
        "What would you like to research?",
        placeholder="For example: India's renewable energy transition",
        help="Use a specific topic for more focused research.",
    )
    email_result = st.checkbox(
        "Email the results",
        disabled=not email_ready,
        help=(
            "Configure GMAIL_ADDRESS, GMAIL_APP_PASSWORD, and EMAIL_RECIPIENT "
            "in your local .env file to enable email."
        ),
    )
    additional_recipient = st.text_input(
        "Also send to another email address (optional)",
        placeholder="name@example.com",
        disabled=not email_ready,
        help=(
            "When email is selected, the configured recipient will still receive "
            "a copy. This adds one more recipient."
        ),
    )
    submitted = st.form_submit_button(
        "Generate research",
        type="primary",
        use_container_width=True,
    )

if not email_ready:
    st.caption(
        "Email is optional. Add Gmail settings to your local .env file to enable it."
    )

if submitted:
    normalized_topic = topic.strip()
    if not normalized_topic:
        st.error("Enter a topic before generating research.")
    elif (
        email_result
        and additional_recipient.strip()
        and not is_valid_email_address(additional_recipient)
    ):
        st.error("Enter a valid additional email address.")
    else:
        with st.spinner("Researching and preparing your briefing…"):
            result = run_research(normalized_topic)
        st.session_state["research_topic"] = normalized_topic
        st.session_state["research_result"] = result

        if email_result:
            try:
                sent = send_result_email(
                    normalized_topic,
                    result,
                    additional_recipient=additional_recipient,
                )
            except (OSError, RuntimeError, smtplib.SMTPException) as exc:
                st.error(f"Research is ready, but email delivery failed: {exc}")
            else:
                if sent:
                    recipients = [os.environ["EMAIL_RECIPIENT"]]
                    if (
                        additional_recipient.strip()
                        and additional_recipient.casefold()
                        != os.environ["EMAIL_RECIPIENT"].casefold()
                    ):
                        recipients.append(additional_recipient.strip())
                    st.success(f"Results emailed to: {', '.join(recipients)}.")
                else:
                    st.warning("Email is not configured, so no email was sent.")

if "research_result" in st.session_state:
    st.divider()
    st.markdown(
        f"### Research briefing: {st.session_state['research_topic']}"
    )
    with st.container(border=True):
        st.markdown(st.session_state["research_result"])
