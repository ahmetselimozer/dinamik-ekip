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
    .stDataFrame { background-color: white; border-radius: 10px; }
    </style>
    """, unsafe_allow_html=True)

st.title("🏦 İkitelli Ticari - Dinamik Ekip Yönetim Paneli")

# 3. VERİ BAĞLANTISI
CSV_URL = "https://docs.google.com/spreadsheets/d/e/2PACX-1vRpvbLTEaAIgtMaId8eNq6bTDA6rxwti_582SZEHAJu6cD_AzoBb8fZCOYfl_zV3DehPKjWOjmvyV_8/pub?gid=1341056098&single=true&output=csv"

@st.cache_data(ttl=1)
def verileri_yukle():
    try:
        taze_url = f"{CSV_URL}&cb={datetime.now().timestamp()}"
        df = pd.read_csv(taze_url)
        # Sütun isimlerindeki tüm boşlukları ve gizli karakterleri temizle
        df.columns = df.columns.str.strip()
        return df
    except:
        return None

df = verileri_yukle()

# 4. SOL PANEL
with st.sidebar:
    st.header("📌 İşlem Yönetimi")
    st.link_button("🚀 YENİ İŞ KAYDI GİR", "https://docs.google.com/forms/d/1r9odjXloW2hhNqlHm4uo-4dV-aicS4l5s_E9J108s6s/viewform")
    st.divider()
    st.info("Kritik işler listede kırmızı satırla vurgulanır.")

# 5. AKILLI SÜTUN BULUCU (Sen isim değiştirsen de bulur)
if df is not None and not df.empty:
    # Sütun isimlerini listele
    cols = df.columns.tolist()
    
    # İçinde 'Aciliyet' geçen sütunu bul
    aciliyet_col = next((c for c in cols if "Aciliyet" in c), None)
    # İçinde 'Zaman' geçen sütunu bul
    zaman_col = next((c for c in cols if "Zaman" in c), None)

    # ÜST METRİKLER
    col1, col2, col3 = st.columns(3)
    col1.metric("Toplam İşlem", len(df))
    
    if aciliyet_col:
        # 'Kritik' kelimesi geçen satırları say
        kritik_sayisi = len(df[df[aciliyet_col].astype(str).str.contains('Kritik', na=False)])
        col2.metric("Kritik Seviye", kritik_sayisi)
    
    col3.metric("Durum", "Aktif")

    # RENKLENDİRME FONKSİYONU
    def satir_stili(row):
        if aciliyet_col and 'Kritik' in str(row[aciliyet_col]):
            return ['background-color: #ffcccc'] * len(row)
        return [''] * len(row)

    st.subheader("📋 Güncel Takip Listesi")
    
    # Zaman sıralaması
    if zaman_col:
        df[zaman_col] = pd.to_datetime(df[zaman_col])
        df = df.sort_values(by=zaman_col, ascending=False)

    # Tabloyu göster
    styled_df = df.style.apply(satir_stili, axis=1)
    st.dataframe(styled_df, use_container_width=True, hide_index=True)

else:
    st.info("Veri bekleniyor... Formu gönderdiyseniz 10 saniye içinde burada görünecektir.")

st.caption(f"Son Güncelleme: {datetime.now().strftime('%H:%M:%S')}")
