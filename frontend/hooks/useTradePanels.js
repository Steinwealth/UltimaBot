import { useEffect, useState } from 'react';
import { io } from 'socket.io-client';

const socket = io('http://localhost:8000'); // Update this to your backend endpoint if needed

export default function useTradePanels() {
  const [openTrades, setOpenTrades] = useState([]);
  const [tradeHistory, setTradeHistory] = useState([]);
  const [panelState, setPanelState] = useState('open'); // 'open' | 'history'

  useEffect(() => {
    // Listen for live open trades
    socket.on('update_open_trades', (data) => {
      setOpenTrades(data);
    });

    // Listen for trade closures (move to history)
    socket.on('trade_closed', (closedTrade) => {
      setOpenTrades((prev) => prev.filter((t) => t.id !== closedTrade.id));
      setTradeHistory((prev) => [closedTrade, ...prev.slice(0, 49)]); // Keep 50 recent
    });

    // Initial load from backend
    socket.emit('request_trade_data');

    return () => {
      socket.off('update_open_trades');
      socket.off('trade_closed');
    };
  }, []);

  const flipPanel = () => {
    setPanelState((prev) => (prev === 'open' ? 'history' : 'open'));
  };

  return {
    panelState,
    openTrades,
    tradeHistory,
    flipPanel,
  };
}
