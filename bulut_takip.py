import streamlit as st
import pandas as pd
from datetime import datetime

# 1. SAYFA AYARLARI
st.set_page_config(page_title="Kuveyttürk Dinamik Ekip PRO", layout="wide", page_icon="🏦")

# 2. KURUMSAL TASARIM
st.markdown("""
    <style>
    .stApp { background-color: #f0f2f6; }
    .stButton>button { background-color: #006736; color: white; border-radius: 12px; height: 3.5em; font-weight: bold; }
    h1 { color: #006736; text-align: center; border-bottom: 2px solid #006736; padding-bottom: 10px; }
    </style>
    """, unsafe_allow_html=True)

st.title("🏦 İkitelli Ticari - Dinamik Ekip Yönetim Paneli")

# 3. VERİ BAĞLANTISI
CSV_URL = "https://docs.google.com/spreadsheets/d/e/2PACX-1vRpvbLTEaAIgtMaId8eNq6bTDA6rxwti_582SZEHAJu6cD_AzoBb8fZCOYfl_zV3DehPKjWOjmvyV_8/pub?gid=1341056098&single=true&output=csv"

@st.cache_data(ttl=2)
def verileri_yukle():
    try:
        taze_url = f"{CSV_URL}&cb={datetime.now().timestamp()}"
        df = pd.read_csv(taze_url)
        df.columns = df.columns.str.strip()
        return df
    except:
        return None

df = verileri_yukle()

# --- SÜTUN İSİMLERİNİ FORMUNA GÖRE TANIMLIYORUZ ---
ACILIYET_SUTUNU = "Aciliyet (Çoktan Seçmeli: Normal, Acil, Kritik)"
ZAMAN_SUTUNU = "Zaman damgası"
FIRMA_SUTUNU = "Firma Ünvanı"

# 4. SOL PANEL
with st.sidebar:
    st.header("📌 Menü")
    st.link_button("🚀 YENİ İŞ KAYDI GİR", "https://docs.google.com/forms/d/1r9odjXloW2hhNqlHm4uo-4dV-aicS4l5s_E9J108s6s/viewform")
    st.divider()
    st.info("Kritik işler kırmızı satırla gösterilir.")

# 5. ÜST ÖZET VE RENKLENDİRME
if df is not None and not df.empty:
    col1, col2, col3 = st.columns(3)
    col1.metric("Toplam İşlem", len(df))
    
    # Kritik işleri say (Metin içinde 'Kritik' geçenleri bulur)
    if ACILIYET_SUTUNU in df.columns:
        kritik_sayisi = len(df[df[ACILIYET_SUTUNU].str.contains('Kritik', na=False)])
        col2.metric("Kritik Seviye", kritik_sayisi)
    
    col3.metric("Durum", "Aktif Çalışıyor")

    # RENKLENDİRME FONKSİYONU
    def satir_stili(row):
        if ACILIYET_SUTUNU in row.index and 'Kritik' in str(row[ACILIYET_SUTUNU]):
            return ['background-color: #ffcccc'] * len(row)
        return [''] * len(row)

    st.subheader("📋 Güncel Takip Listesi")
    
    # Zaman sıralaması
    if ZAMAN_SUTUNU in df.columns:
        df[ZAMAN_SUTUNU] = pd.to_datetime(df[ZAMAN_SUTUNU])
        df = df.sort_values(by=ZAMAN_SUTUNU, ascending=False)

    # Görsel tabloyu oluştur
    styled_df = df.style.apply(satir_stili, axis=1)
    st.dataframe(styled_df, use_container_width=True, hide_index=True)

else:
    st.info("Henüz görüntülenecek veri yok veya tablo bağlantısı kuruluyor.")
