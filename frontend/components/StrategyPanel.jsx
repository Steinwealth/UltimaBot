import React from 'react';
import clsx from 'clsx';

export default function StrategyPanel({ model }) {
  if (!model) {
    return (
      <div className="p-4 rounded-xl bg-neutral-900 text-white shadow-inner">
        <p className="text-sm text-neutral-400 italic">
          No model selected. Select and pair a model to view strategy details.
        </p>
      </div>
    );
  }

  return (
    <div className="p-4 rounded-xl bg-neutral-900 text-white shadow-inner">
      <h2 className="text-lg font-bold mb-2">{model.name} Strategy</h2>

      <div className="text-sm space-y-2">
        <div>
          <span className="font-semibold text-gray-300">Type:</span>{' '}
          <span className="text-blue-300">{model.type}</span>
        </div>

        <div>
          <span className="font-semibold text-gray-300">Confidence Threshold:</span>{' '}
          <span className={clsx(
            'font-mono',
            model.confidenceThreshold > 0.95 ? 'text-green-400' : 'text-yellow-300'
          )}>
            {(model.confidenceThreshold * 100).toFixed(1)}%
          </span>
        </div>

        <div>
          <span className="font-semibold text-gray-300">Risk Mode:</span>{' '}
          {model.riskMode}
        </div>

        <div>
          <span className="font-semibold text-gray-300">TP Logic:</span>{' '}
          <span className="text-teal-400">{model.tpLogic}</span>
        </div>

        <div>
          <span className="font-semibold text-gray-300">SL Logic:</span>{' '}
          <span className="text-red-400">{model.slLogic}</span>
        </div>

        <div>
          <span className="font-semibold text-gray-300">Scaling:</span>{' '}
          {model.streakScaling ? 'Streak-based scaling enabled' : 'Fixed sizing'}
        </div>

        <div>
          <span className="font-semibold text-gray-300">Multi-Model Entry:</span>{' '}
          {model.multiEntry ? 'Yes' : 'No'}
        </div>

        <div>
          <span className="font-semibold text-gray-300">Compounding:</span>{' '}
          {model.compounding ? 'Enabled' : 'Disabled'}
        </div>
      </div>
    </div>
  );
}
