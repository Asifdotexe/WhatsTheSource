"""
This module provides a template for the Large Language Model API prompt.
"""

import google.generativeai as genai
from google.api_core.exceptions import GoogleAPIError

ANALYSIS_PROMPT_TEMPLATE = """
You are an expert academic researcher, Analyze the following {context_type} of a research paper.

Your goal is to extract specific, accurate, and relevant information. If the information is missing, (e.g., Sample Size not mentioned), Strictly say "Not specified in text".
This strictness is required to prevent "hallucinations" ensuring the user trusts the output.

Format the output in clean Markdown.

---
TEXT TO ANALYZE:
{text_content}
---

Please provide the following sections:
    1. Gist: A concise summary of what this paper is about and why it matters
    2. Problem: A clear statement of the problem addressed by the paper
    3. Method: A detailed description of the research methodology used
    4. Assumptions: What theoretical or practical assumptions were made?
    5. Sample Size (N): Specifically look for 'N=' or descriptions of the study participants/dataset size
    6. Key Findings: Bullet points of the most important results, facts, and figures.
    7. Limitations and Caveats: What weakness or limitations did the authors admit to?
    8. Conclusion: A conclusion that ties together the paper's contributions and implications
"""


def analyze_with_gemini(
    api_key: str, text: str, context_type: str, max_tokens: int = 30000
) -> str:
    """
    Orchestrates the LLM interaction to analyze the research text.

    :param api_key: The API key for the Gemini API.
    :param text: The text to analyze.
    :param context_type: The type of context (e.g., abstract, full text).
    :param max_tokens: The maximum number of tokens to generate.
    :return: The analysis result.
    """
    if not api_key:
        raise ValueError("API key is required")

    genai.configure(api_key=api_key)
    model = genai.get_model("gemini-2.5-flash")

    # Truncate to max_tokens as a soft sanity limit.
    truncated_text = text[:max_tokens]

    formatted_prompt = ANALYSIS_PROMPT_TEMPLATE.format(
        context_type, context_type, text_content=truncated_text
    )

    try:
        response = model.generate_content(formatted_prompt)
        return response.text
    except GoogleAPIError as e:
        raise e
