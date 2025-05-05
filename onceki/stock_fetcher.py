# src/modules/stock_fetcher.py

import yfinance as yf
import requests
import os

class StockFetcher:
    def __init__(self):
        self.finnhub_api_key = os.getenv("FINNHUB_API_KEY") or "d0b5op9r01qo0h63f8mg"

    def get_price(self, symbol: str, return_symbol=False):
        symbol = symbol.upper()
        if symbol.isalpha() and 3 <= len(symbol) <= 5:
            price = self._get_price_finnhub(symbol)
            used_symbol = symbol
        else:
            ticker = yf.Ticker(symbol)
            data = ticker.history(period='1d')
            if data.empty:
                raise ValueError(f"Fiyat verisi bulunamadı: {symbol}")
            price = data['Close'].iloc[-1]
            used_symbol = symbol
        return (price, used_symbol) if return_symbol else price

    def _get_price_finnhub(self, symbol: str) -> float:
        url = f"https://finnhub.io/api/v1/quote?symbol={symbol}.IS&token={self.finnhub_api_key}"
        resp = requests.get(url, timeout=10)
        if resp.status_code != 200:
            raise ValueError(f"Finnhub API hatası: {resp.status_code}")
        data = resp.json()
        if 'c' not in data or data['c'] == 0:
            raise ValueError(f"Finnhub: Geçersiz veri ({symbol})")
        return data['c']
