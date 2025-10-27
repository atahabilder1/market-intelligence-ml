"""
Analysis API Endpoints
"""

from fastapi import APIRouter, HTTPException
import sys
from pathlib import Path
import pandas as pd

sys.path.append(str(Path(__file__).parent.parent.parent.parent))

from backend.app.models.schemas import AnalysisRequest, AnalysisResponse
from src.data.fetch_data import fetch_multiple_assets
from src.features.technical_indicators import calculate_all_indicators

router = APIRouter()

@router.post("/", response_model=list[AnalysisResponse])
async def analyze_assets(request: AnalysisRequest):
    """
    Perform comprehensive analysis on assets.

    Returns:
    - Statistical summary
    - Returns analysis
    - Correlations with other assets
    - Current technical indicators
    """
    try:
        # Fetch data
        data_dict = fetch_multiple_assets(
            request.symbols,
            request.start_date,
            request.end_date
        )

        results = []

        # Calculate correlations if requested
        correlations = None
        if request.include_correlations and len(request.symbols) > 1:
            # Get close prices for all symbols
            close_prices = pd.DataFrame({
                sym: data['Close'] for sym, data in data_dict.items()
            })
            returns = close_prices.pct_change().dropna()
            corr_matrix = returns.corr()

        # Analyze each symbol
        for symbol in request.symbols:
            data = data_dict[symbol]
            returns = data['Close'].pct_change().dropna()

            # Basic statistics
            statistics = {
                "mean_price": float(data['Close'].mean()),
                "current_price": float(data['Close'].iloc[-1]),
                "min_price": float(data['Close'].min()),
                "max_price": float(data['Close'].max()),
                "volatility": float(data['Close'].std()),
                "total_data_points": len(data)
            }

            # Returns summary
            returns_summary = {
                "mean_return": float(returns.mean()),
                "total_return": float((data['Close'].iloc[-1] / data['Close'].iloc[0] - 1)),
                "volatility_annual": float(returns.std() * (252 ** 0.5)),
                "skewness": float(returns.skew()),
                "kurtosis": float(returns.kurtosis())
            }

            # Correlations
            symbol_correlations = None
            if request.include_correlations and correlations is not None:
                symbol_correlations = {
                    other: float(corr_matrix.loc[symbol, other])
                    for other in request.symbols if other != symbol
                }

            # Technical indicators
            technical_indicators = None
            if request.include_technical:
                indicators = calculate_all_indicators(data)
                if len(indicators) > 0:
                    latest = indicators.iloc[-1]
                    technical_indicators = {
                        "rsi": float(latest.get('rsi', 0)),
                        "macd": float(latest.get('macd', 0)),
                        "macd_signal": float(latest.get('macd_signal', 0)),
                        "bb_upper": float(latest.get('bb_upper', 0)),
                        "bb_middle": float(latest.get('bb_middle', 0)),
                        "bb_lower": float(latest.get('bb_lower', 0)),
                        "sma_20": float(latest.get('sma_20', 0)),
                        "sma_50": float(latest.get('sma_50', 0))
                    }

            results.append(AnalysisResponse(
                symbol=symbol,
                statistics=statistics,
                returns_summary=returns_summary,
                correlations=symbol_correlations,
                technical_indicators=technical_indicators
            ))

        return results

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Analysis failed: {str(e)}")

@router.get("/price-history/{symbol}")
async def get_price_history(symbol: str, start_date: str, end_date: str):
    """
    Get historical price data for a symbol.
    """
    try:
        data_dict = fetch_multiple_assets([symbol], start_date, end_date)
        data = data_dict[symbol]

        # Convert to list of dicts
        history = []
        for date, row in data.iterrows():
            history.append({
                "date": str(date),
                "open": float(row['Open']),
                "high": float(row['High']),
                "low": float(row['Low']),
                "close": float(row['Close']),
                "volume": float(row['Volume']) if 'Volume' in row else 0
            })

        return {
            "symbol": symbol,
            "data": history,
            "total_points": len(history)
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to fetch price history: {str(e)}")
