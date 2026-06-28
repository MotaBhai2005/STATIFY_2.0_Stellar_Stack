from pydantic import BaseModel, Field
from typing import Optional

class StockPriceInput(BaseModel):
    ticker_symbol: str = Field(
        ..., 
        description="The stock ticker symbol to look up (e.g., AAPL, MSFT, TSLA)."
    )

class StockPriceOutput(BaseModel):
    symbol: Optional[str] = Field(None, description="The ticker symbol of the company")
    company_name: Optional[str] = Field(None, description="The official name of the company")
    current_price: Optional[float] = Field(None, description="The current trading price of the stock")
    day_high: Optional[float] = Field(None, description="The highest price of the stock during the current trading day")
    day_low: Optional[float] = Field(None, description="The lowest price of the stock during the current trading day")
    market_Cap: Optional[int] = Field(None, description="The market capitalization of the company")
    financial_currency: Optional[str] = Field(None, description="The currency in which financial statements are reported")
    currency: Optional[str] = Field(None, description="The trading currency of the stock")
    error: Optional[str] = Field(None, description="Error message if the ticker is not found or invalid")
