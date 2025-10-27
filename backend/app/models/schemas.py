"""
Pydantic Models for API Request/Response
"""

from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any
from datetime import datetime
from enum import Enum

# Enums
class ModelType(str, Enum):
    LINEAR = "linear"
    RANDOM_FOREST = "random_forest"
    XGBOOST = "xgboost"
    LSTM = "lstm"
    ENSEMBLE = "ensemble"

class AssetClass(str, Enum):
    EQUITY = "equity"
    FIXED_INCOME = "fixed_income"
    CRYPTO = "crypto"
    COMMODITY = "commodity"
    MACRO = "macro"

class PredictionHorizon(str, Enum):
    DAY_1 = "1d"
    DAY_5 = "5d"
    DAY_20 = "20d"
    DAY_60 = "60d"

# Request Models
class PredictionRequest(BaseModel):
    """Request for price prediction"""
    symbols: List[str] = Field(..., example=["SPY", "BTC/USDT"])
    model_type: ModelType = Field(default=ModelType.XGBOOST)
    horizon: PredictionHorizon = Field(default=PredictionHorizon.DAY_1)
    start_date: Optional[str] = Field(None, example="2023-01-01")
    end_date: Optional[str] = Field(None, example="2024-12-31")

class BacktestRequest(BaseModel):
    """Request for backtesting"""
    symbols: List[str] = Field(..., example=["SPY"])
    model_type: ModelType = Field(default=ModelType.XGBOOST)
    start_date: str = Field(..., example="2020-01-01")
    end_date: str = Field(..., example="2024-12-31")
    initial_capital: float = Field(default=100000.0)
    transaction_cost: float = Field(default=0.001)
    rebalance_frequency: str = Field(default="daily", example="daily")

class AnalysisRequest(BaseModel):
    """Request for asset analysis"""
    symbols: List[str] = Field(..., example=["SPY", "TLT"])
    start_date: str = Field(..., example="2020-01-01")
    end_date: str = Field(..., example="2024-12-31")
    include_correlations: bool = Field(default=True)
    include_technical: bool = Field(default=True)

# Response Models
class PredictionResult(BaseModel):
    """Single prediction result"""
    symbol: str
    predicted_return: float = Field(..., description="Predicted return percentage")
    confidence: float = Field(..., description="Prediction confidence 0-1")
    signal: str = Field(..., description="BUY, SELL, or HOLD")
    current_price: Optional[float] = None
    predicted_price: Optional[float] = None
    features_used: int
    model_used: str

class PredictionResponse(BaseModel):
    """Response containing predictions"""
    predictions: List[PredictionResult]
    timestamp: datetime
    model_info: Dict[str, Any]

class FeatureImportance(BaseModel):
    """Feature importance"""
    feature_name: str
    importance: float
    rank: int

class AnalysisResponse(BaseModel):
    """Analysis results"""
    symbol: str
    statistics: Dict[str, float]
    returns_summary: Dict[str, float]
    correlations: Optional[Dict[str, float]] = None
    technical_indicators: Optional[Dict[str, float]] = None
    feature_importance: Optional[List[FeatureImportance]] = None

class BacktestMetrics(BaseModel):
    """Backtest performance metrics"""
    total_return: float
    annual_return: float
    volatility: float
    sharpe_ratio: float
    sortino_ratio: float
    calmar_ratio: float
    max_drawdown: float
    win_rate: float
    profit_factor: float
    alpha: Optional[float] = None
    beta: Optional[float] = None
    information_ratio: Optional[float] = None

class BacktestResponse(BaseModel):
    """Backtest results"""
    metrics: BacktestMetrics
    equity_curve: List[Dict[str, Any]]
    trades: List[Dict[str, Any]]
    model_type: str
    symbols: List[str]
    start_date: str
    end_date: str

class AssetInfo(BaseModel):
    """Asset information"""
    symbol: str
    name: str
    asset_class: AssetClass
    description: Optional[str] = None

class AssetListResponse(BaseModel):
    """List of available assets"""
    assets: List[AssetInfo]
    total: int

class ErrorResponse(BaseModel):
    """Error response"""
    error: str
    message: str
    detail: Optional[str] = None
