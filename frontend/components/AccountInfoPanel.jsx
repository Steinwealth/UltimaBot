import React from 'react';
import clsx from 'clsx';

export default function AccountInfoPanel({
  broker,
  onStartTrading,
  onDisconnect,
  onPairModel,
}) {
  const { id, name, account, pairedModel, isTrading } = broker;

  const isReady = !!pairedModel;
  const isActive = isTrading;

  return (
    <div className="p-4 rounded-xl shadow-md bg-neutral-900 text-white border border-neutral-700">
      <div className="flex justify-between items-center mb-2">
        <h3 className="text-lg font-semibold">{name}</h3>
        <span className="text-xs text-gray-400 font-mono">ID: {id}</span>
      </div>

      <div className="grid grid-cols-2 gap-4 text-sm mb-3">
        <div>
          <span className="text-gray-400">Balance:</span>
          <div className="font-bold text-green-400">${account.balance.toLocaleString()}</div>
        </div>
        <div>
          <span className="text-gray-400">Margin:</span>
          <div className="font-bold text-yellow-300">{account.margin.toFixed(1)}%</div>
        </div>
        <div>
          <span className="text-gray-400">Paired Model:</span>
          <div className="font-semibold text-blue-300">
            {pairedModel?.name || 'None'}
          </div>
        </div>
        <div className="flex items-center gap-2">
          <div className={clsx(
            'w-3 h-3 rounded-full shadow',
            isActive ? 'bg-green-400 animate-pulse' : 'bg-gray-400'
          )} />
          <span className="text-xs">{isActive ? 'Active Trading' : 'Idle'}</span>
        </div>
      </div>

      <div className="flex gap-2">
        <button
          onClick={onPairModel}
          className="bg-blue-500 hover:bg-blue-600 text-white text-xs px-3 py-1 rounded"
        >
          🔁 Trade Model
        </button>

        <button
          onClick={() => isActive ? onDisconnect(id) : onStartTrading(broker)}
          disabled={!isReady}
          className={clsx(
            'text-xs font-semibold px-4 py-2 rounded shadow transition-all duration-300',
            !isReady && 'bg-gray-500 cursor-not-allowed',
            isActive && 'bg-red-600 hover:bg-red-700',
            isReady && !isActive && 'bg-lightsteelblue hover:brightness-105 animate-pulse'
          )}
        >
          {isActive ? '🔌 Disconnect' : '🚀 Start Trading'}
        </button>
      </div>

      {account.balance < 25000 ? (
        <div className="mt-2 text-xs text-yellow-400 font-semibold">
          ⚠️ Under $25K – PDT limit active (5 stock trades/week)
        </div>
      ) : (
        <div className="mt-2 text-xs text-green-400 font-semibold">
          ✅ PRO MODE – Unlimited Stock Trading Enabled
        </div>
      )}
    </div>
  );
}
