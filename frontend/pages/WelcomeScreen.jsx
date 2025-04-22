import React, { useState } from 'react';
import { useTheme } from '@/components/ThemeProvider';
import { useNavigate } from 'react-router-dom'; // or useRouter() for Next.js
import { Button } from '@/components/ui/button';
import clsx from 'clsx';

export default function WelcomeScreen() {
  const { theme, toggleTheme } = useTheme();
  const [brokerKey, setBrokerKey] = useState('');
  const [brokerSecret, setBrokerSecret] = useState('');
  const navigate = useNavigate(); // Replace if using Next.js
  const [loading, setLoading] = useState(false);

  const handleStartSession = () => {
    if (!brokerKey || !brokerSecret) return alert('Enter API Key + Secret');
    setLoading(true);

    setTimeout(() => {
      navigate('/dashboard'); // Fake transition
    }, 1400);
  };

  return (
    <div
      className={clsx(
        'min-h-screen flex flex-col items-center justify-center transition-all duration-500',
        theme === 'dark' ? 'bg-black text-white' : 'bg-white text-black'
      )}
    >
      <div className="mb-8 text-center">
        <div className="text-4xl font-extrabold tracking-wider">Ultima Bot</div>
        <div className="text-sm opacity-60 mt-1">AI Trading Engine v7.3</div>
      </div>

      <div className="flex flex-col gap-4 w-80 bg-neutral-800 p-6 rounded-2xl shadow-lg">
        <input
          className="px-3 py-2 rounded text-sm bg-neutral-900 text-white placeholder-gray-400"
          placeholder="Broker API Key"
          value={brokerKey}
          onChange={(e) => setBrokerKey(e.target.value)}
        />
        <input
          className="px-3 py-2 rounded text-sm bg-neutral-900 text-white placeholder-gray-400"
          placeholder="Broker API Secret"
          value={brokerSecret}
          onChange={(e) => setBrokerSecret(e.target.value)}
          type="password"
        />
        <Button onClick={handleStartSession}>
          {loading ? 'Starting...' : 'Start Session'}
        </Button>
      </div>

      <div className="mt-8 flex items-center gap-4">
        <button
          onClick={toggleTheme}
          className="text-xs text-blue-400 hover:underline"
        >
          Toggle Theme
        </button>
        <div className="text-xl animate-pulse">💠 €£$¥</div>
      </div>
    </div>
  );
}
