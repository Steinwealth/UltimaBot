import httpx
import hmac
import hashlib
import time
from urllib.parse import urlencode

class BinanceClient:
    BASE_URL = "https://api.binance.com"
    MARGIN_URL = "https://api.binance.com/sapi/v1/margin/account"

    def __init__(self, api_key: str, api_secret: str, test_mode: bool = False):
        self.api_key = api_key
        self.api_secret = api_secret.encode()  # Secret must be bytes for HMAC
        self.logged_in = False
        self.test_mode = test_mode

    async def login(self):
        """
        Binance API keys are validated by attempting to fetch account info.
        """
        try:
            await self.get_account_info()
            self.logged_in = True
            return True
        except Exception as e:
            print(f"[BinanceClient] Login failed: {e}")
            self.logged_in = False
            return False

    async def is_logged_in(self):
        return self.logged_in

    def _sign_params(self, params: dict):
        """
        Sign the request parameters using HMAC-SHA256.
        """
        query_string = urlencode(params)
        signature = hmac.new(self.api_secret, query_string.encode(), hashlib.sha256).hexdigest()
        return f"{query_string}&signature={signature}"

    async def get_account_info(self):
        """
        Fetch account balances from Binance API or return simulated data if in test mode.
        """
        if self.test_mode:
            # Simulated Binance account data
            return {
                "account_id": "BN-456",
                "balance": 15000.00,
                "cash_available": 5000.00,
                "buying_power": 7000.00,
                "margin_balance": 4000.00,
                "margin_used": 800.00,
                "margin_enabled": True,
                "margin_percent": 20.0
            }

        # Real API call for spot account
        endpoint = "/api/v3/account"
        timestamp = int(time.time() * 1000)
        params = {"timestamp": timestamp}
        signed_params = self._sign_params(params)

        headers = {"X-MBX-APIKEY": self.api_key}

        async with httpx.AsyncClient() as client:
            response = await client.get(f"{self.BASE_URL}{endpoint}?{signed_params}", headers=headers)

        if response.status_code != 200:
            raise Exception(f"Failed to fetch Binance account info: {response.text}")

        data = response.json()
        balances = {item["asset"]: float(item["free"]) for item in data["balances"]}

        usdt_balance = balances.get("USDT", 0.0)

        # Fetch margin account info
        margin_balance = 0.0
        margin_used = 0.0
        margin_enabled = False
        margin_percent = 0.0

        margin_params = {"timestamp": timestamp}
        signed_margin_params = self._sign_params(margin_params)

        margin_response = await client.get(f"{self.MARGIN_URL}?{signed_margin_params}", headers=headers)

        if margin_response.status_code == 200:
            margin_data = margin_response.json()
            margin_balance = float(margin_data.get("totalAssetOfBtc", 0.0))
            margin_used = float(margin_data.get("totalLiabilityOfBtc", 0.0))
            margin_enabled = True if margin_balance > 0 else False
            margin_percent = (margin_used / margin_balance) * 100 if margin_balance > 0 else 0.0

        return {
            "account_id": data.get("accountId", "binance-account"),
            "balance": usdt_balance,
            "cash_available": usdt_balance,
            "buying_power": usdt_balance,
            "margin_balance": margin_balance,
            "margin_used": margin_used,
            "margin_enabled": margin_enabled,
            "margin_percent": margin_percent
        }

    def disconnect(self):
        self.logged_in = False
