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
        # SÜTUN İSİMLERİNİ TEMİZLE (Boşlukları siler, hepsini standart hale getirir)
        df.columns = df.columns.str.strip()
        return df
    except:
        return None

df = verileri_yukle()

# 4. SOL PANEL
with st.sidebar:
    st.header("📌 Menü")
    st.link_button("🚀 YENİ İŞ KAYDI GİR", "https://docs.google.com/forms/d/1r9odjXloW2hhNqlHm4uo-4dV-aicS4l5s_E9J108s6s/viewform")
    st.divider()

# 5. KONTROL VE GÖRÜNTÜLEME
if df is not None and not df.empty:
    # Hata almamak için sütun kontrolü yapıyoruz
    mevcut_sutunlar = df.columns.tolist()
    
    # Eğer 'Aciliyet' sütunu varsa metrikleri hesapla, yoksa güvenli geç
    aciliyet_sutunu = "Aciliyet" if "Aciliyet" in mevcut_sutunlar else None
    
    col1, col2, col3 = st.columns(3)
    col1.metric("Toplam İşlem", len(df))
    
    if aciliyet_sutunu:
        kritik_sayisi = len(df[df[aciliyet_sutunu].str.contains('Kritik', na=False)])
        col2.metric("Kritik Seviye", kritik_sayisi)
    else:
        col2.warning("'Aciliyet' sütunu bulunamadı")
        # Mevcut sütunları göstererek debug yapalım
        st.write("Mevcut Sütunlar:", mevcut_sutunlar)

    col3.metric("Hedeflenen", "2026 Planı")

    # RENKLENDİRME FONKSİYONU (Güvenli hal)
    def satir_stili(row):
        if aciliyet_sutunu and 'Kritik' in str(row[aciliyet_sutunu]):
            return ['background-color: #ffcccc'] * len(row)
        return [''] * len(row)

    st.subheader("📋 Güncel Takip Listesi")
    
    # Zaman sıralaması (Eğer varsa)
    zaman_sutunu = "Zaman damgası" if "Zaman damgası" in mevcut_sutunlar else mevcut_sutunlar[0]
    try:
        df[zaman_sutunu] = pd.to_datetime(df[zaman_sutunu])
        df = df.sort_values(by=zaman_sutunu, ascending=False)
    except:
        pass

    styled_df = df.style.apply(satir_stili, axis=1)
    st.dataframe(styled_df, use_container_width=True, hide_index=True)

else:
    st.info("Henüz görüntülenecek veri yok veya tablo bağlantısı bekleniyor.")
