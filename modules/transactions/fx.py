# modules/transactions/fx.py
import requests
from datetime import date

def fetch_conversion_rate(trade_date: date) -> float:
    """
    1 USD = ? TRY
    free, API anahtarsız exchangerate.host servisi
    """
    url = f"https://api.exchangerate.host/{trade_date.isoformat()}?base=USD&symbols=TRY"
    try:
        r = requests.get(url, timeout=5); r.raise_for_status()
        return r.json()["rates"]["TRY"]
    except Exception:
        return 1.0
