export interface Asset {
  symbol: string
  name: string
  asset_class: 'equity' | 'fixed_income' | 'crypto' | 'commodity' | 'macro'
  description?: string
}

export interface PredictionResult {
  symbol: string
  predicted_return: number
  confidence: number
  signal: 'BUY' | 'SELL' | 'HOLD' | 'ERROR'
  current_price: number | null
  predicted_price: number | null
  features_used: number
  model_used: string
}

export interface PredictionResponse {
  predictions: PredictionResult[]
  timestamp: string
  model_info: {
    model_type: string
    horizon: string
    total_symbols: number
  }
}

export interface BacktestMetrics {
  total_return: number
  annual_return: number
  volatility: number
  sharpe_ratio: number
  sortino_ratio: number
  calmar_ratio: number
  max_drawdown: number
  win_rate: number
  profit_factor: number
  alpha?: number
  beta?: number
  information_ratio?: number
}

export interface BacktestResponse {
  metrics: BacktestMetrics
  equity_curve: Array<{
    date: string
    value: number
    return: number
  }>
  trades: Array<{
    date: string
    symbol: string
    action: 'BUY' | 'SELL'
    quantity: number
    price: number
    value: number
  }>
  model_type: string
  symbols: string[]
  start_date: string
  end_date: string
}

export interface FeatureImportance {
  feature_name: string
  importance: number
  rank: number
}

export interface AnalysisResponse {
  symbol: string
  statistics: Record<string, number>
  returns_summary: Record<string, number>
  correlations?: Record<string, number>
  technical_indicators?: Record<string, number>
  feature_importance?: FeatureImportance[]
}
