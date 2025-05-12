import { useState, useEffect } from 'react';
import axios from 'axios';

const useTradeData = () => {
  const [openTrades, setOpenTrades] = useState([]);
  const [tradeHistory, setTradeHistory] = useState([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  const fetchTrades = async () => {
    setLoading(true);
    try {
      const [openRes, historyRes] = await Promise.all([
        axios.get('/api/trades/open'),
        axios.get('/api/trades/history'),
      ]);
      setOpenTrades(openRes.data);
      setTradeHistory(historyRes.data);
      setError(null);
    } catch (err) {
      setError(err);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchTrades();
    const interval = setInterval(fetchTrades, 10000); // Refresh every 10 seconds
    return () => clearInterval(interval);
  }, []);

  return { openTrades, tradeHistory, loading, error };
};

export default useTradeData;
