import React, { useEffect, useState } from 'react';
import { LineChart, Line, XAxis, YAxis, Tooltip, ResponsiveContainer } from 'recharts';

const ChartsPanel = () => {
  const [equityData, setEquityData] = useState([]);
  const [pnlData, setPnlData] = useState([]);

  useEffect(() => {
    const socket = new WebSocket('wss://chart-data-feed');
    socket.onmessage = (event) => {
      const data = JSON.parse(event.data);
      if (data.type === 'equity') {
        setEquityData((prev) => [...prev.slice(-49), data.payload]);
      } else if (data.type === 'pnl') {
        setPnlData((prev) => [...prev.slice(-49), data.payload]);
      }
    };
    return () => socket.close();
  }, []);

  return (
    <div className="grid grid-cols-1 gap-6 md:grid-cols-2">
      {/* Equity Curve */}
      <div className="p-4 bg-gray-100 border border-gray-300 rounded-lg dark:bg-gray-800 dark:border-gray-700">
        <h3 className="mb-2 text-lg font-semibold text-gray-900 dark:text-white">Equity Curve</h3>
        <ResponsiveContainer width="100%" height={200}>
          <LineChart data={equityData}>
            <XAxis dataKey="time" hide />
            <YAxis domain={['auto', 'auto']} />
            <Tooltip />
            <Line type="monotone" dataKey="balance" stroke="var(--logo-color)" strokeWidth={2} dot={false} />
          </LineChart>
        </ResponsiveContainer>
      </div>

      {/* PnL Chart */}
      <div className="p-4 bg-gray-100 border border-gray-300 rounded-lg dark:bg-gray-800 dark:border-gray-700">
        <h3 className="mb-2 text-lg font-semibold text-gray-900 dark:text-white">PnL Chart</h3>
        <ResponsiveContainer width="100%" height={200}>
          <LineChart data={pnlData}>
            <XAxis dataKey="time" hide />
            <YAxis domain={['auto', 'auto']} />
            <Tooltip />
            <Line type="monotone" dataKey="pnl" stroke="var(--logo-color)" strokeWidth={2} dot={false} />
          </LineChart>
        </ResponsiveContainer>
      </div>
    </div>
  );
};

export default ChartsPanel;
