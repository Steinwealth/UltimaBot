import React, { useEffect, useState } from 'react';
import { Card, CardContent } from "@/window/components/ui/card";
import { Line } from "react-chartjs-2";
import Chart from "chart.js/auto";
import { useTheme } from "@/hooks/useTheme";

const OpenTrades = () => {
  const { theme } = useTheme();
  const [trades, setTrades] = useState([]);
  const [page, setPage] = useState(1);
  const TRADES_PER_PAGE = 10;

  useEffect(() => {
    if (import.meta.env.MODE === 'development') {
      // Inject 20 mock trades for testing UI
      const mock = Array.from({ length: 20 }, (_, i) => {
        const entry = 100 + i;
        const tp = entry + 10;
        const sl = entry - 10;
        return {
          trade_id: `MOCK-${i}`,
          symbol: ['BTC', 'ETH', 'SOL', 'ADA'][i % 4],
          entry_price: entry,
          take_profit: tp,
          stop_loss: sl,
          pnl: parseFloat((Math.random() * 30 - 5).toFixed(2)),
          confidence: 0.96 + Math.random() * 0.04,
          price_history: Array.from({ length: 30 }, (_, j) => entry + Math.sin(j / 5) + Math.random())
        };
      });
      setTrades(mock);
    } else {
      const socket = new WebSocket('wss://trade-updates-feed');
      socket.onmessage = (event) => {
        try {
          const update = JSON.parse(event.data);
          setTrades((prev) => {
            const exists = prev.find((t) => t.trade_id === update.trade_id);
            return exists
              ? prev.map((t) => (t.trade_id === update.trade_id ? update : t))
              : [...prev, update];
          });
        } catch (err) {
          console.error("WebSocket error:", err);
        }
      };
      return () => socket.close();
    }
  }, []);

  const sortedTrades = trades
    .filter((t) => t.pnl !== undefined)
    .sort((a, b) => b.pnl - a.pnl);

  const paginated = sortedTrades.slice((page - 1) * TRADES_PER_PAGE, page * TRADES_PER_PAGE);

  return (
    <div className="flex flex-col gap-4 overflow-y-auto max-h-[calc(100vh-300px)] px-1">
      {paginated.length > 0 ? (
        paginated.map((trade) => {
          const chartData = {
            labels: trade.price_history?.map((_, idx) => idx),
            datasets: [
              {
                label: "Price Path",
                data: trade.price_history || [],
                borderColor: "#3b82f6",
                backgroundColor: "transparent",
                tension: 0.4,
              },
              {
                label: "Entry",
                data: new Array(trade.price_history?.length).fill(trade.entry_price),
                borderColor: "#6b7280",
                borderDash: [5, 5],
                pointRadius: 0,
              },
              {
                label: "TP",
                data: new Array(trade.price_history?.length).fill(trade.take_profit),
                borderColor: "#10b981",
                borderDash: [5, 5],
                pointRadius: 0,
              },
              {
                label: "SL",
                data: new Array(trade.price_history?.length).fill(trade.stop_loss),
                borderColor: "#ef4444",
                borderDash: [5, 5],
                pointRadius: 0,
              },
            ],
          };

          const chartOptions = {
            responsive: true,
            plugins: { legend: { display: false } },
            scales: {
              x: { display: false },
              y: {
                ticks: {
                  color: theme === "dark" ? "#fff" : "#111",
                  callback: (val) => `$${val.toFixed(2)}`
                },
              },
            },
          };

          const confidence = (trade.confidence || 0).toFixed(3);
          const pnlColor = trade.pnl >= 0 ? "text-green-500" : "text-red-500";
          const confidenceColor = (trade.confidence ?? 0) >= 0.974 ? "text-green-400" : "text-red-400";

          return (
            <Card key={trade.trade_id} className="rounded-2xl shadow-md dark:bg-gray-900 bg-white relative">
              <CardContent className="p-4">
                <div className={`absolute top-4 right-6 font-bold ${confidenceColor}`} style={{ fontSize: 50 }}>
                  % {confidence}
                </div>

                <div className="mb-2 text-lg font-bold dark:text-white">{trade.symbol}</div>

                <div className="h-48">
                  <Line data={chartData} options={chartOptions} />
                </div>

                <div className="flex justify-between mt-3 text-sm dark:text-gray-300 text-gray-700">
                  <div>Entry: ${trade.entry_price?.toFixed(2) || '--'}</div>
                  <div className={pnlColor}>PnL: {trade.pnl?.toFixed(2)}%</div>
                </div>
              </CardContent>
            </Card>
          );
        })
      ) : (
        <div className="text-center py-10 text-gray-600 dark:text-gray-400">No open trades</div>
      )}

      {/* Pagination Controls */}
      {sortedTrades.length > TRADES_PER_PAGE && (
        <div className="flex justify-center mt-2 gap-4">
          <button
            className="px-3 py-1 bg-gray-300 rounded dark:bg-gray-700 text-sm"
            onClick={() => setPage((p) => Math.max(1, p - 1))}
          >
            Prev
          </button>
          <span className="text-sm font-medium dark:text-white">{page}</span>
          <button
            className="px-3 py-1 bg-gray-300 rounded dark:bg-gray-700 text-sm"
            onClick={() => setPage((p) => p + 1)}
          >
            Next
          </button>
        </div>
      )}
    </div>
  );
};

export default OpenTrades;
