import time
import requests
from requests_oauthlib import OAuth1Session
from typing import Dict, List

CONSUMER_KEY = "YOUR_ETRADE_CONSUMER_KEY"
CONSUMER_SECRET = "YOUR_ETRADE_CONSUMER_SECRET"
SANDBOX = False

BASE_URL = "https://apisb.etrade.com" if SANDBOX else "https://api.etrade.com"


def get_account_info(oauth_token: str, oauth_token_secret: str) -> Dict:
    url = f"{BASE_URL}/v1/accounts/list.json"
    oauth = OAuth1Session(CONSUMER_KEY, CONSUMER_SECRET, oauth_token, oauth_token_secret)
    response = oauth.get(url)
    if response.status_code == 200:
        data = response.json()
        account = data["accounts"][0]["accountId"]
        balance_url = f"{BASE_URL}/v1/accounts/{account}/balance.json"
        balance_response = oauth.get(balance_url)
        if balance_response.status_code == 200:
            bdata = balance_response.json()["accountBalance"]
            return {
                "broker": "E*TRADE",
                "balance": float(bdata.get("accountBalance", 0)),
                "available_margin_pct": 0.90,
                "used_margin_pct": 0.10,
                "open_drawdown_pct": 0.01
            }
    return {"error": f"E*TRADE account retrieval failed: {response.status_code}"}


def get_live_market_data(symbols: List[str], oauth_token: str, oauth_token_secret: str) -> Dict:
    oauth = OAuth1Session(CONSUMER_KEY, CONSUMER_SECRET, oauth_token, oauth_token_secret)
    market_data = {}
    for symbol in symbols:
        url = f"{BASE_URL}/v1/market/quote/{symbol}.json"
        response = oauth.get(url)
        if response.status_code == 200:
            quote = response.json().get("quoteResponse", {}).get("quoteData", [{}])[0]
            market_data[symbol] = {
                "price": float(quote.get("lastTrade", 0)),
                "volume": int(quote.get("totalVolume", 0)),
                "confidence": 0.95
            }
        else:
            market_data[symbol] = {"error": f"Failed: {response.status_code}"}
    return market_data


def place_order(oauth_token: str, oauth_token_secret: str, account_id: str, symbol: str, quantity: int, side: str) -> Dict:
    url = f"{BASE_URL}/v1/accounts/{account_id}/orders/place.json"
    payload = {
        "PlaceOrderRequest": {
            "orderType": "MARKET",
            "clientOrderId": str(int(time.time())),
            "orderTerm": "GOOD_FOR_DAY",
            "marketSession": "REGULAR",
            "priceType": "MARKET",
            "orderAction": side.upper(),
            "quantity": quantity,
            "allOrNone": False,
            "instrument": [{
                "symbol": symbol,
                "orderAction": side.upper(),
                "quantity": quantity,
                "quantityType": "QUANTITY"
            }]
        }
    }
    oauth = OAuth1Session(CONSUMER_KEY, CONSUMER_SECRET, oauth_token, oauth_token_secret)
    response = oauth.post(url, json=payload)
    if response.status_code in [200, 201]:
        return response.json()
    else:
        return {"error": f"Order failed: {response.status_code} - {response.text}"}
