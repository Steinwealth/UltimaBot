import httpx
import hmac
import hashlib
import time
import base64
from urllib.parse import urlencode
import asyncio
import websockets
import json

class KrakenClient:
    BASE_URL = "https://api.kraken.com"

    def __init__(self, api_key: str, api_secret: str, test_mode: bool = False):
        self.api_key = api_key
        self.api_secret = api_secret.encode()
        self.logged_in = False
        self.test_mode = test_mode

    def _nonce(self):
        return int(time.time() * 1000)

    async def login(self):
        try:
            await self.get_account_info()
            self.logged_in = True
            return True
        except Exception as e:
            print(f"[KrakenClient] Login failed: {type(e).__name__} - {e}")
            self.logged_in = False
            return False

    def is_logged_in(self) -> bool:
        return self.logged_in

    async def logout(self):
        self.logged_in = False

    def _sign(self, url_path, data):
        postdata = urlencode(data)
        encoded = (str(data['nonce']) + postdata).encode()
        message = url_path.encode() + hashlib.sha256(encoded).digest()
        mac = hmac.new(base64.b64decode(self.api_secret), message, hashlib.sha512)
        sigdigest = base64.b64encode(mac.digest())
        return sigdigest.decode()

    async def _safe_request(self, client, method, url, **kwargs):
        retries = 5
        backoff = 1
        for attempt in range(retries):
            response = await client.request(method, url, **kwargs)
            if response.status_code == 429:
                retry_after = int(response.headers.get("Retry-After", backoff))
                await asyncio.sleep(retry_after)
                backoff *= 2
            else:
                return response
        raise Exception(f"Rate limit exceeded after {retries} retries.")

    async def get_account_info(self):
        if self.test_mode:
            return {
                "account_id": "KR-987",
                "balance": 12000.00,
                "cash_available": 8000.00,
                "buying_power": 8000.00,
                "margin_balance": 4000.00,
                "margin_used": 1000.00,
                "margin_enabled": True,
                "margin_percent": 25.0
            }

        async with httpx.AsyncClient() as client:
            url_path = "/0/private/Balance"
            url = f"{self.BASE_URL}{url_path}"
            data = {"nonce": self._nonce()}
            headers = {
                "API-Key": self.api_key,
                "API-Sign": self._sign(url_path, data)
            }
            response = await self._safe_request(client, "POST", url, data=data, headers=headers)
            if response.status_code != 200:
                raise Exception(f"Failed to fetch balance: {response.text}")
            balances = response.json()["result"]
            usdt_balance = float(balances.get("USDT", 0.0))

            url_path = "/0/private/TradeBalance"
            url = f"{self.BASE_URL}{url_path}"
            data = {"nonce": self._nonce()}
            headers["API-Sign"] = self._sign(url_path, data)
            response = await self._safe_request(client, "POST", url, data=data, headers=headers)

            margin_balance = 0.0
            margin_used = 0.0
            margin_enabled = False
            margin_percent = 0.0

            if response.status_code == 200 and "result" in response.json():
                margin_data = response.json()["result"]
                margin_balance = float(margin_data.get("eb", 0.0))
                margin_used = float(margin_data.get("mf", 0.0))
                margin_enabled = margin_balance > 0
                margin_percent = (margin_used / margin_balance) * 100 if margin_balance > 0 else 0.0

        return {
            "account_id": "kraken-account",
            "balance": usdt_balance,
            "cash_available": usdt_balance,
            "buying_power": usdt_balance,
            "margin_balance": margin_balance,
            "margin_used": margin_used,
            "margin_enabled": margin_enabled,
            "margin_percent": margin_percent
        }

    async def ws_market_trade_updates(self):
        uri = "wss://ws.kraken.com"
        async with websockets.connect(uri) as ws:
            subscribe = {
                "event": "subscribe",
                "pair": ["BTC/USD"],
                "subscription": {"name": "ticker"}
            }
            print("Subscribing to Kraken market updates...")
            await ws.send(json.dumps(subscribe))
            async for message in ws:
                data = json.loads(message)
                print("Market Update:", data)

    async def ws_private_trade_updates(self):
        uri = "wss://ws-auth.kraken.com"
        token = await self._get_ws_token()
        async with websockets.connect(uri) as ws:
            subscribe = {
                "event": "subscribe",
                "subscription": {"name": "ownTrades", "token": token}
            }
            print("Subscribing to private trade updates...")
            await ws.send(json.dumps(subscribe))
            async for message in ws:
                data = json.loads(message)
                print("Trade Execution Update:", data)

    async def _get_ws_token(self):
        url_path = "/0/private/GetWebSocketsToken"
        url = f"{self.BASE_URL}{url_path}"
        data = {"nonce": self._nonce()}
        headers = {
            "API-Key": self.api_key,
            "API-Sign": self._sign(url_path, data)
        }

        async with httpx.AsyncClient() as client:
            response = await self._safe_request(client, "POST", url, data=data, headers=headers)

        if response.status_code != 200:
            raise Exception(f"Failed to fetch Kraken WebSocket token: {response.text}")

        return response.json()["result"]["token"]

    async def disconnect(self):
        self.logged_in = False
