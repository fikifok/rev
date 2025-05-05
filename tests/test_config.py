import pytest
from core.config import SETTINGS

def test_finnhub_key_exists():
    assert SETTINGS['finnhub_api_key'] is not None
