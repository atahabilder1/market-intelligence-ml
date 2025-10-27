"""
Prediction Service - Handles ML predictions
"""

import sys
from pathlib import Path
import pandas as pd
import numpy as np
from typing import List, Dict, Any, Tuple

sys.path.append(str(Path(__file__).parent.parent.parent.parent))

from src.data.fetch_data import fetch_multiple_assets, get_close_prices
from src.features.technical_indicators import calculate_all_indicators
from src.features.cross_asset_features import calculate_asset_ratios
from src.models.xgboost_model import XGBoostPredictor
from src.models.baseline_models import LinearRegressionModel, RandomForestModel
from backend.app.core.config import settings

class PredictionService:
    """Service for making price predictions"""

    def __init__(self):
        self.models = {}
        self.trained_models = {}

    def prepare_features(self, symbol: str, data: pd.DataFrame) -> pd.DataFrame:
        """
        Prepare features for prediction.

        Parameters:
        -----------
        symbol : str
            Asset symbol
        data : pd.DataFrame
            Price data

        Returns:
        --------
        pd.DataFrame: Feature matrix
        """
        # Calculate technical indicators
        features = calculate_all_indicators(data)

        # Add returns
        features['returns_1d'] = data['Close'].pct_change()
        features['returns_5d'] = data['Close'].pct_change(5)
        features['returns_20d'] = data['Close'].pct_change(20)

        # Add volume features if available
        if 'Volume' in data.columns:
            features['volume_sma_20'] = data['Volume'].rolling(20).mean()
            features['volume_ratio'] = data['Volume'] / features['volume_sma_20']

        # Drop NaN values
        features = features.dropna()

        return features

    def create_target(self, data: pd.DataFrame, horizon: str = "1d") -> pd.Series:
        """
        Create target variable (future returns).

        Parameters:
        -----------
        data : pd.DataFrame
            Price data
        horizon : str
            Prediction horizon (1d, 5d, 20d, 60d)

        Returns:
        --------
        pd.Series: Target returns
        """
        horizon_map = {
            "1d": 1,
            "5d": 5,
            "20d": 20,
            "60d": 60
        }

        periods = horizon_map.get(horizon, 1)
        target = data['Close'].pct_change(periods).shift(-periods)

        return target

    def train_model(self, symbol: str, model_type: str, start_date: str, end_date: str, horizon: str = "1d"):
        """
        Train a prediction model.

        Parameters:
        -----------
        symbol : str
            Asset symbol
        model_type : str
            Type of model (xgboost, linear, random_forest)
        start_date : str
            Training start date
        end_date : str
            Training end date
        horizon : str
            Prediction horizon
        """
        # Fetch data
        data_dict = fetch_multiple_assets([symbol], start_date, end_date)
        data = data_dict[symbol]

        # Prepare features
        features = self.prepare_features(symbol, data)
        target = self.create_target(data, horizon)

        # Align features and target
        common_idx = features.index.intersection(target.index)
        X = features.loc[common_idx]
        y = target.loc[common_idx]

        # Remove rows with NaN in target
        valid_idx = ~y.isna()
        X = X[valid_idx]
        y = y[valid_idx]

        # Split train/val
        split_idx = int(len(X) * 0.8)
        X_train, y_train = X[:split_idx], y[:split_idx]
        X_val, y_val = X[split_idx:], y[split_idx:]

        # Train model
        if model_type == "xgboost":
            model = XGBoostPredictor()
            model.fit(X_train, y_train, eval_set=[(X_val, y_val)], early_stopping_rounds=50, verbose=False)
        elif model_type == "linear":
            model = LinearRegressionModel()
            model.fit(X_train, y_train)
        elif model_type == "random_forest":
            model = RandomForestModel()
            model.fit(X_train, y_train)
        else:
            raise ValueError(f"Unknown model type: {model_type}")

        # Store model
        model_key = f"{symbol}_{model_type}_{horizon}"
        self.trained_models[model_key] = {
            "model": model,
            "features": X.columns.tolist(),
            "symbol": symbol,
            "horizon": horizon
        }

        return model

    def predict(self, symbols: List[str], model_type: str, horizon: str = "1d",
                start_date: str = None, end_date: str = None) -> List[Dict[str, Any]]:
        """
        Make predictions for given symbols.

        Parameters:
        -----------
        symbols : List[str]
            List of asset symbols
        model_type : str
            Model type to use
        horizon : str
            Prediction horizon
        start_date : str, optional
            Data start date
        end_date : str, optional
            Data end date

        Returns:
        --------
        List[Dict]: Prediction results
        """
        if start_date is None:
            start_date = settings.DEFAULT_START_DATE
        if end_date is None:
            end_date = settings.DEFAULT_END_DATE

        results = []

        for symbol in symbols:
            try:
                # Check if model exists, otherwise train it
                model_key = f"{symbol}_{model_type}_{horizon}"
                if model_key not in self.trained_models:
                    self.train_model(symbol, model_type, start_date, end_date, horizon)

                model_info = self.trained_models[model_key]
                model = model_info["model"]

                # Fetch latest data
                data_dict = fetch_multiple_assets([symbol], start_date, end_date)
                data = data_dict[symbol]

                # Prepare features
                features = self.prepare_features(symbol, data)

                # Get latest features
                latest_features = features.iloc[-1:][model_info["features"]]

                # Predict
                prediction = model.predict(latest_features)[0]

                # Get current price
                current_price = data['Close'].iloc[-1]
                predicted_price = current_price * (1 + prediction)

                # Determine signal
                if prediction > 0.02:  # > 2% gain
                    signal = "BUY"
                    confidence = min(abs(prediction) * 10, 1.0)
                elif prediction < -0.02:  # > 2% loss
                    signal = "SELL"
                    confidence = min(abs(prediction) * 10, 1.0)
                else:
                    signal = "HOLD"
                    confidence = 1.0 - abs(prediction) * 5

                results.append({
                    "symbol": symbol,
                    "predicted_return": float(prediction),
                    "confidence": float(confidence),
                    "signal": signal,
                    "current_price": float(current_price),
                    "predicted_price": float(predicted_price),
                    "features_used": len(model_info["features"]),
                    "model_used": model_type
                })

            except Exception as e:
                results.append({
                    "symbol": symbol,
                    "error": str(e),
                    "predicted_return": 0.0,
                    "confidence": 0.0,
                    "signal": "ERROR",
                    "current_price": None,
                    "predicted_price": None,
                    "features_used": 0,
                    "model_used": model_type
                })

        return results

    def get_feature_importance(self, symbol: str, model_type: str, horizon: str = "1d", top_n: int = 20) -> List[Dict[str, Any]]:
        """
        Get feature importance for a trained model.

        Parameters:
        -----------
        symbol : str
            Asset symbol
        model_type : str
            Model type
        horizon : str
            Prediction horizon
        top_n : int
            Number of top features

        Returns:
        --------
        List[Dict]: Feature importance
        """
        model_key = f"{symbol}_{model_type}_{horizon}"

        if model_key not in self.trained_models:
            raise ValueError(f"Model not trained for {symbol} with {model_type}")

        model_info = self.trained_models[model_key]
        model = model_info["model"]

        # Get feature importance
        if hasattr(model, 'get_feature_importance'):
            importance = model.get_feature_importance(top_n=top_n)

            result = []
            for rank, (feature, imp) in enumerate(importance.items(), 1):
                result.append({
                    "feature_name": feature,
                    "importance": float(imp),
                    "rank": rank
                })

            return result
        else:
            return []

# Global service instance
prediction_service = PredictionService()
