from pydantic import BaseModel, Field
from typing import List, Literal


class NewsInput(BaseModel):
    company: str = Field(description="Company name or stock ticker.")


class NewsArticle(BaseModel):
    title: str = Field(description="News title")
    summary: str = Field(description="Brief news summary")
    source: str = Field(description="News source")
    url: str = Field(description="Article URL")
    sentiment: Literal[
        "Bullish",
        "Bearish",
        "Neutral"
    ] = Field(description="News sentiment")


class NewsResponse(BaseModel):
    company: str = Field(description="Company name")
    category: str = Field(description="News category")
    articles: List[NewsArticle] = Field(description="List of news articles")