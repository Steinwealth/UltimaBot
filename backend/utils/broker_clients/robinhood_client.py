import httpx
import asyncio
import websockets
import json

class RobinhoodClient:
    BASE_URL = "https://api.robinhood.com"

    def __init__(self, username: str, password: str, test_mode: bool = False):
        self.username = username
        self.password = password
        self.logged_in = False
        self.auth_token = None
        self.test_mode = test_mode

    async def login(self):
        if self.test_mode:
            self.logged_in = True
            return True

        login_payload = {"username": self.username, "password": self.password}

        async with httpx.AsyncClient() as client:
            response = await client.post(f"{self.BASE_URL}/oauth2/token/", data=login_payload)

        if response.status_code != 200:
            raise Exception(f"Robinhood login failed: {response.text}")

        data = response.json()
        self.auth_token = data.get("access_token")
        self.logged_in = True
        return True

    async def is_logged_in(self):
        return self.logged_in

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
                "account_id": "RH-654",
                "balance": 10000.00,
                "cash_available": 2500.00,
                "buying_power": 6000.00,
                "margin_balance": 4000.00,
                "margin_used": 900.00,
                "margin_enabled": True,
                "margin_percent": 22.5
            }

        headers = {"Authorization": f"Bearer {self.auth_token}"}

        async with httpx.AsyncClient() as client:
            response = await self._safe_request(client, "GET", f"{self.BASE_URL}/accounts/", headers=headers)

        profile_data = response.json()["results"][0]
        account_id = profile_data.get("account_number")
        margin_balances = profile_data.get("margin_balances", {})
        margin_balance = float(margin_balances.get("unallocated_margin_cash", 0.0))
        margin_used = float(margin_balances.get("margin_withdrawable", 0.0))
        margin_enabled = margin_balance > 0

        return {
            "account_id": account_id,
            "balance": float(profile_data.get("equity", 0.0)),
            "cash_available": float(profile_data.get("cash_available_for_withdrawal", 0.0)),
            "buying_power": float(profile_data.get("buying_power", 0.0)),
            "margin_balance": margin_balance,
            "margin_used": margin_used,
            "margin_enabled": margin_enabled,
            "margin_percent": (margin_used / margin_balance) * 100 if margin_enabled else 0.0
        }

    async def get_crypto_account_info(self):
        if self.test_mode:
            return {
                "crypto_account_id": "RH-CRYPTO-654",
                "crypto_balance": 5000.00,
                "available_crypto": 4800.00,
            }

        headers = {"Authorization": f"Bearer {self.auth_token}"}

        async with httpx.AsyncClient() as client:
            response = await self._safe_request(client, "GET", f"{self.BASE_URL}/crypto/accounts/", headers=headers)

        data = response.json()["results"][0]
        return {
            "crypto_account_id": data.get("id"),
            "crypto_balance": float(data.get("equity", 0.0)),
            "available_crypto": float(data.get("cash_available_for_withdrawal", 0.0))
        }

    async def ws_market_updates(self):
        uri = "wss://api.robinhood.com/market"
        async with websockets.connect(uri) as ws:
            subscribe = {"event": "subscribe", "channel": "ticker", "symbol": "BTC/USD"}
            await ws.send(json.dumps(subscribe))
            async for message in ws:
                data = json.loads(message)
                print("Market Update:", data)

    async def ws_trade_updates(self):
        uri = "wss://api.robinhood.com/trades"
        async with websockets.connect(uri) as ws:
            subscribe = {"event": "subscribe", "channel": "orders", "symbol": "BTC/USD"}
            await ws.send(json.dumps(subscribe))
            async for message in ws:
                data = json.loads(message)
                print("Trade Execution Update:", data)

    def disconnect(self):
        self.logged_in = False
        self.auth_token = None
