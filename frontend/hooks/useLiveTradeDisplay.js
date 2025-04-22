import { useEffect, useState } from 'react';
import { io } from 'socket.io-client';

const socket = io('http://localhost:8000'); // Update with actual backend URL if needed

export default function useLiveTradeDisplay() {
  const [openTrades, setOpenTrades] = useState([]);
  const [closedTrades, setClosedTrades] = useState([]);
  const [panelView, setPanelView] = useState('open'); // or 'history'

  useEffect(() => {
    // On socket init, request current state
    socket.emit('request_trade_data');

    // Listen for new or updated open trades
    socket.on('open_trades_update', (data) => {
      setOpenTrades(data);
    });

    // Listen for trade closure
    socket.on('trade_closed', (closed) => {
      setOpenTrades((prev) => prev.filter((t) => t.id !== closed.id));
      setClosedTrades((prev) => [closed, ...prev.slice(0, 49)]); // max 50 history
    });

    return () => {
      socket.off('open_trades_update');
      socket.off('trade_closed');
    };
  }, []);

  const flipPanel = () => {
    setPanelView((prev) => (prev === 'open' ? 'history' : 'open'));
  };

  return {
    openTrades,
    closedTrades,
    panelView,
    flipPanel,
    trades: panelView === 'open' ? openTrades : closedTrades,
  };
}
