// frontend/components/WelcomeLayout.jsx

import React, { useState } from 'react'
import { FiKey, FiLock, FiSettings, FiSun, FiZap } from 'react-icons/fi'

const WelcomeLayout = ({ onSubmit }) => {
  const [apiKey, setApiKey] = useState('')
  const [apiSecret, setApiSecret] = useState('')
  const [polygonKey, setPolygonKey] = useState('')
  const [showSettings, setShowSettings] = useState(false)

  const handleSubmit = () => {
    if (apiKey && apiSecret) onSubmit(apiKey, apiSecret, polygonKey)
  }

  return (
    <div className="flex flex-col items-center justify-center min-h-screen p-8 space-y-4 bg-gradient-to-tr from-[#edf1fb] via-[#e1e7ff] to-[#d8e0ff] text-black relative overflow-hidden">
      <div className="absolute inset-0 pointer-events-none z-0">
        <div className="absolute inset-0 bg-gradient-to-tr from-white/40 via-indigo-100/30 to-indigo-400 opacity-60 shadow-[inset_-30px_-30px_120px_rgba(0,0,0,0.25)] animate-pulse"></div>
        <div className="absolute top-0 left-0 w-1/3 h-1/3 bg-white/20 blur-3xl rounded-full opacity-50 animate-[wiggle_8s_ease-in-out_infinite]" />
        <div className="absolute bottom-0 right-0 w-1/4 h-1/4 bg-indigo-200 blur-2xl rounded-full opacity-40 animate-[wiggle_10s_ease-in-out_infinite]" />
        <div className="absolute inset-0 bg-[radial-gradient(ellipse_at_bottom_left,_var(--tw-gradient-stops))] from-indigo-100 via-white/30 to-transparent opacity-20 animate-[fade_12s_ease-in-out_infinite] mix-blend-lighten" />
        <div className="absolute inset-0 bg-white opacity-20 animate-[fade_6s_ease-in-out_infinite] mix-blend-screen"></div>
      </div>

      <div className="absolute top-4 right-4 flex items-center space-x-6">
        <div className="text-xs font-semibold text-blue-500 px-2 py-1 bg-blue-100 border border-blue-300 rounded shadow">
          Market Hours: 24/7 Crypto · 6:30AM–1PM US Stocks (PT)
        </div>
        <button title="Theme" className="hover:text-sky-500">
          <FiSun size={20} />
        </button>
        <button onClick={() => setShowSettings(true)} title="Settings" className="text-black hover:text-yellow-500">
          <FiSettings size={20} />
        </button>
      </div>

      <div className="absolute" style={{ bottom: '66px', right: '100px' }}>
        <div className="text-[5vw] font-semibold tracking-widest font-serif text-white drop-shadow-[0_0_25px_rgba(255,255,255,0.8)] animate-[fadeGlow_4s_ease-in-out_infinite]">
          <span className="animate-[fade_2.4s_ease-in-out_infinite]">€</span>
          <span className="animate-[fade_2.4s_0.2s_ease-in-out_infinite]">£</span>
          <span className="animate-[fade_2.4s_0.4s_ease-in-out_infinite]">$</span>
          <span className="animate-[fade_2.4s_0.6s_ease-in-out_infinite]">¥</span>
        </div>
      </div>

      <div className="flex flex-col w-full max-w-sm space-y-2">
        <select className="w-full bg-white border border-slate-400 rounded px-3 py-2 text-black">
          <option>Coinbase</option>
          <option>Binance</option>
          <option>Kraken</option>
          <option>E*TRADE</option>
          <option>Robinhood</option>
          <option>IBKR</option>
          <option>Gemini</option>
          <option>Fidelity</option>
          <option>Charles Schwab</option>
          <option>TD Ameritrade</option>
          <option>Tastytrade</option>
        </select>
        <div className="flex items-center w-full space-x-2 bg-white px-3 py-2 rounded border border-slate-400">
          <FiKey />
          <input
            type="text"
            value={apiKey}
            onChange={(e) => setApiKey(e.target.value)}
            placeholder="API Key"
            className="bg-transparent outline-none text-black w-full"
          />
        </div>
      </div>

      <div className="flex items-center w-full max-w-sm space-x-2 bg-white px-3 py-2 rounded border border-slate-400">
        <FiLock />
        <input
          type="password"
          value={apiSecret}
          onChange={(e) => setApiSecret(e.target.value)}
          placeholder="API Secret"
          className="bg-transparent outline-none text-black w-full"
        />
      </div>

      <div className="flex items-center w-full max-w-sm space-x-2 bg-white px-3 py-2 rounded border border-slate-400">
        <FiZap />
        <input
          type="text"
          value={polygonKey}
          onChange={(e) => setPolygonKey(e.target.value)}
          placeholder="Polygon Key (Optional*)"
          className="bg-transparent outline-none text-black w-full"
        />
      </div>

      <button onClick={handleSubmit} className="bg-gradient-to-r from-pink-300 via-purple-300 to-indigo-400 text-black w-full max-w-sm py-2 px-4 rounded font-semibold hover:opacity-90 shadow-lg">
        Start Session
      </button>

      {showSettings && (
        <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
          <div className="bg-white p-6 rounded-xl shadow-lg space-y-4 w-full max-w-sm text-black">
            <h2 className="text-xl font-semibold">Settings</h2>
            <div className="flex items-center justify-between">
              <span>Mute Sounds</span>
              <input type="checkbox" />
            </div>
            <div className="flex items-center justify-between">
              <span>Use Custom Sounds</span>
              <input type="checkbox" />
            </div>
            <div className="flex items-center justify-between">
              <span>Mode</span>
              <select className="bg-slate-200 text-black rounded px-2 py-1">
                <option>Easy Mode</option>
                <option>Hard Mode</option>
              </select>
            </div>
            <button onClick={() => setShowSettings(false)} className="w-full mt-2 bg-slate-300 text-black py-2 px-4 rounded hover:bg-slate-400">
              Close
            </button>
          </div>
        </div>
      )}
    </div>
  )
}

export default WelcomeLayout
