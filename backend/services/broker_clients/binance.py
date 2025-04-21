import time
import hmac
import hashlib
import requests
from typing import Dict, List

BASE_URL = "https://api.binance.com"


def generate_signature(secret: str, query_string: str) -> str:
    return hmac.new(secret.encode(), query_string.encode(), hashlib.sha256).hexdigest()


def get_account_info(api_key: str, api_secret: str) -> Dict:
    endpoint = "/api/v3/account"
    timestamp = int(time.time() * 1000)
    query_string = f"timestamp={timestamp}"
    signature = generate_signature(api_secret, query_string)
    headers = {"X-MBX-APIKEY": api_key}
    url = f"{BASE_URL}{endpoint}?{query_string}&signature={signature}"
    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        balances = response.json().get("balances", [])
        total_balance = sum(float(b["free"]) for b in balances if float(b["free"]) > 0)
        return {
            "broker": "Binance",
            "balance": total_balance,
            "available_margin_pct": 0.80,
            "used_margin_pct": 0.20,
            "open_drawdown_pct": 0.03
        }
    else:
        return {"error": f"Failed to retrieve account info: {response.status_code}"}


def get_live_market_data(symbols: List[str], api_key: str, api_secret: str) -> Dict:
    market_data = {}
    for symbol in symbols:
        binance_symbol = symbol.replace("-", "").upper()
        url = f"{BASE_URL}/api/v3/ticker/24hr?symbol={binance_symbol}"
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            market_data[symbol] = {
                "price": float(data.get("lastPrice", 0)),
                "volume": float(data.get("quoteVolume", 0)),
                "confidence": 0.96  # placeholder
            }
        else:
            market_data[symbol] = {"error": f"Failed to fetch: {response.status_code}"}
    return market_data
