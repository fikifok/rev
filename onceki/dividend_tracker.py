# dividend_tracker.py – Temettü ve stake gelir takibi
import sqlite3
from typing import List, Dict
from datetime import datetime

class DividendTracker:
    def __init__(self, db_path: str):
        self.db_path = db_path
        self.conn = sqlite3.connect(self.db_path)
        self._ensure_tables()

    def _ensure_tables(self):
        """Temettü/stake tablolarını oluşturur (yoksa)"""
        c = self.conn.cursor()
        c.execute("""
            CREATE TABLE IF NOT EXISTS passive_income (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                date TEXT,
                symbol TEXT,
                amount REAL,
                type TEXT CHECK(type IN ('dividend', 'stake'))
            )
        """)
        self.conn.commit()

    def add_entry(self, date: str, symbol: str, amount: float, income_type: str = 'dividend'):
        """Yeni temettü veya stake geliri ekler"""
        if income_type not in ('dividend', 'stake'):
            raise ValueError("income_type must be 'dividend' or 'stake'")
        self.conn.execute(
            "INSERT INTO passive_income (date, symbol, amount, type) VALUES (?, ?, ?, ?)",
            (date, symbol.upper(), amount, income_type)
        )
        self.conn.commit()

    def get_all_entries(self) -> List[Dict]:
        """Tüm temettü ve stake kayıtlarını döndürür"""
        self.conn.row_factory = sqlite3.Row
        rows = self.conn.execute("SELECT * FROM passive_income").fetchall()
        return [dict(row) for row in rows]

    def get_total_income_by_type(self, income_type: str) -> float:
        """Belirli bir gelir türüne göre toplamı döndürür"""
        row = self.conn.execute(
            "SELECT SUM(amount) FROM passive_income WHERE type = ?",
            (income_type,)
        ).fetchone()
        return row[0] or 0.0

    def get_monthly_summary(self) -> Dict[str, float]:
        """Aylık toplam temettü+stake özetini verir"""
        rows = self.conn.execute("""
            SELECT 
                strftime('%Y-%m', date) as month,
                SUM(amount) as total
            FROM passive_income
            GROUP BY month
            ORDER BY month
        """).fetchall()
        return {row[0]: row[1] for row in rows}

    def close(self):
        """Bağlantıyı kapatır"""
        if self.conn:
            self.conn.close()
