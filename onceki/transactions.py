# src/modules/transactions.py

import sqlite3
from typing import List, Dict, Any

class TransactionManager:
    def __init__(self, db_path: str):
        self.db_path = db_path
        self.conn = sqlite3.connect(self.db_path)
        self.conn.row_factory = sqlite3.Row
        self._create_table()

    def _create_table(self):
        query = """
        CREATE TABLE IF NOT EXISTS transactions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            date TEXT NOT NULL,
            type TEXT NOT NULL,
            asset_type TEXT NOT NULL,
            symbol TEXT NOT NULL,
            quantity REAL NOT NULL,
            price_per_unit REAL NOT NULL
        )
        """
        self.conn.execute(query)
        self.conn.commit()

    def add_transaction(self, date: str, tx_type: str, asset_type: str,
                        symbol: str, quantity: float, price_per_unit: float):
        query = """
        INSERT INTO transactions (date, type, asset_type, symbol, quantity, price_per_unit)
        VALUES (?, ?, ?, ?, ?, ?)
        """
        self.conn.execute(query, (date, tx_type, asset_type, symbol, quantity, price_per_unit))
        self.conn.commit()

    def list_transactions(self) -> List[Dict[str, Any]]:
        query = "SELECT * FROM transactions ORDER BY date DESC"
        cursor = self.conn.execute(query)
        return [dict(row) for row in cursor]

    def close(self):
        self.conn.close()
