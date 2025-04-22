import React from 'react';
import clsx from 'clsx';

export default function TradeStatusCard({
  symbol,
  model,
  confidence,
  tp,
  sl,
  status,
  gain,
  isClosed = false,
  theme = 'dark'
}) {
  const confidenceColor =
    confidence > 0.98
      ? 'text-green-400'
      : confidence > 0.95
      ? 'text-yellow-400'
      : 'text-red-400';

  const gainColor =
    gain > 0
      ? 'text-green-500'
      : gain < 0
      ? 'text-red-500'
      : 'text-neutral-400';

  const statusColor = isClosed ? 'border-neutral-500' : 'border-blue-500';

  return (
    <div
      className={clsx(
        'rounded-2xl shadow-md border px-4 py-2 mb-3 transition-all',
        statusColor,
        theme === 'dark' ? 'bg-neutral-900 text-white' : 'bg-white text-black'
      )}
    >
      <div className="flex justify-between items-center mb-1">
        <div className="text-lg font-bold">{symbol}</div>
        <div
          className={clsx(
            'px-2 py-0.5 rounded-full text-xs font-semibold',
            isClosed ? 'bg-neutral-600' : 'bg-blue-600',
            'text-white'
          )}
        >
          {isClosed ? 'Closed' : 'Open'}
        </div>
      </div>

      <div className="text-sm mb-1">
        <span className="font-medium">Model:</span> {model}
      </div>
      <div className="text-sm mb-1">
        <span className="font-medium">Confidence:</span>{' '}
        <span className={confidenceColor}>{(confidence * 100).toFixed(2)}%</span>
      </div>
      <div className="text-sm mb-1">
        <span className="font-medium">TP:</span> {tp} | <span className="font-medium">SL:</span> {sl}
      </div>
      <div className="text-sm">
        <span className="font-medium">Gain/Loss:</span>{' '}
        <span className={gainColor}>{gain.toFixed(2)}%</span>
      </div>
    </div>
  );
}
