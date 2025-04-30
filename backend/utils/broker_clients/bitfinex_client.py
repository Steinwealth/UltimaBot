import httpx
import hmac
import hashlib
import time
import json
import asyncio
import websockets

class BitfinexClient:
    BASE_URL = "https://api.bitfinex.com"

    def __init__(self, api_key: str, api_secret: str, test_mode: bool = False):
        self.api_key = api_key
        self.api_secret = api_secret.encode()
        self.logged_in = False
        self.test_mode = test_mode

    async def login(self):
        try:
            await self.get_account_info()
            self.logged_in = True
            return True
        except Exception as e:
            print(f"[BitfinexClient] Login failed: {e}")
            self.logged_in = False
            return False

    async def is_logged_in(self):
        return self.logged_in

    def _sign_request(self, endpoint: str, body: dict):
        nonce = str(int(time.time() * 1000))
        body_json = json.dumps(body)
        payload = f"/api/{endpoint}{nonce}{body_json}"
        signature = hmac.new(self.api_secret, payload.encode(), hashlib.sha384).hexdigest()
        return nonce, signature

    async def get_account_info(self):
        if self.test_mode:
            return {
                "account_id": "BF-888",
                "balance": 15000.00,
                "cash_available": 10000.00,
                "buying_power": 12000.00,
                "margin_balance": 5000.00,
                "margin_used": 1500.00,
                "margin_enabled": True,
                "margin_percent": 30.0
            }

        endpoint = "v2/auth/r/wallets"
        url = f"{self.BASE_URL}/{endpoint}"
        body = {}
        nonce, signature = self._sign_request(endpoint, body)

        headers = {
            "bfx-apikey": self.api_key,
            "bfx-signature": signature,
            "bfx-nonce": nonce,
            "Content-Type": "application/json"
        }

        async with httpx.AsyncClient() as client:
            response = await self._safe_request(client, "POST", url, headers=headers, json=body)

        if response.status_code != 200:
            raise Exception(f"Failed to fetch Bitfinex account info: {response.text}")

        wallets = response.json()
        usd_wallet = next((w for w in wallets if w[0] == "exchange" and w[1] == "USD"), [None, None, 0.0])
        usd_balance = float(usd_wallet[2])

        margin_wallet = next((w for w in wallets if w[0] == "margin" and w[1] == "USD"), [None, None, 0.0])
        margin_balance = float(margin_wallet[2])
        margin_used = margin_balance * 0.3  # Example calculation
        margin_enabled = margin_balance > 0
        margin_percent = (margin_used / margin_balance) * 100 if margin_enabled else 0.0

        return {
            "account_id": "bitfinex-account",
            "balance": usd_balance,
            "cash_available": usd_balance,
            "buying_power": usd_balance,
            "margin_balance": margin_balance,
            "margin_used": margin_used,
            "margin_enabled": margin_enabled,
            "margin_percent": margin_percent
        }

    async def ws_market_updates(self):
        uri = "wss://api-pub.bitfinex.com/ws/2"
        async with websockets.connect(uri) as ws:
            subscribe = {
                "event": "subscribe",
                "channel": "ticker",
                "symbol": "tBTCUSD"
            }
            await ws.send(json.dumps(subscribe))
            async for message in ws:
                data = json.loads(message)
                print("Market Update:", data)

    async def ws_trade_updates(self):
        uri = "wss://api.bitfinex.com/ws/2"
        nonce = str(int(time.time() * 1000))
        payload = {
            "event": "auth",
            "apiKey": self.api_key,
            "authSig": hmac.new(self.api_secret, f"AUTH{nonce}".encode(), hashlib.sha384).hexdigest(),
            "authPayload": f"AUTH{nonce}",
            "authNonce": nonce
        }
        async with websockets.connect(uri) as ws:
            await ws.send(json.dumps(payload))
            async for message in ws:
                data = json.loads(message)
                print("Trade Execution Update:", data)

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

    def disconnect(self):
        self.logged_in = False
