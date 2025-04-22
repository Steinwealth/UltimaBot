import React from 'react';
import { Button } from '@/components/ui/button';
import clsx from 'clsx';

export default function AccountInfoPanel({
  broker,
  account,
  pairedModel,
  onStartTrading,
  onPairModel,
}) {
  const isPro = account?.balance > 25000;

  return (
    <div
      className={clsx(
        'p-4 rounded-xl shadow-md flex flex-col gap-2',
        'bg-neutral-900 text-white border border-neutral-700'
      )}
    >
      <div className="flex justify-between items-center">
        <h3 className="text-lg font-semibold">{broker.name}</h3>
        <span className="text-xs font-mono text-gray-400">ID: {broker.id}</span>
      </div>

      <div className="grid grid-cols-2 gap-4 text-sm">
        <div>
          <span className="text-gray-400">Balance:</span>
          <div className="font-bold text-green-400">${account.balance.toLocaleString()}</div>
        </div>
        <div>
          <span className="text-gray-400">Margin:</span>
          <div
            className={clsx(
              'font-bold',
              account.margin > 70 ? 'text-green-300' : 'text-yellow-300'
            )}
          >
            {account.margin.toFixed(1)}%
          </div>
        </div>
        <div>
          <span className="text-gray-400">Paired Model:</span>
          <div className="font-semibold text-blue-300">
            {pairedModel?.name || 'None'}
          </div>
        </div>
        <div>
          <span className="text-gray-400">Risk Mode:</span>
          <div className="font-semibold">{pairedModel?.riskMode || '--'}</div>
        </div>
      </div>

      <div className="flex gap-2 mt-3">
        <Button onClick={onPairModel}>Trade Model</Button>
        <Button onClick={onStartTrading} className="bg-lightsteelblue hover:bg-blue-400">
          Start Trading
        </Button>
      </div>

      {isPro && (
        <div className="mt-2 text-xs text-green-400 font-semibold">
          ✅ PRO MODE – Unlimited Stock Trading Enabled
        </div>
      )}

      {!isPro && (
        <div className="mt-2 text-xs text-yellow-400 font-semibold">
          ⚠️ Under $25K – Limited to 5 stock trades/week (PDT Rule)
        </div>
      )}
    </div>
  );
}
