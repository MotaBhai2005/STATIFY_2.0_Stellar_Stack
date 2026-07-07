import yfinance as yf
from langchain_core.tools import tool
from schema import StockPriceInput, StockPriceOutput, NewsInput
from ddgs import DDGS
from pathlib import Path
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_chroma import Chroma

#Get stock price
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

#Technical Indicator
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

#News
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

# RAG
retriever = None
vector_db = None
embedding_model = None

BASE_DIR = Path(__file__).resolve().parent
CHROMA_DIR = BASE_DIR / "chroma_db"

def load_pdf(pdf_path: str | Path):
    loader = PyPDFLoader(str(pdf_path))
    return loader.load()

def split_documents(documents: list):
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=500,
        chunk_overlap=50
    )

    return splitter.split_documents(documents)

def create_embedding_model():

    return HuggingFaceEmbeddings(
        model_name="sentence-transformers/all-MiniLM-L6-v2"
    )

def create_vector_database(chunks, embedding_model):

    return Chroma.from_documents(
        documents=chunks,
        embedding=embedding_model,
        persist_directory=str(CHROMA_DIR)
    )

def initialize_rag(pdf_path, k=3):

    global retriever
    global vector_db
    global embedding_model

    if retriever is not None:
        return
    
    try:
        documents = load_pdf(pdf_path)
    except Exception as e:
       raise RuntimeError(
        f"Failed to initialize RAG: {e}"
    )

    chunks = split_documents(documents)

    embedding_model = create_embedding_model()

    vector_db = create_vector_database(
        chunks,
        embedding_model
    )

    retriever = vector_db.as_retriever(
    search_kwargs={"k": k}
    )

    print("RAG initialized successfully.")

def retrieve_context(query):

    if retriever is None:
        raise RuntimeError(
            "RAG has not been initialized."
        )

    docs = retriever.invoke(query)

    return "\n\n".join(
        doc.page_content
        for doc in docs
    )

if __name__ == "__main__":

    PDF_PATH = (
        BASE_DIR
        / "data"
        / "Module 2_Technical Analysis.pdf"
    )

    initialize_rag(PDF_PATH)

    print(retrieve_context("RSI above 70"))