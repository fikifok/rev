import pytest
import requests
from datetime import date
from modules.transactions.fx import fetch_conversion_rate

class DummyResponse:
    def __init__(self, data, status_code=200):
        self._data = data
        self.status_code = status_code
    def raise_for_status(self):
        if self.status_code != 200:
            raise requests.HTTPError()
    def json(self):
        return self._data

def test_fetch_conversion_rate_success(monkeypatch):
    dummy = DummyResponse({"rates": {"TRY": 8.123}})
    monkeypatch.setattr(requests, "get", lambda *args, **kw: dummy)
    rate = fetch_conversion_rate(date(2021, 1, 1))
    assert rate == 8.123

def test_fetch_conversion_rate_failure(monkeypatch):
    # HTTP hatası ya da timeout durumunda 1.0 dönmeli
    monkeypatch.setattr(requests, "get", lambda *args, **kw: (_ for _ in ()).throw(requests.RequestException()))
    rate = fetch_conversion_rate(date(2021, 1, 1))
    assert rate == 1.0
