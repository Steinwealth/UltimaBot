# backend/utils/broker_clients/base_evm_wallet_client.py

from web3 import Web3
import asyncio

class BaseEVMWalletClient:
    def __init__(self, wallet_address: str, rpc_url: str, test_mode: bool = False):
        self.wallet_address = Web3.to_checksum_address(wallet_address)
        self.rpc_url = rpc_url
        self.web3 = Web3(Web3.HTTPProvider(rpc_url))
        self.test_mode = test_mode
        self.logged_in = False

    async def login(self):
        if self.test_mode:
            self.logged_in = True
            return True

        if not self.web3.isConnected():
            raise ConnectionError("RPC connection failed")

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
                "balance": 10000.0,
                "cash_available": 10000.0,
                "buying_power": 10000.0,
                "margin_balance": 0.0,
                "margin_used": 0.0,
                "margin_enabled": False,
                "margin_percent": 0.0
            }

        if not self.web3.isConnected():
            raise ConnectionError("Web3 not connected")

        balance_wei = self.web3.eth.get_balance(self.wallet_address)
        balance_eth = self.web3.from_wei(balance_wei, 'ether')

        return {
            "account_id": self.wallet_address,
            "balance": float(balance_eth),
            "cash_available": float(balance_eth),
            "buying_power": float(balance_eth),
            "margin_balance": 0.0,
            "margin_used": 0.0,
            "margin_enabled": False,
            "margin_percent": 0.0
        }

    async def disconnect(self):
        self.logged_in = False
