# backend/utils/broker_clients/trust_wallet_client.py

from web3 import Web3
from decimal import Decimal

class TrustWalletClient:
    def __init__(self, wallet_address: str, rpc_url: str = "https://polygon-rpc.com", test_mode: bool = False):
        self.wallet_address = Web3.to_checksum_address(wallet_address)
        self.rpc_url = rpc_url
        self.web3 = Web3(Web3.HTTPProvider(rpc_url))
        self.logged_in = False
        self.test_mode = test_mode

    async def login(self, wallet_address=None, rpc_url=None):
        if wallet_address:
            self.wallet_address = Web3.to_checksum_address(wallet_address)
        if rpc_url:
            self.rpc_url = rpc_url
            self.web3 = Web3(Web3.HTTPProvider(rpc_url))

        if self.test_mode:
            self.logged_in = True
            return True

        if not self.web3.isConnected():
            raise ConnectionError("Trust Wallet RPC connection failed")

        if not self.web3.is_address(self.wallet_address):
            raise ValueError("Invalid Ethereum wallet address")

        self.logged_in = True
        return True

    async def is_logged_in(self):
        return self.logged_in

    async def logout(self):
        self.logged_in = False

    async def get_account_info(self):
        if self.test_mode:
            return {
                "account_id": self.wallet_address,
                "balance": 200.00,
                "cash_available": 200.00,
                "buying_power": 200.00,
                "margin_balance": 0.0,
                "margin_used": 0.0,
                "margin_enabled": False,
                "margin_percent": 0.0,
                "native_currency": "MATIC",
                "layer2": True
            }

        if not self.web3.isConnected():
            raise ConnectionError("Web3 not connected")

        balance_wei = self.web3.eth.get_balance(self.wallet_address)
        balance_native = self.web3.from_wei(balance_wei, 'ether')
        balance_float = float(Decimal(balance_native).quantize(Decimal("0.0001")))

        return {
            "account_id": self.wallet_address,
            "balance": balance_float,
            "cash_available": balance_float,
            "buying_power": balance_float,
            "margin_balance": 0.0,
            "margin_used": 0.0,
            "margin_enabled": False,
            "margin_percent": 0.0,
            "native_currency": self._detect_native_token(),
            "layer2": self._is_layer2()
        }

    def _detect_native_token(self):
        if "polygon" in self.rpc_url.lower():
            return "MATIC"
        elif "arbitrum" in self.rpc_url.lower():
            return "ETH"
        else:
            return "ETH"

    def _is_layer2(self):
        return any(net in self.rpc_url.lower() for net in ["polygon", "arbitrum", "optimism"])

    async def get_crypto_account_info(self):
        return await self.get_account_info()

    async def disconnect(self):
        self.logged_in = False
