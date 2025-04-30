import React, { useState, useEffect } from 'react';
import { Button } from '@/components/ui/button';
import { Settings } from 'lucide-react';
import { useNavigate } from 'react-router-dom';
import SettingsOverlay from './SettingsOverlay';
import Particles from 'react-tsparticles';
import { motion, AnimatePresence } from 'framer-motion';
import { useTheme } from '../../hooks/useTheme';

const brokers = [
  "Binance", "Coinbase", "E*TRADE", "Robinhood", "Interactive Brokers",
  "Kraken", "Tastytrade", "Charles Schwab", "Bitfinex", "Gemini"
];

const WelcomeScreenLight = () => {
  const navigate = useNavigate();
  const { theme, toggleTheme } = useTheme();
  const [broker, setBroker] = useState('');
  const [apiKey, setApiKey] = useState('');
  const [apiSecret, setApiSecret] = useState('');
  const [polygonKey, setPolygonKey] = useState('');
  const [showSettings, setShowSettings] = useState(false);
  const [sessionStarted, setSessionStarted] = useState(false);
  const [errors, setErrors] = useState({});

  useEffect(() => {
    const savedBroker = localStorage.getItem('broker');
    const savedApiKey = localStorage.getItem('apiKey');
    const savedApiSecret = localStorage.getItem('apiSecret');
    const savedPolygonKey = localStorage.getItem('polygonKey');
    if (savedBroker) setBroker(savedBroker);
    if (savedApiKey) setApiKey(savedApiKey);
    if (savedApiSecret) setApiSecret(savedApiSecret);
    if (savedPolygonKey) setPolygonKey(savedPolygonKey);
  }, []);

  const handleStartSession = () => {
    const newErrors = {};
    if (!broker) newErrors.broker = 'Broker required';
    if (!apiKey) newErrors.apiKey = 'API Key required';
    if (!apiSecret) newErrors.apiSecret = 'API Secret required';
    setErrors(newErrors);

    if (Object.keys(newErrors).length === 0) {
      localStorage.setItem('broker', broker);
      localStorage.setItem('apiKey', apiKey);
      localStorage.setItem('apiSecret', apiSecret);
      localStorage.setItem('polygonKey', polygonKey);
      setSessionStarted(true);
      setTimeout(() => navigate('/dashboard-light'), 600);
    }
  };

  const isStockBroker = ['E*TRADE', 'Robinhood', 'Interactive Brokers', 'Tastytrade', 'Charles Schwab'].includes(broker);
  const isDisabled = !(broker && apiKey && apiSecret);

  return (
    <AnimatePresence>
      {!sessionStarted && (
        <motion.div
          initial={{ opacity: 1 }}
          exit={{ opacity: 0, y: -50 }}
          transition={{ duration: 0.6, ease: "easeInOut" }}
          className="relative flex flex-col items-center justify-center h-screen text-gray-900 bg-white"
        >
          <Particles
            className="absolute inset-0 z-0"
            options={{
              background: { color: { value: "#ffffff" } },
              particles: {
                number: { value: 50 },
                color: { value: "#3b82f6" },
                links: { enable: true, color: "#3b82f6" },
                move: { enable: true, speed: 0.5 },
                size: { value: 3 }
              }
            }}
          />
          <motion.div
            initial={{ opacity: 0, y: 30 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.8, ease: "easeOut" }}
            className="relative z-10 flex flex-col items-center justify-center h-full"
          >
            <div className="absolute flex gap-4 top-4 right-4">
              <div className="text-sm text-gray-500">
                Market Hours: U.S. Stocks 9:30 AM – 4:00 PM ET | Crypto: 24/7
              </div>
              <Button variant="outline" onClick={toggleTheme}>Theme</Button>
              <Button variant="outline" onClick={() => setShowSettings(true)}><Settings className="mr-2" /> Settings</Button>
            </div>
            <div className="mb-6 text-4xl font-bold text-blue-600">Ultima Bot (PlayStation Theme)</div>
            <div className="mb-4 text-lg">Welcome to your trading companion</div>
            <select
              value={broker}
              onChange={(e) => setBroker(e.target.value)}
              className="px-4 py-2 mb-2 border rounded"
            >
              <option value="">Select Broker</option>
              {brokers.map((b) => <option key={b}>{b}</option>)}
            </select>
            {errors.broker && <div className="mb-2 text-sm text-red-500">{errors.broker}</div>}
            <input
              type="text"
              placeholder="API Key"
              value={apiKey}
              onChange={(e) => setApiKey(e.target.value)}
              className="w-64 px-4 py-2 mb-2 border rounded"
            />
            {errors.apiKey && <div className="mb-2 text-sm text-red-500">{errors.apiKey}</div>}
            <input
              type="password"
              placeholder="API Secret"
              value={apiSecret}
              onChange={(e) => setApiSecret(e.target.value)}
              className="w-64 px-4 py-2 mb-2 border rounded"
            />
            {errors.apiSecret && <div className="mb-2 text-sm text-red-500">{errors.apiSecret}</div>}
            {isStockBroker && (
              <input
                type="text"
                placeholder="Polygon Key (Optional)"
                value={polygonKey}
                onChange={(e) => setPolygonKey(e.target.value)}
                className="w-64 px-4 py-2 mb-4 border rounded"
              />
            )}
            <div className="flex gap-4 mb-8">
              <Button disabled={isDisabled} onClick={handleStartSession} className="px-6 py-3 text-lg text-white bg-blue-500 hover:bg-blue-600">
                Start Session
              </Button>
            </div>
            <div className="absolute text-3xl font-bold text-blue-500 bottom-6 right-6 animate-pulse">
              €£$¥
            </div>
          </motion.div>
          {showSettings && <SettingsOverlay onClose={() => setShowSettings(false)} />}
        </motion.div>
      )}
    </AnimatePresence>
  );
};

export default WelcomeScreenLight;
