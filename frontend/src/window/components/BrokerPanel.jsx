// BrokerPanel.jsx

import React, { useEffect, useState } from 'react';
import { Button } from '@/window/components/ui/button';
import { useTheme } from '@/hooks/useTheme';

const BrokerPanel = ({
  broker,
  models,
  pairedModel,
  setPairedModel,
  isTradingActive,
  setIsTradingActive,
  autoPair = true
}) => {
  const { theme } = useTheme();
  const isDark = theme === 'dark';

  const [defaultModel, setDefaultModel] = useState(pairedModel);

  useEffect(() => {
    if (autoPair && !pairedModel) {
      const brokerName = broker.name.toLowerCase();
      const model = brokerName.includes('coin') || brokerName.includes('wallet') || brokerName.includes('kraken') || brokerName.includes('binance')
        ? 'Antimatter'
        : 'Dianastone';
      setDefaultModel(model);
      setPairedModel(model);
    }
  }, [broker.name, pairedModel, setPairedModel, autoPair]);

  return (
    <div className={`p-4 rounded-xl shadow-md border transition-all duration-300 hover:shadow-lg ${isDark ? 'bg-gray-900 border-gray-700' : 'bg-white border-blue-200'}`}>
      <div className="flex items-start justify-between">
        <div className="flex flex-col gap-2">
          <div className="text-lg font-bold leading-tight">{broker.name}</div>
          <div className="text-xs opacity-70">ID: {broker.account_id}</div>
          <div className="text-lg font-semibold">
            Balance: <span className="text-green-400">${broker.balance}</span> | 
            Margin: <span className="text-blue-400">{broker.margin}%</span>
          </div>
          <div className="text-sm mt-1 font-medium text-yellow-500">
            Model: {pairedModel || defaultModel}
          </div>
        </div>

        <div className="flex flex-col items-end gap-2">
          <Button
            onClick={() => setIsTradingActive(true)}
            className="text-xs text-white bg-green-500 hover:bg-green-400"
          >
            Start Trading
          </Button>

          {isTradingActive && (
            <div className="text-xs font-bold text-green-400">🟢 Trading Active</div>
          )}
        </div>
      </div>
    </div>
  );
};

export default BrokerPanel;
