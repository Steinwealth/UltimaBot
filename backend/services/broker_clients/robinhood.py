import requests
from typing import Dict, List

BASE_URL = "https://api.robinhood.com"


def login(username: str, password: str) -> Dict:
    # Simulated login (Robinhood uses OAuth and device tokens; this requires a headless browser or token)
    return {
        "access_token": "demo-token",
        "refresh_token": "demo-refresh",
        "account_id": "123456789"
    }


def get_account_info(access_token: str) -> Dict:
    headers = {"Authorization": f"Bearer {access_token}"}
    response = requests.get(f"{BASE_URL}/accounts/", headers=headers)
    if response.status_code == 200:
        result = response.json()["results"][0]
        balance = float(result.get("portfolio_cash", 0))
        return {
            "broker": "Robinhood",
            "balance": balance,
            "available_margin_pct": 0.87,
            "used_margin_pct": 0.13,
            "open_drawdown_pct": 0.02
        }
    return {"error": f"Robinhood login failed: {response.status_code}"}


def get_live_market_data(symbols: List[str], access_token: str) -> Dict:
    headers = {"Authorization": f"Bearer {access_token}"}
    market_data = {}
    for symbol in symbols:
        quote_url = f"{BASE_URL}/quotes/{symbol}/"
        response = requests.get(quote_url, headers=headers)
        if response.status_code == 200:
            quote = response.json()
            market_data[symbol] = {
                "price": float(quote.get("last_trade_price", 0)),
                "volume": int(quote.get("volume", 0)),
                "confidence": 0.95
            }
        else:
            market_data[symbol] = {"error": f"Quote error: {response.status_code}"}
    return market_data
