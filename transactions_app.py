import streamlit as st
from datetime import datetime

# Mevcut transactions modülünüzü kullanıyoruz:
from modules.transactions.transactions import (
    init_db, add_transaction, get_transactions, summarize_cash_flow
)

# Sayfa başında DB’yi başlat (ilk form gösteriminde tablo oluşsun)
init_db()

st.title("🗃️ Transactions Demo")

# --- 1) Form ile yeni işlem girişi ---
st.header("Yeni İşlem Ekle")
with st.form("tx_form", clear_on_submit=True):
    ts = st.date_input("Tarih", value=datetime.today())
    tm = st.time_input("Saat", value=datetime.now().time().replace(second=0, microsecond=0))
    asset = st.selectbox("Varlık Türü", ["hs","yf","bes","crypto","cash"])
    symbol = st.text_input("Sembol / Açıklama")
    qty = st.number_input("Adet / Miktar", min_value=0.0, step=1.0)
    price = st.number_input("Birim Fiyat (USD)", min_value=0.0, step=0.01)
    rate = st.number_input("Kur (1 USD = ? TL)", min_value=0.0, step=0.01, value=1.0)
    submitted = st.form_submit_button("Ekle")
    if submitted:
        timestamp = datetime.combine(ts, tm)
        add_transaction(timestamp, asset, symbol, qty, price, "USD", rate)
        st.success("İşlem eklendi!")

# --- 2) Tabloda tüm işlemleri göster ---
st.header("Tüm İşlemler")
txs = get_transactions()
if txs:
    st.dataframe(txs)
else:
    st.write("Henüz işlem yok.")

# --- 3) Aylık özet ve grafik ---
st.header("Aylık Özet")
sel_ym = st.selectbox("Ay seçin", sorted({tx["year_month"] for tx in txs}))
if sel_ym:
    summary = summarize_cash_flow(sel_ym)
    st.write("Toplamlar döviz bazında:", summary["total_by_currency"])
    st.write("USD cinsinden toplam:", summary["total_in_usd"])

    # Grafik
    import pandas as pd
    df = pd.DataFrame.from_dict(summary["total_by_currency"], orient="index", columns=["Amount"])
    st.bar_chart(df)

