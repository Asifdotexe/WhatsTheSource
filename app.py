import os

import streamlit as st
from dotenv import load_dotenv

from wts import gemini_utils

load_dotenv()

st.set_page_config(page_title="What's The Source?", page_icon="🎓", layout="wide")

st.markdown(
    """
<style>
    .stTextInput input {
        font-size: 1.2rem;
        padding: 15px;
    }
</style>
""",
    unsafe_allow_html=True,
)

st.title("🎓 What's The Source?")
st.caption("Powered by Gemini 2.5 Flash")


with st.sidebar:
    st.header("Configuration")

    env_key = os.getenv("GEMINI_API_KEY", "")

    # Always show the input box, pre-filled with the env key if available.
    # This ensures the user can override it if needed, or see that it's present (masked).
    api_key = st.text_input(
        "Gemini API Key",
        value=env_key,
        type="password",
        help="Get your key from Google AI Studio",
    )

    if env_key:
        st.caption("✅ Key loaded from .env file")
    else:
        st.info("Tip: Create a .env file to auto-load your key.")

    st.markdown("---")
    st.info(
        "This tool uses Gemini's live Google Search capability to read papers from Links or DOIs."
    )

st.markdown("### What are we reading today?")
user_input = st.text_input(
    "Paste a Link, DOI, or Title",
    placeholder="e.g., https://arxiv.org/abs/1706.03762 or 10.1038/s41586-020-2649-2",
)

if st.button("Analyze Paper", type="primary", use_container_width=True):
    if not user_input:
        st.warning("Please enter a link or DOI first.")
    elif not api_key:
        st.error("Please enter your API Key in the sidebar or your .env file.")
    else:
        st.divider()

        # We use a status container to show the user the AI is "working"
        with st.status("🤖 Agent is searching and reading...", expanded=True) as status:
            try:
                # Direct call to the simplified logic
                # We pass the api_key (from env or input) explicitly
                response = gemini_utils.analyze_via_search(api_key, user_input)

                status.update(
                    label="Analysis Complete!", state="complete", expanded=False
                )

                st.subheader("Research Summary")
                st.markdown(response)

            except Exception as e:
                status.update(label="Error occurred", state="error")
                st.error(f"Agent failed: {str(e)}")
