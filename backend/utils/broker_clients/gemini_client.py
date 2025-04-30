import httpx
import hmac
import hashlib
import base64
import json
import time

class GeminiClient:
    BASE_URL = "https://api.gemini.com"

    def __init__(self, api_key: str, api_secret: str, test_mode: bool = False):
        self.api_key = api_key
        self.api_secret = api_secret.encode()
        self.logged_in = False
        self.test_mode = test_mode

    async def login(self):
        """
        Validate Gemini API keys by attempting to fetch account balances.
        """
        try:
            await self.get_account_info()
            self.logged_in = True
            return True
        except Exception as e:
            print(f"[GeminiClient] Login failed: {e}")
            self.logged_in = False
            return False

    async def is_logged_in(self):
        return self.logged_in

    def _sign_payload(self, payload: dict):
        payload_json = json.dumps(payload)
        b64_payload = base64.b64encode(payload_json.encode())
        signature = hmac.new(self.api_secret, b64_payload, hashlib.sha384).hexdigest()
        return b64_payload.decode(), signature

    async def get_account_info(self):
        """
        Fetch Gemini account balances or return simulated data in test mode.
        """
        if self.test_mode:
            return {
                "account_id": "GM-321",
                "balance": 10000.00,
                "cash_available": 8000.00,
                "buying_power": 8000.00,
                "margin_balance": 0.0,
                "margin_used": 0.0,
                "margin_enabled": False,
                "margin_percent": 0.0
            }

        endpoint = "/v1/balances"
        url = f"{self.BASE_URL}{endpoint}"
        payload = {
            "request": endpoint,
            "nonce": int(time.time() * 1000)
        }
        b64_payload, signature = self._sign_payload(payload)

        headers = {
            "X-GEMINI-APIKEY": self.api_key,
            "X-GEMINI-PAYLOAD": b64_payload,
            "X-GEMINI-SIGNATURE": signature
        }

        async with httpx.AsyncClient() as client:
            response = await client.post(url, headers=headers)

        if response.status_code != 200:
            raise Exception(f"Failed to fetch Gemini account info: {response.text}")

        balances = response.json()
        usd_balance = next((float(b["amount"]) for b in balances if b["currency"] == "USD"), 0.0)

        return {
            "account_id": "gemini-account",
            "balance": usd_balance,
            "cash_available": usd_balance,
            "buying_power": usd_balance,
            "margin_balance": 0.0,  # Gemini does not offer margin for most accounts
            "margin_used": 0.0,
            "margin_enabled": False,
            "margin_percent": 0.0
        }

    def disconnect(self):
        self.logged_in = False
