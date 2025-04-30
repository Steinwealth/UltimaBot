import React from 'react';
import { Card } from '@/components/ui/card';

const MarketSentiment = ({ sentimentData }) => {
  return (
    <Card className="p-4 rounded-2xl shadow-soft">
      <h2 className="text-xl font-semibold mb-4">Market Sentiment</h2>
      {Array.isArray(sentimentData) && sentimentData.length > 0 ? (
        <div className="grid grid-cols-2 gap-4">
          {sentimentData.map((item) => (
            <div key={item.symbol} className="flex flex-col items-center p-2 border rounded-lg">
              <span className="text-lg font-medium">{item.symbol}</span>
              <span className={`text-sm font-bold ${item.sentiment === 'Bullish' ? 'text-green-600' : 'text-red-600'}`}>{item.sentiment}</span>
              <span className="text-xs text-gray-500">Volume: {item.volume}</span>
            </div>
          ))}
        </div>
      ) : (
        <div className="text-center text-gray-500">No sentiment data available</div>
      )}
    </Card>
  );
};

export default MarketSentiment;
