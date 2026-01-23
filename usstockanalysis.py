from fastapi import FastAPI
from datetime import datetime, timedelta
import pandas as pd
import yfinance as yf

# -------------------------------------------------
# Create FastAPI app
# -------------------------------------------------
app = FastAPI()

# -------------------------------------------------
# Health check endpoint
# -------------------------------------------------
@app.get("/health")
def health_check():
    return {"message": "US Stocks API is running"}

# -------------------------------------------------
# Stock analysis function
# -------------------------------------------------
def generate_us_stock_summary():

    end_date = datetime.now().date()
    start_date = end_date - timedelta(days=365)

    # Manually selected US IT stocks
    symbols = [
        "NVDA", "GOOGL", "AAPL", "MSFT", "AMZN",
        "META", "AVGO", "TSLA", "ORCL", "PLTR"
    ]

    stockdata = yf.download(
        tickers=symbols,
        start=start_date,
        end=end_date,
        progress=False
    )

    closeprice_df = stockdata["Close"].copy()
    returns_df = closeprice_df.pct_change() * 100

    summary_df = pd.DataFrame({
        "Ticker": closeprice_df.columns,
        "Max_Value": closeprice_df.max().values,
        "Min_Value": closeprice_df.min().values,
        "Current_Value": closeprice_df.iloc[-1].values,
        "Avg_Daily_Return_%": returns_df.mean().values,
        "Volatility_%": returns_df.std().values
    })

    return summary_df

# -------------------------------------------------
# API endpoint consumed by Excel VBA
# -------------------------------------------------
@app.get("/us-stocks")
def us_it_stock_summary():
    df = generate_us_stock_summary()
    return df.round(4).to_dict(orient="records")
