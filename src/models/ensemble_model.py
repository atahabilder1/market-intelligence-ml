"""
Ensemble model combining multiple predictors.
"""

import numpy as np
import pandas as pd
from sklearn.linear_model import Ridge, LinearRegression
from typing import List, Dict, Optional

class EnsemblePredictor:
    """Meta-model combining multiple base models."""

    def __init__(self, base_models: List, meta_model=None, weights=None):
        """
        Initialize ensemble model.

        Parameters:
        -----------
        base_models : list
            List of base model instances (must have fit/predict methods)
        meta_model : object, optional
            Meta-learner model (default: Ridge regression)
        weights : list, optional
            Fixed weights for simple weighted average (if None, use meta-model)
        """
        self.base_models = base_models
        self.meta_model = meta_model if meta_model is not None else Ridge(alpha=1.0)
        self.weights = np.array(weights) if weights is not None else None
        self.is_fitted = False
        self.use_meta_model = weights is None

    def fit(self, X, y, X_val=None, y_val=None):
        """
        Fit ensemble model.

        Parameters:
        -----------
        X : pd.DataFrame
            Training features
        y : pd.Series
            Target variable
        X_val : pd.DataFrame, optional
            Validation features for meta-model training
        y_val : pd.Series, optional
            Validation target for meta-model training
        """
        # Train base models
        for i, model in enumerate(self.base_models):
            print(f"Training base model {i+1}/{len(self.base_models)}...")
            model.fit(X, y)

        # Train meta-model if using stacking
        if self.use_meta_model:
            if X_val is None or y_val is None:
                # Use out-of-fold predictions on training data
                base_predictions = self._get_base_predictions(X)
            else:
                # Use validation set
                base_predictions = self._get_base_predictions(X_val)
                y = y_val

            # Ensure no NaN values
            valid_idx = ~np.isnan(base_predictions).any(axis=1)
            base_predictions_clean = base_predictions[valid_idx]
            y_clean = y.iloc[valid_idx] if isinstance(y, pd.Series) else y[valid_idx]

            print("Training meta-model...")
            self.meta_model.fit(base_predictions_clean, y_clean)

        self.is_fitted = True

    def predict(self, X):
        """
        Make ensemble predictions.

        Parameters:
        -----------
        X : pd.DataFrame
            Features

        Returns:
        --------
        np.ndarray: Ensemble predictions
        """
        if not self.is_fitted:
            raise ValueError("Model must be fitted before making predictions")

        # Get base model predictions
        base_predictions = self._get_base_predictions(X)

        # Combine predictions
        if self.use_meta_model:
            # Use meta-model
            valid_idx = ~np.isnan(base_predictions).any(axis=1)
            predictions = np.full(len(X), np.nan)
            predictions[valid_idx] = self.meta_model.predict(base_predictions[valid_idx])
        else:
            # Use fixed weights
            predictions = np.average(base_predictions, axis=1, weights=self.weights)

        return predictions

    def _get_base_predictions(self, X):
        """
        Get predictions from all base models.

        Parameters:
        -----------
        X : pd.DataFrame
            Features

        Returns:
        --------
        np.ndarray: Base model predictions (n_samples, n_models)
        """
        predictions = []

        for model in self.base_models:
            pred = model.predict(X)
            predictions.append(pred)

        return np.column_stack(predictions)

    def get_model_weights(self):
        """
        Get model combination weights.

        Returns:
        --------
        np.ndarray or dict: Weights used for combining models
        """
        if self.use_meta_model:
            if hasattr(self.meta_model, 'coef_'):
                return {
                    'type': 'meta_model',
                    'weights': self.meta_model.coef_,
                    'intercept': self.meta_model.intercept_
                }
            else:
                return {'type': 'meta_model', 'weights': 'complex model'}
        else:
            return {
                'type': 'fixed_weights',
                'weights': self.weights
            }

    def get_base_model_performance(self, X, y):
        """
        Evaluate individual base model performance.

        Parameters:
        -----------
        X : pd.DataFrame
            Features
        y : pd.Series
            True values

        Returns:
        --------
        pd.DataFrame: Performance metrics for each base model
        """
        from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score

        results = []

        for i, model in enumerate(self.base_models):
            pred = model.predict(X)

            # Handle NaN values
            valid_idx = ~np.isnan(pred)
            pred_clean = pred[valid_idx]
            y_clean = y.iloc[valid_idx] if isinstance(y, pd.Series) else y[valid_idx]

            if len(pred_clean) > 0:
                mse = mean_squared_error(y_clean, pred_clean)
                mae = mean_absolute_error(y_clean, pred_clean)
                r2 = r2_score(y_clean, pred_clean)

                results.append({
                    'model': f'Model_{i+1}',
                    'mse': mse,
                    'rmse': np.sqrt(mse),
                    'mae': mae,
                    'r2': r2
                })

        # Add ensemble performance
        ensemble_pred = self.predict(X)
        valid_idx = ~np.isnan(ensemble_pred)
        ensemble_pred_clean = ensemble_pred[valid_idx]
        y_clean = y.iloc[valid_idx] if isinstance(y, pd.Series) else y[valid_idx]

        if len(ensemble_pred_clean) > 0:
            mse = mean_squared_error(y_clean, ensemble_pred_clean)
            mae = mean_absolute_error(y_clean, ensemble_pred_clean)
            r2 = r2_score(y_clean, ensemble_pred_clean)

            results.append({
                'model': 'Ensemble',
                'mse': mse,
                'rmse': np.sqrt(mse),
                'mae': mae,
                'r2': r2
            })

        return pd.DataFrame(results)


