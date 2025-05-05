"""
modules/transactions/transactions.py

Handles all CRUD operations and summaries for portfolio transactions.
"""
import sqlite3
from datetime import datetime
from core.db import get_connection

def init_db():
    """
    Create `transactions` table if it does not exist.
    """
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS transactions (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        timestamp TEXT NOT NULL,
        year_month TEXT NOT NULL,
        asset_type TEXT NOT NULL,
        symbol TEXT NOT NULL,
        quantity REAL NOT NULL,
        unit_price REAL NOT NULL,
        total_amount REAL NOT NULL,
        currency TEXT NOT NULL,
        conversion_rate REAL NOT NULL
    )
    """)
    conn.commit()
    conn.close()

def add_transaction(timestamp: datetime, asset_type: str, symbol: str,
                    quantity: float, unit_price: float,
                    currency: str, conversion_rate: float) -> int:
    """
    Add a new transaction record.
    """
    year_month = timestamp.strftime("%Y-%m")
    total_amount = quantity * unit_price

    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
    INSERT INTO transactions (
        timestamp, year_month, asset_type, symbol,
        quantity, unit_price, total_amount, currency, conversion_rate
    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        timestamp.isoformat(), year_month, asset_type, symbol,
        quantity, unit_price, total_amount, currency, conversion_rate
    ))
    conn.commit()
    tx_id = cursor.lastrowid
    conn.close()
    return tx_id

def get_transactions(asset_type: str = None, symbol: str = None,
                     start_ym: str = None, end_ym: str = None):
    """
    Retrieve transactions matching given filters.
    """
    conn = get_connection()
    cursor = conn.cursor()
    query = "SELECT * FROM transactions WHERE 1=1"
    params = []

    if asset_type:
        query += " AND asset_type = ?"
        params.append(asset_type)
    if symbol:
        query += " AND symbol = ?"
        params.append(symbol)
    if start_ym:
        query += " AND year_month >= ?"
        params.append(start_ym)
    if end_ym:
        query += " AND year_month <= ?"
        params.append(end_ym)

    query += " ORDER BY timestamp"
    cursor.execute(query, params)
    rows = cursor.fetchall()
    conn.close()

    return [dict(r) for r in rows]

def update_transaction(tx_id: int, **fields):
    """
    Update specified fields for a transaction.
    """
    allowed = {"timestamp", "asset_type", "symbol", "quantity",
               "unit_price", "currency", "conversion_rate"}
    set_clauses = []
    params = []

    for key, value in fields.items():
        if key in allowed:
            if key == "timestamp":
                ts_val = value.isoformat()
                ym_val = value.strftime("%Y-%m")
                set_clauses.append("timestamp = ?")
                params.append(ts_val)
                set_clauses.append("year_month = ?")
                params.append(ym_val)
            else:
                set_clauses.append(f"{key} = ?")
                params.append(value)

    if not set_clauses:
        return False

    sql = f"UPDATE transactions SET {', '.join(set_clauses)} WHERE id = ?"
    params.append(tx_id)

    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(sql, params)
    conn.commit()
    updated = cursor.rowcount
    conn.close()
    return updated > 0

def delete_transaction(tx_id: int):
    """
    Delete transaction by ID.
    """
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM transactions WHERE id = ?", (tx_id,))
    conn.commit()
    deleted = cursor.rowcount
    conn.close()
    return deleted > 0

def summarize_cash_flow(year_month: str):
    """
    Summarize cash inflow/outflow for the given month.
    Returns:
      { "total_by_currency": { ... },
        "total_in_usd": float }
    """
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
    SELECT currency, SUM(total_amount) AS sum_amt, AVG(conversion_rate) AS avg_rate
    FROM transactions
    WHERE year_month = ?
    GROUP BY currency
    """, (year_month,))
    rows = cursor.fetchall()
    conn.close()

    totals = {}
    total_usd = 0.0
    for r in rows:
        curr = r["currency"]
        amt = r["sum_amt"] or 0.0
        rate = r["avg_rate"] or 1.0
        totals[curr] = amt
        if curr == "USD":
            total_usd += amt
        elif curr == "TL":
            total_usd += amt / rate

    return {"total_by_currency": totals, "total_in_usd": total_usd}

def calculate_positions(as_of_ym: str):
    """
    Calculate net quantity and average cost for each asset up to the given month.
    Returns:
      { (asset_type, symbol): { "quantity": q, "avg_cost": c, "currency": curr } }
    """
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
    SELECT asset_type, symbol,
           SUM(quantity) AS total_qty,
           SUM(total_amount) AS total_cost,
           currency
    FROM transactions
    WHERE year_month <= ?
    GROUP BY asset_type, symbol, currency
    """, (as_of_ym,))
    rows = cursor.fetchall()
    conn.close()

    positions = {}
    for r in rows:
        qty = r["total_qty"] or 0.0
        cost = r["total_cost"] or 0.0
        avg_cost = cost / qty if qty else 0.0
        positions[(r["asset_type"], r["symbol"])] = {
            "quantity": qty,
            "avg_cost": avg_cost,
            "currency": r["currency"]
        }
    return positions

# Optional export (csv/json) if needed in future
def export_transactions(fmt: str, path: str, **filters):
    import csv, json
    data = get_transactions(**filters)
    if fmt == "csv":
        with open(path, "w", newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=data[0].keys())
            writer.writeheader()
            writer.writerows(data)
    elif fmt == "json":
        with open(path, "w", encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
