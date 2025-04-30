// frontend/src/components/Dashboard/AccountEquityChart.jsx

import React from 'react';
import { LineChart, Line, XAxis, YAxis, Tooltip, Legend, ResponsiveContainer } from 'recharts';

const AccountEquityChart = ({ equityHistory }) => (
  <ResponsiveContainer width="100%" height={200}>
    <LineChart data={equityHistory}>
      <XAxis dataKey="timestamp" tick={{ fontSize: 12 }} />
      <YAxis />
      <Tooltip />
      <Legend />
      <Line type="monotone" dataKey="balance" stroke="#82ca9d" name="Balance" />
      <Line type="monotone" dataKey="margin" stroke="#8884d8" name="Margin" />
    </LineChart>
  </ResponsiveContainer>
);

export default AccountEquityChart;
