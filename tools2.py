from langchain.tools import tool
from ddgs import DDGS

from schema2 import NewsInput


POSITIVE_WORDS = [
    "profit",
    "growth",
    "record",
    "approval",
    "surge",
    "contract",
    "launch",
    "beat",
    "investment",
    "expansion",
    "partnership",
    "acquisition",
    "upgrade",
]

NEGATIVE_WORDS = [
    "loss",
    "decline",
    "fall",
    "fraud",
    "lawsuit",
    "recall",
    "delay",
    "bankruptcy",
    "downgrade",
    "penalty",
    "investigation",
]


def get_sentiment(text: str):

    text = text.lower()

    if any(word in text for word in POSITIVE_WORDS):
        return "Bullish"

    if any(word in text for word in NEGATIVE_WORDS):
        return "Bearish"

    return "Neutral"


def fetch_news(company: str, query: str, max_results: int = 5):

    try:

        with DDGS() as ddgs:

            results = list(
                ddgs.text(
                    query,
                    max_results=max_results
                )
            )
            

        if not results:
            return f"No news found for {company}."

        formatted_news = []

        for i, article in enumerate(results, start=1):

            title = article.get("title", "No Title")

            summary = article.get("body", "No Summary Available")

            source = article.get("source", "DuckDuckGo")

            url = article.get("href", "No URL")

            sentiment = get_sentiment(title + " " + summary)

            formatted_news.append(
                f"""
==============================

News {i}

Title:
{title}

Summary:
{summary}

Source:
{source}

URL:
{url}

Sentiment:
{sentiment}

==============================
"""
            )

        return "\n".join(formatted_news)

    except Exception as e:
        return f"Error fetching news: {str(e)}"


@tool(args_schema=NewsInput)
def company_news(company: str) -> str:
    """
    Fetch latest company news.
    """
    return fetch_news(
        company,
        f"{company} latest company news"
    )


@tool(args_schema=NewsInput)
def breaking_news(company: str) -> str:
    """
    Fetch breaking news.
    """
    return fetch_news(
        company,
        f"{company} breaking news today"
    )


@tool(args_schema=NewsInput)
def earnings_news(company: str) -> str:
    """
    Fetch earnings related news.
    """
    return fetch_news(
        company,
        f"{company} quarterly earnings OR financial results"
    )


@tool(args_schema=NewsInput)
def ceo_news(company: str) -> str:
    """
    Fetch CEO related news.
    """
    return fetch_news(
        company,
        f"{company} CEO interview OR CEO announcement"
    )


@tool(args_schema=NewsInput)
def government_orders(company: str) -> str:
    """
    Fetch government contracts/orders.
    """
    return fetch_news(
        company,
        f"{company} government contract OR government order"
    )


@tool(args_schema=NewsInput)
def product_launches(company: str) -> str:
    """
    Fetch product launch news.
    """
    return fetch_news(
        company,
        f"{company} new product launch"
    )