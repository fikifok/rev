# tests/conftest.py
import sys
import os

# Proje kök dizinini path’in en başına ekliyoruz
root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
if root not in sys.path:
    sys.path.insert(0, root)

import pytest
from core.config import SETTINGS

@pytest.fixture(autouse=True)
def use_temp_sqlite(tmp_path, monkeypatch):
    # 1) Disk-tabanlı geçici DB:
    db_file = tmp_path / "test_transactions.db"
    monkeypatch.setitem(SETTINGS, 'database_path', str(db_file))
    #
    # Eğer in-memory ile devam etmek isterseniz, bunun yerine:
    # uri = "file:tests_transactions?mode=memory&cache=shared"
    # monkeypatch.setitem(SETTINGS, 'database_path', uri)
    # (ve get_connection() içinde uri=True ayarlı olmalı)
    yield
