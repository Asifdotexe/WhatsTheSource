"""
Utility functions for fetching and working with papers.
"""

import io
import logging
from http import HTTPStatus
from typing import Optional

import requests
from pypdf import PdfReader
from pypdf.errors import PyPdfError
from requests.exceptions import RequestException

logger = logging.getLogger(__name__)


def get_paper_metadata(doi: str) -> Optional[dict]:
    """
    Fetches metadata for a paper given its DOI.

        :param doi: The DOI (Digital Object Identifier) of the paper.

    :return: A dictionary containing paper metadata (title, abstract, OA status)
                or None if the request fails or the DOI is invalid.
    """
    # We strip standard prefixes to ensure successful resolution regardless of user input format.
    clean_doi = doi.strip().replace("https://doi.org/", "")

    # We explicitly request only necassary field to minimize payload size and latency
    fields = "title,abstract,isOpenAccess,openAccessPdf,authors,year"
    url = f"https://api.semanticscholar.org/graph/v1/paper/DOI:{clean_doi}?fields={fields}"

    try:
        response = requests.get(url, timeout=10)

        if response.status_code == HTTPStatus.OK:
            return response.json()

        logger.warning(
            f"Semantic Scholar API returned status: {response.status_code} for DOI {clean_doi}"
        )

    except RequestException as e:
        logger.error(f"Request error: {e}")


def extract_text_from_pdf(pdf_url: str) -> Optional[str]:
    """
    Streams a PDF from a URL into memory and extracts text content.

    :param pdf_url: The URL of the PDF file.
    :return: The extracted text content or None if the PDF cannot be read.
    """
    try:
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
        }

        response = requests.get(pdf_url, headers=headers, timeout=15)
        response.raise_for_status()

        # Creating Bytestream to handle PDF in RAM
        with io.BytesIO(response.content) as pdf_stream:
            reader = PdfReader(pdf_stream)

            text_parts: list[str] = []

            for page in reader.pages:
                extracted_text = page.extract_text()
                if extracted_text:
                    text_parts.append(extracted_text)

            return "\n".join(text_parts)

    except (RequestException, PyPdfError) as e:
        logger.error(f"Failed to extract PDF text from {pdf_url}: {e}")
