# core/db.py
import sqlite3
from core.config import SETTINGS
from pathlib import Path

def get_connection():
    # 1) Bu dosyanın bulunduğu klasörden bir seviye yukarı çıkıp 'data/transactions.db' dosyasını gösterir
    base_dir = Path(__file__).resolve().parent.parent
    db_path = base_dir / "data" / "transactions.db"

    db_path.parent.mkdir(parents=True, exist_ok=True)

    # 3) Dosya yolunu str() ile verip SQLite'a bağlan
    conn = sqlite3.connect(str(db_path), check_same_thread=False)
    # 4) Satırları hem sütun adı ile hem indeks ile erişilebilir hale getir
    conn.row_factory = sqlite3.Row
    return conn

_conn = None
