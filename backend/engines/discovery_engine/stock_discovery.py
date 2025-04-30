from backend.utils.market_data import StockMarketData

class StockDiscoveryEngine:
    def __init__(self, broker_client, strategy):
        self.broker_client = broker_client
        self.strategy = strategy
        self.market_data = StockMarketData(broker_client)
        self.liquidity_floor = 2_000_000  # Minimum daily volume
        self.blacklist = ["XYZQ", "ABCD"]  # Example blacklist

    async def find_symbols(self):
        symbols = await self.market_data.get_symbols()
        qualified_symbols = []

        for symbol in symbols:
            try:
                if symbol in self.blacklist:
                    continue  # Exclude blacklisted stocks

                data = await self.market_data.get_symbol_data(symbol)

                # Global liquidity filter
                if data.get('volume_24h', 0) < self.liquidity_floor:
                    continue

                # Strategy-specific filters
                if self.strategy == "freshman":
                    if (data['market_cap'] <= 500_000_000 and 
                        data['rsi'] > 55 and 
                        data['macd'] > 0 and 
                        data['ema_5'] > data['ema_20']):
                        qualified_symbols.append(symbol)

                elif self.strategy == "top_volume":
                    if (data['volume_24h'] >= 10_000_000 and 
                        data['rsi'] > 50 and 
                        data['macd'] > 0):
                        qualified_symbols.append(symbol)

                elif self.strategy == "large_cap":
                    if (data['market_cap'] >= 10_000_000_000 and 
                        data['rsi'] > 50 and 
                        data['macd'] > 0 and 
                        data['atr'] < 5):
                        qualified_symbols.append(symbol)

                elif self.strategy == "super_leverage":
                    if (data['is_etf'] and data['leverage'] > 1 and 
                        data['rsi'] > 50 and 
                        data['macd'] > 0):
                        qualified_symbols.append(symbol)

                elif self.strategy == "cameron":
                    # Cameron Strategy: $1-$10 price, RVOL ≥ 5, volume ≥ 100k, float ≤ 20M
                    if (1 <= data['price'] <= 10 and 
                        data.get('rvol', 0) >= 5 and 
                        data['volume_24h'] >= 100_000 and 
                        data.get('float', 0) <= 20_000_000):
                        qualified_symbols.append(symbol)

            except Exception as e:
                # Optionally log symbol errors
                continue

        return qualified_symbols
