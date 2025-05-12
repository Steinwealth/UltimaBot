import React, { useEffect, useState } from 'react';
import { Card } from "@/window/components/ui/card";

const TradeHistory = () => {
  const [history, setHistory] = useState([]);

  useEffect(() => {
    const socket = new WebSocket('wss://trade-history-feed');
    socket.onmessage = (event) => {
      const trade = JSON.parse(event.data);
      setHistory((prevHistory) => [trade, ...prevHistory.slice(0, 19)]); // Keep last 20 trades
    };
    return () => socket.close();
  }, []);

  return (
    <div className="grid grid-cols-1 gap-4">
      {Array.isArray(history) && history.length > 0 ? (
        history.map((trade) => (
          <Card key={trade.trade_id} className="p-4 bg-gray-100 rounded-2xl shadow-soft dark:bg-gray-800">
            <div className="flex justify-between">
              <div>
                <div className="text-lg font-semibold text-gray-900 dark:text-white">{trade.symbol}</div>
                <div className="text-sm text-gray-600 dark:text-gray-400">Entry: {trade.entry_price}</div>
                <div className="text-sm text-gray-600 dark:text-gray-400">Exit: {trade.exit_price}</div>
                <div className="text-sm text-gray-600 dark:text-gray-400">Reason: {trade.exit_reason}</div>
              </div>
              <div className="text-right">
                <div className="text-sm font-medium text-gray-800 dark:text-gray-200">Confidence: {trade.confidence}</div>
                <div className={`text-sm font-bold ${trade.pnl >= 0 ? 'text-green-500' : 'text-red-500'}`}>PnL: {trade.pnl}%</div>
              </div>
            </div>
          </Card>
        ))
      ) : (
        <div className="text-center text-gray-600 dark:text-gray-400">No trade history</div>
      )}
    </div>
  );
};

export default TradeHistory;
