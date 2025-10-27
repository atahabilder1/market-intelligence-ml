import { useState, useEffect } from 'react'
import { useQuery } from '@tanstack/react-query'
import { getAssetCategories } from '../services/api'
import { X } from 'lucide-react'

interface AssetSelectorProps {
  selectedAssets: string[]
  onChange: (assets: string[]) => void
  maxSelections?: number
}

export default function AssetSelector({
  selectedAssets,
  onChange,
  maxSelections = 10,
}: AssetSelectorProps) {
  const [searchTerm, setSearchTerm] = useState('')

  const { data: categories, isLoading } = useQuery({
    queryKey: ['asset-categories'],
    queryFn: getAssetCategories,
  })

  const handleToggle = (symbol: string) => {
    if (selectedAssets.includes(symbol)) {
      onChange(selectedAssets.filter((s) => s !== symbol))
    } else if (selectedAssets.length < maxSelections) {
      onChange([...selectedAssets, symbol])
    }
  }

  const handleRemove = (symbol: string) => {
    onChange(selectedAssets.filter((s) => s !== symbol))
  }

  if (isLoading) return <div>Loading assets...</div>

  // Flatten all symbols
  const allSymbols = categories
    ? Object.values(categories).flat()
    : []

  const filteredSymbols = allSymbols.filter((symbol) =>
    symbol.toLowerCase().includes(searchTerm.toLowerCase())
  )

  return (
    <div className="space-y-4">
      {/* Selected Assets */}
      {selectedAssets.length > 0 && (
        <div className="flex flex-wrap gap-2">
          {selectedAssets.map((symbol) => (
            <span
              key={symbol}
              className="inline-flex items-center gap-1 bg-primary-100 text-primary-800 px-3 py-1 rounded-full text-sm"
            >
              {symbol}
              <button
                onClick={() => handleRemove(symbol)}
                className="hover:text-primary-900"
              >
                <X className="w-4 h-4" />
              </button>
            </span>
          ))}
        </div>
      )}

      {/* Search */}
      <input
        type="text"
        placeholder="Search assets..."
        value={searchTerm}
        onChange={(e) => setSearchTerm(e.target.value)}
        className="input w-full"
      />

      {/* Asset Grid */}
      <div className="grid grid-cols-2 md:grid-cols-4 gap-2 max-h-64 overflow-y-auto border border-gray-200 rounded-lg p-3">
        {filteredSymbols.map((symbol) => (
          <button
            key={symbol}
            onClick={() => handleToggle(symbol)}
            disabled={
              !selectedAssets.includes(symbol) &&
              selectedAssets.length >= maxSelections
            }
            className={`px-3 py-2 rounded-md text-sm font-medium transition-colors ${
              selectedAssets.includes(symbol)
                ? 'bg-primary-600 text-white'
                : 'bg-gray-100 text-gray-700 hover:bg-gray-200 disabled:opacity-50 disabled:cursor-not-allowed'
            }`}
          >
            {symbol}
          </button>
        ))}
      </div>

      <p className="text-sm text-gray-500">
        Selected: {selectedAssets.length} / {maxSelections}
      </p>
    </div>
  )
}
