"""
Baseline models: Linear Regression, Random Forest.
"""

from sklearn.linear_model import LinearRegression, Ridge, Lasso
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import TimeSeriesSplit, cross_val_score
import numpy as np
import pandas as pd
from typing import Tuple, Optional

class LinearRegressionModel:
    """
    Linear Regression baseline model for return prediction.
    """

    def __init__(self, regularization=None, alpha=1.0):
        """
        Initialize Linear Regression model.

        Parameters:
        -----------
        regularization : str, optional
            Type of regularization: 'ridge', 'lasso', or None
        alpha : float
            Regularization strength
        """
        if regularization == 'ridge':
            self.model = Ridge(alpha=alpha)
        elif regularization == 'lasso':
            self.model = Lasso(alpha=alpha)
        else:
            self.model = LinearRegression()

        self.feature_names = None
        self.is_fitted = False

    def fit(self, X, y):
        """
        Fit the model.

        Parameters:
        -----------
        X : pd.DataFrame or np.ndarray
            Features
        y : pd.Series or np.ndarray
            Target variable
        """
        if isinstance(X, pd.DataFrame):
            self.feature_names = X.columns.tolist()
            X = X.values

        if isinstance(y, pd.Series):
            y = y.values

        self.model.fit(X, y)
        self.is_fitted = True

    def predict(self, X):
        """
        Make predictions.

        Parameters:
        -----------
        X : pd.DataFrame or np.ndarray
            Features

        Returns:
        --------
        np.ndarray: Predictions
        """
        if not self.is_fitted:
            raise ValueError("Model must be fitted before making predictions")

        if isinstance(X, pd.DataFrame):
            X = X.values

        return self.model.predict(X)

    def get_feature_importance(self):
        """
        Get feature coefficients.

        Returns:
        --------
        pd.Series: Feature coefficients
        """
        if not self.is_fitted:
            raise ValueError("Model must be fitted first")

        if self.feature_names is None:
            return pd.Series(self.model.coef_)

        return pd.Series(self.model.coef_, index=self.feature_names).sort_values(ascending=False)

    def cross_validate(self, X, y, n_splits=5):
        """
        Perform time series cross-validation.

        Parameters:
        -----------
        X : pd.DataFrame
            Features
        y : pd.Series
            Target
        n_splits : int
            Number of CV folds

        Returns:
        --------
        dict: Cross-validation scores
        """
        if isinstance(X, pd.DataFrame):
            X = X.values
        if isinstance(y, pd.Series):
            y = y.values

        tscv = TimeSeriesSplit(n_splits=n_splits)

        scores = cross_val_score(self.model, X, y, cv=tscv, scoring='r2')

        return {
            'mean_r2': scores.mean(),
            'std_r2': scores.std(),
            'scores': scores
        }


class RandomForestModel:
    """
    Random Forest model for return prediction.
    """

    def __init__(self, n_estimators=100, max_depth=10, min_samples_split=5,
                 random_state=42):
        """
        Initialize Random Forest model.

        Parameters:
        -----------
        n_estimators : int
            Number of trees
        max_depth : int
            Maximum tree depth
        min_samples_split : int
            Minimum samples to split a node
        random_state : int
            Random seed
        """
        self.model = RandomForestRegressor(
            n_estimators=n_estimators,
            max_depth=max_depth,
            min_samples_split=min_samples_split,
            random_state=random_state,
            n_jobs=-1
        )
        self.feature_names = None
        self.is_fitted = False

    def fit(self, X, y):
        """
        Fit the model.

        Parameters:
        -----------
        X : pd.DataFrame or np.ndarray
            Features
        y : pd.Series or np.ndarray
            Target variable
        """
        if isinstance(X, pd.DataFrame):
            self.feature_names = X.columns.tolist()
            X = X.values

        if isinstance(y, pd.Series):
            y = y.values

        self.model.fit(X, y)
        self.is_fitted = True

    def predict(self, X):
        """
        Make predictions.

        Parameters:
        -----------
        X : pd.DataFrame or np.ndarray
            Features

        Returns:
        --------
        np.ndarray: Predictions
        """
        if not self.is_fitted:
            raise ValueError("Model must be fitted before making predictions")

        if isinstance(X, pd.DataFrame):
            X = X.values

        return self.model.predict(X)

    def get_feature_importance(self, top_n=20):
        """
        Get feature importances.

        Parameters:
        -----------
        top_n : int
            Number of top features to return

        Returns:
        --------
        pd.Series: Feature importances
        """
        if not self.is_fitted:
            raise ValueError("Model must be fitted first")

        importances = self.model.feature_importances_

        if self.feature_names is None:
            feat_imp = pd.Series(importances)
        else:
            feat_imp = pd.Series(importances, index=self.feature_names)

        return feat_imp.sort_values(ascending=False).head(top_n)

    def cross_validate(self, X, y, n_splits=5):
        """
        Perform time series cross-validation.

        Parameters:
        -----------
        X : pd.DataFrame
            Features
        y : pd.Series
            Target
        n_splits : int
            Number of CV folds

        Returns:
        --------
        dict: Cross-validation scores
        """
        if isinstance(X, pd.DataFrame):
            X = X.values
        if isinstance(y, pd.Series):
            y = y.values

        tscv = TimeSeriesSplit(n_splits=n_splits)

        scores = cross_val_score(self.model, X, y, cv=tscv, scoring='r2')

        return {
            'mean_r2': scores.mean(),
            'std_r2': scores.std(),
            'scores': scores
        }


def walk_forward_validation(model, X, y, train_size=0.7, step_size=20):
    """
    Perform walk-forward validation for time series.

    Parameters:
    -----------
    model : object
        Model with fit() and predict() methods
    X : pd.DataFrame
        Features
    y : pd.Series
        Target
    train_size : float
        Initial training set proportion
    step_size : int
        Number of periods to move forward

    Returns:
    --------
    dict: Predictions and actual values
    """
    n_samples = len(X)
    initial_train_size = int(n_samples * train_size)

    predictions = []
    actuals = []
    dates = []

    for i in range(initial_train_size, n_samples, step_size):
        # Training data
        X_train = X.iloc[:i]
        y_train = y.iloc[:i]

        # Test data
        end_idx = min(i + step_size, n_samples)
        X_test = X.iloc[i:end_idx]
        y_test = y.iloc[i:end_idx]

        # Fit and predict
        model.fit(X_train, y_train)
        preds = model.predict(X_test)

        predictions.extend(preds)
        actuals.extend(y_test.values)
        dates.extend(X_test.index if isinstance(X, pd.DataFrame) else range(i, end_idx))

    return {
        'predictions': np.array(predictions),
        'actuals': np.array(actuals),
        'dates': dates
    }
