import sqlite3
from datetime import datetime
import pytest
from modules.transactions import db, service, repository

@pytest.fixture
def temp_db(tmp_path, monkeypatch):
    # proje kökünde tmp_path/test.db dosyası
    db_file = tmp_path / "test.db"
    conn = sqlite3.connect(str(db_file))
    # core.db.get_connection → bu dosyaya
    import core.db as core_db
    monkeypatch.setattr(core_db, "get_connection", lambda: sqlite3.connect(str(db_file)))
    # aynı dosyayı repository ve service de kullansın
    db.init_db()
    yield conn
    conn.close()

def test_full_flow(temp_db):
    # 1) Asset tipini kaydet
    repository.set_asset_type("XYZ", "Kripto Para")

    # 2) İşlem ekle
    ts = datetime(2023, 1, 15, 9, 0)
    tx_id = service.add_transaction(ts, symbol="XYZ", quantity=5, unit_price=2.0, currency="USD")
    assert isinstance(tx_id, int)

    # 3) get_transactions ile okuyalım
    rows = repository.get_transactions(symbol="XYZ")
    assert len(rows) == 1
    assert rows[0]["id"] == tx_id

    # 4) aylık akış verisini al
    data = service.get_monthly_cashflow(1)
    # en az bir öğe döner ve format doğru
    assert isinstance(data, list)
    assert "year_month" in data[0] and "total_in_usd" in data[0]
