import sqlite3
import pytest
from modules.transactions import db

@pytest.fixture
def mem_conn(monkeypatch):
    # tüm get_connection çağrılarını bellek içi SQLite'a yönlendir
    conn = sqlite3.connect(":memory:")
    monkeypatch.setattr(db, "get_connection", lambda: conn)
    yield conn
    conn.close()

def test_init_db_creates_tables(mem_conn):
    cur = mem_conn.cursor()
    # henüz tablo yokken SELECT denemesi OperationalError verir
    with pytest.raises(sqlite3.OperationalError):
        cur.execute("SELECT * FROM transactions")
    # init_db() çalışınca tablolar oluşmalı
    db.init_db()
    cur.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='transactions'")
    assert cur.fetchone() is not None
    cur.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='assets'")
    assert cur.fetchone() is not None
