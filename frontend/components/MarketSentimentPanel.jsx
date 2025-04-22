import React, { useState, useEffect } from 'react';
import clsx from 'clsx';

export default function MarketSentimentPanel() {
  const [predictions, setPredictions] = useState([]);
  const [expanded, setExpanded] = useState(false);

  useEffect(() => {
    // Simulate live prediction fetch
    setPredictions([
      { symbol: 'GLD', direction: 'up', move: '+1.2%' },
      { symbol: 'SPY', direction: 'down', move: '-0.4%' },
      { symbol: 'QQQ', direction: 'up', move: '+0.9%' },
      { symbol: 'DXY', direction: 'down', move: '-0.6%' },
      { symbol: 'AAPL', direction: 'up', move: '+2.3%' }, // Top Cap
      { symbol: 'TSLA', direction: 'down', move: '-1.1%' } // Top Volume
    ]);
  }, []);

  const renderItem = (p) => (
    <div
      key={p.symbol}
      className={clsx(
        'flex justify-between items-center px-3 py-2 rounded-lg text-sm font-medium',
        p.direction === 'up'
          ? 'bg-green-900 text-green-300'
          : 'bg-red-900 text-red-300'
      )}
    >
      <div>{p.symbol}</div>
      <div className="font-mono">{p.move}</div>
    </div>
  );

  return (
    <div className="p-4 bg-neutral-900 rounded-xl shadow-md text-white">
      <div className="flex justify-between items-center mb-2">
        <h2 className="text-lg font-bold">Market Sentiment</h2>
        <button
          onClick={() => setExpanded(!expanded)}
          className="text-xs text-blue-400 hover:underline"
        >
          {expanded ? 'Show Less' : 'See More Predictions'}
        </button>
      </div>

      <div className="grid grid-cols-2 gap-2">
        {(expanded ? predictions : predictions.slice(0, 3)).map(renderItem)}
      </div>
    </div>
  );
}
