import React, { useEffect, useState } from 'react';
import { Card } from '@/components/ui/card';

const OpenTrades = () => {
  const [trades, setTrades] = useState([]);

  useEffect(() => {
    const socket = new WebSocket('wss://trade-updates-feed');
    socket.onmessage = (event) => {
      const tradeUpdate = JSON.parse(event.data);
      setTrades((prevTrades) => {
        const existing = prevTrades.find((t) => t.trade_id === tradeUpdate.trade_id);
        if (existing) {
          return prevTrades.map((t) => (t.trade_id === tradeUpdate.trade_id ? tradeUpdate : t));
        } else {
          return [...prevTrades, tradeUpdate];
        }
      });
    };
    return () => socket.close();
  }, []);

  return (
    <div className="grid grid-cols-1 gap-4">
      {Array.isArray(trades) && trades.length > 0 ? (
        trades.map((trade) => (
          <Card key={trade.trade_id} className="p-4 bg-gray-100 rounded-2xl shadow-soft dark:bg-gray-800">
            <div className="flex justify-between">
              <div>
                <div className="text-lg font-semibold text-gray-900 dark:text-white">{trade.symbol}</div>
                <div className="text-sm text-gray-600 dark:text-gray-400">Entry: {trade.entry_price}</div>
                <div className="text-sm text-gray-600 dark:text-gray-400">TP: {trade.take_profit}</div>
                <div className="text-sm text-gray-600 dark:text-gray-400">SL: {trade.stop_loss}</div>
              </div>
              <div className="text-right">
                <div className="text-sm font-medium text-gray-800 dark:text-gray-200">Confidence: {trade.confidence}</div>
                <div className={`text-sm font-bold ${trade.pnl >= 0 ? 'text-green-500' : 'text-red-500'}`}>PnL: {trade.pnl}%</div>
              </div>
            </div>
          </Card>
        ))
      ) : (
        <div className="text-center text-gray-600 dark:text-gray-400">No open trades</div>
      )}
    </div>
  );
};

export default OpenTrades;
