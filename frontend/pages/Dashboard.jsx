import React, { useState } from 'react';
import AccountInfoPanel from '@/components/AccountInfoPanel';
import StrategyPanel from '@/components/StrategyPanel';
import ModelSelectionPanel from '@/components/ModelSelectionPanel';
import ModelViewerPanel from '@/components/ModelViewerPanel';
import TradePanel from '@/components/TradePanel';
import MarqueeBar from '@/components/MarqueeBar';
// import MarketSentimentPanel from '@/components/MarketSentimentPanel'; // Optional

// Mock data for preview/testing
const mockBrokers = [
  {
    id: 'CB-001',
    name: 'Coinbase',
    account: { balance: 14820.32, margin: 83.5 }
  },
  {
    id: 'ET-002',
    name: 'E*TRADE',
    account: { balance: 26450.19, margin: 91.2 }
  }
];

const mockModels = [
  {
    name: 'Radiant',
    type: 'Crypto Model',
    accuracy: 0.984,
    confidenceThreshold: 0.95,
    riskMode: 'Easy Mode',
    tpLogic: 'Dynamic TP v4.5',
    slLogic: 'Adaptive SL Lock',
    compounding: true,
    streakScaling: true,
    multiEntry: true,
    description:
      'Radiant identifies momentum breakouts across crypto pairs using adaptive gain logic and trailing forecast.',
    performance: [
      'Win Rate: 98.4%',
      'Max Drawdown: 2.6%',
      'Avg Gain: 3.8%',
      'Avg Trades/Day: 21.7'
    ],
    roles: ['Discovery', 'Forecast Engine', 'Gain Optimizer']
  },
  {
    name: 'Dianastone',
    type: 'Stock Model',
    accuracy: 0.961,
    confidenceThreshold: 0.96,
    riskMode: 'Hard Mode',
    tpLogic: 'Forecast Trail Optimizer',
    slLogic: 'Drawdown Guard v3.0',
    compounding: true,
    streakScaling: true,
    multiEntry: false,
    description:
      'Dianastone uses institutional order flow and RSI breakouts to guide precision stock entries with safe exits.',
    performance: [
      'Win Rate: 97.1%',
      'Max Drawdown: 3.1%',
      'Avg Gain: 3.3%',
      'Avg Trades/Day: 6.9'
    ],
    roles: ['Strategy Engine', 'Risk Engine', 'SL Curve Logic']
  }
];

export default function Dashboard() {
  const [pairedModels, setPairedModels] = useState({}); // key: brokerId

  const handleModelPair = (brokerId, model) => {
    setPairedModels((prev) => ({ ...prev, [brokerId]: model }));
  };

  return (
    <div className="min-h-screen bg-neutral-950 text-white pb-20 px-4 pt-6">
      <h1 className="text-2xl font-bold mb-4">Ultima Bot Dashboard</h1>

      <div className="grid gap-6">
        {mockBrokers.map((broker) => (
          <div key={broker.id} className="grid grid-cols-1 md:grid-cols-3 gap-4">
            {/* LEFT: Account Info */}
            <AccountInfoPanel
              broker={broker}
              account={broker.account}
              pairedModel={pairedModels[broker.id]}
              onStartTrading={() =>
                console.log(`Start trading on ${broker.name} with model`, pairedModels[broker.id])
              }
              onPairModel={() => console.log(`Select model for ${broker.name}`)}
            />

            {/* CENTER: Strategy Panel */}
            <StrategyPanel model={pairedModels[broker.id]} />

            {/* RIGHT: Model Viewer */}
            <ModelViewerPanel model={pairedModels[broker.id]} />
          </div>
        ))}

        {/* MODEL SELECTION */}
        <ModelSelectionPanel
          models={mockModels}
          onModelPair={(model) => handleModelPair(mockBrokers[0].id, model)}
        />

        {/* TRADE PANEL */}
        <TradePanel />

        {/* MARKET SENTIMENT PANEL (optional) */}
        {/* <MarketSentimentPanel /> */}
      </div>

      <MarqueeBar />
    </div>
  );
}
