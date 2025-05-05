# currency_converter.py – frankfurter.app tabanlı döviz çevirici
import requests

class CurrencyConverter:
    def __init__(self):
        self.api_url = "https://api.frankfurter.app/latest"

    def get_usd_to_try(self) -> float:
        """USD → TRY kuru"""
        response = requests.get(self.api_url, params={"from": "USD", "to": "TRY"})
        data = response.json()
        return data["rates"]["TRY"]

    def convert(self, amount: float, from_currency: str, to_currency: str) -> float:
        """Genel çevirici"""
        response = requests.get(self.api_url, params={"from": from_currency, "to": to_currency})
        data = response.json()
        rate = data["rates"][to_currency]
        return amount * rate

    def get_btc_to_usd(self) -> float:
        """BTC → USD fiyatı (CoinGecko üzerinden)"""
        response = requests.get(
            "https://api.coingecko.com/api/v3/simple/price",
            params={"ids": "bitcoin", "vs_currencies": "usd"}
        )
        data = response.json()
        return float(data["bitcoin"]["usd"])
