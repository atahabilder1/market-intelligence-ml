import { useState } from 'react'
import { useMutation } from '@tanstack/react-query'
import { runBacktest } from '../services/api'
import AssetSelector from '../components/AssetSelector'
import { Loader2, TrendingUp, AlertTriangle } from 'lucide-react'
import {
  LineChart,
  Line,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  Legend,
  ResponsiveContainer,
} from 'recharts'

export default function Backtest() {
  const [selectedAssets, setSelectedAssets] = useState<string[]>([])
  const [modelType, setModelType] = useState('xgboost')
  const [startDate, setStartDate] = useState('2020-01-01')
  const [endDate, setEndDate] = useState('2024-12-31')
  const [initialCapital, setInitialCapital] = useState(100000)

  const mutation = useMutation({
    mutationFn: runBacktest,
  })

  const handleBacktest = () => {
    if (selectedAssets.length === 0) {
      alert('Please select at least one asset')
      return
    }

    mutation.mutate({
      symbols: selectedAssets,
      model_type: modelType,
      start_date: startDate,
      end_date: endDate,
      initial_capital: initialCapital,
      transaction_cost: 0.001,
      rebalance_frequency: 'daily',
    })
  }

  const formatCurrency = (value: number) => {
    return new Intl.NumberFormat('en-US', {
      style: 'currency',
      currency: 'USD',
      minimumFractionDigits: 0,
      maximumFractionDigits: 0,
    }).format(value)
  }

  const formatPercent = (value: number) => {
    return `${(value * 100).toFixed(2)}%`
  }

  return (
    <div className="space-y-6">
      <div>
        <h2 className="text-2xl font-bold text-gray-900">Backtesting</h2>
        <p className="text-gray-600 mt-1">
          Test your strategy with realistic transaction costs
        </p>
      </div>

      {/* Configuration */}
      <div className="card">
        <h3 className="text-lg font-semibold text-gray-900 mb-4">
          Backtest Configuration
        </h3>

        <div className="space-y-4">
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">
              Select Assets
            </label>
            <AssetSelector
              selectedAssets={selectedAssets}
              onChange={setSelectedAssets}
              maxSelections={3}
            />
          </div>

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
                <option value="xgboost">XGBoost</option>
                <option value="random_forest">Random Forest</option>
                <option value="linear">Linear Regression</option>
              </select>
            </div>

            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                Initial Capital
              </label>
              <input
                type="number"
                value={initialCapital}
                onChange={(e) => setInitialCapital(Number(e.target.value))}
                className="input w-full"
                min="1000"
                step="1000"
              />
            </div>

            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                Start Date
              </label>
              <input
                type="date"
                value={startDate}
                onChange={(e) => setStartDate(e.target.value)}
                className="input w-full"
              />
            </div>

            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                End Date
              </label>
              <input
                type="date"
                value={endDate}
                onChange={(e) => setEndDate(e.target.value)}
                className="input w-full"
              />
            </div>
          </div>

          <button
            onClick={handleBacktest}
            disabled={mutation.isPending || selectedAssets.length === 0}
            className="btn-primary w-full md:w-auto flex items-center justify-center space-x-2 disabled:opacity-50"
          >
            {mutation.isPending && <Loader2 className="w-5 h-5 animate-spin" />}
            <span>{mutation.isPending ? 'Running Backtest...' : 'Run Backtest'}</span>
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
        <div className="space-y-6">
          {/* Metrics Grid */}
          <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
            <div className="card">
              <p className="text-sm text-gray-500">Total Return</p>
              <p className={`text-2xl font-bold ${mutation.data.metrics.total_return >= 0 ? 'text-green-600' : 'text-red-600'}`}>
                {formatPercent(mutation.data.metrics.total_return)}
              </p>
            </div>

            <div className="card">
              <p className="text-sm text-gray-500">Annual Return</p>
              <p className={`text-2xl font-bold ${mutation.data.metrics.annual_return >= 0 ? 'text-green-600' : 'text-red-600'}`}>
                {formatPercent(mutation.data.metrics.annual_return)}
              </p>
            </div>

            <div className="card">
              <p className="text-sm text-gray-500">Sharpe Ratio</p>
              <p className={`text-2xl font-bold ${mutation.data.metrics.sharpe_ratio >= 1 ? 'text-green-600' : 'text-yellow-600'}`}>
                {mutation.data.metrics.sharpe_ratio.toFixed(2)}
              </p>
            </div>

            <div className="card">
              <p className="text-sm text-gray-500">Max Drawdown</p>
              <p className="text-2xl font-bold text-red-600">
                {formatPercent(mutation.data.metrics.max_drawdown)}
              </p>
            </div>

            <div className="card">
              <p className="text-sm text-gray-500">Win Rate</p>
              <p className="text-2xl font-bold text-gray-900">
                {formatPercent(mutation.data.metrics.win_rate)}
              </p>
            </div>

            <div className="card">
              <p className="text-sm text-gray-500">Volatility</p>
              <p className="text-2xl font-bold text-gray-900">
                {formatPercent(mutation.data.metrics.volatility)}
              </p>
            </div>

            {mutation.data.metrics.alpha !== undefined && (
              <div className="card">
                <p className="text-sm text-gray-500">Alpha</p>
                <p className={`text-2xl font-bold ${mutation.data.metrics.alpha >= 0 ? 'text-green-600' : 'text-red-600'}`}>
                  {formatPercent(mutation.data.metrics.alpha)}
                </p>
              </div>
            )}

            <div className="card">
              <p className="text-sm text-gray-500">Profit Factor</p>
              <p className="text-2xl font-bold text-gray-900">
                {mutation.data.metrics.profit_factor.toFixed(2)}
              </p>
            </div>
          </div>

          {/* Equity Curve */}
          <div className="card">
            <h3 className="text-lg font-semibold text-gray-900 mb-4">
              Equity Curve
            </h3>
            <ResponsiveContainer width="100%" height={400}>
              <LineChart data={mutation.data.equity_curve}>
                <CartesianGrid strokeDasharray="3 3" />
                <XAxis
                  dataKey="date"
                  tickFormatter={(value) => new Date(value).toLocaleDateString()}
                />
                <YAxis tickFormatter={(value) => formatCurrency(value)} />
                <Tooltip
                  formatter={(value: number) => formatCurrency(value)}
                  labelFormatter={(label) => new Date(label).toLocaleDateString()}
                />
                <Legend />
                <Line
                  type="monotone"
                  dataKey="value"
                  stroke="#0ea5e9"
                  strokeWidth={2}
                  dot={false}
                  name="Portfolio Value"
                />
              </LineChart>
            </ResponsiveContainer>
          </div>

          {/* Target Metrics Comparison */}
          <div className="card">
            <h3 className="text-lg font-semibold text-gray-900 mb-4">
              Target Metrics Comparison
            </h3>
            <div className="space-y-3">
              {[
                { label: 'Directional Accuracy (Win Rate)', value: mutation.data.metrics.win_rate, target: 0.55 },
                { label: 'Sharpe Ratio', value: mutation.data.metrics.sharpe_ratio, target: 1.0 },
                { label: 'Annual Alpha', value: mutation.data.metrics.alpha || 0, target: 0.05 },
              ].map((metric) => (
                <div key={metric.label}>
                  <div className="flex justify-between text-sm mb-1">
                    <span className="text-gray-700">{metric.label}</span>
                    <span className="font-medium">
                      {metric.label.includes('Rate') || metric.label.includes('Alpha')
                        ? formatPercent(metric.value)
                        : metric.value.toFixed(2)}
                      {' / '}
                      {metric.label.includes('Rate') || metric.label.includes('Alpha')
                        ? formatPercent(metric.target)
                        : metric.target.toFixed(1)}
                    </span>
                  </div>
                  <div className="w-full bg-gray-200 rounded-full h-2">
                    <div
                      className={`h-2 rounded-full ${
                        metric.value >= metric.target ? 'bg-green-600' : 'bg-yellow-600'
                      }`}
                      style={{
                        width: `${Math.min((metric.value / metric.target) * 100, 100)}%`,
                      }}
                    ></div>
                  </div>
                </div>
              ))}
            </div>
          </div>
        </div>
      )}
    </div>
  )
}
