import requests
from typing import Dict, List

BASE_URL = "https://api.robinhood.com"


def login(username: str, password: str) -> Dict:
    url = f"{BASE_URL}/oauth2/token/"
    payload = {
        "grant_type": "password",
        "client_id": "c82SH0WZOsabOXGP2sxqcj34FxkvfnWR",  # Robinhood mobile client_id (public)
        "scope": "internal",
        "username": username,
        "password": password,
    }
    response = requests.post(url, data=payload)
    if response.status_code == 200:
        return response.json()
    return {"error": f"Login failed: {response.status_code}"}


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
    return {"error": f"Robinhood account retrieval failed: {response.status_code}"}


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


def place_order(access_token: str, account_url: str, symbol: str, quantity: int, side: str) -> Dict:
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json"
    }
    instrument_url = f"{BASE_URL}/instruments/?symbol={symbol}"
    inst_res = requests.get(instrument_url, headers=headers)
    if inst_res.status_code != 200 or not inst_res.json().get("results"):
        return {"error": "Unable to retrieve instrument URL."}

    instrument = inst_res.json()["results"][0]["url"]
    payload = {
        "account": account_url,
        "instrument": instrument,
        "symbol": symbol,
        "type": "market",
        "time_in_force": "gfd",
        "trigger": "immediate",
        "price": None,
        "quantity": quantity,
        "side": side.lower()
    }
    response = requests.post(f"{BASE_URL}/orders/", json=payload, headers=headers)
    if response.status_code in [200, 201]:
        return response.json()
    return {"error": f"Order failed: {response.status_code} - {response.text}"}
