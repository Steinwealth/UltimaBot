from backend.utils.market_data import CryptoMarketData

class CryptoDiscoveryEngine:
    def __init__(self, broker_client, strategy=None):
        self.broker_client = broker_client
        self.strategy = strategy
        self.market_data = CryptoMarketData(broker_client)
        self.liquidity_floor = 1_000_000  # Global liquidity floor

    async def find_symbols(self):
        # Define prioritization and target allocation per strategy
        target_per_strategy = {
            "CoinMarketCap": 8,
            "Micro Cap Moonshot": 6,
            "100X Volume Spike": 6,
            "PumpFun_Trending": 5,
            "GMGN_Trending": 5,
            "Original": 5,
            "Mid-Low Cap": 5,
        }
        priority_order = list(target_per_strategy.keys())

        # Collect symbols from each strategy
        strategy_outputs = {}
        for strat in target_per_strategy:
            self.strategy = strat
            symbols = await self._discover_strategy()
            strategy_outputs[strat] = symbols

        # Combine symbols by priority, respecting target allocation
        combined_symbols = []
        for strat in priority_order:
            allocated = strategy_outputs.get(strat, [])[:target_per_strategy[strat]]
            combined_symbols.extend(allocated)

        return combined_symbols

    async def _discover_strategy(self):
        if self.strategy == "CoinMarketCap":
            return await self._discover_coinmarketcap()
        elif self.strategy == "GMGN_Trending":
            return await self._discover_gmgn_trending()
        elif self.strategy == "PumpFun_Trending":
            return await self._discover_pumpfun_trending()
        elif self.strategy in ["Original", "100X Volume Spike", "Mid-Low Cap", "Micro Cap Moonshot"]:
            return await self._discover_broker_based()
        else:
            return []

    async def _discover_coinmarketcap(self):
        broker_symbols = await self.market_data.get_broker_symbols(volume_filter=True)
        cmc_new = await self.market_data.get_cmc_new_coins_filtered()
        cmc_trending = await self.market_data.get_cmc_trending_sorted()

        symbols = []
        for cmc_list in [cmc_new, cmc_trending]:
            for symbol, data in cmc_list.items():
                if data.get('volume_24h', 0) >= self.liquidity_floor and symbol in broker_symbols:
                    symbols.append(symbol)
        return symbols

    async def _discover_gmgn_trending(self):
        broker_symbols = await self.market_data.get_broker_symbols(volume_filter=True)
        gmgn_trending = await self.market_data.get_gmgn_trending()
        return [symbol for symbol in broker_symbols if symbol in gmgn_trending]

    async def _discover_pumpfun_trending(self):
        broker_symbols = await self.market_data.get_broker_symbols(volume_filter=True)
        pumpfun_trending = await self.market_data.get_pumpfun_trending()
        return [symbol for symbol in broker_symbols if symbol in pumpfun_trending]

    async def _discover_broker_based(self):
        broker_symbols = await self.market_data.get_broker_symbols(volume_filter=True)
        qualified_symbols = []

        for symbol in broker_symbols:
            try:
                data = await self.market_data.get_symbol_data(symbol)
                cmc_symbol_data = await self.market_data.get_cmc_symbol_data(symbol)

                if not cmc_symbol_data or cmc_symbol_data.get('volume_24h', 0) < self.liquidity_floor:
                    continue

                atr_percent = data['atr'] / data['price'] if data['price'] > 0 else 0
                if atr_percent > 0.05:
                    continue

                if data.get('ema_5m') <= data.get('ema_15m'):
                    continue

                # Enhance: Confidence-weighted filters (example threshold: 0.95)
                confidence = data.get('confidence', 0.0)
                if confidence < 0.95:
                    continue

                if self.strategy == "Original":
                    if data['volume'] > 500_000 and data['rsi'] > 55 and data['macd'] > 0:
                        qualified_symbols.append(symbol)

                elif self.strategy == "100X Volume Spike":
                    if (data['volume_spike_5m'] >= 500_000 and data['recent_spike_candles'] <= 2 and
                        data['rsi'] > 55 and data['macd'] > 0 and data['velocity'] > 0.03):
                        qualified_symbols.append(symbol)

                elif self.strategy == "Mid-Low Cap":
                    volume_market_cap_ratio = cmc_symbol_data['volume_24h'] / cmc_symbol_data['market_cap'] if cmc_symbol_data['market_cap'] > 0 else 0
                    if (cmc_symbol_data['market_cap'] <= 1_500_000 and data['volume'] > 300_000 and
                        data['rsi'] > 55 and volume_market_cap_ratio > 0.5):
                        qualified_symbols.append(symbol)

                elif self.strategy == "Micro Cap Moonshot":
                    if (cmc_symbol_data['market_cap'] <= 1_000_000 and data['volume_spike_5m'] >= 250_000 and
                        data['atr'] > 0.01 and data['velocity'] > 0.05):
                        qualified_symbols.append(symbol)

            except Exception as e:
                continue

        return qualified_symbols
