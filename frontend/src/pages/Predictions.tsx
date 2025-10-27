import { useState } from 'react'
import { useMutation } from '@tanstack/react-query'
import { predictReturns } from '../services/api'
import AssetSelector from '../components/AssetSelector'
import { TrendingUp, TrendingDown, Minus, Loader2 } from 'lucide-react'
import type { PredictionResult } from '../types'

export default function Predictions() {
  const [selectedAssets, setSelectedAssets] = useState<string[]>([])
  const [modelType, setModelType] = useState('xgboost')
  const [horizon, setHorizon] = useState('1d')

  const mutation = useMutation({
    mutationFn: predictReturns,
  })

  const handlePredict = () => {
    if (selectedAssets.length === 0) {
      alert('Please select at least one asset')
      return
    }

    mutation.mutate({
      symbols: selectedAssets,
      model_type: modelType,
      horizon: horizon,
    })
  }

  const getSignalColor = (signal: string) => {
    switch (signal) {
      case 'BUY':
        return 'bg-green-100 text-green-800 border-green-300'
      case 'SELL':
        return 'bg-red-100 text-red-800 border-red-300'
      case 'HOLD':
        return 'bg-yellow-100 text-yellow-800 border-yellow-300'
      default:
        return 'bg-gray-100 text-gray-800 border-gray-300'
    }
  }

  const getSignalIcon = (signal: string) => {
    switch (signal) {
      case 'BUY':
        return <TrendingUp className="w-5 h-5" />
      case 'SELL':
        return <TrendingDown className="w-5 h-5" />
      default:
        return <Minus className="w-5 h-5" />
    }
  }

  return (
    <div className="space-y-6">
      <div>
        <h2 className="text-2xl font-bold text-gray-900">Price Predictions</h2>
        <p className="text-gray-600 mt-1">
          Get ML-powered return forecasts with confidence scores
        </p>
      </div>

      {/* Configuration */}
      <div className="card">
        <h3 className="text-lg font-semibold text-gray-900 mb-4">
          Configuration
        </h3>

        <div className="space-y-4">
          {/* Asset Selection */}
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">
              Select Assets
            </label>
            <AssetSelector
              selectedAssets={selectedAssets}
              onChange={setSelectedAssets}
              maxSelections={5}
            />
          </div>

          {/* Model Selection */}
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                Model Type
              </label>
              <select
                value={modelType}
                onChange={(e) => setModelType(e.target.value)}
                className="input w-full"
              >
                <option value="xgboost">XGBoost (Recommended)</option>
                <option value="random_forest">Random Forest</option>
                <option value="linear">Linear Regression</option>
                <option value="lstm">LSTM</option>
                <option value="ensemble">Ensemble</option>
              </select>
            </div>

            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                Prediction Horizon
              </label>
              <select
                value={horizon}
                onChange={(e) => setHorizon(e.target.value)}
                className="input w-full"
              >
                <option value="1d">1 Day</option>
                <option value="5d">5 Days</option>
                <option value="20d">20 Days</option>
                <option value="60d">60 Days</option>
              </select>
            </div>
          </div>

          <button
            onClick={handlePredict}
            disabled={mutation.isPending || selectedAssets.length === 0}
            className="btn-primary w-full md:w-auto flex items-center justify-center space-x-2 disabled:opacity-50"
          >
            {mutation.isPending && <Loader2 className="w-5 h-5 animate-spin" />}
            <span>{mutation.isPending ? 'Predicting...' : 'Generate Predictions'}</span>
          </button>
        </div>
      </div>

      {/* Results */}
      {mutation.isError && (
        <div className="card bg-red-50 border border-red-200">
          <p className="text-red-800">
            Error: {mutation.error instanceof Error ? mutation.error.message : 'An error occurred'}
          </p>
        </div>
      )}

      {mutation.data && (
        <div className="space-y-4">
          <div className="card">
            <h3 className="text-lg font-semibold text-gray-900 mb-2">
              Prediction Results
            </h3>
            <p className="text-sm text-gray-500">
              Model: {mutation.data.model_info.model_type} | Horizon: {mutation.data.model_info.horizon}
            </p>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
            {mutation.data.predictions.map((pred: PredictionResult) => (
              <div key={pred.symbol} className="card hover:shadow-lg transition-shadow">
                <div className="flex items-start justify-between mb-3">
                  <div>
                    <h4 className="text-lg font-bold text-gray-900">{pred.symbol}</h4>
                    <p className="text-sm text-gray-500">
                      {pred.current_price ? `$${pred.current_price.toFixed(2)}` : 'N/A'}
                    </p>
                  </div>
                  <span
                    className={`px-3 py-1 rounded-full text-xs font-semibold border flex items-center space-x-1 ${getSignalColor(
                      pred.signal
                    )}`}
                  >
                    {getSignalIcon(pred.signal)}
                    <span>{pred.signal}</span>
                  </span>
                </div>

                <div className="space-y-2">
                  <div>
                    <p className="text-xs text-gray-500">Predicted Return</p>
                    <p
                      className={`text-2xl font-bold ${
                        pred.predicted_return >= 0
                          ? 'text-green-600'
                          : 'text-red-600'
                      }`}
                    >
                      {pred.predicted_return >= 0 ? '+' : ''}
                      {(pred.predicted_return * 100).toFixed(2)}%
                    </p>
                  </div>

                  {pred.predicted_price && (
                    <div>
                      <p className="text-xs text-gray-500">Target Price</p>
                      <p className="text-lg font-semibold text-gray-900">
                        ${pred.predicted_price.toFixed(2)}
                      </p>
                    </div>
                  )}

                  <div className="pt-2 border-t border-gray-200">
                    <div className="flex justify-between text-xs">
                      <span className="text-gray-500">Confidence:</span>
                      <span className="font-medium text-gray-900">
                        {(pred.confidence * 100).toFixed(0)}%
                      </span>
                    </div>
                    <div className="w-full bg-gray-200 rounded-full h-2 mt-1">
                      <div
                        className="bg-primary-600 h-2 rounded-full"
                        style={{ width: `${pred.confidence * 100}%` }}
                      ></div>
                    </div>
                  </div>

                  <div className="text-xs text-gray-500">
                    Features: {pred.features_used} | Model: {pred.model_used}
                  </div>
                </div>
              </div>
            ))}
          </div>
        </div>
      )}
    </div>
  )
}
