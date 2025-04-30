import httpx
import hmac
import hashlib
import time
import asyncio
import json

class CoinbaseClient:
    BASE_URL = "https://api.coinbase.com/v2"
    
    def __init__(self, api_key: str, api_secret: str, passphrase: str, test_mode: bool = False):
        self.api_key = api_key
        self.api_secret = api_secret
        self.passphrase = passphrase
        self.session = None
        self.logged_in = False
        self.auth_token = None
        self.test_mode = test_mode
    
    def _generate_signature(self, method: str, url: str, body: str = ""):
        """
        Generates Coinbase API signature.
        """
        timestamp = str(int(time.time()))
        message = timestamp + method + url + body
        signature = hmac.new(self.api_secret.encode(), message.encode(), hashlib.sha256).hexdigest()
        return timestamp, signature

    async def login(self):
        if self.test_mode:
            self.logged_in = True
            return True
        
        headers = {
            "CB-ACCESS-KEY": self.api_key,
            "CB-ACCESS-PASSPHRASE": self.passphrase,
            "CB-ACCESS-TIMESTAMP": str(int(time.time())),
            "CB-ACCESS-SIGN": self._generate_signature("GET", "/accounts", "")[1]
        }

        async with httpx.AsyncClient() as client:
            response = await client.get(f"{self.BASE_URL}/accounts", headers=headers)

        if response.status_code != 200:
            raise Exception(f"Coinbase login failed: {response.text}")
        
        self.logged_in = True
        self.auth_token = response.json()['data']
        return True

    async def is_logged_in(self):
        return self.logged_in

    async def get_account_info(self):
        """
        Fetch account balances from Coinbase API or use simulated data in test mode.
        """
        if self.test_mode:
            return {
                "account_id": "CB-123",
                "balance": 5000.00,
                "cash_available": 2000.00,
                "buying_power": 2000.00,
                "margin_balance": 0.00,
                "margin_used": 0.00,
                "margin_enabled": False,
                "margin_percent": 0.0
            }
        
        headers = {
            "Authorization": f"Bearer {self.auth_token}",
            "CB-ACCESS-KEY": self.api_key,
            "CB-ACCESS-PASSPHRASE": self.passphrase,
            "CB-ACCESS-TIMESTAMP": str(int(time.time())),
            "CB-ACCESS-SIGN": self._generate_signature("GET", "/accounts", "")[1]
        }

        async with httpx.AsyncClient() as client:
            response = await client.get(f"{self.BASE_URL}/accounts", headers=headers)

        if response.status_code != 200:
            raise Exception(f"Failed to fetch Coinbase account info: {response.text}")

        data = response.json()["data"]
        account_balance = sum(float(acc["balance"]["amount"]) for acc in data if acc["currency"] == "USD")
        cash_available = account_balance  # Assume cash account, no margin

        return {
            "account_id": data[0]["id"],
            "balance": account_balance,
            "cash_available": cash_available,
            "buying_power": cash_available,  # Cash account has buying power equivalent to cash balance
            "margin_balance": 0.0,
            "margin_used": 0.0,
            "margin_enabled": False,
            "margin_percent": 0.0
        }
    
    async def get_crypto_account_info(self):
        """
        Fetch crypto account balances from Coinbase API or use simulated data in test mode.
        """
        if self.test_mode:
            return {
                "crypto_account_id": "CB-CRYPTO-123",
                "crypto_balance": 3000.00,
                "available_crypto": 2900.00,
            }
        
        headers = {
            "Authorization": f"Bearer {self.auth_token}",
            "CB-ACCESS-KEY": self.api_key,
            "CB-ACCESS-PASSPHRASE": self.passphrase,
            "CB-ACCESS-TIMESTAMP": str(int(time.time())),
            "CB-ACCESS-SIGN": self._generate_signature("GET", "/accounts", "")[1]
        }

        async with httpx.AsyncClient() as client:
            response = await client.get(f"{self.BASE_URL}/accounts", headers=headers)

        if response.status_code != 200:
            raise Exception(f"Failed to fetch Coinbase crypto account info: {response.text}")

        data = response.json()["data"]
        crypto_balance = sum(float(acc["balance"]["amount"]) for acc in data if acc["currency"] != "USD")
        
        return {
            "crypto_account_id": data[0]["id"],
            "crypto_balance": crypto_balance,
            "available_crypto": crypto_balance,
        }

    def disconnect(self):
        self.logged_in = False
        self.auth_token = None
