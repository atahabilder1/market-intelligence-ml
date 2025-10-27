"""
Prediction API Endpoints
"""

from fastapi import APIRouter, HTTPException
from datetime import datetime
import sys
from pathlib import Path

sys.path.append(str(Path(__file__).parent.parent.parent.parent))

from backend.app.models.schemas import (
    PredictionRequest,
    PredictionResponse,
    PredictionResult,
    FeatureImportance
)
from backend.app.services.prediction_service import prediction_service

router = APIRouter()

@router.post("/", response_model=PredictionResponse)
async def predict_returns(request: PredictionRequest):
    """
    Predict future returns for given assets.

    This endpoint:
    - Trains ML models on historical data
    - Generates predictions for specified horizon
    - Returns confidence scores and trading signals
    """
    try:
        # Make predictions
        predictions = prediction_service.predict(
            symbols=request.symbols,
            model_type=request.model_type.value,
            horizon=request.horizon.value,
            start_date=request.start_date,
            end_date=request.end_date
        )

        # Convert to response format
        prediction_results = [
            PredictionResult(**pred) for pred in predictions
        ]

        return PredictionResponse(
            predictions=prediction_results,
            timestamp=datetime.now(),
            model_info={
                "model_type": request.model_type.value,
                "horizon": request.horizon.value,
                "total_symbols": len(request.symbols)
            }
        )

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Prediction failed: {str(e)}")

@router.get("/feature-importance/{symbol}")
async def get_feature_importance(
    symbol: str,
    model_type: str = "xgboost",
    horizon: str = "1d",
    top_n: int = 20
):
    """
    Get feature importance for a trained model.

    Shows which technical indicators are most influential for predictions.
    """
    try:
        importance = prediction_service.get_feature_importance(
            symbol=symbol,
            model_type=model_type,
            horizon=horizon,
            top_n=top_n
        )

        return {
            "symbol": symbol,
            "model_type": model_type,
            "features": [FeatureImportance(**feat) for feat in importance]
        }

    except Exception as e:
        raise HTTPException(status_code=404, detail=f"Model not found or error: {str(e)}")
