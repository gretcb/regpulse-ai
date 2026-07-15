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
    Create a concise NewsAPI query for candidate retrieval.

    The query focuses on commercial maritime activity and
    environmental regulation.

    The selected country is not mandatory in the API query,
    because European regulations may affect that country
    without mentioning it explicitly in the article.
    Country relevance will be evaluated later through
    local scoring.
    """

    query = (
        '("maritime industry" OR "shipping industry" OR '
        '"maritime transport" OR "vessel operator" OR shipowner) AND '
        '("FuelEU Maritime" OR "EU ETS" OR MARPOL OR '
        '"maritime emissions" OR "shore power" OR '
        '"alternative marine fuels" OR "maritime regulation")'
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

    # Stop the request if the NewsAPI key is missing.
    if not NEWS_API_KEY:
        logger.error(
            "NEWS_API_KEY is missing."
        )

        return []

    # Parameters sent to the NewsAPI endpoint.
    parameters = {
        "q": query,
        "searchIn": "title,description",
        "from": from_date,
        "language": "en",
        "sortBy": "relevancy",
        "pageSize": 20,
        "apiKey": NEWS_API_KEY,
    }

    try:
        logger.info(
            "Retrieving maritime environmental news..."
        )

        # Send the request to NewsAPI.
        response = requests.get(
            NEWS_API_URL,
            params=parameters,
            timeout=15,
        )

        # Raise an error for invalid HTTP responses.
        response.raise_for_status()

        # Convert the JSON response into a Python dictionary.
        data = response.json()

        # Extract the list of articles.
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
# Relevance taxonomy
# ---------------------------------------------------------
#
# These signal groups are used to evaluate whether an article
# is genuinely relevant to maritime environmental regulation.
#
# The system does not rely only on the NewsAPI query.
# It also validates each candidate article locally.
# ---------------------------------------------------------

MARITIME_SIGNALS = {
    "maritime industry",
    "shipping industry",
    "maritime transport",
    "commercial shipping",
    "merchant shipping",
    "shipowner",
    "shipowners",
    "vessel operator",
    "vessel operators",
    "shipping company",
    "shipping companies",
    "maritime fleet",
    "marine",
    "shipping",
    "vessel",
    "vessels",
    "ship",
    "ships",
    "boat",
    "boats",
}

ENVIRONMENTAL_SIGNALS = {
    "fueleu maritime",
    "eu ets",
    "marpol",
    "maritime emissions",
    "shipping emissions",
    "shore power",
    "alternative marine fuels",
    "environmental compliance",
    "maritime regulation",
    "emissions monitoring",
    "decarbonisation",
    "decarbonization",
    "environmental impact",
    "marine environment",
    "marine pollution",
    "pollution prevention",
    "green shipping",
    "carbon emissions",
    "carbon intensity",
    "ghg emissions",
    "greenhouse gas emissions",
    "energy efficiency",
    "sustainable shipping",
}

REGULATORY_ACTION_SIGNALS = {
    "entered into force",
    "implementation",
    "implemented",
    "adopted",
    "approved",
    "amendment",
    "amended",
    "compliance deadline",
    "mandatory",
    "requirement",
    "requirements",
    "official guidance",
    "enforcement",
    "reporting obligation",
    "reporting requirements",
    "directive",
    "regulation",
    "consultation",
}

NOISE_SIGNALS = {
    "diabetes",
    "metformin",
    "pharmaceutical",
    "healthcare",
    "travel",
    "tourism",
    "holiday",
    "hotel",
    "restaurant",
    "food destination",
    "home improvement",
    "diy",
    "free shipping",
    "discount",
    "promotion",
    "promotional",
    "ecommerce",
    "retailers",
    "consumer products",
}
def score_article(
    article: dict,
    country: str,
) -> tuple[int, list[str]]:
    """
    Calculate a transparent relevance score.

    Maritime and environmental signals are mandatory.
    Regulatory actions and country mentions increase
    the final score.
    """

    title = article.get("title", "")
    description = article.get("description", "")

    searchable_text = (
        f"{title} {description}"
    ).casefold()

    reasons = []

    # -----------------------------
    # Reject noisy articles
    # -----------------------------

    noise_matches = [
        signal
        for signal in NOISE_SIGNALS
        if signal in searchable_text
    ]

    if noise_matches:
        return (
            -100,
            [
                "Noise detected: "
                + ", ".join(noise_matches)
            ],
        )

    # -----------------------------
    # Positive signals
    # -----------------------------

    maritime_matches = [
        signal
        for signal in MARITIME_SIGNALS
        if signal in searchable_text
    ]

    environmental_matches = [
        signal
        for signal in ENVIRONMENTAL_SIGNALS
        if signal in searchable_text
    ]

    regulatory_matches = [
        signal
        for signal in REGULATORY_ACTION_SIGNALS
        if signal in searchable_text
    ]

    # Maritime is mandatory

    if not maritime_matches:
        return (
            0,
            [
                "Missing maritime signal."
            ],
        )

    # Environmental is mandatory

    if not environmental_matches:
        return (
            0,
            [
                "Missing environmental signal."
            ],
        )

    score = 6

    reasons.append(
        "Maritime: "
        + ", ".join(maritime_matches)
    )

    reasons.append(
        "Environmental: "
        + ", ".join(environmental_matches)
    )

    # Regulatory language improves ranking
    # but is not mandatory.

    if regulatory_matches:

        score += 4

        reasons.append(
            "Regulatory: "
            + ", ".join(regulatory_matches)
        )

    # Country is a bonus, not a filter.

    if country.casefold() in searchable_text:

        score += 3

        reasons.append(
            f"Country detected: {country}"
        )

    return score, reasons

def filter_and_rank_articles(
    articles: list,
    country: str,
) -> list:
    """
    Filter candidate articles using the relevance score
    and return the three highest-scoring articles.
    """

    scored_articles = []

    for article in articles:

        score, reasons = score_article(
            article=article,
            country=country,
        )

        title = article.get(
            "title",
            "Unknown title",
        )

        if score > 0:

            logger.info(
                f"Accepted (Score: {score})"
            )

            logger.info(
                f"Title: {title}"
            )

            for reason in reasons:
                logger.info(
                    f"✓ {reason}"
                )

            scored_articles.append(
                (score, article)
            )

        else:

            logger.info(
                "Rejected"
            )

            logger.info(
                f"Title: {title}"
            )

            for reason in reasons:
                logger.info(
                    f"✗ {reason}"
                )

    scored_articles.sort(
        key=lambda item: item[0],
        reverse=True,
    )

    return [
        article
        for _, article in scored_articles[:3]
    ]

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
            article.get("description")
            or article.get("content")
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
            from_date,
        )

        articles = filter_and_rank_articles(
            articles=articles,
            country=country,
        )

        if not articles:

            logger.warning(
                "No relevant regulatory maritime news "
                "matched the current criteria."
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