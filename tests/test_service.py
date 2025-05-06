import pytest
from datetime import datetime, date
from modules.transactions import service
from modules.transactions.repository import set_asset_type

def test_add_transaction_missing_asset(monkeypatch):
    # hiçbir sembol kaydı yoksa MissingAssetType
    with pytest.raises(service.MissingAssetType):
        service.add_transaction(datetime.now(), symbol="ZZZ", quantity=1, unit_price=1, currency="USD")

def test_add_transaction_auto_conversion_and_insert(monkeypatch):
    # asset_type ve conversion_rate otomatik
    called = {}
    # önce repo.get_asset_type -> "USD"
    monkeypatch.setattr(service, "get_asset_type", lambda s: "USD")
    # sonra fetch_conversion_rate
    monkeypatch.setattr(service, "fetch_conversion_rate", lambda d: 8.0)
    # repo.insert_transaction yerine stub
    def fake_insert(tx):
        called["tx"] = tx
        return 42
    monkeypatch.setattr(service, "insert_transaction", fake_insert)

    ts = datetime(2022, 5, 6, 10, 0)
    tx_id = service.add_transaction(ts, symbol="AAA", quantity=2, unit_price=3.0, currency="TL")
    assert tx_id == 42
    tx = called["tx"]
    # asset_type geldi
    assert tx.asset_type == "USD"
    # conversion_rate tarihli kur
    assert tx.conversion_rate == 8.0
    # total_amount hesaplanmış
    assert tx.total_amount == pytest.approx(2 * 3.0)
