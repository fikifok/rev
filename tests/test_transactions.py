"""
tests/test_transactions.py

Unit tests for transactions module.
"""
import pytest
from datetime import datetime
from core.config import SETTINGS

# Use in-memory database for tests
SETTINGS['database_path'] = ":memory:"

from core.db import get_connection
from modules.transactions.transactions import (
    init_db, add_transaction, get_transactions,
    update_transaction, delete_transaction,
    summarize_cash_flow, calculate_positions
)

@pytest.fixture(autouse=True)
def setup_db():
    init_db()
    yield

def test_add_and_get_transaction():
    ts = datetime(2023, 5, 15, 10, 30)
    tx_id = add_transaction(ts, "hs", "TEST", 10, 100.0, "TL", 23.5)
    txs = get_transactions()
    assert len(txs) == 1
    assert txs[0]["id"] == tx_id
    assert txs[0]["symbol"] == "TEST"

def test_update_transaction():
    ts = datetime(2023, 5, 15, 10, 30)
    tx_id = add_transaction(ts, "crypto", "COIN", 5, 20.0, "USD", 23.5)
    success = update_transaction(tx_id, quantity=7)
    assert success
    txs = get_transactions()
    assert txs[0]["quantity"] == 7

def test_delete_transaction():
    ts = datetime(2023, 5, 15, 10, 30)
    tx_id = add_transaction(ts, "yf", "FUND", 2, 50.0, "TL", 23.5)
    assert delete_transaction(tx_id)
    assert get_transactions() == []

def test_summarize_cash_flow():
    add_transaction(datetime(2023, 5, 1), "hs", "A", 1, 100.0, "TL", 20.0)
    add_transaction(datetime(2023, 5, 2), "crypto", "B", 2, 10.0, "USD", 20.0)
    summary = summarize_cash_flow("2023-05")
    assert summary["total_by_currency"]["TL"] == 100.0
    assert summary["total_by_currency"]["USD"] == 20.0
    # 100 TL @20 => 5 USD + 20 USD
    assert pytest.approx(summary["total_in_usd"], rel=1e-6) == 25.0

def test_calculate_positions():
    add_transaction(datetime(2023, 1, 1), "hs", "A", 3, 100.0, "TL", 18.0)
    add_transaction(datetime(2023, 2, 1), "hs", "A", 2, 200.0, "TL", 18.0)
    pos = calculate_positions("2023-02")
    key = ("hs", "A")
    assert key in pos
    assert pos[key]["quantity"] == 5
    assert pytest.approx(pos[key]["avg_cost"], rel=1e-6) == 140.0
    assert pos[key]["currency"] == "TL"
