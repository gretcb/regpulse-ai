"""
LLM Processing Module

Author: Gretel

Purpose
-------
This module is responsible for transforming retrieved maritime news
into structured business insights using the OpenAI API.

Workflow
--------
Retrieved news
        ↓
Clean text
        ↓
Build prompts
        ↓
Call OpenAI
        ↓
Parse JSON response
        ↓
Return Python dictionary
"""

# ============================================================
# IMPORTS
# ============================================================

import json
import os

from dotenv import load_dotenv
from openai import OpenAI

from src.prompts import (
    SYSTEM_PROMPT,
    build_user_prompt,
)

# ============================================================
# ENVIRONMENT AND OPENAI CLIENT
# ============================================================
#
# load_dotenv() reads the variables stored in the local .env file.
#
# The API key is checked before creating the OpenAI client so
# the application can show a clear error if the key is missing.
# ============================================================

load_dotenv()

api_key = os.getenv("OPENAI_API_KEY")

if not api_key:
    raise EnvironmentError(
        "OPENAI_API_KEY is not set. "
        "Add it to your local .env file."
    )

client = OpenAI(api_key=api_key)

# ============================================================
# TEXT CLEANING
# ============================================================
#
# This function validates and cleans the news text before
# sending it to the OpenAI API.
#
# Why do we need it?
# - It prevents empty requests.
# - It removes unnecessary spaces.
# - It reduces repeated blank lines.
# - It keeps the prompt cleaner and easier for the model to read.
# ============================================================

def clean_news_text(news_text: str) -> str:
    """
    Validate and clean the retrieved news text.

    Args:
        news_text:
            Text returned by the News Retrieval module.

    Returns:
        Clean text ready to be included in the OpenAI prompt.

    Raises:
        ValueError:
            If the news text is empty or contains only spaces.
    """

    # Stop the process before calling OpenAI if no news was retrieved.
    if not news_text or not news_text.strip():
        raise ValueError(
            "No relevant maritime environmental news was found "
            "for the selected country and timeframe."
        )

    # Remove unnecessary spaces at the beginning and end of each line.
    lines = [
        line.strip()
        for line in news_text.splitlines()
    ]

    # Join the cleaned lines again.
    cleaned_text = "\n".join(lines)

    # Replace three or more consecutive line breaks with two.
    while "\n\n\n" in cleaned_text:
        cleaned_text = cleaned_text.replace("\n\n\n", "\n\n")

    # Remove spaces or line breaks at the beginning and end.
    return cleaned_text.strip()


# ============================================================
# LLM PROCESSING
# ============================================================
#
# This is the main function of this module.
#
# It:
# 1. Validates and cleans the retrieved news.
# 2. Builds the dynamic prompt.
# 3. Sends the prompt to OpenAI.
# 4. Parses the JSON response.
# 5. Checks that all required fields are present.
# 6. Returns clean values for the next modules.
# ============================================================

def process_news(
    news_text: str,
    country: str,
    timeframe: str,
) -> dict[str, str]:
    """
    Analyze retrieved maritime news using OpenAI.

    Args:
        news_text:
            News returned by the News Retrieval module.

        country:
            EU country selected by the user.

        timeframe:
            Selected period, such as Last Week or Last Month.

    Returns:
        Dictionary containing:
        - summary
        - impact
        - podcast_script

    Raises:
        ValueError:
            If the input is empty, the OpenAI response is empty,
            the JSON is invalid, or required fields are missing.
    """

    # Clean and validate the retrieved news before calling OpenAI.
    cleaned_news = clean_news_text(news_text)

    # Build the user prompt with the selected country, timeframe,
    # and cleaned news content.
    user_prompt = build_user_prompt(
        news_text=cleaned_news,
        country=country,
        timeframe=timeframe,
    )

    # Call the OpenAI Responses API.
    response = client.responses.create(
        model="gpt-4.1-mini",
        instructions=SYSTEM_PROMPT,
        input=user_prompt,
    )

    # Extract and clean the model's text response.
    raw_response = response.output_text.strip()

    # Stop if the model returns no content.
    if not raw_response:
        raise ValueError(
            "OpenAI returned an empty response."
        )

    # Convert the JSON text into a Python dictionary.
    try:
        result = json.loads(raw_response)

    except json.JSONDecodeError as error:
        raise ValueError(
            "OpenAI returned an invalid JSON response."
        ) from error

    # Define the exact keys required by the rest of the application.
    required_keys = {
        "summary",
        "impact",
        "podcast_script",
    }

    # Find any required keys that are missing.
    missing_keys = required_keys.difference(result.keys())

    if missing_keys:
        raise ValueError(
            "OpenAI response is missing required fields: "
            f"{', '.join(sorted(missing_keys))}"
        )

    # Return clean strings for Gradio and Text-to-Speech.
    return {
        "summary": str(result["summary"]).strip(),
        "impact": str(result["impact"]).strip(),
        "podcast_script": str(
            result["podcast_script"]
        ).strip(),
    }