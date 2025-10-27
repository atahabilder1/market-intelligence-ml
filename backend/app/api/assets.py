"""
Assets API Endpoints
"""

from fastapi import APIRouter, HTTPException
from typing import List
import sys
from pathlib import Path

sys.path.append(str(Path(__file__).parent.parent.parent.parent))

from backend.app.models.schemas import AssetListResponse, AssetInfo, AssetClass
from src.utils.config import load_config
from backend.app.core.config import settings

router = APIRouter()

# Predefined asset information
ASSET_INFO = {
    # Equities
    "SPY": {"name": "SPDR S&P 500 ETF", "class": AssetClass.EQUITY, "desc": "S&P 500 Index Fund"},
    "XLK": {"name": "Technology Select Sector SPDR", "class": AssetClass.EQUITY, "desc": "Technology Sector"},
    "XLF": {"name": "Financial Select Sector SPDR", "class": AssetClass.EQUITY, "desc": "Financial Sector"},
    "XLV": {"name": "Health Care Select Sector SPDR", "class": AssetClass.EQUITY, "desc": "Healthcare Sector"},
    "XLE": {"name": "Energy Select Sector SPDR", "class": AssetClass.EQUITY, "desc": "Energy Sector"},
    "XLI": {"name": "Industrial Select Sector SPDR", "class": AssetClass.EQUITY, "desc": "Industrial Sector"},

    # Fixed Income
    "TLT": {"name": "iShares 20+ Year Treasury Bond ETF", "class": AssetClass.FIXED_INCOME, "desc": "Long-term Treasury Bonds"},
    "IEF": {"name": "iShares 7-10 Year Treasury Bond ETF", "class": AssetClass.FIXED_INCOME, "desc": "Mid-term Treasury Bonds"},

    # Alternatives
    "GLD": {"name": "SPDR Gold Trust", "class": AssetClass.COMMODITY, "desc": "Gold ETF"},
    "BTC/USDT": {"name": "Bitcoin", "class": AssetClass.CRYPTO, "desc": "Bitcoin vs USD Tether"},
    "ETH/USDT": {"name": "Ethereum", "class": AssetClass.CRYPTO, "desc": "Ethereum vs USD Tether"},
    "SOL/USDT": {"name": "Solana", "class": AssetClass.CRYPTO, "desc": "Solana vs USD Tether"},

    # Macro
    "^VIX": {"name": "CBOE Volatility Index", "class": AssetClass.MACRO, "desc": "Market Volatility Indicator"},
}

@router.get("/", response_model=AssetListResponse)
async def get_available_assets():
    """
    Get list of all available assets for analysis.
    """
    try:
        # Load config
        config = load_config(str(settings.CONFIG_PATH))

        # Gather all assets
        all_symbols = []
        for category in ['equities', 'fixed_income', 'alternatives', 'crypto', 'macro']:
            if category in config['assets']:
                all_symbols.extend(config['assets'][category])

        # Build response
        assets = []
        for symbol in all_symbols:
            info = ASSET_INFO.get(symbol, {
                "name": symbol,
                "class": AssetClass.EQUITY,
                "desc": None
            })

            assets.append(AssetInfo(
                symbol=symbol,
                name=info["name"],
                asset_class=info["class"],
                description=info.get("desc")
            ))

        return AssetListResponse(
            assets=assets,
            total=len(assets)
        )

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to load assets: {str(e)}")

@router.get("/categories")
async def get_asset_categories():
    """
    Get assets grouped by category.
    """
    try:
        config = load_config(str(settings.CONFIG_PATH))

        categories = {}
        for category in ['equities', 'fixed_income', 'alternatives', 'crypto', 'macro']:
            if category in config['assets']:
                categories[category] = config['assets'][category]

        return categories

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to load categories: {str(e)}")

@router.get("/{symbol}")
async def get_asset_info(symbol: str):
    """
    Get detailed information about a specific asset.
    """
    if symbol not in ASSET_INFO:
        raise HTTPException(status_code=404, detail=f"Asset {symbol} not found")

    info = ASSET_INFO[symbol]
    return AssetInfo(
        symbol=symbol,
        name=info["name"],
        asset_class=info["class"],
        description=info.get("desc")
    )
