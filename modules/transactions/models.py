# modules/transactions/models.py
from dataclasses import dataclass
from datetime import datetime

@dataclass
class Transaction:
    id: int | None
    timestamp: datetime
    year_month: str
    asset_type: str
    symbol: str
    quantity: float
    unit_price: float
    total_amount: float
    currency: str
    conversion_rate: float

@dataclass
class Asset:
    symbol: str
    asset_type: str
