import streamlit as st
import pandas as pd
from datetime import datetime

# Sayfa Ayarları
st.set_page_config(page_title="Dinamik Ekip Takip", page_icon="🏦", layout="wide")

# Kurumsal Stil (Kuveyttürk Yeşili)
st.markdown("""
    <style>
    .main { background-color: #f5f5f5; }
    .stButton>button { background-color: #006736; color: white; border-radius: 5px; }
    div.stTitle { color: #006736 !important; font-weight: bold; }
    </style>
    """, unsafe_allow_html=True)

st.title("🏦 Dinamik Ekip Portföy Yönetimi")

# Veri Saklama Mantığı
if 'is_listesi' not in st.session_state:
    st.session_state.is_listesi = pd.DataFrame(columns=["Firma", "Kategori", "Aciliyet", "Durum", "Zaman"])

# Yan Panel
with st.sidebar:
    st.header("Yeni İşlem Girişi")
    firma = st.text_input("Firma Ünvanı")
    kategori = st.selectbox("İşlem Türü", ["Tahsis", "Kredi (Nakit)", "Kredi (Gayrinakit)", "Dış Ticaret", "Hazine", "Nakit Yönetimi"])
    acil = st.select_slider("Aciliyet Durumu", options=["Normal", "Yüksek", "Kritik"])
    
    if st.button("Havuza Ekle"):
        if firma:
            yeni_is = pd.DataFrame([[firma, kategori, acil, "Bekliyor", datetime.now().strftime("%H:%M")]], 
                                  columns=["Firma", "Kategori", "Aciliyet", "Durum", "Zaman"])
            st.session_state.is_listesi = pd.concat([st.session_state.is_listesi, yeni_is], ignore_index=True)
            st.rerun()

# Liste Görüntüleme
if not st.session_state.is_listesi.empty:
    st.dataframe(st.session_state.is_listesi, use_container_width=True)
    
    # İşlem Yönetimi
    col1, col2 = st.columns(2)
    with col1:
        secilen = st.number_input("Güncellenecek Sıra No", min_value=0, max_value=len(st.session_state.is_listesi)-1, step=1)
    with col2:
        if st.button("Seçiliyi TAMAMLANDI Yap"):
            st.session_state.is_listesi.at[secilen, "Durum"] = "✅ TAMAMLANDI"
            st.rerun()
else:
    st.info("Şu an bekleyen bir işlem yok.")
