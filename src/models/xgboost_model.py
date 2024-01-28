"""
XGBoost model implementation.
"""

import xgboost as xgb
from sklearn.model_selection import TimeSeriesSplit, GridSearchCV
import numpy as np
import pandas as pd
from typing import Optional, Dict

class XGBoostPredictor:
    """XGBoost model for return prediction."""

    def __init__(self, n_estimators=100, max_depth=5, learning_rate=0.01,
                 subsample=0.8, colsample_bytree=0.8, random_state=42):
        """
        Initialize XGBoost model.

        Parameters:
        -----------
        n_estimators : int
            Number of boosting rounds
        max_depth : int
            Maximum tree depth
        learning_rate : float
            Learning rate (eta)
        subsample : float
            Subsample ratio of training instances
        colsample_bytree : float
            Subsample ratio of columns
        random_state : int
            Random seed
        """
        self.model = xgb.XGBRegressor(
            n_estimators=n_estimators,
            max_depth=max_depth,
            learning_rate=learning_rate,
            subsample=subsample,
            colsample_bytree=colsample_bytree,
            random_state=random_state,
            tree_method='hist',
            n_jobs=-1
        )
        self.feature_names = None
        self.is_fitted = False

    def fit(self, X, y, eval_set=None, early_stopping_rounds=None, verbose=False):
        """
        Fit the XGBoost model.

        Parameters:
        -----------
        X : pd.DataFrame or np.ndarray
            Training features
        y : pd.Series or np.ndarray
            Target variable
        eval_set : list of tuples, optional
            Evaluation sets for early stopping [(X_val, y_val)]
        early_stopping_rounds : int, optional
            Early stopping rounds
        verbose : bool
            Print training progress
        """
        if isinstance(X, pd.DataFrame):
            self.feature_names = X.columns.tolist()
            X = X.values

        if isinstance(y, pd.Series):
            y = y.values

        # Prepare evaluation set
        if eval_set is not None and len(eval_set) > 0:
            eval_set_processed = []
            for X_eval, y_eval in eval_set:
                if isinstance(X_eval, pd.DataFrame):
                    X_eval = X_eval.values
                if isinstance(y_eval, pd.Series):
                    y_eval = y_eval.values
                eval_set_processed.append((X_eval, y_eval))
            eval_set = eval_set_processed

        # Fit model
        self.model.fit(
            X, y,
            eval_set=eval_set,
            early_stopping_rounds=early_stopping_rounds,
            verbose=verbose
        )
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

    def get_feature_importance(self, importance_type='gain', top_n=20):
        """
        Get feature importances.

        Parameters:
        -----------
        importance_type : str
            Type of importance: 'gain', 'weight', 'cover'
        top_n : int
            Number of top features to return

        Returns:
        --------
        pd.Series: Feature importances
        """
        if not self.is_fitted:
            raise ValueError("Model must be fitted first")

        # Get importance from booster
        importance_dict = self.model.get_booster().get_score(importance_type=importance_type)

        if self.feature_names is None:
            feat_imp = pd.Series(importance_dict)
        else:
            # Map feature names
            feat_imp_mapped = {}
            for feat_id, importance in importance_dict.items():
                # XGBoost uses f0, f1, etc. as feature names
                idx = int(feat_id.replace('f', ''))
                if idx < len(self.feature_names):
                    feat_imp_mapped[self.feature_names[idx]] = importance

            feat_imp = pd.Series(feat_imp_mapped)

        return feat_imp.sort_values(ascending=False).head(top_n)

    def tune_hyperparameters(self, X, y, param_grid=None, n_splits=3):
        """
        Tune hyperparameters using GridSearchCV with TimeSeriesSplit.

        Parameters:
        -----------
        X : pd.DataFrame
            Features
        y : pd.Series
            Target
        param_grid : dict, optional
            Parameter grid for search
        n_splits : int
            Number of CV folds

        Returns:
        --------
        dict: Best parameters and score
        """
        if param_grid is None:
            param_grid = {
                'max_depth': [3, 5, 7],
                'learning_rate': [0.01, 0.05, 0.1],
                'n_estimators': [100, 200],
                'subsample': [0.8, 1.0],
                'colsample_bytree': [0.8, 1.0]
            }

        if isinstance(X, pd.DataFrame):
            X = X.values
        if isinstance(y, pd.Series):
            y = y.values

        tscv = TimeSeriesSplit(n_splits=n_splits)

        grid_search = GridSearchCV(
            self.model,
            param_grid,
            cv=tscv,
            scoring='neg_mean_squared_error',
            n_jobs=-1,
            verbose=1
        )

        grid_search.fit(X, y)

        return {
            'best_params': grid_search.best_params_,
            'best_score': -grid_search.best_score_,  # Convert back to positive MSE
            'cv_results': grid_search.cv_results_
        }

    def plot_feature_importance(self, importance_type='gain', top_n=20):
        """
        Plot feature importance.

        Parameters:
        -----------
        importance_type : str
            Type of importance: 'gain', 'weight', 'cover'
        top_n : int
            Number of top features to plot
        """
        import matplotlib.pyplot as plt

        feat_imp = self.get_feature_importance(importance_type, top_n)

        plt.figure(figsize=(10, 6))
        feat_imp.plot(kind='barh')
        plt.xlabel('Importance')
        plt.title(f'Top {top_n} Features by {importance_type.capitalize()}')
        plt.gca().invert_yaxis()
        plt.tight_layout()
        plt.show()

    def save_model(self, filepath):
        """
        Save model to file.

        Parameters:
        -----------
        filepath : str
            Path to save model
        """
        if not self.is_fitted:
            raise ValueError("Model must be fitted before saving")

        self.model.save_model(filepath)

    def load_model(self, filepath):
        """
        Load model from file.

        Parameters:
        -----------
        filepath : str
            Path to load model from
        """
        self.model.load_model(filepath)
        self.is_fitted = True
