# backend/app/engines/discovery_engine/crypto_discovery_engine.py

from app.engines.discovery_engine.market_data import CryptoMarketData

class CryptoDiscoveryEngine:
    def __init__(self, broker_client, strategy: str = None):
        self.broker_client = broker_client
        self.strategy = strategy
        self.market_data = CryptoMarketData(broker_client)
        self.liquidity_floor = 1_000_000  # Minimum volume filter

    async def find_symbols(self):
        """
        Run all discovery strategies and return a combined prioritized list of symbols.
        """
        target_per_strategy = {
            "CoinMarketCap": 8,
            "Micro Cap Moonshot": 6,
            "100X Volume Spike": 6,
            "PumpFun_Trending": 5,
            "GMGN_Trending": 5,
            "Original": 5,
            "Mid-Low Cap": 5,
        }

        combined_symbols = []
        for strat in target_per_strategy:
            self.strategy = strat
            symbols = await self._discover_strategy()
            combined_symbols.extend(symbols[:target_per_strategy[strat]])

        return combined_symbols

    async def _discover_strategy(self):
        """
        Delegates symbol discovery to the appropriate strategy method.
        """
        if self.strategy == "CoinMarketCap":
            return await self._discover_coinmarketcap()
        elif self.strategy == "GMGN_Trending":
            return await self._discover_gmgn_trending()
        elif self.strategy == "PumpFun_Trending":
            return await self._discover_pumpfun_trending()
        elif self.strategy in ["Original", "100X Volume Spike", "Mid-Low Cap", "Micro Cap Moonshot"]:
            return await self._discover_broker_based()
        return []

    async def _discover_coinmarketcap(self):
        broker_symbols = await self.market_data.get_broker_symbols(volume_filter=True)
        cmc_new = await self.market_data.get_cmc_new_coins_filtered()
        cmc_trending = await self.market_data.get_cmc_trending_sorted()

        symbols = []
        for source in [cmc_new, cmc_trending]:
            for symbol, data in source.items():
                if data.get("volume_24h", 0) >= self.liquidity_floor and symbol in broker_symbols:
                    symbols.append(symbol)
        return symbols

    async def _discover_gmgn_trending(self):
        broker_symbols = await self.market_data.get_broker_symbols(volume_filter=True)
        gmgn_trending = await self.market_data.get_gmgn_trending()
        return [s for s in broker_symbols if s in gmgn_trending]

    async def _discover_pumpfun_trending(self):
        broker_symbols = await self.market_data.get_broker_symbols(volume_filter=True)
        pumpfun_trending = await self.market_data.get_pumpfun_trending()
        return [s for s in broker_symbols if s in pumpfun_trending]

    async def _discover_broker_based(self):
        broker_symbols = await self.market_data.get_broker_symbols(volume_filter=True)
        results = []

        for symbol in broker_symbols:
            try:
                data = await self.market_data.get_symbol_data(symbol)
                cmc_data = await self.market_data.get_cmc_symbol_data(symbol)
                if not cmc_data or cmc_data.get("volume_24h", 0) < self.liquidity_floor:
                    continue

                # Filters
                atr_pct = data["atr"] / data["price"] if data["price"] > 0 else 0
                if atr_pct > 0.05:
                    continue
                if data.get("ema_5m", 0) <= data.get("ema_15m", 0):
                    continue
                if data.get("confidence", 0) < 0.95:
                    continue

                # Strategy-specific logic
                if self.strategy == "Original":
                    if data["volume"] > 500_000 and data["rsi"] > 55 and data["macd"] > 0:
                        results.append(symbol)

                elif self.strategy == "100X Volume Spike":
                    if (data["volume_spike_5m"] >= 500_000 and data["recent_spike_candles"] <= 2 and
                        data["rsi"] > 55 and data["macd"] > 0 and data["velocity"] > 0.03):
                        results.append(symbol)

                elif self.strategy == "Mid-Low Cap":
                    market_cap = cmc_data.get("market_cap", 0)
                    vol = cmc_data.get("volume_24h", 0)
                    if market_cap <= 1_500_000 and data["volume"] > 300_000 and data["rsi"] > 55 and vol / market_cap > 0.5:
                        results.append(symbol)

                elif self.strategy == "Micro Cap Moonshot":
                    if (cmc_data.get("market_cap", 0) <= 1_000_000 and
                        data["volume_spike_5m"] >= 250_000 and data["atr"] > 0.01 and data["velocity"] > 0.05):
                        results.append(symbol)

            except Exception:
                continue  # Continue safely on failure

        return results
