import time
import hmac
import hashlib
import base64
import requests
import json
from typing import Dict, List

BASE_URL = "https://api.exchange.coinbase.com"


def authenticate(api_key: str, api_secret: str, passphrase: str, method: str, request_path: str, body: str = "") -> Dict:
    timestamp = str(time.time())
    message = f"{timestamp}{method.upper()}{request_path}{body}"
    hmac_key = base64.b64decode(api_secret)
    signature = hmac.new(hmac_key, message.encode('utf-8'), hashlib.sha256)
    signature_b64 = base64.b64encode(signature.digest()).decode('utf-8')

    return {
        "CB-ACCESS-KEY": api_key,
        "CB-ACCESS-SIGN": signature_b64,
        "CB-ACCESS-TIMESTAMP": timestamp,
        "CB-ACCESS-PASSPHRASE": passphrase,
        "Content-Type": "application/json"
    }


def validate_credentials(api_key: str, api_secret: str, passphrase: str) -> bool:
    headers = authenticate(api_key, api_secret, passphrase, "GET", "/accounts")
    response = requests.get(f"{BASE_URL}/accounts", headers=headers)
    return response.status_code == 200


def get_account_info(api_key: str, api_secret: str, passphrase: str) -> Dict:
    headers = authenticate(api_key, api_secret, passphrase, "GET", "/accounts")
    response = requests.get(f"{BASE_URL}/accounts", headers=headers)
    if response.status_code == 200:
        balances = response.json()
        total_balance = sum(float(acc['balance']) for acc in balances if float(acc['balance']) > 0)
        return {
            "broker": "Coinbase",
            "balance": total_balance,
            "available_margin_pct": 0.85,  # placeholder
            "used_margin_pct": 0.15,
            "open_drawdown_pct": 0.02
        }
    else:
        return {"error": f"Unable to fetch account info: {response.status_code}"}


def get_live_market_data(symbols: List[str], api_key: str, api_secret: str, passphrase: str) -> Dict:
    market_data = {}
    for symbol in symbols:
        cb_symbol = symbol.replace("-", "-").upper()
        headers = authenticate(api_key, api_secret, passphrase, "GET", f"/products/{cb_symbol}/ticker")
        response = requests.get(f"{BASE_URL}/products/{cb_symbol}/ticker", headers=headers)
        if response.status_code == 200:
            data = response.json()
            market_data[symbol] = {
                "price": float(data.get("price", 0)),
                "volume": float(data.get("volume", 0)),
                "confidence": 0.96  # placeholder
            }
        else:
            market_data[symbol] = {"error": f"Failed to fetch: {response.status_code}"}
    return market_data


def place_order(api_key: str, api_secret: str, passphrase: str, symbol: str, side: str, size: float, order_type: str = "market") -> Dict:
    request_path = "/orders"
    method = "POST"
    body_dict = {
        "type": order_type,
        "side": side,
        "product_id": symbol.upper(),
        "size": str(size)
    }
    body = json.dumps(body_dict)
    headers = authenticate(api_key, api_secret, passphrase, method, request_path, body)
    response = requests.post(f"{BASE_URL}{request_path}", headers=headers, data=body)
    if response.status_code == 200 or response.status_code == 201:
        return response.json()
    else:
        return {"error": f"Order failed: {response.status_code} - {response.text}"}
