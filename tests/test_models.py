"""
Unit tests for model modules.
"""

import pytest
import numpy as np
import pandas as pd
from src.models.baseline_models import LinearRegressionModel, RandomForestModel
from src.models.xgboost_model import XGBoostPredictor

@pytest.fixture
def sample_data():
    """Create sample data for testing."""
    np.random.seed(42)
    X = pd.DataFrame(np.random.randn(100, 5), columns=[f'feature_{i}' for i in range(5)])
    y = pd.Series(np.random.randn(100))
    return X, y

def test_linear_regression_model(sample_data):
    """Test Linear Regression model."""
    X, y = sample_data

    model = LinearRegressionModel()
    model.fit(X, y)

    assert model.is_fitted
    predictions = model.predict(X)
    assert len(predictions) == len(y)
    assert isinstance(predictions, np.ndarray)

def test_random_forest_model(sample_data):
    """Test Random Forest model."""
    X, y = sample_data

    model = RandomForestModel(n_estimators=10, max_depth=3)
    model.fit(X, y)

    assert model.is_fitted
    predictions = model.predict(X)
    assert len(predictions) == len(y)

    # Test feature importance
    feat_imp = model.get_feature_importance(top_n=5)
    assert len(feat_imp) <= 5

def test_xgboost_model(sample_data):
    """Test XGBoost model."""
    X, y = sample_data

    model = XGBoostPredictor(n_estimators=10, max_depth=3)
    model.fit(X, y)

    assert model.is_fitted
    predictions = model.predict(X)
    assert len(predictions) == len(y)

def test_model_cross_validation(sample_data):
    """Test cross-validation."""
    X, y = sample_data

    model = LinearRegressionModel()
    cv_results = model.cross_validate(X, y, n_splits=3)

    assert 'mean_r2' in cv_results
    assert 'std_r2' in cv_results
    assert isinstance(cv_results['mean_r2'], float)
