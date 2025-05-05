# -*- coding: utf-8 -*-
"""
Created on Sat May  3 15:17:57 2025

@author: e
"""

# bes_tracker.py – Bireysel Emeklilik Fon Takibi
import sqlite3
from typing import List, Dict
from datetime import datetime

class BESTracker:
    def __init__(self, db_path: str):
        self.db_path = db_path
        self._ensure_tables()

    def _ensure_tables(self):
        with sqlite3.connect(self.db_path) as conn:
            c = conn.cursor()
            c.execute("""
                CREATE TABLE IF NOT EXISTS bes_contributions (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    date TEXT,
                    amount REAL
                )
            """)
            c.execute("""
                CREATE TABLE IF NOT EXISTS bes_funds (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    date TEXT,
                    fund_name TEXT,
                    amount REAL
                )
            """)
            conn.commit()

    def add_contribution(self, date: str, amount: float):
        """Katkı payı ekle"""
        with sqlite3.connect(self.db_path) as conn:
            conn.execute(
                "INSERT INTO bes_contributions (date, amount) VALUES (?, ?)",
                (date, amount)
            )

    def add_fund_allocation(self, date: str, fund_name: str, amount: float):
        """Fon alımı kaydı ekle"""
        with sqlite3.connect(self.db_path) as conn:
            conn.execute(
                "INSERT INTO bes_funds (date, fund_name, amount) VALUES (?, ?, ?)",
                (date, fund_name.upper(), amount)
            )

    def get_total_contributions(self) -> float:
        with sqlite3.connect(self.db_path) as conn:
            row = conn.execute("SELECT SUM(amount) FROM bes_contributions").fetchone()
            return row[0] or 0.0

    def get_total_by_fund(self) -> Dict[str, float]:
        with sqlite3.connect(self.db_path) as conn:
            rows = conn.execute("""
                SELECT fund_name, SUM(amount) FROM bes_funds
                GROUP BY fund_name
            """).fetchall()
            return {row[0]: row[1] for row in rows}

    def get_monthly_summary(self) -> Dict[str, float]:
        """Aylık katkı payı toplamı"""
        with sqlite3.connect(self.db_path) as conn:
            rows = conn.execute("""
                SELECT strftime('%Y-%m', date) as month, SUM(amount)
                FROM bes_contributions
                GROUP BY month
                ORDER BY month
            """).fetchall()
            return {row[0]: row[1] for row in rows}
