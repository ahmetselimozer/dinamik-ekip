import streamlit as st
import pandas as pd
from datetime import datetime

# 1. SAYFA AYARLARI
st.set_page_config(page_title="Kuveyttürk Dinamik Ekip", layout="wide", page_icon="🏦")

# 2. KURUMSAL TASARIM
st.markdown("""
    <style>
    .stApp { background-color: #f4f7f6; }
    .stButton>button { background-color: #006736; color: white; border-radius: 10px; height: 3.5em; width: 100%; font-weight: bold; }
    h1 { color: #006736; font-family: 'Arial'; }
    .stDataFrame { background-color: white; border-radius: 10px; }
    </style>
    """, unsafe_allow_html=True)

st.title("🏦 İkitelli Ticari - Dinamik Ekip Paneli")

# 3. GOOGLE SHEETS ID (Senin dosyanın ID'si)
# Eğer dosya değişmediyse bu ID sabit kalmalı:
SHEET_ID = "1FOy_NSRZUtJIApBe7oirdKSp17qfJk9arb_yOwcPo1g"
# En sağlam indirme linki formatı budur:
SHEET_URL = f"https://docs.google.com/spreadsheets/d/{SHEET_ID}/export?format=csv"

# 4. VERİ ÇEKME FONKSİYONU
@st.cache_data(ttl=5)
def verileri_yukle():
    try:
        # Linkin sonuna benzersiz bir sayı ekleyerek Google'ı zorluyoruz (Cache temizleme)
        taze_url = f"{SHEET_URL}&v={datetime.now().timestamp()}"
        df = pd.read_csv(taze_url)
        return df
    except Exception as e:
        # Eğer hala hata alıyorsak, hatayı ekrana yazdır ki sorunu görelim
        st.error(f"Bağlantı sorunu yaşanıyor. Lütfen Google Sheets 'Paylaş' ayarlarını kontrol edin. Hata: {e}")
        return pd.DataFrame()

is_listesi = verileri_yukle()

# 5. SOL PANEL
with st.sidebar:
    st.header("📌 İşlem Yönetimi")
    st.link_button("🚀 YENİ İŞ KAYDI GİR", "https://docs.google.com/forms/d/1r9odjXloW2hhNqlHm4uo-4dV-aicS4l5s_E9J108s6s/viewform")
    st.divider()
    st.info("Kayıtlar doğrudan Google Sheets'e işlenir.")

# 6. ANA PANEL
st.subheader("📋 Aktif İş Takip Listesi")

if not is_listesi.empty:
    st.dataframe(is_listesi, use_container_width=True, hide_index=True)
else:
    st.warning("Şu an tablo verisi çekilemiyor. Dosyanın 'Bağlantıya sahip olan herkes: Görüntüleyebilir' olduğundan emin olun.")
