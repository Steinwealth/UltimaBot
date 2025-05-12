# backend/app/engines/discovery_engine/market_data.py

import aiohttp

class CryptoMarketData:
    def __init__(self, broker_client):
        self.broker_client = broker_client
        self.session = aiohttp.ClientSession()

    async def get_broker_symbols(self, volume_filter=False):
        """
        Returns broker symbols. Applies volume filter if specified.
        """
        symbols = await self.broker_client.get_symbols()
        if volume_filter:
            symbols = [s for s in symbols if s.get('volume_24h', 0) >= 1_000_000]
        return [s['symbol'] for s in symbols if 'symbol' in s]

    async def get_cmc_new_coins_filtered(self):
        """
        Simulated CoinMarketCap fetch for new coins.
        """
        return {
            'SKITTEN': {'volume_24h': 4_803_383},
            'SMS': {'volume_24h': 3_954_617},
            '$GOLD': {'volume_24h': 5_409_807},
        }

    async def get_cmc_trending_sorted(self):
        """
        Simulated CoinMarketCap trending coins by volume.
        """
        return {
            'ALPACA': {'volume_24h': 323_887_691},
            'BSV': {'volume_24h': 443_875_452},
        }

    async def get_gmgn_trending(self):
        """
        Simulated GMGN trending symbols.
        """
        return ['ZAC', 'MUBARA']

    async def get_pumpfun_trending(self):
        """
        Simulated Pump.Fun trending symbols.
        """
        return ['ZALA', 'TRENCHER']

    async def get_symbol_data(self, symbol):
        """
        Simulated symbol analysis data.
        """
        return {
            'price': 1.00,
            'volume': 500_000,
            'rsi': 60,
            'macd': 0.5,
            'ema_5m': 1.01,
            'ema_15m': 1.00,
            'atr': 0.02,
            'velocity': 0.04,
            'volume_spike_5m': 600_000,
            'recent_spike_candles': 1,
            'confidence': 0.96,
        }

    async def get_cmc_symbol_data(self, symbol):
        """
        Simulated CMC volume/market cap data for a coin.
        """
        return {
            'volume_24h': 5_000_000,
            'market_cap': 1_200_000,
        }

    async def close(self):
        """Close the aiohttp session to prevent leaks."""
        if not self.session.closed:
            await self.session.close()


class StockMarketData:
    def __init__(self, broker_client):
        self.broker_client = broker_client

    async def get_broker_symbols(self):
        """
        Returns tradable stock symbols from broker.
        """
        return await self.broker_client.get_symbols()

    async def get_symbol_data(self, symbol):
        """
        Simulated stock data for Discovery Engine filtering.
        """
        return {
            'price': 10.0,
            'volume_24h': 600_000,
            'market_cap': 2_000_000_000,
            'rsi': 58,
            'is_leveraged_etf': False,
            'macd': 0.4,
            'ema_5': 10.3,
            'ema_20': 10.1,
            'atr': 0.6,
            'rvol': 7.1,
            'float': 18_000_000,
            'leverage': 3,
            'is_etf': True
        }
