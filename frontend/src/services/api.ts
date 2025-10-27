import axios from 'axios'
import type {
  Asset,
  PredictionResponse,
  BacktestResponse,
  AnalysisResponse,
} from '../types'

const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000'

const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
})

// Assets
export const getAssets = async (): Promise<{ assets: Asset[]; total: number }> => {
  const response = await api.get('/api/assets/')
  return response.data
}

export const getAssetCategories = async (): Promise<Record<string, string[]>> => {
  const response = await api.get('/api/assets/categories')
  return response.data
}

// Predictions
export const predictReturns = async (data: {
  symbols: string[]
  model_type?: string
  horizon?: string
  start_date?: string
  end_date?: string
}): Promise<PredictionResponse> => {
  const response = await api.post('/api/predict/', data)
  return response.data
}

export const getFeatureImportance = async (
  symbol: string,
  model_type: string = 'xgboost',
  horizon: string = '1d'
): Promise<{ symbol: string; model_type: string; features: any[] }> => {
  const response = await api.get(`/api/predict/feature-importance/${symbol}`, {
    params: { model_type, horizon },
  })
  return response.data
}

// Backtesting
export const runBacktest = async (data: {
  symbols: string[]
  model_type?: string
  start_date: string
  end_date: string
  initial_capital?: number
  transaction_cost?: number
  rebalance_frequency?: string
}): Promise<BacktestResponse> => {
  const response = await api.post('/api/backtest/', data)
  return response.data
}

export const getQuickStats = async (
  symbol: string,
  start_date: string,
  end_date: string
): Promise<{ symbol: string; metrics: any; data_points: number }> => {
  const response = await api.get(`/api/backtest/quick-stats/${symbol}`, {
    params: { start_date, end_date },
  })
  return response.data
}

// Analysis
export const analyzeAssets = async (data: {
  symbols: string[]
  start_date: string
  end_date: string
  include_correlations?: boolean
  include_technical?: boolean
}): Promise<AnalysisResponse[]> => {
  const response = await api.post('/api/analysis/', data)
  return response.data
}

export const getPriceHistory = async (
  symbol: string,
  start_date: string,
  end_date: string
): Promise<{
  symbol: string
  data: Array<{
    date: string
    open: number
    high: number
    low: number
    close: number
    volume: number
  }>
  total_points: number
}> => {
  const response = await api.get(`/api/analysis/price-history/${symbol}`, {
    params: { start_date, end_date },
  })
  return response.data
}

export default api
