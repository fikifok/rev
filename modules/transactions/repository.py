# modules/transactions/repository.py
from .db import get_connection
from .models import Transaction, Asset
from typing import Optional

# --- asset registry ---
def get_asset_type(symbol: str) -> Optional[str]:
    conn = get_connection(); cur = conn.cursor()
    cur.execute("SELECT asset_type FROM assets WHERE symbol = ?", (symbol.upper(),))
    row = cur.fetchone()
    return row[0] if row else None

def set_asset_type(symbol: str, asset_type: str):
    conn = get_connection(); cur = conn.cursor()
    cur.execute("""
      INSERT INTO assets(symbol, asset_type)
      VALUES (?, ?)
      ON CONFLICT(symbol) DO UPDATE SET asset_type=excluded.asset_type
    """, (symbol.upper(), asset_type))
    conn.commit()

# --- transactions CRUD ---
def insert_transaction(tx: Transaction) -> int:
    conn = get_connection(); cur = conn.cursor()
    cur.execute("""
      INSERT INTO transactions (
        timestamp, year_month, asset_type, symbol,
        quantity, unit_price, total_amount, currency, conversion_rate
      ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (
      tx.timestamp.isoformat(),
      tx.year_month,
      tx.asset_type,
      tx.symbol.upper(),
      tx.quantity,
      tx.unit_price,
      tx.total_amount,
      tx.currency.upper(),
      tx.conversion_rate
    ))
    conn.commit()
    tx_id = cur.lastrowid
    return tx_id

def get_transactions(**filters) -> list[dict]:
    conn = get_connection(); cur = conn.cursor()
    query = "SELECT * FROM transactions WHERE 1=1"
    params = []
    if f := filters.get("asset_type"):
        query += " AND asset_type = ?"; params.append(f)
    if f := filters.get("symbol"):
        query += " AND symbol = ?"; params.append(f.upper())
    if f := filters.get("start_ym"):
        query += " AND year_month >= ?"; params.append(f)
    if f := filters.get("end_ym"):
        query += " AND year_month <= ?"; params.append(f)
    query += " ORDER BY timestamp"
    cur.execute(query, params)

    cols = [d[0] for d in cur.description]
    rows = cur.fetchall()

    return [dict(zip(cols, r)) for r in rows]

def update_transaction(tx_id: int, **fields) -> bool:
    allowed = {"timestamp","asset_type","symbol","quantity","unit_price","currency","conversion_rate"}
    sets, params = [], []
    for k,v in fields.items():
        if k in allowed:
            if k == "timestamp":
                sets.append("timestamp=?"); params.append(v.isoformat())
                sets.append("year_month=?"); params.append(v.strftime("%Y-%m"))
            else:
                sets.append(f"{k}=?"); params.append(v)
    if not sets: return False
    sql = f"UPDATE transactions SET {','.join(sets)} WHERE id=?"
    params.append(tx_id)
    conn = get_connection(); cur = conn.cursor()
    cur.execute(sql, params)
    conn.commit()
    ok = cur.rowcount>0
    return ok

def delete_transaction(tx_id: int) -> bool:
    conn = get_connection(); cur = conn.cursor()
    cur.execute("DELETE FROM transactions WHERE id=?", (tx_id,))
    conn.commit()
    ok = cur.rowcount>0
    return ok
