import { useQuery } from '@tanstack/react-query'
import { getAssets } from '../services/api'
import { TrendingUp, BarChart3, Activity, AlertCircle } from 'lucide-react'
import { Link } from 'react-router-dom'

export default function Dashboard() {
  const { data: assetsData, isLoading } = useQuery({
    queryKey: ['assets'],
    queryFn: getAssets,
  })

  const features = [
    {
      icon: TrendingUp,
      title: 'Price Predictions',
      description: 'ML-powered return forecasts with confidence scores',
      link: '/predictions',
      color: 'bg-blue-500',
    },
    {
      icon: BarChart3,
      title: 'Backtesting',
      description: 'Test strategies with realistic transaction costs',
      link: '/backtest',
      color: 'bg-green-500',
    },
    {
      icon: Activity,
      title: 'Asset Analysis',
      description: 'Technical indicators and correlation analysis',
      link: '/analysis',
      color: 'bg-purple-500',
    },
  ]

  return (
    <div className="space-y-8">
      {/* Hero Section */}
      <div className="bg-gradient-to-r from-primary-600 to-primary-800 rounded-lg shadow-lg p-8 text-white">
        <h2 className="text-3xl font-bold mb-2">
          Welcome to Market Intelligence ML
        </h2>
        <p className="text-primary-100 text-lg">
          Multi-asset predictive modeling for equities, fixed income & digital
          assets
        </p>
      </div>

      {/* Stats */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
        <div className="card">
          <div className="flex items-center justify-between">
            <div>
              <p className="text-gray-500 text-sm font-medium">
                Available Assets
              </p>
              <p className="text-3xl font-bold text-gray-900 mt-1">
                {isLoading ? '...' : assetsData?.total || 0}
              </p>
            </div>
            <div className="bg-blue-100 p-3 rounded-full">
              <BarChart3 className="w-8 h-8 text-blue-600" />
            </div>
          </div>
        </div>

        <div className="card">
          <div className="flex items-center justify-between">
            <div>
              <p className="text-gray-500 text-sm font-medium">
                ML Models
              </p>
              <p className="text-3xl font-bold text-gray-900 mt-1">5</p>
            </div>
            <div className="bg-green-100 p-3 rounded-full">
              <Activity className="w-8 h-8 text-green-600" />
            </div>
          </div>
        </div>

        <div className="card">
          <div className="flex items-center justify-between">
            <div>
              <p className="text-gray-500 text-sm font-medium">
                Features Engineered
              </p>
              <p className="text-3xl font-bold text-gray-900 mt-1">80+</p>
            </div>
            <div className="bg-purple-100 p-3 rounded-full">
              <TrendingUp className="w-8 h-8 text-purple-600" />
            </div>
          </div>
        </div>
      </div>

      {/* Features Grid */}
      <div>
        <h3 className="text-xl font-bold text-gray-900 mb-4">
          What You Can Do
        </h3>
        <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
          {features.map((feature) => {
            const Icon = feature.icon
            return (
              <Link
                key={feature.title}
                to={feature.link}
                className="card hover:shadow-lg transition-shadow cursor-pointer group"
              >
                <div
                  className={`${feature.color} w-12 h-12 rounded-lg flex items-center justify-center mb-4 group-hover:scale-110 transition-transform`}
                >
                  <Icon className="w-6 h-6 text-white" />
                </div>
                <h4 className="text-lg font-bold text-gray-900 mb-2">
                  {feature.title}
                </h4>
                <p className="text-gray-600">{feature.description}</p>
              </Link>
            )
          })}
        </div>
      </div>

      {/* Getting Started */}
      <div className="card bg-blue-50 border border-blue-200">
        <div className="flex items-start space-x-3">
          <AlertCircle className="w-6 h-6 text-blue-600 mt-0.5" />
          <div>
            <h4 className="font-bold text-blue-900 mb-2">
              Getting Started
            </h4>
            <ul className="text-blue-800 space-y-1 text-sm">
              <li>• Select assets from equities, crypto, bonds, or commodities</li>
              <li>• Choose an ML model (XGBoost recommended for best results)</li>
              <li>• Get predictions with confidence scores and trading signals</li>
              <li>• Backtest your strategy to see historical performance</li>
            </ul>
          </div>
        </div>
      </div>
    </div>
  )
}
