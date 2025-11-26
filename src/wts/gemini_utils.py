import streamlit as st
from google import genai

ANALYSIS_PROMPT = """
You are an expert academic research assistant.
Your task is to find and analyze the research paper identified by the following query: "{query}"

Use Google Search to find the paper's full text, abstract, or detailed summary.
Once found, extract specific, accurate information to fill the report below.

STRICTNESS RULES:
- If you cannot find specific details (like Sample Size) in the search results, strictly write "Not specified in search results".
- Do not hallucinate or guess numbers.

---
REPORT FORMAT:

1. Gist: A concise summary of what this paper is about and why it matters.
2. Problem: A clear statement of the problem addressed by the paper.
3. Method: A detailed description of the research methodology used.
4. Assumptions: What theoretical or practical assumptions were made?
5. Sample Size (N): The specific number of participants or dataset size (look for N=...).
6. Key Findings: Bullet points of the most important results, facts, and figures.
7. Limitations and Caveats: What weakness or limitations did the authors admit to?
8. Conclusion: A conclusion that ties together the paper's contributions and implications.
"""


@st.cache_data(show_spinner=False)
def analyze_via_search(api_key: str, user_query: str) -> str | None:
    """
    Uses Gemini to find and analyze a paper.

    :param api_key: Gemini API Key
    :param user_query: A DOI, URL, or Paper Title.
    """
    if not api_key:
        raise ValueError("API Key is missing.")

    client = genai.Client()

    formatted_prompt = ANALYSIS_PROMPT.format(query=user_query)

    try:
        response = client.models.generate_content(
            model="gemini-2.5-flash", contents=formatted_prompt
        )
        return response.text
    except Exception as e:
        raise e
