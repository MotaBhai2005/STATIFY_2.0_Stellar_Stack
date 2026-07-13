from fastapi import FastAPI,HTTPException
from pydantic import BaseModel,Field
from tools3 import (
    company_news,
    breaking_news,
    earnings_news
)

app=FastAPI(title="Statify 2.0 API",version="3.0")
class AnalyzeRequest(BaseModel):
    ticker: str = Field(
        ...,
        example="RELIANCE.NS"
    )

    position_size: float = Field(
        ...,
        example=1000000
    )
class AnalyzeResponse(BaseModel):

    ticker: str

    status: str

    message: str

    result: dict | None = None
@app.post("/api/v1/analyze")
def analyze_stock(request: AnalyzeRequest):
    news = "\n".join([
    company_news.invoke({"company": request.ticker}),
    breaking_news.invoke({"company": request.ticker})
    ])
    return {
    "ticker": request.ticker,
    "position_size": request.position_size,
    "news": news,
    "stock": "Pending Member 2",
    "technical_analysis": "Pending Member 2",
    "mcp_context": "Pending Member 4",
    "status": "success"
    }
