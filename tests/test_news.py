"""
Manual test for the News Retrieval module.

This test verifies that the News Retrieval module
works independently before integrating it with the
LLM and Text-to-Speech modules.
"""

from src.news_fetcher import get_news


# ============================================================
# TEST EXECUTION
# ============================================================

news_text = get_news(
    country="France",
    timeframe="Last Month",
)


# ============================================================
# VALIDATION
# ============================================================

# Verify that the module always returns a string.
assert isinstance(news_text, str)

print("=" * 70)
print("NEWS RETRIEVAL RESULT")
print("=" * 70)

if news_text:
    print(news_text)
else:
    print("No relevant news was found.")