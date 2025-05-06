# modules/transactions/service.py
from datetime import datetime
from .repository import (
    get_asset_type, set_asset_type,
    insert_transaction, get_transactions
)
from .fx import fetch_conversion_rate
from .models import Transaction

class MissingAssetType(Exception):
    def __init__(self, symbol): super().__init__(symbol); self.symbol = symbol

def add_transaction(
    timestamp: datetime,
    symbol: str,
    quantity: float,
    unit_price: float,
    currency: str,
    asset_type: str | None = None,
    conversion_rate: float | None = None
) -> int:
    # 1) asset_type otomatik
    if asset_type is None:
        asset_type = get_asset_type(symbol)
        if not asset_type:
            raise MissingAssetType(symbol)

    # 2) conversion_rate otomatik
    curr = currency.upper()
    if conversion_rate is None:
        if curr == "USD":
            conversion_rate = 1.0
        elif curr in ("TL","TRY"):
            conversion_rate = fetch_conversion_rate(timestamp.date())
        else:
            conversion_rate = 1.0

    ym = timestamp.strftime("%Y-%m")
    total = quantity * unit_price

    tx = Transaction(
      id=None, timestamp=timestamp, year_month=ym,
      asset_type=asset_type, symbol=symbol.upper(),
      quantity=quantity, unit_price=unit_price,
      total_amount=total, currency=curr,
      conversion_rate=conversion_rate
    )
    return insert_transaction(tx)

def summarize_cash_flow(year_month: str) -> dict:
    """
    Tek ay için toplamı currency bazlı ve USD eşdeğeri olarak döner.
    """
    rows = get_transactions(start_ym=year_month, end_ym=year_month)
    totals, usd = {}, 0.0
    for r in rows:
        amt, rate = r["total_amount"], r["conversion_rate"]
        curr = r["currency"]
        totals.setdefault(curr, 0.0)
        totals[curr] += amt
        usd += (amt if curr=="USD" else amt / rate)
    return {"total_by_currency": totals, "total_in_usd": usd}

def get_monthly_cashflow(period_years: int) -> list[dict]:
    """
    period_years: 1|3|5|10
    Bugünden geriye her ay {"year_month","total_in_usd"} listesi.
    """
    now = datetime.now()
    start_year = now.year - period_years
    start_month = now.month

    y, m = start_year, start_month
    out = []
    while (y < now.year) or (y==now.year and m <= now.month):
        ym = f"{y:04d}-{m:02d}"
        cf = summarize_cash_flow(ym)["total_in_usd"]
        out.append({"year_month": ym, "total_in_usd": cf})
        m+=1
        if m==13: m, y = 1, y+1
    return out
