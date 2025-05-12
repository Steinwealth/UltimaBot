import React from 'react';
import { Card, CardContent } from "@/window/components/ui/card";
import { TrendingUp, TrendingDown } from 'lucide-react';

const MarketSentiment = ({ sentimentData }) => {
  return (
    <Card className="p-4 rounded-2xl shadow-lg bg-white dark:bg-gray-900">
      <CardContent>
        <h2 className="text-xl font-semibold mb-4 text-gray-900 dark:text-white">Market Sentiment</h2>

        {Array.isArray(sentimentData) && sentimentData.length > 0 ? (
          <div className="grid grid-cols-2 sm:grid-cols-3 gap-4">
            {sentimentData.map((item, index) => {
              const isBullish = item.sentiment?.toLowerCase() === 'bullish';
              return (
                <div
                  key={item.symbol || index}
                  className={`flex flex-col items-center justify-center p-3 rounded-xl border-2 shadow-md transition-all
                    ${isBullish ? 'border-green-500 bg-green-50 dark:bg-green-950' : 'border-red-500 bg-red-50 dark:bg-red-950'}`}
                >
                  <span className="text-lg font-semibold text-gray-900 dark:text-white">{item.symbol}</span>
                  <span className={`flex items-center gap-1 font-bold ${isBullish ? 'text-green-600' : 'text-red-500'}`}>
                    {isBullish ? <TrendingUp size={16} /> : <TrendingDown size={16} />}
                    {item.sentiment}
                  </span>
                  <span className="text-xs text-gray-600 dark:text-gray-300">Vol: {formatVolume(item.volume)}</span>
                </div>
              );
            })}
          </div>
        ) : (
          <div className="text-center text-gray-500 dark:text-gray-400 py-6">
            No sentiment data available
          </div>
        )}
      </CardContent>
    </Card>
  );
};

// Helper to format large numbers like 3200000000 => 3.2B
const formatVolume = (val) => {
  const num = typeof val === 'number' ? val : parseFloat(val);
  if (isNaN(num)) return '--';
  if (num >= 1e9) return `${(num / 1e9).toFixed(1)}B`;
  if (num >= 1e6) return `${(num / 1e6).toFixed(1)}M`;
  return num.toLocaleString();
};

export default MarketSentiment;
