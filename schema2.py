from pydantic import BaseModel, Field
from typing import List, Literal


class NewsInput(BaseModel):
    company: str = Field(description="Company name to search news for")


class NewsArticle(BaseModel):
    title: str = Field(description="Title of the news article")
    summary: str = Field(description="Brief summary of the article")
    source: str = Field(description="Source of the news article")
    url: str = Field(description="URL of the article")
    sentiment: Literal["Bullish", "Bearish", "Neutral"] = Field(
        description="Sentiment of the article"
    )


class NewsResponse(BaseModel):
    company: str = Field(description="Company name")
    category: str = Field(description="News category")
    articles: List[NewsArticle] = Field(
        description="List of latest news articles"
    )