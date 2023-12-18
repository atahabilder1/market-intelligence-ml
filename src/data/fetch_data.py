"""Data fetching module for market data."""

import yfinance as yf
import pandas as pd

def fetch_stock_data(ticker, start_date, end_date):
    """Fetch OHLCV data for stocks/ETFs."""
    data = yf.download(ticker, start=start_date, end=end_date)
    return data

def fetch_multiple_assets(tickers, start_date, end_date):
    """Fetch data for multiple assets."""
    data = {}
    for ticker in tickers:
        data[ticker] = fetch_stock_data(ticker, start_date, end_date)
    return data
