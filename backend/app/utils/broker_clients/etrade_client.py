import httpx
import time
from requests_oauthlib import OAuth1

class ETradeClient:
    BASE_URL = "https://api.etrade.com/v1"

    def __init__(self, api_key: str, api_secret: str, oauth_token: str, oauth_token_secret: str):
        self.api_key = api_key
        self.api_secret = api_secret
        self.oauth_token = oauth_token
        self.oauth_token_secret = oauth_token_secret
        self.logged_in = False
        self.account_id = None

    async def login(self):
        """
        E*TRADE uses OAuth 1.0a. We validate by fetching account info.
        """
        try:
            await self.get_account_info()
            self.logged_in = True
            return True
        except Exception as e:
            print(f"[ETradeClient] Login failed: {e}")
            self.logged_in = False
            return False

    async def is_logged_in(self):
        return self.logged_in

    def _oauth_headers(self):
        """
        Generate OAuth1 headers for E*TRADE API requests.
        """
        oauth = OAuth1(
            client_key=self.api_key,
            client_secret=self.api_secret,
            resource_owner_key=self.oauth_token,
            resource_owner_secret=self.oauth_token_secret,
            signature_method='HMAC-SHA1'
        )
        return oauth

    async def get_account_info(self):
        """
        Fetch account balances from E*TRADE API.
        """
        url = f"{self.BASE_URL}/accounts/list.json"
        async with httpx.AsyncClient() as client:
            response = await client.get(url, auth=self._oauth_headers())

        if response.status_code != 200:
            raise Exception(f"Failed to fetch E*TRADE account info: {response.text}")

        data = response.json()["Accounts"]["Account"]
        # Assume first account (or enhance to select specific one)
        account = data[0]
        self.account_id = account["accountId"]

        # Get balance details
        balance_url = f"{self.BASE_URL}/accounts/{self.account_id}/balance.json"
        response = await client.get(balance_url, auth=self._oauth_headers())
        if response.status_code != 200:
            raise Exception(f"Failed to fetch E*TRADE balances: {response.text}")

        balance_data = response.json()["accountBalance"]
        cash_available = balance_data.get("cashAvailableForInvestment", 0.0)
        margin_balance = balance_data.get("netCash", 0.0)
        margin_enabled = balance_data.get("marginBuyingPower", 0.0) > 0.0

        return {
            "account_id": self.account_id,
            "balance": balance_data.get("totalAccountValue", 0.0),
            "cash_available": cash_available,
            "buying_power": balance_data.get("marginBuyingPower", cash_available),
            "margin_balance": margin_balance,
            "margin_used": balance_data.get("cashBalance", 0.0),
            "margin_enabled": margin_enabled,
            "margin_percent": (balance_data.get("marginBalance", 0.0) / balance_data.get("totalAccountValue", 1.0)) * 100 if margin_enabled else 0.0
        }

    def disconnect(self):
        self.logged_in = False
