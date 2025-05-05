# ETF takibi yapan sınıf – src/modules/etf_tracker.py

import pandas as pd
from typing import List, Dict

class ETFTracker:
    def __init__(self):
        self.etfs: Dict[str, pd.DataFrame] = {}

    def add_etf_data(self, symbol: str, data: pd.DataFrame):
        """
        Yeni bir ETF'nin fiyat verisini ekler.
        Veri DataFrame formatında olmalı ve en azından 'Date' ve 'Close' sütunlarını içermeli.
        """
        if "Date" not in data.columns or "Close" not in data.columns:
            raise ValueError("DataFrame must contain 'Date' and 'Close' columns")
        df = data.copy()
        df["Date"] = pd.to_datetime(df["Date"])
        df.set_index("Date", inplace=True)
        self.etfs[symbol.upper()] = df

    def get_latest_price(self, symbol: str) -> float:
        """
        Belirtilen ETF'nin en güncel kapanış fiyatını döner.
        """
        df = self.etfs.get(symbol.upper())
        if df is None or df.empty:
            raise ValueError(f"No data found for ETF: {symbol}")
        return df["Close"].iloc[-1]

    def calculate_returns(self, symbol: str) -> pd.Series:
        """
        Belirtilen ETF için günlük getiri oranlarını hesaplar.
        """
        df = self.etfs.get(symbol.upper())
        if df is None:
            raise ValueError(f"No data found for ETF: {symbol}")
        return df["Close"].pct_change().dropna()
