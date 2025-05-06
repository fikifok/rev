# modules/transactions/db.py
from core.db import get_connection as core_get_connection

def get_connection():
    return core_get_connection()

def init_db():
    """
    transactions ve assets tablolarını oluşturur.
    """
    conn = get_connection()
    cur = conn.cursor()

    # 1) İşlemler tablosu
    cur.execute("""
    CREATE TABLE IF NOT EXISTS transactions (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        timestamp TEXT NOT NULL,
        year_month TEXT NOT NULL,
        asset_type TEXT NOT NULL,
        symbol TEXT NOT NULL,
        quantity REAL NOT NULL,
        unit_price REAL NOT NULL,
        total_amount REAL NOT NULL,
        currency TEXT NOT NULL,
        conversion_rate REAL NOT NULL
    )
    """)

    # 2) Kayıtlı sembollerin asset_type’ını tutan tablo
    cur.execute("""
    CREATE TABLE IF NOT EXISTS assets (
        symbol TEXT PRIMARY KEY,
        asset_type TEXT NOT NULL
    )
    """)

    conn.commit()
