import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { Settings } from 'lucide-react';
import Particles from 'react-tsparticles';
import { motion, AnimatePresence } from 'framer-motion';
import SettingsOverlay from '@/window/components/SettingsOverlay';
import { useTheme } from '@/hooks/useTheme';

const IndexScreen = () => {
  const navigate = useNavigate();
  const { theme } = useTheme();

  const [password, setPassword] = useState('');
  const [showSettings, setShowSettings] = useState(false);
  const [sessionStarted, setSessionStarted] = useState(false);
  const [error, setError] = useState('');
  const [buttonClicked, setButtonClicked] = useState(false);

  useEffect(() => {
    const cookies = document.cookie.split(';').map(c => c.trim());
    const hasToken = cookies.find(c => c.startsWith('ultimabot-auth=1'));
    if (hasToken) {
      const brokers = localStorage.getItem('ultima-bot-brokers');
      const parsed = brokers && JSON.parse(brokers);
      if (parsed && parsed.length > 0) {
        navigate('/dashboard');
      } else {
        navigate('/welcome');
      }
    }
  }, [navigate]);

  const handleStart = () => {
    if (password === '7777777') {
      setError('');
      setButtonClicked(true);
      const expiry = new Date(Date.now() + 4 * 60 * 60 * 1000).toUTCString();
      document.cookie = `ultimabot-auth=1; path=/; expires=${expiry}; SameSite=Strict`;

      setTimeout(() => {
        setSessionStarted(true);
        const brokers = localStorage.getItem('ultima-bot-brokers');
        const parsed = brokers && JSON.parse(brokers);
        const hasBrokers = parsed && parsed.length > 0;
        navigate(hasBrokers ? '/dashboard' : '/welcome');
      }, 600); // ✅ Semicolon added here
    } else {
      setError('Incorrect Password');
    }
  };

  return (
    <AnimatePresence>
      {!sessionStarted && (
        <motion.div
          initial={{ opacity: 1 }}
          exit={{ opacity: 0, y: -50 }}
          transition={{ duration: 0.6, ease: "easeInOut" }}
          className="relative flex flex-col items-center justify-center min-h-screen overflow-hidden text-white bg-gradient-to-br from-gray-900 via-gray-800 to-black"
        >
          {/* Background Pattern */}
          <div
            className="absolute inset-0 z-0 opacity-10 bg-[length:60px_60px] bg-repeat animate-diagonalScroll"
            style={{
              backgroundImage:
                "url('data:image/svg+xml,%3Csvg xmlns=\"http://www.w3.org/2000/svg\" width=\"16\" height=\"16\" fill=\"%2300ff88\" viewBox=\"0 0 16 16\"%3E%3Cpath fill-rule=\"evenodd\" d=\"M15.528 2.973a.75.75 0 0 1 .472.696v8.662a.75.75 0 0 1-.472.696l-7.25 2.9a.75.75 0 0 1-.557 0l-7.25-2.9A.75.75 0 0 1 0 12.331V3.669a.75.75 0 0 1 .471-.696L7.443.184l.004-.001.274-.11a.75.75 0 0 1 .558 0l.274.11.004.001zm-1.374.527L8 5.962 1.846 3.5 1 3.839v.4l6.5 2.6v7.922l.5.2.5-.2V6.84l6.5-2.6v-.4l-.846-.339Z\"/%3E%3C/svg%3E')"
            }}
          />
          <style>
            {`
              @keyframes diagonalScroll {
                0% { background-position: 0 0; }
                100% { background-position: 180px 180px; }
              }
              .animate-diagonalScroll {
                animation: diagonalScroll 2.8s linear infinite;
              }
              .button-glow:focus {
                box-shadow: 0 0 8px #60a5fa, 0 0 20px #60a5fa;
              }
              .dark .button-glow:focus {
                box-shadow: 0 0 8px #facc15, 0 0 20px #facc15;
              }
            `}
          </style>

          {/* Particles */}
          <Particles
            className="absolute inset-0 z-0"
            options={{
              fullScreen: { enable: false },
              background: { color: { value: "transparent" } },
              particles: {
                number: { value: 120 },
                color: { value: ["#f472b6", "#60a5fa", "#10b981"] },
                shape: { type: "circle" },
                size: { value: { min: 1, max: 3 } },
                links: { enable: true, color: "#4b5563" },
                opacity: { value: 0.4 },
                move: { enable: true, speed: 0.4 }
              }
            }}
          />

          {/* Top Right Settings */}
          <div className="absolute z-20 flex items-center gap-4 px-4 py-2 rounded shadow-md top-6 right-6 bg-black/70">
            <div className="text-sm font-medium text-green-300">Ultima Bot Access</div>
            <button
              onClick={() => setShowSettings(true)}
              className="flex items-center gap-1 px-2 py-1 text-sm border border-gray-600 rounded hover:bg-gray-700"
            >
              <Settings className="w-4 h-4" />
            </button>
          </div>

          {/* Password Input */}
          <motion.div
            initial={{ opacity: 0, y: 30 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.8, ease: "easeOut" }}
            className="relative z-10 w-full max-w-md px-8 py-10 bg-gray-900 border border-gray-700 shadow-xl rounded-xl"
          >
            <input
              type="password"
              placeholder="Enter Password"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              onKeyDown={(e) => e.key === 'Enter' && handleStart()}
              className="w-full px-4 py-2 mb-4 text-white bg-gray-800 border border-gray-600 rounded shadow-sm"
            />
            {error && <div className="mb-4 text-sm text-red-400">{error}</div>}

            <div className="flex gap-4 mt-4">
              <button
                onClick={handleStart}
                disabled={buttonClicked}
                className={`button-glow w-full px-6 py-3 text-lg font-semibold text-black bg-green-400 rounded shadow-md transition duration-300 transform
                  ${buttonClicked
                    ? 'cursor-not-allowed opacity-60'
                    : 'hover:bg-green-300 hover:shadow-lg active:scale-95 focus:outline-none focus:ring-4 focus:ring-blue-400/70 dark:focus:ring-yellow-400/70'}
                `}
              >
                {buttonClicked ? 'Loading...' : 'Enter Ultima Bot'}
              </button>
            </div>
          </motion.div>

          {/* Bottom Corner Logo */}
          <div className="absolute font-bold text-green-500 text-7xl bottom-6 right-6 animate-pulse">
            €£$¥
          </div>

          {showSettings && <SettingsOverlay onClose={() => setShowSettings(false)} />}
        </motion.div>
      )}
    </AnimatePresence>
  );
};

export default IndexScreen;
