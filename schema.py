from pydantic import BaseModel, Field
from typing import List


class NewsInput(BaseModel):
    company: str = Field(description="Company name to search news for")


class NewsArticle(BaseModel):
    title: str = Field(description="Title of the news article")
    summary: str = Field(description="Brief summary of the article")
    link: str = Field(description="URL of the article")


class NewsResponse(BaseModel):
    company: str = Field(description="Company name")
    articles: List[NewsArticle] = Field(description="List of latest news articles")