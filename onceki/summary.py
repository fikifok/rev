# src/modules/summary.py
import pandas as pd

def generate_monthly_summary(transactions_df: pd.DataFrame) -> pd.DataFrame:
    """
    Aylık toplam alım miktarları (quantity) ve tutarları (cost) pivotlanmış DataFrame döner.

    Args:
        transactions_df (pd.DataFrame):
            ['date','type','asset_type','symbol','quantity','price_per_unit'] sütunlarını içeren DataFrame.

    Returns:
        pd.DataFrame: Index'i Period('M') tipinde month olan; sütunları
                      qty_stock, qty_crypto, cost_stock, cost_crypto olan pivot DataFrame.
    """
    df = transactions_df.copy()
    df['date'] = pd.to_datetime(df['date'])
    df['month'] = df['date'].dt.to_period('M')
    df['cost'] = df['quantity'] * df['price_per_unit']
    # Sadece alımlar (buy)
    buys = df[df['type'] == 'buy']
    summary = buys.groupby(['month','asset_type']).agg(
        total_quantity=('quantity','sum'),
        total_cost=('cost','sum')
    ).reset_index()
    # Pivot
    qty_pivot  = summary.pivot(index='month', columns='asset_type', values='total_quantity').fillna(0)
    cost_pivot = summary.pivot(index='month', columns='asset_type', values='total_cost').fillna(0)
    qty_pivot.columns  = [f"qty_{col}" for col in qty_pivot.columns]
    cost_pivot.columns = [f"cost_{col}" for col in cost_pivot.columns]
    result = pd.concat([qty_pivot, cost_pivot], axis=1).sort_index()
    return result

def generate_cumulative_summary(monthly_summary_df: pd.DataFrame) -> pd.DataFrame:
    """
    Aylık özet DataFrame üzerinden kümülatif toplamları hesaplar.

    Args:
        monthly_summary_df (pd.DataFrame): generate_monthly_summary çıktısı.

    Returns:
        pd.DataFrame: Her sütunun kümülatif toplamı.
    """
    return monthly_summary_df.cumsum()

class Summary:
    """Boş stub sınıf: test_import_summary için."""
    pass
