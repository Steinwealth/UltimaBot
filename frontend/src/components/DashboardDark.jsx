import React, { useState, useEffect } from 'react';
import { Button } from '@/components/ui/button';
import SettingsOverlay from './SettingsOverlay';
import StrategyPanel from './StrategyPanel';
import OpenTrades from './OpenTrades';
import TradeHistory from './TradeHistory';
import MarketSentiment from './MarketSentiment';
import MarqueeBar from './MarqueeBar';
import ChartsPanel from './ChartsPanel';
import { motion } from 'framer-motion';

const DashboardDark = () => {
  const [showSettings, setShowSettings] = useState(false);
  const [showHistory, setShowHistory] = useState(false);
  const [brokerData, setBrokerData] = useState({ broker: '', accountId: '', balance: 0, margin: 0 });

  useEffect(() => {
    const socket = new WebSocket('wss://broker-data-feed');
    socket.onmessage = (event) => setBrokerData(JSON.parse(event.data));
    return () => socket.close();
  }, []);

  return (
    <motion.div
      initial={{ opacity: 0, y: 30 }}
      animate={{ opacity: 1, y: 0 }}
      exit={{ opacity: 0, y: -30 }}
      transition={{ duration: 0.6, ease: "easeInOut" }}
      className="flex flex-col h-screen text-white bg-gray-900"
    >
      {/* Header */}
      <header className="flex items-center justify-between p-4 border-b border-gray-700">
        <h1 className="text-2xl font-bold text-green-400">Ultima Bot Dashboard (Xbox)</h1>
        <Button variant="outline" className="text-gray-300 border-gray-500" onClick={() => setShowSettings(true)}>Settings</Button>
      </header>

      {/* Main content */}
      <main className="flex-grow p-6 space-y-6 overflow-y-auto">
        {/* Account Information */}
        <div className="p-4 bg-gray-800 border border-gray-700 rounded-lg">
          <div className="flex items-center justify-between">
            <div>
              <div className="font-semibold text-white">Broker: {brokerData.broker || 'Loading...'}</div>
              <div className="text-sm text-gray-400">Account ID: {brokerData.accountId || '---'}</div>
              <div className="text-sm text-gray-400">Balance: ${brokerData.balance.toLocaleString()} | Margin: {brokerData.margin}%</div>
            </div>
            <div className="flex gap-2">
              <select className="px-2 py-1 text-white bg-gray-900 border border-gray-600 rounded">
                <option>Hexacoin</option>
                <option>Antimatter</option>
              </select>
              <Button className="px-4 text-gray-300 border-gray-500">Trade Model</Button>
              <Button className="px-4 text-white bg-green-600 hover:bg-green-500">Start Trading</Button>
            </div>
          </div>
        </div>

        {/* Charts Panel */}
        <ChartsPanel />

        {/* Strategy Panel */}
        <StrategyPanel />

        {/* Open Trades / Trade History Toggle */}
        <div className="p-4 bg-gray-800 border border-gray-700 rounded-lg">
          <div className="flex items-center justify-between mb-2">
            <h2 className="text-xl font-semibold text-white">{showHistory ? 'Trade History' : 'Open Trades'}</h2>
            <button
              onClick={() => setShowHistory(!showHistory)}
              className="px-3 py-1 text-sm text-green-400 border border-green-400 rounded hover:bg-gray-700"
            >
              {showHistory ? 'View Open Trades' : 'View Trade History'}
            </button>
          </div>
          {showHistory ? <TradeHistory /> : <OpenTrades />}
        </div>

        {/* Market Sentiment */}
        <MarketSentiment />
      </main>

      {/* Marquee Bar */}
      <footer>
        <MarqueeBar />
      </footer>

      {/* Settings Overlay */}
      {showSettings && <SettingsOverlay onClose={() => setShowSettings(false)} />}
    </motion.div>
  );
};

export default DashboardDark;
