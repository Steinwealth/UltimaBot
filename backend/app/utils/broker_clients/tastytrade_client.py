import httpx
import time
import asyncio

class TastyTradeClient:
    BASE_URL = "https://api.tastyworks.com"

    def __init__(self, username: str, password: str, test_mode: bool = False):
        self.username = username
        self.password = password
        self.session_token = None
        self.account_number = None
        self.logged_in = False
        self.test_mode = test_mode

    async def login(self):
        if self.test_mode:
            self.logged_in = True
            return True

        login_payload = {
            "login": self.username,
            "password": self.password
        }

        async with httpx.AsyncClient() as client:
            response = await client.post(f"{self.BASE_URL}/sessions", json=login_payload)

        if response.status_code != 200:
            raise Exception(f"Tastytrade login failed: {response.text}")

        self.session_token = response.json().get("data", {}).get("session-token")
        if not self.session_token:
            raise Exception("Failed to retrieve Tastytrade session token.")

        self.logged_in = True
        return True

    def is_logged_in(self) -> bool:
        return self.logged_in

    async def logout(self):
        self.session_token = None
        self.logged_in = False

    async def get_account_info(self):
        if self.test_mode:
            return {
                "account_id": "TASTY-123",
                "balance": 10000.0,
                "cash_available": 5000.0,
                "buying_power": 7000.0,
                "margin_balance": 3000.0,
                "margin_used": 500.0,
                "margin_enabled": True,
                "margin_percent": 16.7
            }

        headers = {
            "Authorization": f"Bearer {self.session_token}"
        }

        async with httpx.AsyncClient() as client:
            accounts_response = await client.get(f"{self.BASE_URL}/accounts", headers=headers)

        if accounts_response.status_code != 200:
            raise Exception(f"Failed to fetch Tastytrade accounts: {accounts_response.text}")

        accounts = accounts_response.json().get("data", [])
        if not accounts:
            raise Exception("No Tastytrade accounts found.")

        account = accounts[0]
        self.account_number = account["account-number"]

        balances_url = f"{self.BASE_URL}/accounts/{self.account_number}/balances"
        async with httpx.AsyncClient() as client:
            balance_response = await client.get(balances_url, headers=headers)

        if balance_response.status_code != 200:
            raise Exception(f"Failed to fetch balances: {balance_response.text}")

        balance_data = balance_response.json().get("data", {})
        cash = float(balance_data.get("cash", {}).get("cash-available-for-trading", 0.0))
        equity = float(balance_data.get("account", {}).get("net-liquidating-value", 0.0))
        margin = float(balance_data.get("account", {}).get("margin-requirement", 0.0))

        margin_enabled = margin > 0.0
        margin_percent = (margin / equity) * 100 if equity > 0 else 0.0

        return {
            "account_id": self.account_number,
            "balance": equity,
            "cash_available": cash,
            "buying_power": cash,
            "margin_balance": equity - cash,
            "margin_used": margin,
            "margin_enabled": margin_enabled,
            "margin_percent": margin_percent
        }

    def disconnect(self):
        self.logged_in = False
        self.session_token = None
