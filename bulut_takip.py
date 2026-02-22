import streamlit as st
import pandas as pd
from datetime import datetime

# BURAYA KENDİ GOOGLE SHEETS LINKINI YAZACAKSIN
SHEET_URL = "https://docs.google.com/spreadsheets/d/SENIN_TABLO_ID_BURAYA/export?format=csv"

st.set_page_config(page_title="Kuveyttürk Dinamik Takip", layout="wide")

# Veri Okuma Fonksiyonu
def veri_getir():
    try:
        return pd.read_csv(SHEET_URL)
    except:
        return pd.DataFrame(columns=["Firma", "Kategori", "Aciliyet", "Durum", "Zaman"])

# Uygulama Arayüzü (Aynen Kalıyor)
st.title("🏦 İkitelli Ticari - Dinamik Ekip")

# Verileri Çek
is_listesi = veri_getir()

# ... (Giriş formu ve tablo gösterme kısımları yukarıdakiyle aynı olacak)
