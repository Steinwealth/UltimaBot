# backend/app/engines/discovery_engine/stock_discovery.py

from app.engines.discovery_engine.market_data import StockMarketData

class StockDiscoveryEngine:
    def __init__(self, broker_client, strategy: str):
        self.broker_client = broker_client
        self.strategy = strategy
        self.market_data = StockMarketData(broker_client)
        self.liquidity_floor = 2_000_000  # Minimum daily volume
        self.blacklist = ["XYZQ", "ABCD"]  # Example ticker blacklist

    async def find_symbols(self):
        """
        Main method to return qualified symbols using the selected strategy.
        """
        symbols = await self.market_data.get_broker_symbols()
        qualified_symbols = []

        for symbol in symbols:
            try:
                if symbol in self.blacklist:
                    continue

                data = await self.market_data.get_symbol_data(symbol)
                if data.get("volume_24h", 0) < self.liquidity_floor:
                    continue

                if self._apply_strategy_filters(data):
                    qualified_symbols.append(symbol)

            except Exception:
                continue  # Optionally log for debugging

        return qualified_symbols

    def _apply_strategy_filters(self, data):
        """
        Applies strategy-specific rules on the given stock data.
        """
        try:
            if self.strategy == "freshman":
                return (
                    data["market_cap"] <= 500_000_000
                    and data["rsi"] > 55
                    and data["macd"] > 0
                    and data.get("ema_5", 0) > data.get("ema_20", 0)
                )

            elif self.strategy == "top_volume":
                return (
                    data["volume_24h"] >= 10_000_000
                    and data["rsi"] > 50
                    and data["macd"] > 0
                )

            elif self.strategy == "large_cap":
                return (
                    data["market_cap"] >= 10_000_000_000
                    and data["rsi"] > 50
                    and data["macd"] > 0
                    and data.get("atr", 999) < 5
                )

            elif self.strategy == "super_leverage":
                return (
                    data.get("is_etf", False)
                    and data.get("leverage", 1) > 1
                    and data["rsi"] > 50
                    and data["macd"] > 0
                )

            elif self.strategy == "cameron":
                return (
                    1 <= data["price"] <= 10
                    and data.get("rvol", 0) >= 5
                    and data["volume_24h"] >= 100_000
                    and data.get("float", 0) <= 20_000_000
                )

        except KeyError:
            return False

        return False
