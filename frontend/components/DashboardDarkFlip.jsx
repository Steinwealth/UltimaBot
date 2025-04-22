import React, { useState } from 'react'
import { FiSettings, FiSun, FiRefreshCw } from 'react-icons/fi'
import { useTheme } from '../context/ThemeProvider'
import { useBrokers } from '../hooks/useBrokers'
import { useTradePanels } from '../hooks/useTradePanels'
import { submitTrade } from '../services/submitTrade'
import TradeStatusCard from './TradeStatusCard'

const DashboardDarkFlip = () => {
  const { toggleTheme } = useTheme()
  const { brokers, loginBroker } = useBrokers()
  const { isHistory, togglePanel, openPositions, tradeHistory } = useTradePanels()
  const [showBrokerOverlay, setShowBrokerOverlay] = useState(false)
  const [form, setForm] = useState({ broker: 'coinbase', apiKey: '', apiSecret: '' })

  const handleSubmit = () => {
    loginBroker(form)
    setShowBrokerOverlay(false)
  }

  const handleTestTrade = async (broker) => {
    try {
      const trade = await submitTrade({
        broker,
        symbol: 'BTC/USD',
        quantity: 0.1,
        side: 'buy',
        type: 'market'
      })
      openPositions.push({ symbol: trade.symbol, gain: '+5.9%', tp: 50000, sl: 48000 });
      import('./MarqueeBar').then(mod => mod.triggerMarqueeMessage(`Test Trade: ${trade.symbol} opened!`));
    } catch (err) {
      console.error(err)
    }
  }

  return (
    <div className="min-h-screen w-full bg-gradient-to-br from-[#0e1015] via-[#1c202a] to-[#272c38] text-white p-6">
      {/* Header */}
      <div className="flex justify-between items-center mb-6">
        <button onClick={() => setShowBrokerOverlay(true)} className="text-white bg-green-700 px-3 py-1 rounded hover:bg-green-600">
          Add Broker
        </button>
        <div className="flex items-center space-x-4">
          <button title="Theme Toggle" onClick={toggleTheme} className="hover:text-green-300">
            <FiSun size={20} />
          </button>
          <button title="Settings" className="hover:text-yellow-300">
            <FiSettings size={20} />
          </button>
        </div>
      </div>

      {/* Broker Info Rows */}
      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
        {brokers.map((b, i) => (
          <div key={i} className="bg-slate-800 p-4 rounded-xl shadow border border-slate-600">
            <h2 className="text-lg font-semibold text-green-400 mb-2">{b.broker.toUpperCase()}</h2>
            <p>ID: {b.accountId}</p>
            <p>Balance: ${b.balance.toFixed(2)}</p>
            <p>Margin: {(b.margin * 100).toFixed(0)}%</p>
            <button
              onClick={() => handleTestTrade(b.broker)}
              className="mt-2 px-3 py-1 text-sm text-white bg-emerald-600 rounded hover:bg-emerald-500"
            >
              [Test Trade]
            </button>
          </div>
        ))}
      </div>

      {/* Flip Control */}
      <div className="mt-10 mb-4 flex justify-between items-center">
        <h3 className="text-md font-bold text-yellow-300">{isHistory ? 'Trade History' : 'Open Positions'}</h3>
        <button onClick={togglePanel} className="flex items-center text-sm text-green-300 hover:text-green-400">
          <FiRefreshCw className="mr-1" /> Flip
        </button>
      </div>

      {/* Trade Panel */}
      <div className="bg-slate-800 p-4 rounded-xl shadow border border-slate-600">
        {(isHistory ? tradeHistory : openPositions).map((trade, i) => (
          <div key={i} className="mb-4">
            <p className="mb-1">
              {trade.symbol} <span className="text-lime-400">{trade.gain}</span>
            </p>
            <TradeStatusCard symbol={trade.symbol} tp={trade.tp} sl={trade.sl} />
          </div>
        ))}
      </div>
    </div>
  )
}

export default DashboardDarkFlip
