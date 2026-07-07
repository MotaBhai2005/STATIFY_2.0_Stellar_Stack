from pydantic import BaseModel, Field
from typing import Optional, Dict, Any

# RAG Schemas
class RetrievalRequest(BaseModel):
    query: str = Field(..., description="Query to search within the vector database")

class RetrievalResponse(BaseModel):
    context: str = Field(..., description="Retrieved context matching the query")

# Node Outputs and State Models passed between graph nodes

class DataFetcherOutput(BaseModel):
    stock_data: Optional[Dict[str, Any]] = Field(None, description="Real-time stock price data from yfinance")
    technical_data: Optional[Dict[str, Any]] = Field(None, description="Calculated technical indicators (RSI, SMA, EMA)")
    news: Optional[str] = Field(None, description="Formatted company news articles from search")

class AnalystOutput(BaseModel):
    recommendation: Optional[str] = Field(None, description="Buy/Sell/Hold recommendation with technical explanation")
    rag_context: Optional[str] = Field(None, description="RAG retrieved context used for analysis validation")

class RiskAuditorOutput(BaseModel):
    needs_more_data: bool = Field(default=False, description="Routing flag indicating if more data is required to resolve contradictions")
    contradiction_reason: Optional[str] = Field(None, description="Explanation of contradictions found during audit")
    final_report: Optional[str] = Field(None, description="Final approved research/audit report")
    retry_count: int = Field(default=0, description="Counter tracking the retry attempts to avoid infinite loops")