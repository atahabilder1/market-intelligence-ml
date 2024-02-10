"""
LSTM model implementation for time series prediction.
"""

import numpy as np
import pandas as pd
from tensorflow import keras
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import LSTM, Dense, Dropout
from tensorflow.keras.callbacks import EarlyStopping, ReduceLROnPlateau
from sklearn.preprocessing import StandardScaler
from typing import Tuple, Optional

class LSTMPredictor:
    """LSTM model for return prediction."""

    def __init__(self, lookback=20, lstm_units=[64, 32], dropout=0.2,
                 learning_rate=0.001, random_state=42):
        """
        Initialize LSTM model.

        Parameters:
        -----------
        lookback : int
            Number of time steps to look back
        lstm_units : list
            Number of units in each LSTM layer
        dropout : float
            Dropout rate
        learning_rate : float
            Learning rate for optimizer
        random_state : int
            Random seed
        """
        self.lookback = lookback
        self.lstm_units = lstm_units
        self.dropout = dropout
        self.learning_rate = learning_rate
        self.random_state = random_state

        np.random.seed(random_state)
        keras.utils.set_random_seed(random_state)

        self.model = None
        self.scaler = StandardScaler()
        self.is_fitted = False
        self.feature_names = None

    def _build_model(self, input_shape):
        """Build LSTM architecture."""
        model = Sequential()

        # First LSTM layer
        model.add(LSTM(
            self.lstm_units[0],
            return_sequences=len(self.lstm_units) > 1,
            input_shape=input_shape
        ))
        model.add(Dropout(self.dropout))

        # Additional LSTM layers
        for i, units in enumerate(self.lstm_units[1:]):
            return_seq = i < len(self.lstm_units) - 2
            model.add(LSTM(units, return_sequences=return_seq))
            model.add(Dropout(self.dropout))

        # Output layer
        model.add(Dense(1))

        # Compile
        model.compile(
            optimizer=keras.optimizers.Adam(learning_rate=self.learning_rate),
            loss='mse',
            metrics=['mae']
        )

        return model

    def _create_sequences(self, X, y=None):
        """
        Create sequences for LSTM input.

        Parameters:
        -----------
        X : np.ndarray
            Features
        y : np.ndarray, optional
            Target values

        Returns:
        --------
        tuple: (X_seq, y_seq) or X_seq if y is None
        """
        X_seq = []
        y_seq = [] if y is not None else None

        for i in range(len(X) - self.lookback):
            X_seq.append(X[i:i + self.lookback])
            if y is not None:
                y_seq.append(y[i + self.lookback])

        X_seq = np.array(X_seq)

        if y is not None:
            y_seq = np.array(y_seq)
            return X_seq, y_seq

        return X_seq

    def fit(self, X, y, validation_split=0.2, epochs=100, batch_size=32,
            verbose=1, early_stopping=True):
        """
        Fit the LSTM model.

        Parameters:
        -----------
        X : pd.DataFrame or np.ndarray
            Training features
        y : pd.Series or np.ndarray
            Target variable
        validation_split : float
            Fraction of data for validation
        epochs : int
            Number of training epochs
        batch_size : int
            Batch size
        verbose : int
            Verbosity level
        early_stopping : bool
            Use early stopping

        Returns:
        --------
        History: Training history
        """
        if isinstance(X, pd.DataFrame):
            self.feature_names = X.columns.tolist()
            X = X.values

        if isinstance(y, pd.Series):
            y = y.values

        # Scale features
        X_scaled = self.scaler.fit_transform(X)

        # Create sequences
        X_seq, y_seq = self._create_sequences(X_scaled, y)

        # Build model
        self.model = self._build_model((self.lookback, X.shape[1]))

        # Callbacks
        callbacks = []
        if early_stopping:
            callbacks.append(EarlyStopping(
                monitor='val_loss',
                patience=10,
                restore_best_weights=True
            ))
            callbacks.append(ReduceLROnPlateau(
                monitor='val_loss',
                factor=0.5,
                patience=5,
                min_lr=1e-7
            ))

        # Train
        history = self.model.fit(
            X_seq, y_seq,
            validation_split=validation_split,
            epochs=epochs,
            batch_size=batch_size,
            callbacks=callbacks,
            verbose=verbose
        )

        self.is_fitted = True
        return history

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

        # Scale and create sequences
        X_scaled = self.scaler.transform(X)
        X_seq = self._create_sequences(X_scaled)

        # Predict
        predictions = self.model.predict(X_seq, verbose=0)

        # Pad predictions to match input length
        padded_predictions = np.full(len(X), np.nan)
        padded_predictions[self.lookback:] = predictions.flatten()

        return padded_predictions

    def save_model(self, filepath):
        """Save model to file."""
        if not self.is_fitted:
            raise ValueError("Model must be fitted before saving")
        self.model.save(filepath)

    def load_model(self, filepath):
        """Load model from file."""
        self.model = keras.models.load_model(filepath)
        self.is_fitted = True
