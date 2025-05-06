import pytest
from datetime import datetime
from modules.transactions.models import Transaction, Asset

def test_transaction_dataclass():
    ts = datetime(2022, 5, 6, 12, 0)
    tx = Transaction(id=None, timestamp=ts, year_month="2022-05",
                     asset_type="Hisse Senedi", symbol="ABC",
                     quantity=3.0, unit_price=10.0,
                     total_amount=30.0, currency="USD", conversion_rate=1.0)
    # alanların doğru atandığını ve total_amount tutarlı
    assert tx.id is None
    assert tx.timestamp == ts
    assert tx.total_amount == pytest.approx(tx.quantity * tx.unit_price)

def test_asset_dataclass():
    a = Asset(symbol="btc", asset_type="Kripto Para")
    assert a.symbol == "btc"
    assert a.asset_type == "Kripto Para"
