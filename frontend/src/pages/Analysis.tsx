import { useState } from 'react'
import { useMutation } from '@tanstack/react-query'
import { analyzeAssets } from '../services/api'
import AssetSelector from '../components/AssetSelector'
import { Loader2 } from 'lucide-react'
import {
  BarChart,
  Bar,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  Legend,
  ResponsiveContainer,
  RadarChart,
  PolarGrid,
  PolarAngleAxis,
  PolarRadiusAxis,
  Radar,
} from 'recharts'

export default function Analysis() {
  const [selectedAssets, setSelectedAssets] = useState<string[]>([])
  const [startDate, setStartDate] = useState('2023-01-01')
  const [endDate, setEndDate] = useState('2024-12-31')

  const mutation = useMutation({
    mutationFn: analyzeAssets,
  })

  const handleAnalyze = () => {
    if (selectedAssets.length === 0) {
      alert('Please select at least one asset')
      return
    }

    mutation.mutate({
      symbols: selectedAssets,
      start_date: startDate,
      end_date: endDate,
      include_correlations: true,
      include_technical: true,
    })
  }

  const formatPercent = (value: number) => `${(value * 100).toFixed(2)}%`
  const formatNumber = (value: number) => value.toFixed(2)

  return (
    <div className="space-y-6">
      <div>
        <h2 className="text-2xl font-bold text-gray-900">Asset Analysis</h2>
        <p className="text-gray-600 mt-1">
          Technical indicators and correlation analysis
        </p>
      </div>

      {/* Configuration */}
      <div className="card">
        <h3 className="text-lg font-semibold text-gray-900 mb-4">
          Analysis Configuration
        </h3>

        <div className="space-y-4">
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">
              Select Assets
            </label>
            <AssetSelector
              selectedAssets={selectedAssets}
              onChange={setSelectedAssets}
              maxSelections={6}
            />
          </div>

          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
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
            onClick={handleAnalyze}
            disabled={mutation.isPending || selectedAssets.length === 0}
            className="btn-primary w-full md:w-auto flex items-center justify-center space-x-2 disabled:opacity-50"
          >
            {mutation.isPending && <Loader2 className="w-5 h-5 animate-spin" />}
            <span>{mutation.isPending ? 'Analyzing...' : 'Run Analysis'}</span>
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
          {/* Asset Cards */}
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
            {mutation.data.map((asset) => (
              <div key={asset.symbol} className="card">
                <h4 className="text-lg font-bold text-gray-900 mb-3">
                  {asset.symbol}
                </h4>

                <div className="space-y-2 text-sm">
                  <div className="flex justify-between">
                    <span className="text-gray-600">Current Price:</span>
                    <span className="font-medium">
                      ${asset.statistics.current_price.toFixed(2)}
                    </span>
                  </div>
                  <div className="flex justify-between">
                    <span className="text-gray-600">Total Return:</span>
                    <span
                      className={`font-medium ${
                        asset.returns_summary.total_return >= 0
                          ? 'text-green-600'
                          : 'text-red-600'
                      }`}
                    >
                      {formatPercent(asset.returns_summary.total_return)}
                    </span>
                  </div>
                  <div className="flex justify-between">
                    <span className="text-gray-600">Volatility (Annual):</span>
                    <span className="font-medium">
                      {formatPercent(asset.returns_summary.volatility_annual)}
                    </span>
                  </div>
                  <div className="flex justify-between">
                    <span className="text-gray-600">Mean Return:</span>
                    <span className="font-medium">
                      {formatPercent(asset.returns_summary.mean_return)}
                    </span>
                  </div>
                </div>

                {/* Technical Indicators */}
                {asset.technical_indicators && (
                  <div className="mt-4 pt-4 border-t border-gray-200">
                    <p className="text-xs font-semibold text-gray-700 mb-2">
                      Technical Indicators
                    </p>
                    <div className="space-y-1 text-xs">
                      <div className="flex justify-between">
                        <span className="text-gray-600">RSI:</span>
                        <span className="font-medium">
                          {asset.technical_indicators.rsi.toFixed(1)}
                        </span>
                      </div>
                      <div className="flex justify-between">
                        <span className="text-gray-600">MACD:</span>
                        <span className="font-medium">
                          {asset.technical_indicators.macd.toFixed(2)}
                        </span>
                      </div>
                      <div className="flex justify-between">
                        <span className="text-gray-600">SMA 20:</span>
                        <span className="font-medium">
                          ${asset.technical_indicators.sma_20.toFixed(2)}
                        </span>
                      </div>
                    </div>
                  </div>
                )}
              </div>
            ))}
          </div>

          {/* Returns Comparison */}
          <div className="card">
            <h3 className="text-lg font-semibold text-gray-900 mb-4">
              Total Returns Comparison
            </h3>
            <ResponsiveContainer width="100%" height={300}>
              <BarChart
                data={mutation.data.map((asset) => ({
                  symbol: asset.symbol,
                  return: asset.returns_summary.total_return * 100,
                }))}
              >
                <CartesianGrid strokeDasharray="3 3" />
                <XAxis dataKey="symbol" />
                <YAxis />
                <Tooltip formatter={(value: number) => `${value.toFixed(2)}%`} />
                <Legend />
                <Bar dataKey="return" fill="#0ea5e9" name="Total Return %" />
              </BarChart>
            </ResponsiveContainer>
          </div>

          {/* Volatility Comparison */}
          <div className="card">
            <h3 className="text-lg font-semibold text-gray-900 mb-4">
              Risk Profile (Annual Volatility)
            </h3>
            <ResponsiveContainer width="100%" height={300}>
              <BarChart
                data={mutation.data.map((asset) => ({
                  symbol: asset.symbol,
                  volatility: asset.returns_summary.volatility_annual * 100,
                }))}
              >
                <CartesianGrid strokeDasharray="3 3" />
                <XAxis dataKey="symbol" />
                <YAxis />
                <Tooltip formatter={(value: number) => `${value.toFixed(2)}%`} />
                <Legend />
                <Bar dataKey="volatility" fill="#f59e0b" name="Volatility %" />
              </BarChart>
            </ResponsiveContainer>
          </div>

          {/* Correlation Matrix */}
          {mutation.data.length > 1 && mutation.data[0].correlations && (
            <div className="card">
              <h3 className="text-lg font-semibold text-gray-900 mb-4">
                Correlation Matrix
              </h3>
              <div className="overflow-x-auto">
                <table className="min-w-full divide-y divide-gray-200">
                  <thead className="bg-gray-50">
                    <tr>
                      <th className="px-4 py-2 text-left text-xs font-medium text-gray-500 uppercase">
                        Asset
                      </th>
                      {selectedAssets.map((symbol) => (
                        <th
                          key={symbol}
                          className="px-4 py-2 text-center text-xs font-medium text-gray-500 uppercase"
                        >
                          {symbol}
                        </th>
                      ))}
                    </tr>
                  </thead>
                  <tbody className="bg-white divide-y divide-gray-200">
                    {mutation.data.map((asset) => (
                      <tr key={asset.symbol}>
                        <td className="px-4 py-2 whitespace-nowrap text-sm font-medium text-gray-900">
                          {asset.symbol}
                        </td>
                        {selectedAssets.map((symbol) => {
                          const corr =
                            symbol === asset.symbol
                              ? 1
                              : asset.correlations?.[symbol] || 0

                          return (
                            <td
                              key={symbol}
                              className="px-4 py-2 whitespace-nowrap text-center text-sm"
                            >
                              <span
                                className={`inline-block px-2 py-1 rounded ${
                                  corr > 0.7
                                    ? 'bg-green-100 text-green-800'
                                    : corr > 0.3
                                    ? 'bg-yellow-100 text-yellow-800'
                                    : corr > -0.3
                                    ? 'bg-gray-100 text-gray-800'
                                    : 'bg-red-100 text-red-800'
                                }`}
                              >
                                {corr.toFixed(2)}
                              </span>
                            </td>
                          )
                        })}
                      </tr>
                    ))}
                  </tbody>
                </table>
              </div>
            </div>
          )}
        </div>
      )}
    </div>
  )
}
