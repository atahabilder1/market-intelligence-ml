"""
FastAPI Main Application
Market Intelligence ML Backend
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import sys
from pathlib import Path

# Add parent directory to path for importing src modules
sys.path.append(str(Path(__file__).parent.parent.parent))

from backend.app.api import prediction, backtest, assets, analysis
from backend.app.core.config import settings

app = FastAPI(
    title="Market Intelligence ML API",
    description="Multi-Asset Predictive Modeling API for Equities, Fixed Income & Digital Assets",
    version="1.0.0",
    docs_url="/api/docs",
    redoc_url="/api/redoc",
)

# CORS Configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Health check endpoint
@app.get("/")
async def root():
    return {
        "message": "Market Intelligence ML API",
        "version": "1.0.0",
        "status": "online",
        "docs": "/api/docs"
    }

@app.get("/health")
async def health_check():
    return {"status": "healthy"}

# Include routers
app.include_router(assets.router, prefix="/api/assets", tags=["Assets"])
app.include_router(prediction.router, prefix="/api/predict", tags=["Predictions"])
app.include_router(backtest.router, prefix="/api/backtest", tags=["Backtesting"])
app.include_router(analysis.router, prefix="/api/analysis", tags=["Analysis"])

# Exception handlers
@app.exception_handler(Exception)
async def global_exception_handler(request, exc):
    return JSONResponse(
        status_code=500,
        content={
            "error": "Internal server error",
            "message": str(exc),
            "type": type(exc).__name__
        }
    )

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True
    )
