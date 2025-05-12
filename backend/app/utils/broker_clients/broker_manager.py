# backend/utils/broker_clients/broker_manager.py

from app.utils.broker_clients.coinbase_client import CoinbaseClient
from app.utils.broker_clients.binance_client import BinanceClient
from app.utils.broker_clients.kraken_client import KrakenClient
from app.utils.broker_clients.bitfinex_client import BitfinexClient
from app.utils.broker_clients.etrade_client import ETradeClient
from app.utils.broker_clients.metamask_client import MetaMaskClient
from app.utils.broker_clients.trust_wallet_client import TrustWalletClient
from app.utils.broker_clients.coinbase_wallet_client import CoinbaseWalletClient
from app.utils.broker_clients.robinhood_client import RobinhoodClient
from app.utils.broker_clients.interactive_brokers_client import InteractiveBrokersClient
from app.utils.broker_clients.gemini_client import GeminiClient
from app.utils.broker_clients.schwab_client import SchwabClient
from app.utils.broker_clients.tastytrade_client import TastyTradeClient


class BrokerManager:
    @staticmethod
    def create_client(broker_name: str, credentials: dict, test_mode: bool = False):
        broker = broker_name.lower()

        if broker == "coinbase":
            return CoinbaseClient(
                api_key=credentials["api_key"],
                api_secret=credentials["api_secret"],
                passphrase=credentials["passphrase"],
                test_mode=test_mode
            )

        elif broker == "binance":
            return BinanceClient(
                api_key=credentials["api_key"],
                api_secret=credentials["api_secret"],
                test_mode=test_mode
            )

        elif broker == "kraken":
            return KrakenClient(
                api_key=credentials["api_key"],
                api_secret=credentials["api_secret"],
                test_mode=test_mode
            )

        elif broker == "bitfinex":
            return BitfinexClient(
                api_key=credentials["api_key"],
                api_secret=credentials["api_secret"],
                test_mode=test_mode
            )

        elif broker == "etrade":
            return ETradeClient(
                api_key=credentials["api_key"],
                api_secret=credentials["api_secret"],
                oauth_token=credentials["oauth_token"],
                oauth_token_secret=credentials["oauth_token_secret"]
            )

        elif broker == "metamask":
            return MetaMaskClient(
                wallet_address=credentials["wallet_address"],
                rpc_url=credentials.get("rpc_url", "https://mainnet.infura.io/v3/YOUR_INFURA_PROJECT_ID"),
                test_mode=test_mode
            )

        elif broker == "trustwallet":
            return TrustWalletClient(
                wallet_address=credentials["wallet_address"],
                rpc_url=credentials.get("rpc_url", "https://rpc.ankr.com/eth"),
                test_mode=test_mode
            )

        elif broker == "coinbasewallet":
            return CoinbaseWalletClient(
                wallet_address=credentials["wallet_address"],
                rpc_url=credentials.get("rpc_url", "https://rpc.ankr.com/eth"),
                test_mode=test_mode
            )

        elif broker == "robinhood":
            return RobinhoodClient(
                username=credentials["username"],
                password=credentials["password"],
                test_mode=test_mode
            )

        elif broker == "interactivebrokers":
            return InteractiveBrokersClient(
                api_key=credentials["api_key"],
                account_id=credentials["account_id"],
                test_mode=test_mode
            )

        elif broker == "gemini":
            return GeminiClient(
                api_key=credentials["api_key"],
                api_secret=credentials["api_secret"],
                test_mode=test_mode
            )

        elif broker == "schwab":
            return SchwabClient(
                client_id=credentials["client_id"],
                client_secret=credentials["client_secret"],
                test_mode=test_mode
            )

        elif broker == "tastytrade":
            return TastyTradeClient(
                username=credentials["username"],
                password=credentials["password"],
                test_mode=test_mode
            )

        else:
            raise ValueError(f"Unsupported broker or wallet type: {broker_name}")
