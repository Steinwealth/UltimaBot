import React from 'react';
import useTradePanels from '@/hooks/useTradePanels';
import TradeStatusCard from '@/components/TradeStatusCard';
import { Button } from '@/components/ui/button';
import { useTheme } from '@/components/ThemeProvider';

export default function TradePanel() {
  const { panelState, openTrades, tradeHistory, flipPanel } = useTradePanels();
  const { theme } = useTheme();

  const trades = panelState === 'open' ? openTrades : tradeHistory;

  return (
    <div className="p-4 rounded-xl shadow-md bg-neutral-800 dark:bg-neutral-900 text-white">
      <div className="flex justify-between items-center mb-4">
        <h2 className="text-lg font-bold tracking-wide">
          {panelState === 'open' ? 'Open Positions' : 'Trade History'}
        </h2>
        <Button onClick={flipPanel} className="text-xs px-3 py-1">
          Flip to {panelState === 'open' ? 'History' : 'Open'}
        </Button>
      </div>

      <div className="space-y-3 max-h-[380px] overflow-y-auto pr-1">
        {trades.length === 0 ? (
          <div className="text-neutral-400 text-sm italic">
            {panelState === 'open' ? 'No open trades.' : 'No trade history yet.'}
          </div>
        ) : (
          trades.map((trade) => (
            <TradeStatusCard
              key={trade.id}
              symbol={trade.symbol}
              model={trade.model}
              confidence={trade.confidence}
              tp={trade.tp}
              sl={trade.sl}
              status={trade.status}
              gain={trade.gain}
              isClosed={panelState === 'history'}
              theme={theme}
            />
          ))
        )}
      </div>
    </div>
  );
}
