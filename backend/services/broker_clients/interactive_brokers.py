import requests
from typing import Dict, List

BASE_URL = "https://localhost:5000/v1/api"  # Gateway or TWS Web API default port


def get_account_info(session_token: str) -> Dict:
    headers = {"Authorization": f"Bearer {session_token}"}
    response = requests.get(f"{BASE_URL}/iserver/accounts", headers=headers, verify=False)
    if response.status_code == 200:
        accounts = response.json()
        account_id = accounts["accounts"][0]
        response = requests.get(f"{BASE_URL}/portfolio/{account_id}/summary", headers=headers, verify=False)
        if response.status_code == 200:
            data = response.json()
            return {
                "broker": "Interactive Brokers",
                "balance": float(data.get("totalcashvalue", 0)),
                "available_margin_pct": 0.85,
                "used_margin_pct": 0.15,
                "open_drawdown_pct": 0.02
            }
    return {"error": "IBKR account info retrieval failed"}


def get_live_market_data(symbols: List[str], session_token: str) -> Dict:
    headers = {"Authorization": f"Bearer {session_token}"}
    market_data = {}
    for symbol in symbols:
        response = requests.get(f"{BASE_URL}/iserver/marketdata/snapshot?conids={symbol}&fields=31,55", headers=headers, verify=False)
        if response.status_code == 200:
            data = response.json()
            if isinstance(data, list) and data:
                item = data[0]
                market_data[symbol] = {
                    "price": float(item.get("31", 0)),
                    "volume": int(item.get("55", 0)),
                    "confidence": 0.95
                }
        else:
            market_data[symbol] = {"error": f"Failed to fetch: {response.status_code}"}
    return market_data
