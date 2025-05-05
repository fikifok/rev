# benchmark.py – Portföy benchmark karşılaştırmaları
import pandas as pd
import yfinance as yf
from typing import Dict

class Benchmark:
    def __init__(self, symbols: Dict[str, str]):
        """
        symbols: {"BIST100": "XU100.IS", "GOLD": "GLD", ...}
        """
        self.symbols = symbols

    def fetch_data(self, start: str, end: str) -> pd.DataFrame:
        frames = []
        for name, ticker in self.symbols.items():
            df = yf.download(ticker, start=start, end=end)[['Close']].rename(columns={'Close': name})
            frames.append(df)
        merged = pd.concat(frames, axis=1)
        return merged.dropna()

    def normalize_returns(self, price_df: pd.DataFrame) -> pd.DataFrame:
        """Fiyat serilerini normalize eder (ilk gün = 1)"""
        return price_df / price_df.iloc[0]

    def calculate_returns(self, price_df: pd.DataFrame) -> pd.Series:
        """Toplam yüzdesel değişimi hesaplar"""
        return ((price_df.iloc[-1] / price_df.iloc[0]) - 1) * 100

    def calculate_portfolio_returns(self, transactions_df: pd.DataFrame, start: str, end: str) -> float:
        """
        Portföyün tarih aralığındaki yüzdesel getirisini hesaplar.
        Basit metot: alım toplamı vs güncel değer.
        """
        df = transactions_df.copy()
        df['date'] = pd.to_datetime(df['date'])
        mask = (df['date'] >= pd.to_datetime(start)) & (df['date'] <= pd.to_datetime(end))
        df = df.loc[mask & (df['type'] == 'buy')]

        if df.empty:
            return 0.0

        df['cost'] = df['quantity'] * df['price_per_unit']
        total_cost = df['cost'].sum()

        latest_prices = {}
        for symbol in df['symbol'].unique():
            try:
                yf_symbol = symbol.upper() if not symbol.isalpha() or len(symbol) > 5 else f"{symbol.upper()}.IS"
                ticker = yf.Ticker(yf_symbol)
                price = ticker.history(start=end, end=end)['Close'].iloc[0]
                latest_prices[symbol] = price
            except:
                latest_prices[symbol] = 0.0

        df['latest_price'] = df['symbol'].map(latest_prices)
        df['current_value'] = df['latest_price'] * df['quantity']
        total_value = df['current_value'].sum()

        return ((total_value - total_cost) / total_cost) * 100
