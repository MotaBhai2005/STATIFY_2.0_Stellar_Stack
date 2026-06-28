import yfinance as yf
from langchain.tools import tool
from schema import StockPriceInput, StockPriceOutput

@tool("get_stock_price", args_schema=StockPriceInput)
def get_stock_price(ticker_symbol: str) -> dict:
    """
    Fetch real-time stock price and details for a given company ticker symbol.
    Use this tool to find current stock price, day high, day low, and market cap.
    """
    try:
        ticker = yf.Ticker(ticker_symbol)
        info = ticker.info
        if info.get('currentPrice') is None:
            return {"error": "Ticker not found"}
        
        details = {
            "symbol": info.get('symbol'),
            "company_name": info.get('longName'),
            "current_price": info.get('currentPrice'),
            "day_high": info.get('dayHigh'),
            "day_low": info.get('dayLow'),
            "market_Cap": info.get('marketCap'),
            "financial_currency": info.get('financialCurrency'),
            "currency": info.get('currency')
        }
        # Validate output schema
        validated_details = StockPriceOutput(**details)
        return validated_details.model_dump()
    except Exception as e:
        return {"error": f"Failed to fetch stock data: {str(e)}"}


