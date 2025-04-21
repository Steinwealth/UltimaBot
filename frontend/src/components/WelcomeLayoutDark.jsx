import React, { useState } from 'react'
import { FiKey, FiLock, FiSettings, FiSun, FiZap } from 'react-icons/fi'

const WelcomeLayoutDark = ({ onSubmit }) => {
  const [apiKey, setApiKey] = useState('')
  const [apiSecret, setApiSecret] = useState('')
  const [polygonKey, setPolygonKey] = useState('')
  const [showSettings, setShowSettings] = useState(false)

  const handleSubmit = () => {
    if (apiKey && apiSecret) onSubmit(apiKey, apiSecret, polygonKey)
  }

  return (
    <div className="flex flex-col items-center justify-center min-h-screen p-8 space-y-4 bg-gradient-to-br from-[#0a0d12] via-[#1b1f27] to-[#2b2f38] text-white relative overflow-hidden">
      <div className="absolute inset-0 pointer-events-none z-0">
        <div className="absolute inset-0 bg-gradient-to-br from-purple-800/40 via-transparent to-green-700/30 opacity-60 shadow-[inset_-40px_-40px_100px_rgba(0,0,0,0.3)] animate-pulse"></div>
        <div className="absolute top-0 left-0 w-1/3 h-1/3 bg-purple-600/15 blur-3xl rounded-full animate-[floatSlow_14s_ease-in-out_infinite]"></div>
        <div className="absolute bottom-0 right-0 w-1/4 h-1/4 bg-green-500/15 blur-2xl rounded-full animate-[floatSlow_12s_ease-in-out_infinite]"></div>
        <div className="absolute inset-0 bg-white opacity-10 animate-[fade_8s_ease-in-out_infinite] mix-blend-overlay"></div>
      </div>

      <div className="absolute top-4 right-4 flex items-center space-x-6">
        <div className="text-xs font-semibold text-green-400 px-2 py-1 bg-slate-800 border border-slate-600 rounded shadow">
          Market Hours: 24/7 Crypto · 6:30AM–1PM US Stocks (PT)
        </div>
        <button title="Theme" className="text-white hover:text-green-300">
          <FiSun size={20} />
        </button>
        <button onClick={() => setShowSettings(true)} title="Settings" className="text-white hover:text-yellow-300">
          <FiSettings size={20} />
        </button>
      </div>

      <div className="absolute" style={{ bottom: '66px', right: '100px' }}>
        <div className="text-[5vw] font-semibold tracking-widest font-mono text-white drop-shadow-[0_0_25px_rgba(0,255,150,0.7)] animate-[fadeGlow_3s_ease-in-out_infinite]">
          <span className="animate-[fade_2.4s_ease-in-out_infinite]">€</span>
          <span className="animate-[fade_2.4s_0.2s_ease-in-out_infinite]">£</span>
          <span className="animate-[fade_2.4s_0.4s_ease-in-out_infinite]">$</span>
          <span className="animate-[fade_2.4s_0.6s_ease-in-out_infinite]">¥</span>
        </div>
      </div>

      <div className="flex flex-col w-full max-w-sm space-y-2">
        <select className="w-full bg-slate-900 border border-slate-600 rounded px-3 py-2 text-white">
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
        <div className="flex items-center w-full space-x-2 bg-slate-800 px-3 py-2 rounded border border-slate-600">
          <FiKey />
          <input
            type="text"
            value={apiKey}
            onChange={(e) => setApiKey(e.target.value)}
            placeholder="API Key"
            className="bg-transparent outline-none text-white w-full"
          />
        </div>
      </div>

      <div className="flex items-center w-full max-w-sm space-x-2 bg-slate-800 px-3 py-2 rounded border border-slate-600">
        <FiLock />
        <input
          type="password"
          value={apiSecret}
          onChange={(e) => setApiSecret(e.target.value)}
          placeholder="API Secret"
          className="bg-transparent outline-none text-white w-full"
        />
      </div>

      <div className="flex items-center w-full max-w-sm space-x-2 bg-slate-800 px-3 py-2 rounded border border-slate-600">
        <FiZap />
        <input
          type="text"
          value={polygonKey}
          onChange={(e) => setPolygonKey(e.target.value)}
          placeholder="Polygon Key (Optional*)"
          className="bg-transparent outline-none text-white w-full"
        />
      </div>

      <button onClick={handleSubmit} className="bg-gradient-to-r from-green-600 via-green-500 to-emerald-400 text-white w-full max-w-sm py-2 px-4 rounded font-semibold hover:opacity-90 shadow-lg">
        Start Session
      </button>

      {showSettings && (
        <div className="fixed inset-0 bg-black bg-opacity-60 flex items-center justify-center z-50">
          <div className="bg-slate-800 p-6 rounded-xl shadow-lg space-y-4 w-full max-w-sm text-white">
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
              <select className="bg-slate-700 text-white rounded px-2 py-1">
                <option>Easy Mode</option>
                <option>Hard Mode</option>
              </select>
            </div>
            <button onClick={() => setShowSettings(false)} className="w-full mt-2 bg-slate-600 text-white py-2 px-4 rounded hover:bg-slate-500">
              Close
            </button>
          </div>
        </div>
      )}
    </div>
  )
}

export default WelcomeLayoutDark
