import React from 'react';
import { X } from 'lucide-react';
import { useTheme } from "@/hooks/useTheme";
import useModeSettings from "@/hooks/useModeSettings";
import useSoundSettings from '@/hooks/useSoundSettings';


const SettingsOverlay = ({ onClose, brokers = [], onDisconnect }) => {
  const { theme, toggleTheme } = useTheme();
  const { mode, setMode } = useModeSettings();
  const { soundMuted, toggleMute, customSounds, toggleCustomSounds } = useSoundSettings();

  return (
    <div
      className="fixed inset-0 z-50 flex items-center justify-center transition-opacity duration-300 bg-black bg-opacity-50"
      role="dialog"
      aria-modal="true"
    >
      <div className="relative p-6 transition-transform duration-300 transform scale-95 rounded-lg shadow-lg bg-white/50 dark:bg-gray-800/50 w-96 backdrop-blur-sm">
        {/* Close Button */}
        <button
          onClick={onClose}
          aria-label="Close settings"
          className="absolute top-2 right-2 p-1 text-gray-600 dark:text-gray-300 hover:text-red-500"
        >
          <X className="w-5 h-5" />
        </button>

        {/* Title */}
        <h2 className="mb-4 text-2xl font-bold text-gray-900 dark:text-white">Settings</h2>

        {/* Connected Brokers */}
        <div className="mb-4">
          <span className="block mb-2 text-gray-700 dark:text-gray-200 font-medium">Connected Brokers</span>
          {brokers.length === 0 ? (
            <p className="text-sm text-gray-500 dark:text-gray-400">No brokers connected.</p>
          ) : (
            <ul className="space-y-2">
              {brokers.map((broker) => (
                <li
                  key={broker.account_id}
                  className="flex items-center justify-between px-3 py-2 text-sm text-white bg-black border border-gray-600 rounded"
                >
                  <span>{broker.name} ({broker.account_id})</span>
                  <button
                    onClick={() => onDisconnect(broker.account_id)}
                    className="text-red-400 hover:text-red-600"
                    title="Disconnect"
                  >
                    <X className="w-4 h-4" />
                  </button>
                </li>
              ))}
            </ul>
          )}
        </div>

        {/* Theme Toggle */}
        <div className="flex items-center justify-between mb-4">
          <span className="text-gray-700 dark:text-gray-200">Theme</span>
          <button
            onClick={toggleTheme}
            className="px-3 py-1 bg-gray-200 rounded dark:bg-gray-700"
          >
            {theme === 'dark' ? 'Xbox (Dark)' : 'PlayStation (Light)'}
          </button>
        </div>

        {/* Mode Selection */}
        <div className="mb-4">
          <span className="block mb-2 text-gray-700 dark:text-gray-200">Mode</span>
          <div className="flex space-x-2">
            {['easy', 'hard', 'hero'].map((m) => (
              <button
                key={m}
                onClick={() => setMode(m)}
                className={`px-3 py-1 rounded ${
                  mode === m
                    ? 'bg-blue-500 text-white'
                    : 'bg-gray-200 dark:bg-gray-700 text-gray-800 dark:text-gray-200'
                }`}
              >
                {m.charAt(0).toUpperCase() + m.slice(1)} Mode
              </button>
            ))}
          </div>
        </div>

        {/* Sound Toggle */}
        <div className="flex items-center justify-between mb-4">
          <span className="text-gray-700 dark:text-gray-200">Mute Sounds</span>
          <button
            onClick={toggleMute}
            className="px-3 py-1 bg-gray-200 rounded dark:bg-gray-700"
          >
            {soundMuted ? 'Muted' : 'Unmuted'}
          </button>
        </div>

        {/* Custom Sounds Toggle */}
        <div className="flex items-center justify-between">
          <span className="text-gray-700 dark:text-gray-200">Custom Sounds</span>
          <button
            onClick={toggleCustomSounds}
            className="px-3 py-1 bg-gray-200 rounded dark:bg-gray-700"
          >
            {customSounds ? 'Enabled' : 'Disabled'}
          </button>
        </div>
      </div>
    </div>
  );
};

export default SettingsOverlay;
