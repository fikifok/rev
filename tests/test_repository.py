import sqlite3
import pytest
from modules.transactions import db, repository
from modules.transactions.models import Transaction
from datetime import datetime as _dt

@pytest.fixture
def mem_db(monkeypatch):
    # bellek içi DB ve init
    conn = sqlite3.connect(":memory:")
    monkeypatch.setattr(repo_db := __import__("modules.transactions.db", fromlist=["get_connection"]), "get_connection", lambda: conn)
    # repository.get_connection de aynı conn'i kullansın
    monkeypatch.setattr(repository, "get_connection", lambda: conn)
    # tabloları oluştur
    db.init_db()
    yield conn
    conn.close()

def test_set_and_get_asset_type(mem_db):
    repository.set_asset_type("xyz", "Kripto Para")
    assert repository.get_asset_type("xyz") == "Kripto Para"
    # güncelleme
    repository.set_asset_type("xyz", "USD")
    assert repository.get_asset_type("XYZ") == "USD"

def test_insert_get_update_delete_transaction(mem_db):
    # Transaction objesi yerine dict bazlı insert

    tx = Transaction(
        id=None,
        timestamp=_dt.fromisoformat("2022-05-06T12:00:00"),
                     year_month="2022-05", asset_type="Hisse Senedi",
                     symbol="ABC", quantity=2, unit_price=5.0,
                     total_amount=10.0, currency="USD", conversion_rate=1.0)
    tx_id = repository.insert_transaction(tx)
    assert isinstance(tx_id, int)

    # get_transactions
    rows = repository.get_transactions(symbol="ABC")
    assert len(rows) == 1
    assert rows[0]["symbol"] == "ABC"

    # update
    ok = repository.update_transaction(tx_id, quantity=5)
    assert ok
    rows2 = repository.get_transactions(symbol="ABC")
    assert rows2[0]["quantity"] == 5

    # delete
    ok2 = repository.delete_transaction(tx_id)
    assert ok2
    assert repository.get_transactions(symbol="ABC") == []
