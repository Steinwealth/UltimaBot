// Updated Dashboard.jsx with responsive 1v1, 2v1, 2v2 Broker Layout using <BrokerPanel />

import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { useTheme } from '@/hooks/useTheme';
import { Button } from '@/window/components/ui/button';
import BrokerLoginOverlay from '@/window/components/BrokerLoginOverlay';
import SettingsOverlay from '@/window/components/SettingsOverlay';
import UploadModelOverlay from '@/window/components/UploadModelOverlay';
import StrategyPanel from '@/window/components/StrategyPanel';
import OpenTrades from '@/window/components/OpenTrades';
import TradeHistory from '@/window/components/TradeHistory';
import MarketSentiment from '@/window/components/MarketSentiment';
import BrokerPanel from '@/window/components/BrokerPanel';
import { motion, AnimatePresence } from 'framer-motion';

const Dashboard = () => {
  const navigate = useNavigate();
  const { theme, toggleTheme } = useTheme();
  const isDark = theme === 'dark';

  const [brokers, setBrokers] = useState([]);
  const [models, setModels] = useState([]);
  const [model, setModel] = useState('');
  const [pairedModel, setPairedModel] = useState('');
  const [isTradingActive, setIsTradingActive] = useState(false);
  const [showOverlay, setShowOverlay] = useState(false);
  const [showSettings, setShowSettings] = useState(false);
  const [showUploadModal, setShowUploadModal] = useState(false);
  const [showTradeHistory, setShowTradeHistory] = useState(false);
  const [confidenceThreshold, setConfidenceThreshold] = useState(0.95);
  const [tpForecast, setTpForecast] = useState(12.3);
  const [slForecast, setSlForecast] = useState(3.4);

  useEffect(() => {
    const isAuthenticated = document.cookie.includes('ultimabot-auth=1');
    if (!isAuthenticated) navigate('/');
    fetch("/api/models").then(res => res.json()).then(setModels);
  }, [navigate]);

  const sortedModels = [...models].sort((a, b) => b.performance - a.performance);

  const textColor = isDark ? 'text-green-300' : 'text-blue-600';
  const bgColor = isDark ? 'bg-gradient-to-br from-gray-900 via-gray-800 to-black' : 'bg-gradient-to-br from-white via-blue-50 to-white';
  const borderColor = isDark ? 'border-gray-700' : 'border-blue-300';
  const marqueeColor = isDark ? 'bg-green-400 text-black' : 'bg-yellow-400 text-black';

  const gridLayout =
    brokers.length === 1 ? 'grid-cols-1' :
    brokers.length === 2 ? 'grid-cols-2' :
    brokers.length === 3 ? 'grid-cols-2 grid-rows-2' :
    'grid-cols-2 grid-rows-2';

  return (
    <div className={`relative flex flex-col h-screen overflow-hidden ${bgColor}`}>
      <div className="absolute inset-0 z-0 opacity-10 bg-[length:60px_60px] bg-repeat animate-diagonalScroll"
        style={{ backgroundImage: isDark ? "url('data:image/svg+xml,%3Csvg fill=%22%23ec4899%22 ...')" : "url('data:image/svg+xml,%3Csvg fill=%223b82f6%22 ...')" }}
      />
      <style>{`
        @keyframes diagonalScroll {
          0% { background-position: 0 0; }
          100% { background-position: 180px 180px; }
        }
        .animate-diagonalScroll {
          animation: diagonalScroll 2.8s linear infinite;
        }
      `}</style>

      {/* Top Bar */}
      <div className={`z-10 flex items-center justify-between px-4 py-2 mb-4 shadow bg-white/70 dark:bg-black/70 border ${borderColor} rounded-xl`}>
        <div className={`text-sm font-medium ${textColor}`}>
          Market Hours: Crypto 24/7 | Stocks 9:30 AM – 4:00 PM ET
        </div>
        <div className="flex gap-2">
          <Button onClick={toggleTheme}>Theme</Button>
          <Button onClick={() => setShowOverlay(true)}>Add Broker</Button>
          <Button onClick={() => setShowSettings(true)}>Settings</Button>
        </div>
      </div>

      {/* Broker Panels */}
      <div className={`grid ${gridLayout} gap-4 px-4`}>
        {brokers.map((broker, index) => (
          <BrokerPanel
            key={index}
            broker={broker}
            models={sortedModels}
            model={model}
            pairedModel={pairedModel}
            setModel={setModel}
            setPairedModel={setPairedModel}
            isTradingActive={isTradingActive}
            setIsTradingActive={setIsTradingActive}
            setShowUploadModal={setShowUploadModal}
          />
        ))}
      </div>

      {/* Strategy and Trades */}
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-4 px-4 mt-6 flex-grow overflow-hidden">
        <div>
          <StrategyPanel
            model={model}
            strategy="Dynamic TP"
            confidenceThreshold={confidenceThreshold}
            setConfidenceThreshold={setConfidenceThreshold}
            tpForecast={tpForecast}
            slForecast={slForecast}
          />
        </div>
        <div className="col-span-2 overflow-y-auto h-[48vh] pr-1">
          {showTradeHistory ? <TradeHistory /> : <OpenTrades />}
        </div>
      </div>

      {/* Sentiment + Flip */}
      <div className="flex items-center justify-between mt-6 px-4">
        <MarketSentiment sentimentData={[
          { symbol: 'BTC', sentiment: 'Bullish', volume: '3.2B' },
          { symbol: 'ETH', sentiment: 'Bullish', volume: '1.8B' },
          { symbol: 'SOL', sentiment: 'Bearish', volume: '900M' }
        ]} />
        <Button onClick={() => setShowTradeHistory(!showTradeHistory)} className="ml-4 bg-yellow-500 hover:bg-yellow-400 text-black">
          {showTradeHistory ? 'Show Open Trades' : 'Flip to Trade History'}
        </Button>
      </div>

      {/* Marquee */}
      <footer className={`fixed bottom-0 left-0 w-full py-4 text-sm text-center ${marqueeColor} animate-pulse h-14 text-md z-20`}>
        🔔 Live Trading Active | BTC +3.5% 🚀 | ETH +2.1% | SOL +6.8% | AI Models Monitoring 24/7 🔄
      </footer>

      {/* Overlays */}
      <AnimatePresence>
        {showOverlay && (
          <motion.div initial={{ opacity: 0 }} animate={{ opacity: 1 }} exit={{ opacity: 0 }}
            className="fixed inset-0 z-50 flex items-center justify-center bg-black/60 backdrop-blur">
            <BrokerLoginOverlay
              onClose={() => setShowOverlay(false)}
              onSuccess={(data) => {
                setBrokers(prev => [...prev, data]);
                setShowOverlay(false);
              }}
            />
          </motion.div>
        )}
        {showSettings && (
          <motion.div initial={{ opacity: 0 }} animate={{ opacity: 1 }} exit={{ opacity: 0 }}
            className="fixed inset-0 z-50 flex items-center justify-center bg-black/60 backdrop-blur">
            <SettingsOverlay
              onClose={() => setShowSettings(false)}
              brokers={brokers}
              onDisconnect={(accountId) => setBrokers(prev => prev.filter(b => b.account_id !== accountId))}
            />
          </motion.div>
        )}
        {showUploadModal && (
          <motion.div initial={{ opacity: 0 }} animate={{ opacity: 1 }} exit={{ opacity: 0 }}
            className="fixed inset-0 z-50 flex items-center justify-center bg-black/60 backdrop-blur">
            <UploadModelOverlay
              onClose={() => setShowUploadModal(false)}
              onUploadSuccess={() => {
                fetch("/api/models")
                  .then(res => res.json())
                  .then(setModels);
              }}
            />
          </motion.div>
        )}
      </AnimatePresence>
    </div>
  );
};

export default Dashboard;
