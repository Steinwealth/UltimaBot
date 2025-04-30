// frontend/src/components/WelcomeScreenDark.jsx

import React, { useState, useEffect } from 'react';
import { Button } from '@/components/ui/button';
import { Settings } from 'lucide-react';
import { useNavigate } from 'react-router-dom';
import SettingsOverlay from './SettingsOverlay';
import Particles from 'react-tsparticles';
import { useTheme } from '../../hooks/useTheme';

const WelcomeScreenDark = () => {
  const navigate = useNavigate();
  const { theme, toggleTheme } = useTheme();
  const [broker, setBroker] = useState('');
  const [apiKey, setApiKey] = useState('');
  const [apiSecret, setApiSecret] = useState('');
  const [polygonKey, setPolygonKey] = useState('');
  const [showSettings, setShowSettings] = useState(false);
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
      navigate('/dashboard-dark');
    }
  };

  const isStockBroker = ['E*TRADE', 'Robinhood', 'Interactive Brokers', 'Tastytrade', 'Charles Schwab', 'Fidelity', 'TD Ameritrade'].includes(broker);
  const isDisabled = !(broker && apiKey && apiSecret);

  return (
    <div className="relative flex flex-col items-center justify-center h-screen text-white bg-gray-900">
      <Particles
        className="absolute inset-0 z-0"
        options={{
          background: { color: { value: "#111827" } },
          particles: {
            number: { value: 50 },
            color: { value: "#22c55e" },
            links: { enable: true, color: "#22c55e" },
            move: { enable: true, speed: 0.5 },
            size: { value: 3 },
          },
        }}
      />
      <div className="relative z-10 flex flex-col items-center justify-center h-full">
        <div className="absolute flex gap-4 top-4 right-4">
          <div className="text-sm text-gray-400">
            Market Hours: U.S. Stocks 9:30 AM – 4:00 PM ET | Crypto: 24/7
          </div>
          <Button variant="outline" onClick={toggleTheme}>Theme</Button>
          <Button variant="outline" onClick={() => setShowSettings(true)}><Settings className="mr-2" /> Settings</Button>
        </div>

        <div className="mb-6 text-4xl font-bold text-green-400">Ultima Bot (Xbox Theme)</div>
        <div className="mb-4 text-lg text-gray-300">Welcome to your trading companion</div>

        <select
          value={broker}
          onChange={(e) => setBroker(e.target.value)}
          className="px-4 py-2 mb-2 text-white bg-gray-800 border border-gray-600 rounded"
        >
          <option value="">Select Broker</option>
          <option value="Coinbase">Coinbase</option>
          <option value="Binance">Binance</option>
          <option value="Kraken">Kraken</option>
          <option value="Gemini">Gemini</option>
          <option value="E*TRADE">E*TRADE</option>
          <option value="Robinhood">Robinhood</option>
          <option value="Interactive Brokers">Interactive Brokers</option>
          <option value="Tastytrade">Tastytrade</option>
          <option value="Charles Schwab">Charles Schwab</option>
          <option value="Fidelity">Fidelity</option>
          <option value="TD Ameritrade">TD Ameritrade</option>
        </select>
        {errors.broker && <div className="mb-2 text-sm text-red-500">{errors.broker}</div>}

        <input
          type="text"
          placeholder="API Key"
          value={apiKey}
          onChange={(e) => setApiKey(e.target.value)}
          className="w-64 px-4 py-2 mb-2 text-white bg-gray-800 border border-gray-600 rounded"
        />
        {errors.apiKey && <div className="mb-2 text-sm text-red-500">{errors.apiKey}</div>}

        <input
          type="password"
          placeholder="API Secret"
          value={apiSecret}
          onChange={(e) => setApiSecret(e.target.value)}
          className="w-64 px-4 py-2 mb-2 text-white bg-gray-800 border border-gray-600 rounded"
        />
        {errors.apiSecret && <div className="mb-2 text-sm text-red-500">{errors.apiSecret}</div>}

        {isStockBroker && (
          <input
            type="text"
            placeholder="Polygon Key (Optional)"
            value={polygonKey}
            onChange={(e) => setPolygonKey(e.target.value)}
            className="w-64 px-4 py-2 mb-4 text-white bg-gray-800 border border-gray-600 rounded"
          />
        )}

        <div className="flex gap-4 mb-8">
          <Button disabled={isDisabled} onClick={handleStartSession} className="px-6 py-3 text-lg text-white bg-green-600 hover:bg-green-500">
            Start Session
          </Button>
        </div>

        <div className="absolute text-3xl font-bold text-green-400 bottom-6 right-6 animate-pulse">
          €£$¥
        </div>
      </div>

      {showSettings && <SettingsOverlay onClose={() => setShowSettings(false)} />}
    </div>
  );
};

export default WelcomeScreenDark;
