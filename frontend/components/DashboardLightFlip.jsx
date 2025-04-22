import React, { useState } from 'react'
import { FiSettings, FiSun, FiRefreshCw } from 'react-icons/fi'
import { useTheme } from '../context/ThemeProvider'
import { useBrokers } from '../hooks/useBrokers'
import { useTradePanels } from '../hooks/useTradePanels'
import { submitTrade } from '../services/submitTrade'
import TradeStatusCard from './TradeStatusCard'

const DashboardLightFlip = () => {
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
    <div className="min-h-screen w-full bg-gradient-to-br from-[#f4f8ff] via-[#e8eff9] to-[#dfe7f1] text-black p-6">
      {/* Header */}
      <div className="flex justify-between items-center mb-6">
        <button onClick={() => setShowBrokerOverlay(true)} className="text-white bg-blue-500 px-3 py-1 rounded hover:bg-blue-400">
          Add Broker
        </button>
        <div className="flex items-center space-x-4">
          <button title="Theme Toggle" onClick={toggleTheme} className="hover:text-blue-600">
            <FiSun size={20} />
          </button>
          <button title="Settings" className="hover:text-yellow-500">
            <FiSettings size={20} />
          </button>
        </div>
      </div>

      {/* Broker Info Rows */}
      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
        {brokers.map((b, i) => (
          <div key={i} className="bg-white p-4 rounded-xl shadow border border-slate-300">
            <h2 className="text-lg font-semibold text-indigo-600 mb-2">{b.broker.toUpperCase()}</h2>
            <p>ID: {b.accountId}</p>
            <p>Balance: ${b.balance.toFixed(2)}</p>
            <p>Margin: {(b.margin * 100).toFixed(0)}%</p>
            <button
              onClick={() => handleTestTrade(b.broker)}
              className="mt-2 px-3 py-1 text-sm text-white bg-blue-600 rounded hover:bg-blue-500"
            >
              [Test Trade]
            </button>
          </div>
        ))}
      </div>

      {/* Flip Control */}
      <div className="mt-10 mb-4 flex justify-between items-center">
        <h3 className="text-md font-bold text-pink-600">{isHistory ? 'Trade History' : 'Open Positions'}</h3>
        <button onClick={togglePanel} className="flex items-center text-sm text-blue-500 hover:text-blue-600">
          <FiRefreshCw className="mr-1" /> Flip
        </button>
      </div>

      {/* Trade Panel */}
      <div className="bg-white p-4 rounded-xl shadow border border-slate-300">
        {(isHistory ? tradeHistory : openPositions).map((trade, i) => (
          <div key={i} className="mb-4">
            <p className="mb-1">
              {trade.symbol} <span className="text-blue-700 font-medium">{trade.gain}</span>
            </p>
            <TradeStatusCard symbol={trade.symbol} tp={trade.tp} sl={trade.sl} />
          </div>
        ))}
      </div>
    </div>
  )
}

export default DashboardLightFlip