class SimpleAverageEnsemble:
    """Simple averaging ensemble (equal weights)."""

    def __init__(self, base_models: List):
        """
        Initialize simple average ensemble.

        Parameters:
        -----------
        base_models : list
            List of base model instances
        """
        self.base_models = base_models
        self.is_fitted = False

    def fit(self, X, y):
        """Fit all base models."""
        for model in self.base_models:
            model.fit(X, y)
        self.is_fitted = True

    def predict(self, X):
        """Make predictions using simple average."""
        if not self.is_fitted:
            raise ValueError("Model must be fitted first")

        predictions = []
        for model in self.base_models:
            predictions.append(model.predict(X))

        return np.mean(predictions, axis=0)


class WeightedEnsemble:
    """Weighted ensemble with performance-based weights."""

    def __init__(self, base_models: List):
        """
        Initialize weighted ensemble.

        Parameters:
        -----------
        base_models : list
            List of base model instances
        """
        self.base_models = base_models
        self.weights = None
        self.is_fitted = False

    def fit(self, X, y, X_val, y_val):
        """
        Fit models and calculate performance-based weights.

        Parameters:
        -----------
        X : pd.DataFrame
            Training features
        y : pd.Series
            Training target
        X_val : pd.DataFrame
            Validation features
        y_val : pd.Series
            Validation target
        """
        from sklearn.metrics import mean_squared_error

        # Train base models
        for model in self.base_models:
            model.fit(X, y)

        # Calculate weights based on validation performance
        errors = []
        for model in self.base_models:
            pred = model.predict(X_val)
            valid_idx = ~np.isnan(pred)
            pred_clean = pred[valid_idx]
            y_val_clean = y_val.iloc[valid_idx] if isinstance(y_val, pd.Series) else y_val[valid_idx]

            mse = mean_squared_error(y_val_clean, pred_clean)
            errors.append(mse)

        # Inverse error weighting (lower error = higher weight)
        inv_errors = 1.0 / (np.array(errors) + 1e-10)
        self.weights = inv_errors / inv_errors.sum()

        self.is_fitted = True

    def predict(self, X):
        """Make weighted predictions."""
        if not self.is_fitted:
            raise ValueError("Model must be fitted first")

        predictions = []
        for model in self.base_models:
            predictions.append(model.predict(X))

        return np.average(predictions, axis=0, weights=self.weights)
