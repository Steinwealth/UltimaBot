import React, { useState } from 'react';
import { X } from 'lucide-react';

const BrokerLoginOverlay = ({ onClose, onSuccess }) => {
  const [broker, setBroker] = useState('');
  const [apiKey, setApiKey] = useState('');
  const [apiSecret, setApiSecret] = useState('');
  const [loading, setLoading] = useState(false);

  const isWallet = ['metamask', 'trustwallet', 'coinbasewallet'].includes(broker);

  const formatName = (str) => str.charAt(0).toUpperCase() + str.slice(1);

  const handleConnect = async () => {
    if (!broker) return alert("Please select a broker or wallet.");

    if (!isWallet) {
      if (!apiKey || !apiSecret) return alert("Please enter your API credentials.");

      const brokerData = {
        type: 'cex',
        name: formatName(broker),
        account_id: `${broker.toUpperCase()}-ACC-${Math.floor(Math.random() * 1000)}`,
        balance: 12500,
        margin: 72,
      };

      onSuccess(brokerData);
      onClose();
    }

    if (broker === 'metamask') {
      if (typeof window.ethereum === 'undefined') {
        alert("MetaMask is not installed.");
        return;
      }

      try {
        setLoading(true);
        const accounts = await window.ethereum.request({ method: 'eth_requestAccounts' });
        const walletAddress = accounts[0];
        const walletData = {
          type: 'wallet',
          name: 'MetaMask',
          account_id: walletAddress,
          balance: 0,
          margin: 0,
        };
        onSuccess(walletData);
        onClose();
      } catch (err) {
        alert("MetaMask login failed.");
        console.error(err);
      } finally {
        setLoading(false);
      }
    }

    if (broker === 'trustwallet' || broker === 'coinbasewallet') {
      alert(`${formatName(broker)} login is not yet supported. Please use MetaMask or a CEX broker for now.`);
    }
  };

  return (
    <div className="relative w-full max-w-md p-6 bg-gray-900 border border-gray-700 rounded-xl shadow-2xl">
      {/* Close Button */}
      <button
        onClick={onClose}
        className="absolute top-2 right-2 p-1 text-white hover:text-red-400"
      >
        <X className="w-5 h-5" />
      </button>

      <h2 className="mb-4 text-xl font-semibold text-white">Add Broker / Wallet</h2>

      {/* Broker Dropdown */}
      <label htmlFor="broker" className="block mb-2 text-sm text-gray-400">Select Broker or Wallet:</label>
      <select
        id="broker"
        className="w-full px-3 py-2 mb-4 text-white bg-black border border-gray-600 rounded focus:outline-none focus:ring-2 focus:ring-blue-500"
        value={broker}
        onChange={(e) => setBroker(e.target.value)}
      >
        <option value="">-- Select --</option>
        <option value="metamask">MetaMask</option>
        <option value="trustwallet">Trust Wallet</option>
        <option value="coinbasewallet">Coinbase Wallet</option>
        <option value="robinhood">Robinhood</option>
        <option value="coinbase">Coinbase</option>
        <option value="binance">Binance</option>
        <option value="kraken">Kraken</option>
        <option value="bitfinex">Bitfinex</option>
        <option value="etrade">E*TRADE</option>
        <option value="ibkr">Interactive Brokers</option>
      </select>

      {/* API Key / Secret for CEX brokers */}
      {!isWallet && broker && (
        <>
          <label htmlFor="apiKey" className="block mb-1 text-sm text-gray-400">API Key:</label>
          <input
            id="apiKey"
            type="text"
            value={apiKey}
            onChange={(e) => setApiKey(e.target.value)}
            className="w-full px-3 py-2 mb-4 text-white bg-black border border-gray-600 rounded focus:outline-none focus:ring-2 focus:ring-blue-500"
            placeholder="Enter your API Key"
          />

          <label htmlFor="apiSecret" className="block mb-1 text-sm text-gray-400">API Secret:</label>
          <input
            id="apiSecret"
            type="password"
            value={apiSecret}
            onChange={(e) => setApiSecret(e.target.value)}
            className="w-full px-3 py-2 mb-4 text-white bg-black border border-gray-600 rounded focus:outline-none focus:ring-2 focus:ring-blue-500"
            placeholder="Enter your API Secret"
          />
        </>
      )}

      <button
        onClick={handleConnect}
        disabled={loading || !broker}
        className={`w-full px-4 py-2 text-black bg-green-400 rounded hover:bg-green-300 ${!broker ? 'cursor-not-allowed opacity-50' : ''}`}
      >
        {loading ? 'Connecting...' : 'Connect'}
      </button>
    </div>
  );
};

export default BrokerLoginOverlay;
