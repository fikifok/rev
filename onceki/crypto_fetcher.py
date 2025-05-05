# src/modules/crypto_fetcher.py

import requests

class CryptoFetcher:
    SYMBOL_MAP = {
        "btc": "bitcoin",
        "eth": "ethereum",
        "dot": "polkadot",
        "avax": "avalanche-2",
        "sol": "solana",
        "ada": "cardano",
        "doge": "dogecoin",
        "shib": "shiba-inu",
        "mina": "mina-protocol"
    }

    def get_price(self, coin_id: str) -> float:
        """
        CoinGecko API üzerinden USD fiyatı döner. Kısaltma girilirse eşleme yapılır.
        """
        coin_id = coin_id.lower()
        coin_id = self.SYMBOL_MAP.get(coin_id, coin_id)  # Eşle varsa kullan

        url = f"https://api.coingecko.com/api/v3/simple/price?ids={coin_id}&vs_currencies=usd"
        response = requests.get(url, timeout=10)
        if response.status_code != 200:
            raise ValueError(f"API hatası: {response.status_code}")
        data = response.json()
        if coin_id not in data or 'usd' not in data[coin_id]:
            raise ValueError(f"Geçersiz coin ID: {coin_id}")
        return data[coin_id]['usd']
