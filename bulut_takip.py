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
    .stDataFrame { background-color: white; border-radius: 10px; box-shadow: 0 2px 4px rgba(0,0,0,0.1); }
    </style>
    """, unsafe_allow_html=True)

st.title("🏦 İkitelli Ticari - Dinamik Ekip Paneli")

# 3. GOOGLE SHEETS BAĞLANTISI (Doğrudan Link Yöntemi)
# Buradaki linki "Paylaş" butonuna bastığında aldığın linkle değiştirelim
SHEET_PUBLIC_LINK = "https://docs.google.com/spreadsheets/d/1FOy_NSRZUtJIApBe7oirdKSp17qfJk9arb_yOwcPo1g/edit?usp=sharing"

# 4. VERİ ÇEKME FONKSİYONU
@st.cache_data(ttl=5)
def verileri_yukle(url):
    # Linki CSV formatına dönüştüren güvenli yöntem
    csv_url = url.replace('/edit?usp=sharing', '/export?format=csv')
    try:
        df = pd.read_csv(csv_url)
        return df
    except Exception as e:
        st.error(f"Bağlantı Hatası: {e}")
        return pd.DataFrame()

is_listesi = verileri_yukle(SHEET_PUBLIC_LINK)

# 5. SOL PANEL
with st.sidebar:
    st.header("📌 İşlem Yönetimi")
    st.link_button("🚀 YENİ İŞ KAYDI GİR", "https://docs.google.com/forms/d/1r9odjXloW2hhNqlHm4uo-4dV-aicS4l5s_E9J108s6s/viewform")
    st.divider()
    st.info("Kayıtlar doğrudan Google Sheets'e işlenir.")

# 6. ANA PANEL
st.subheader("📋 Aktif İş Takip Listesi")

if not is_listesi.empty:
    # Sütunları temizleyelim (Boş sütunları gösterme)
    is_listesi = is_listesi.dropna(how='all', axis=1)
    st.dataframe(is_listesi, use_container_width=True, hide_index=True)
else:
    st.info("Tablo okunuyor veya henüz veri yok. Lütfen Google Sheets dosyanızda 'Bağlantıya sahip olan herkes: Görüntüleyebilir' ayarının açık olduğundan emin olun.")

st.caption(f"Son Senkronizasyon: {datetime.now().strftime('%H:%M:%S')}")
