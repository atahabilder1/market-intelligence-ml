"""Data fetching module for market data."""

import yfinance as yf
import pandas as pd
import ccxt
from datetime import datetime
import time

def fetch_stock_data(ticker, start_date, end_date):
    """
    Fetch OHLCV data for stocks/ETFs via yfinance.

    Parameters:
    -----------
    ticker : str
        Ticker symbol
    start_date : str
        Start date
    end_date : str
        End date

    Returns:
    --------
    pd.DataFrame: OHLCV data
    """
    try:
        data = yf.download(ticker, start=start_date, end=end_date, progress=False)
        return data
    except Exception as e:
        print(f"Error fetching {ticker}: {e}")
        return pd.DataFrame()

def fetch_crypto_data(symbol, start_date, end_date, exchange='binance'):
    """
    Fetch cryptocurrency data via CCXT.

    Parameters:
    -----------
    symbol : str
        Trading pair (e.g., 'BTC/USDT')
    start_date : str
        Start date
    end_date : str
        End date
    exchange : str
        Exchange name (default: 'binance')

    Returns:
    --------
    pd.DataFrame: OHLCV data
    """
    try:
        # Initialize exchange
        exchange_class = getattr(ccxt, exchange)
        exchange_obj = exchange_class()

        # Convert dates to timestamps
        start_ts = int(datetime.strptime(start_date, '%Y-%m-%d').timestamp() * 1000)
        end_ts = int(datetime.strptime(end_date, '%Y-%m-%d').timestamp() * 1000)

        # Fetch data
        all_data = []
        current_ts = start_ts

        while current_ts < end_ts:
            try:
                ohlcv = exchange_obj.fetch_ohlcv(symbol, '1d', since=current_ts, limit=1000)
                if not ohlcv:
                    break

                all_data.extend(ohlcv)
                current_ts = ohlcv[-1][0] + 86400000  # Move to next day
                time.sleep(exchange_obj.rateLimit / 1000)  # Rate limiting

            except Exception as e:
                print(f"Error fetching {symbol}: {e}")
                break

        # Convert to DataFrame
        if all_data:
            df = pd.DataFrame(all_data, columns=['timestamp', 'Open', 'High', 'Low', 'Close', 'Volume'])
            df['timestamp'] = pd.to_datetime(df['timestamp'], unit='ms')
            df.set_index('timestamp', inplace=True)
            return df
        else:
            return pd.DataFrame()

    except Exception as e:
        print(f"Error initializing exchange for {symbol}: {e}")
        return pd.DataFrame()

def fetch_multiple_assets(tickers, start_date, end_date, crypto_tickers=None):
    """
    Fetch data for multiple assets (stocks, ETFs, and crypto).

    Parameters:
    -----------
    tickers : list
        List of stock/ETF tickers
    start_date : str
        Start date
    end_date : str
        End date
    crypto_tickers : list, optional
        List of crypto trading pairs

    Returns:
    --------
    dict: Dictionary of ticker -> DataFrame
    """
    data = {}

    # Fetch stock/ETF data
    for ticker in tickers:
        print(f"Fetching {ticker}...")
        data[ticker] = fetch_stock_data(ticker, start_date, end_date)

    # Fetch crypto data
    if crypto_tickers:
        for crypto in crypto_tickers:
            print(f"Fetching {crypto}...")
            # Convert format: 'BTC-USD' to 'BTC/USDT'
            crypto_symbol = crypto.replace('-USD', '/USDT').replace('USDT', 'USDT')
            df = fetch_crypto_data(crypto_symbol, start_date, end_date)
            if not df.empty:
                data[crypto] = df

    return data

def get_close_prices(data_dict):
    """
    Extract close prices from dictionary of DataFrames.

    Parameters:
    -----------
    data_dict : dict
        Dictionary of asset -> DataFrame

    Returns:
    --------
    pd.DataFrame: Close prices for all assets
    """
    close_prices = {}

    for asset, df in data_dict.items():
        if not df.empty:
            if 'Close' in df.columns:
                close_prices[asset] = df['Close']
            elif 'Adj Close' in df.columns:
                close_prices[asset] = df['Adj Close']

    return pd.DataFrame(close_prices)
