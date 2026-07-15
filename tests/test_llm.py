"""
Manual test for the LLM Processing module.

This test uses sample news so the LLM module can be tested
without depending on the News Retrieval module.
"""

from src.llm_processor import process_news


# ============================================================
# SAMPLE INPUT
# ============================================================
#
# This mocked news text simulates the format that the News
# Retrieval module should return.
# ============================================================

sample_news = """
ARTICLE 1

Title: EU maritime emissions update

Source: Example Maritime News

Published date: 2026-07-10

URL: https://example.com/article

Content:
Shipping companies are reviewing their emissions monitoring systems
and operating costs in response to new environmental obligations.

ARTICLE 2

Title: European ports expand shore power projects

Source: Example Port News

Published date: 2026-07-12

URL: https://example.com/article-2

Content:
Several European ports are investing in shore-side electricity
infrastructure to reduce vessel emissions while ships are docked.
"""


# ============================================================
# TEST EXECUTION
# ============================================================

analysis = process_news(
    news_text=sample_news,
    country="France",
    timeframe="Last Week",
)


# ============================================================
# RESULTS
# ============================================================

print("=" * 70)
print("EXECUTIVE SUMMARY")
print("=" * 70)
print(analysis["summary"])

print("\n" + "=" * 70)
print("BUSINESS IMPACT")
print("=" * 70)
print(analysis["impact"])

print("\n" + "=" * 70)
print("PODCAST SCRIPT")
print("=" * 70)
print(analysis["podcast_script"])