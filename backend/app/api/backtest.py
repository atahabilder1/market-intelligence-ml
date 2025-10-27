"""
Backtest API Endpoints
"""

from fastapi import APIRouter, HTTPException
import sys
from pathlib import Path

sys.path.append(str(Path(__file__).parent.parent.parent.parent))

from backend.app.models.schemas import BacktestRequest, BacktestResponse, BacktestMetrics
from backend.app.services.backtest_service import backtest_service

router = APIRouter()

@router.post("/", response_model=BacktestResponse)
async def run_backtest(request: BacktestRequest):
    """
    Run backtesting simulation.

    This endpoint:
    - Simulates trading strategy using ML predictions
    - Calculates realistic transaction costs
    - Returns comprehensive performance metrics
    - Provides equity curve and trade history
    """
    try:
        result = backtest_service.run_backtest(
            symbols=request.symbols,
            model_type=request.model_type.value,
            start_date=request.start_date,
            end_date=request.end_date,
            initial_capital=request.initial_capital,
            transaction_cost=request.transaction_cost,
            rebalance_frequency=request.rebalance_frequency
        )

        return BacktestResponse(
            metrics=BacktestMetrics(**result["metrics"]),
            equity_curve=result["equity_curve"],
            trades=result["trades"],
            model_type=request.model_type.value,
            symbols=request.symbols,
            start_date=request.start_date,
            end_date=request.end_date
        )

    except Exception as e:
        import traceback
        traceback.print_exc()  # Print full error to console
        raise HTTPException(status_code=500, detail=f"Backtest failed: {str(e)}")

@router.get("/quick-stats/{symbol}")
async def get_quick_stats(symbol: str, start_date: str, end_date: str):
    """
    Get quick statistics for an asset without full backtest.
    """
    try:
        from src.data.fetch_data import fetch_multiple_assets
        from src.backtest.metrics import calculate_all_metrics

        # Fetch data
        data_dict = fetch_multiple_assets([symbol], start_date, end_date)
        data = data_dict[symbol]

        # Calculate returns
        returns = data['Close'].pct_change().dropna()

        # Calculate metrics
        metrics = calculate_all_metrics(returns)

        return {
            "symbol": symbol,
            "metrics": metrics,
            "data_points": len(data)
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to get stats: {str(e)}")
