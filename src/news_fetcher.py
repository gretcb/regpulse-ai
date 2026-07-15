"""
LLM Processing Module

Uses the OpenAI API to transform retrieved news into:

- Executive Summary
- Business Impact
- Podcast Script
"""

"""
RegPulse AI - News Retrieval Module

Purpose:
    Retrieve recent maritime environmental news using NewsAPI.

Workflow:
    User selects:
        - EU country
        - Timeframe (Last Week / Last Month)

    Then:
        1. Build a maritime environmental search query.
        2. Request relevant articles from NewsAPI.
        3. Extract useful article information.
        4. Return formatted text for LLM processing.

This module only handles news retrieval.
It does NOT:
    - call OpenAI
    - generate summaries
    - create podcasts
    - generate audio
"""


import os
import logging
from datetime import datetime, timedelta

import requests
from dotenv import load_dotenv


# ---------------------------------------------------------
# Configuration
# ---------------------------------------------------------

# Load environment variables from .env file.
# This keeps API keys separate from the source code.
load_dotenv()


# Configure application logging.
# Logging helps developers understand the processing flow
# without exposing sensitive information.
logging.basicConfig(level=logging.INFO)

logger = logging.getLogger(__name__)


# NewsAPI endpoint for searching articles.
NEWS_API_URL = "https://newsapi.org/v2/everything"


# API key stored in environment variables.
NEWS_API_KEY = os.getenv("NEWS_API_KEY")


# ---------------------------------------------------------
# Query creation
# ---------------------------------------------------------

def build_query(country: str) -> str:
    """
    Create a NewsAPI search query.

    The MVP focuses only on European maritime
    environmental topics.

    Args:
        country:
            Selected EU country.

    Returns:
        A search query string used by NewsAPI.

    Example:
        France ->
        maritime OR shipping emissions France
    """

    query = (
        f'maritime OR shipping '
        f'emissions OR sustainability '
        f'"FuelEU Maritime" OR "EU ETS" '
        f'{country}'
    )

    return query


# ---------------------------------------------------------
# Timeframe handling
# ---------------------------------------------------------

def get_date_from_timeframe(timeframe: str) -> str:
    """
    Convert the user's timeframe selection into
    a date that NewsAPI can understand.

    Supported values:
        - Last Week
        - Last Month

    Args:
        timeframe:
            User-selected period.

    Returns:
        Date string in YYYY-MM-DD format.
    """

    today = datetime.now()


    if timeframe == "Last Week":

        start_date = today - timedelta(days=7)


    elif timeframe == "Last Month":

        start_date = today - timedelta(days=30)


    else:

        raise ValueError(
            "Timeframe must be 'Last Week' or 'Last Month'"
        )


    return start_date.strftime("%Y-%m-%d")


# ---------------------------------------------------------
# NewsAPI request
# ---------------------------------------------------------

def fetch_news(query: str, from_date: str) -> list:
    """
    Retrieve articles from NewsAPI.

    The function requests only the latest three
    relevant articles because the LLM only needs
    a small amount of high-quality input.

    Args:
        query:
            Search query.

        from_date:
            Start date for article search.

    Returns:
        List of article dictionaries.

        Returns an empty list if retrieval fails.
    """

    if not NEWS_API_KEY:

        logger.error(
            "NEWS_API_KEY is missing."
        )

        return []


    parameters = {

        "q": query,

        "from": from_date,

        "language": "en",

        "sortBy": "publishedAt",

        "pageSize": 3,

        "apiKey": NEWS_API_KEY

    }


    try:

        logger.info(
            "Retrieving maritime environmental news..."
        )


        response = requests.get(
            NEWS_API_URL,
            params=parameters,
            timeout=15
        )


        response.raise_for_status()


        data = response.json()


        articles = data.get(
            "articles",
            []
        )


        logger.info(
            f"Retrieved {len(articles)} articles."
        )


        return articles


    except requests.RequestException as error:

        logger.error(
            f"NewsAPI request failed: {error}"
        )

        return []



# ---------------------------------------------------------
# Article formatting
# ---------------------------------------------------------

def format_articles(articles: list) -> str:
    """
    Convert NewsAPI response into clean text.

    This format is important because the next module
    (LLM processing) expects a single text input.

    Output example:

        ARTICLE 1

        Title:
        Source:
        Published date:
        URL:
        Content:

    Args:
        articles:
            List returned by NewsAPI.

    Returns:
        Formatted article text.
    """

    if not articles:

        return ""


    formatted_output = []


    for number, article in enumerate(
        articles[:3],
        start=1
    ):


        title = article.get(
            "title",
            "Unknown"
        )


        source = article.get(
            "source",
            {}
        ).get(
            "name",
            "Unknown"
        )


        published_date = article.get(
            "publishedAt",
            "Unknown"
        )


        url = article.get(
            "url",
            ""
        )


        # NewsAPI often provides either:
        # - content
        # - description
        #
        # We use whichever is available.
        content = (
            article.get("content")
            or article.get("description")
            or "No content available."
        )


        formatted_output.append(
            f"""
ARTICLE {number}

Title: {title}
Source: {source}
Published date: {published_date}
URL: {url}
Content:
{content}
"""
        )


    return "\n".join(formatted_output)



# ---------------------------------------------------------
# Main function used by the application
# ---------------------------------------------------------

def get_news(country: str, timeframe: str) -> str:
    """
    Main public function.

    This is the only function other modules need to call.

    Workflow:

        Country + Timeframe
                |
                v
        Build query
                |
                v
        Retrieve news
                |
                v
        Format articles
                |
                v
        Return text


    Args:
        country:
            EU country selected by user.

        timeframe:
            Last Week or Last Month.

    Returns:
        Formatted news string.

        Returns empty string if no usable news exists.
    """

    try:

        query = build_query(country)


        from_date = get_date_from_timeframe(
            timeframe
        )


        articles = fetch_news(
            query,
            from_date
        )


        if not articles:

            logger.warning(
                "No relevant news found."
            )

            return ""


        return format_articles(
            articles
        )


    except Exception as error:

        logger.error(
            f"News retrieval failed: {error}"
        )

        return ""



# ---------------------------------------------------------
# Local test
# ---------------------------------------------------------

if __name__ == "__main__":

    """
    Simple standalone test.

    This allows Andreas to test this module
    independently before integration with Gradio.
    """

    news_text = get_news(
        country="France",
        timeframe="Last Week"
    )


    print(news_text)