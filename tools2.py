import yfinance as yf
from langchain_core.tools import tool
from schema import StockPriceInput, StockPriceOutput, NewsInput
from ddgs import DDGS

@tool("get_stock_price", args_schema=StockPriceInput)
def get_stock_price(ticker_symbol: str) -> dict:
    """
    Retrieve real-time stock information for a given stock ticker symbol.

   Input:
   -ticker_symbol (str): Stock ticker (e.g., AAPL, MSFT, TSLA)

   Returns:
        Dictionary containing company name, stock price,
        day high, day low, market capitalization,
        and currency information.
    """
    if not ticker_symbol.strip():
          return StockPriceOutput(
              error="Ticker symbol cannot be empty."
          ).model_dump()
    try:
        
        ticker = yf.Ticker(ticker_symbol)
        info = ticker.info
        if info.get('currentPrice') is None:
            return StockPriceOutput(
               error=f"Ticker '{ticker_symbol}' not found."
            ).model_dump()
        
        details = {
            "symbol": info.get('symbol'),
            "company_name": info.get('longName'),
            "current_price": info.get('currentPrice'),
            "day_high": info.get('dayHigh'),
            "day_low": info.get('dayLow'),
            "market_cap": info.get('marketCap'),
            # "financial_currency": info.get('financialCurrency'),
            "currency": info.get('currency'),
            "open_price" : info.get('open'),
            "previous_close" : info.get('previousClose'),   
            "volume" : info.get('volume')
        }
        # Validate output schema
        validated_details = StockPriceOutput(**details)
        return validated_details.model_dump()
    except Exception as e:
        return StockPriceOutput(
           error=f"Failed to fetch stock data: {str(e)}"
        ).model_dump()



@tool("get_company_news",args_schema=NewsInput)
def get_company_news(company: str) -> str:
    """
    Fetch the latest news articles for a given company using DuckDuckGo Search.
    """
    if not company.strip():
        return "Company name cannot be empty."
    try:
        with DDGS() as ddgs:
            results = list(
                ddgs.text(
                    f"{company} latest stock news",
                    max_results=3
                )
            )

        if not results:
            return f"No recent news found for {company}."

        formatted_news = []

        for i, article in enumerate(results, start=1):

            title = article.get("title", "No Title")
            summary = article.get("body", "No Summary Available")
            link = article.get("href", "No Link")

            formatted_news.append(
                f"News {i}\n"
                f"Title: {title}\n"
                f"Summary: {summary}\n"
                f"Link: {link}\n"
            )

        return "\n".join(formatted_news)

    except Exception as e:
        return f"Error fetching news: {str(e)}"

@tool("get_technical_indicators")
def get_technical_indicators(ticker_symbol: str) -> dict:
    """
    Calculate technical indicators (RSI, SMA, EMA) for a given ticker.
    """
    try:
        ticker = yf.Ticker(ticker_symbol)
        hist = ticker.history(period="6mo")
        
        if hist.empty:
            return {"error": "No historical data found"}
        
        close = hist['Close']
        
        # SMA - you already know how to do this
        sma_20 = close.rolling(window=20).mean()
        sma_50 = close.rolling(window=50).mean()
        
        # EMA - similar to SMA but use .ewm()
        ema_20 = close.ewm(span=20, adjust=False).mean()
        
        # RSI - follow the 8-step logic from earlier
        delta = close.diff()
        gain = delta.clip(lower=0)
        loss = -delta.clip(upper=0)
        avg_gain = gain.rolling(window=14).mean()
        avg_loss = loss.rolling(window=14).mean()
        rs = avg_gain/avg_loss
        rsi = 100.0 - (100.0 / (1.0 + rs))
        
        return {
            "sma_20": round(float(sma_20.iloc[-1]), 2),
            "sma_50": round(float(sma_50.iloc[-1]), 2),
            "ema_20": round(float(ema_20.iloc[-1]), 2),
            "rsi_14": round(float(rsi.iloc[-1]), 2),
        }
    except Exception as e:
        return {"error": f"Failed to calculate indicators: {str(e)}"}
