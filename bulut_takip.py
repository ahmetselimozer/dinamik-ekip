import streamlit as st
from b_connector import GSheetConnector # Yardımcı bağlantı aracı
import pandas as pd
from datetime import datetime

# Sayfa Konfigürasyonu
st.set_page_config(page_title="Kuveyttürk Dinamik Ekip", layout="wide")

# Kurumsal Tema
st.markdown("""
    <style>
    .stApp { background-color: #f8f9fa; }
    .stButton>button { background-color: #006736; color: white; border-radius: 8px; font-weight: bold; }
    h1 { color: #006736; }
    </style>
    """, unsafe_allow_html=True)

st.title("🏦 İkitelli Ticari - Dinamik Ekip")

# Google Sheets Bağlantı Bilgisi (Dün verdiğin ID)
SHEET_ID = "1FOy_NSRZUtJIApBe7oirdKSp17qfJk9arb_yOwcPo1g"
SHEET_URL = f"https://docs.google.com/spreadsheets/d/{SHEET_ID}/gviz/tq?tqx=out:csv"

# Verileri Google Sheets'ten Çekme
@st.cache_data(ttl=10) # 10 saniyede bir veriyi tazeler
def verileri_yukle():
    try:
        return pd.read_csv(SHEET_URL)
    except:
        return pd.DataFrame(columns=["Firma", "Kategori", "Aciliyet", "Durum", "Zaman"])

is_listesi = verileri_yukle()

# --- YAN PANEL (GİRİŞ FORMU) ---
with st.sidebar:
    st.header("📌 Yeni İşlem Girişi")
    firma = st.text_input("Firma Ünvanı")
    kategori = st.selectbox("İşlem Türü", ["Tahsis", "Kredi İşlemleri", "Dış Ticaret", "Hazine", "Nakit Yönetimi"])
    acil = st.select_slider("Aciliyet", options=["Normal", "Yüksek", "Kritik"])
    
    if st.button("Havuza Gönder"):
        if firma:
            st.success(f"{firma} başarıyla eklendi! (Tabloyu manuel güncelleyin)")
            # Şimdilik listeye ekleme simülasyonu
            st.info("Not: Verilerin kalıcı yazılması için Google izni gereklidir.")

# --- ANA PANEL ---
st.subheader("📋 Mevcut İş Listesi")
if not is_listesi.empty:
    st.dataframe(is_listesi, use_container_width=True)
else:
    st.warning("Henüz tabloda veri bulunamadı. Lütfen Google Sheets dosyanıza ilk satır başlıklarını ekleyin.")

st.info("💡 İpucu: Telefonundan 'Ana Ekrana Ekle' yaparak uygulama gibi kullanabilirsin.")
