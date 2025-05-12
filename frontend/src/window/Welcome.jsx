import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { motion, AnimatePresence } from 'framer-motion';
import { useTheme } from '@/hooks/useTheme';
import { Button } from '@/window/components/ui/button';
import BrokerLoginOverlay from '@/window/components/BrokerLoginOverlay';
import SettingsOverlay from '@/window/components/SettingsOverlay';

const Welcome = () => {
  const navigate = useNavigate();
  const { theme, toggleTheme } = useTheme();

  const [showSettings, setShowSettings] = useState(false);
  const [brokers, setBrokers] = useState([]);

  useEffect(() => {
    const isAuthenticated = document.cookie.includes('ultimabot-auth=1');
    if (!isAuthenticated) navigate('/');
  }, [navigate]);

  useEffect(() => {
    if (brokers.length > 0) {
      navigate('/dashboard');
    }
  }, [brokers, navigate]);

  const isDark = theme === 'dark';

  const backgroundSVG = isDark
    ? "url('data:image/svg+xml,%3Csvg xmlns=%22http://www.w3.org/2000/svg%22 width=%2216%22 height=%2216%22 fill=%22%23ec4899%22 viewBox=%220 0 16 16%22%3E%3Cpath fill-rule=%22evenodd%22 d=%22M15.528 2.973a.75.75 0 0 1 .472.696v8.662a.75.75 0 0 1-.472.696l-7.25 2.9a.75.75 0 0 1-.557 0l-7.25-2.9A.75.75 0 0 1 0 12.331V3.669a.75.75 0 0 1 .471-.696L7.443.184l.004-.001.274-.11a.75.75 0 0 1 .558 0l.274.11.004.001zm-1.374.527L8 5.962 1.846 3.5 1 3.839v.4l6.5 2.6v7.922l.5.2.5-.2V6.84l6.5-2.6v-.4l-.846-.339Z%22/%3E%3C/svg%3E')"
    : "url('data:image/svg+xml,%3Csvg xmlns=%22http://www.w3.org/2000/svg%22 width=%2216%22 height=%2216%22 fill=%223b82f6%22 viewBox=%220 0 16 16%22%3E%3Cpath d=%22M5.5 9.511c.076.954.83 1.697 2.182 1.785V12h.6v-.709c1.4-.098 2.218-.846 2.218-1.932 0-.987-.626-1.496-1.745-1.76l-.473-.112V5.57c.6.068.982.396 1.074.85h1.052c-.076-.919-.864-1.638-2.126-1.716V4h-.6v.719c-1.195.117-2.01.836-2.01 1.853 0 .9.606 1.472 1.613 1.707l.397.098v2.034c-.615-.093-1.022-.43-1.114-.9zm2.177-2.166c-.59-.137-.91-.416-.91-.836 0-.47.345-.822.915-.925v1.76h-.005zm.692 1.193c.717.166 1.048.435 1.048.91 0 .542-.412.914-1.135.982V8.518z%22/%3E%3Cpath d=%22M8 15A7 7 0 1 1 8 1a7 7 0 0 1 0 14m0 1A8 8 0 1 0 8 0a8 8 0 0 0 0 16%22/%3E%3Cpath d=%22M8 13.5a5.5 5.5 0 1 1 0-11 5.5 5.5 0 0 1 0 11m0 .5A6 6 0 1 0 8 2a6 6 0 0 0 0 12%22/%3E%3C/svg%3E')";

  const marqueeColor = isDark ? 'bg-green-400 text-black' : 'bg-yellow-400 text-black';
  const barColor = isDark ? 'bg-black/70 border-gray-700 text-green-300' : 'bg-white/70 border-blue-300 text-blue-600';

  return (
    <div className={`relative flex flex-col items-center min-h-screen px-6 overflow-hidden ${isDark ? 'text-white' : 'text-gray-900'} ${isDark ? 'bg-gradient-to-br from-gray-900 via-gray-800 to-black' : 'bg-gradient-to-br from-white via-blue-50 to-white'}`}>
      {/* Background SVG */}
      <div className="absolute inset-0 z-0 opacity-10 bg-[length:60px_60px] bg-repeat animate-diagonalScroll"
        style={{ backgroundImage: backgroundSVG }}
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

      {/* Market Hours Bar */}
      <div className={`z-10 flex items-center justify-between w-full max-w-6xl px-4 py-3 mb-8 border rounded-xl shadow ${barColor}`}>
        <div className="text-sm font-medium">
          Market Hours: Crypto: 24/7 – Stocks: 9:30 AM – 4:00 PM ET
        </div>
        <div className="flex gap-2">
          <Button onClick={toggleTheme}>Theme</Button>
          <Button onClick={() => setShowSettings(true)}>Settings</Button>
        </div>
      </div>

      {/* Center Broker Login */}
      <div className="z-10 flex items-center justify-center w-full max-w-lg">
        <BrokerLoginOverlay
          onClose={() => {}}
          onSuccess={(data) => setBrokers((prev) => [...prev, data])}
          theme={theme}
          alwaysVisible
        />
      </div>

      {/* Neon Marquee */}
      <footer className={`fixed bottom-0 left-0 w-full py-4 text-sm text-center animate-pulse h-14 text-md z-20 ${marqueeColor}`}>
        🔔 Welcome to Ultima Bot | Real-time AI Trading Engine Active | Market Sync: OK ✅
      </footer>

      {/* Settings Overlay */}
      <AnimatePresence>
        {showSettings && (
          <motion.div initial={{ opacity: 0 }} animate={{ opacity: 1 }} exit={{ opacity: 0 }}
            className="fixed inset-0 z-50 flex items-center justify-center bg-black/60 backdrop-blur">
            <SettingsOverlay
              onClose={() => setShowSettings(false)}
              brokers={[]}
              onDisconnect={() => {}}
            />
          </motion.div>
        )}
      </AnimatePresence>
    </div>
  );
};

export default Welcome;
