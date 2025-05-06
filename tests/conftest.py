# tests/conftest.py

import sqlite3
import pytest

# tests/conftest.py
import sys, os
# proje kökünü path’e ekle
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))


@pytest.fixture(autouse=True)
def in_memory_db(monkeypatch):
    # 1) Her test için tek ortak in-memory bağlantısı oluştur
    conn = sqlite3.connect(":memory:")

    # 2) init_db() çağrıldığında modules/transactions/db.py’nin get_connection’ı in-memory’e dönsün
    import modules.transactions.db as db_mod
    monkeypatch.setattr(db_mod, "get_connection", lambda: conn)

    # 3) repository içindeki get_connection de aynı conn’a dönsün
    import modules.transactions.repository as repo_mod
    monkeypatch.setattr(repo_mod, "get_connection", lambda: conn)

    # 4) Şema (transactions + assets tabloları) in-memory DB’de oluşturulsun
    from modules.transactions.db import init_db
    init_db()

    yield conn

    # Testten sonra bağlantıyı kapat
    conn.close()
