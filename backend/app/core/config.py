"""
Application Configuration
"""

from pydantic_settings import BaseSettings
from typing import List
import os
from pathlib import Path

class Settings(BaseSettings):
    """Application settings"""

    # API Settings
    API_V1_STR: str = "/api"
    PROJECT_NAME: str = "Market Intelligence ML"
    VERSION: str = "1.0.0"

    # CORS
    ALLOWED_ORIGINS: List[str] = [
        "http://localhost:3000",
        "http://localhost:5173",
        "http://127.0.0.1:3000",
        "http://127.0.0.1:5173",
    ]

    # Paths
    BASE_DIR: Path = Path(__file__).parent.parent.parent.parent
    DATA_DIR: Path = BASE_DIR / "data"
    MODELS_DIR: Path = BASE_DIR / "results" / "models"
    CONFIG_PATH: Path = BASE_DIR / "configs" / "config.yaml"

    # ML Settings
    DEFAULT_MODEL: str = "xgboost"
    CACHE_PREDICTIONS: bool = True
    CACHE_TTL: int = 3600  # 1 hour

    # Data Settings
    DEFAULT_START_DATE: str = "2018-01-01"
    DEFAULT_END_DATE: str = "2025-01-01"

    class Config:
        env_file = ".env"
        case_sensitive = True

settings = Settings()

# Create necessary directories
settings.DATA_DIR.mkdir(parents=True, exist_ok=True)
settings.MODELS_DIR.mkdir(parents=True, exist_ok=True)
