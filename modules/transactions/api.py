# modules/transactions/api.py
import streamlit as st
from datetime import datetime
import pandas as pd
from .service import add_transaction, MissingAssetType, get_monthly_cashflow
from .repository import set_asset_type

ASSET_TYPES = ["Hisse Senedi", "Yatırım Fonu", "Kripto Para", "USD", "Yeni Tür"]
def show_cashflow_chart():
    """
    Sidebar’da 1/3/5/10 yıllık net USD akışı çizgi grafiği.
    """
    st.sidebar.header("Aylık Net Akış")
    yrs = st.sidebar.selectbox("Dönem (yıl)", [1, 3, 5, 10], index=0)
    data = get_monthly_cashflow(yrs)
    # pandas DataFrame’e çevir, index’i year_month olsun
    df = pd.DataFrame(data).set_index("year_month")
    st.line_chart(df["total_in_usd"], height=300)


def transaction_form():
    st.sidebar.header("Yeni İşlem Ekle")
    ts     = st.sidebar.date_input("Tarih", datetime.today())
    symbol = st.sidebar.text_input("Sembol").upper()
    qty    = st.sidebar.number_input("Adet", min_value=0.0, step=0.1)
    price  = st.sidebar.number_input("Birim Fiyat", min_value=0.0, step=0.01)
    curr   = st.sidebar.selectbox("Para Birimi", ["USD", "TL"])

    # İşlemi ekle butonu
    if st.sidebar.button("Ekle"):
        try:
            add_transaction(
                timestamp=datetime.combine(ts, datetime.min.time()),
                symbol=symbol,
                quantity=qty,
                unit_price=price,
                currency=curr
            )
            st.success("İşlem kaydedildi.")
        except MissingAssetType as e:
            st.session_state.pending_symbol = e.symbol
            st.session_state.ask_asset = True

    # Eğer bir sembol için henüz asset type kaydı yoksa formu göster
    if st.session_state.get("ask_asset"):
        with st.sidebar.form("asset_type_form"):
            st.write(f"‘{st.session_state.pending_symbol}’ için varlık türü seçin:")
            at = st.selectbox("Varlık Türü", ASSET_TYPES)
            if at == "Yeni Tür":
                at = st.text_input("Yeni Tür Adı")
            submit = st.form_submit_button("Kaydet")

            # Bu blok da mutlaka form içinde girintili olmalı
            if submit:
                set_asset_type(st.session_state.pending_symbol, at)
                st.session_state.ask_asset = False
                # İşlemi tekrar çalıştırır; modal yerine formu kapatır
                st.experimental_rerun()
def run_app():
    # Veritabanı tablolarını hazırla
    from .db import init_db
    init_db()

    st.title("Portföy Takip")
    # Formu ve grafiği alt alta ekle
    transaction_form()
    show_cashflow_chart()
