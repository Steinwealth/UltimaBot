import httpx

class SchwabClient:
    BASE_URL = "https://api.schwabapi.com/v1"
    AUTH_URL = "https://api.schwabapi.com/v1/oauth2/token"

    def __init__(self, client_id: str, client_secret: str, refresh_token: str, test_mode: bool = False):
        self.client_id = client_id
        self.client_secret = client_secret
        self.refresh_token = refresh_token
        self.access_token = None
        self.logged_in = False
        self.account_id = None
        self.test_mode = test_mode

    async def login(self):
        """
        Obtain a new access token using the refresh token (OAuth 2.0).
        """
        if self.test_mode:
            self.logged_in = True
            return True

        payload = {
            "grant_type": "refresh_token",
            "refresh_token": self.refresh_token,
            "client_id": self.client_id,
            "client_secret": self.client_secret
        }

        async with httpx.AsyncClient() as client:
            response = await client.post(self.AUTH_URL, data=payload)

        if response.status_code != 200:
            raise Exception(f"Schwab OAuth 2.0 login failed: {response.text}")

        data = response.json()
        self.access_token = data.get("access_token")
        self.logged_in = True
        return True

    async def is_logged_in(self):
        return self.logged_in

    def _auth_headers(self):
        """
        Generate Bearer token headers for Schwab API requests.
        """
        return {"Authorization": f"Bearer {self.access_token}"}

    async def get_account_info(self):
        """
        Fetch Schwab account balances or return simulated data in test mode.
        """
        if self.test_mode:
            return {
                "account_id": "SCH-321",
                "balance": 30000.00,
                "cash_available": 10000.00,
                "buying_power": 20000.00,
                "margin_balance": 5000.00,
                "margin_used": 1000.00,
                "margin_enabled": True,
                "margin_percent": 20.0
            }

        url = f"{self.BASE_URL}/accounts"

        async with httpx.AsyncClient() as client:
            response = await client.get(url, headers=self._auth_headers())

        if response.status_code != 200:
            raise Exception(f"Failed to fetch Schwab account info: {response.text}")

        data = response.json()["securitiesAccount"]
        self.account_id = data.get("accountId")

        balance_data = data.get("currentBalances", {})
        cash_available = balance_data.get("availableFunds", 0.0)
        margin_balance = balance_data.get("marginBalance", 0.0)
        margin_used = balance_data.get("shortOptionValue", 0.0)
        margin_enabled = margin_balance > 0

        return {
            "account_id": self.account_id,
            "balance": balance_data.get("totalCash", 0.0),
            "cash_available": cash_available,
            "buying_power": balance_data.get("buyingPower", cash_available),
            "margin_balance": margin_balance,
            "margin_used": margin_used,
            "margin_enabled": margin_enabled,
            "margin_percent": (margin_used / margin_balance) * 100 if margin_enabled else 0.0
        }

    def disconnect(self):
        self.logged_in = False
        self.access_token = None
