import streamlit as st
import pandas as pd
from datetime import datetime

# Sayfa Ayarları
st.set_page_config(page_title="Dinamik Ekip Takip", page_icon="🏦", layout="wide")

# Kurumsal Stil (Kuveyttürk Yeşili)
st.markdown("""
    <style>
    .main { background-color: #f5f5f5; }
    .stButton>button { background-color: #006736; color: white; width: 100%; }
    .stTitle { color: #006736; font-family: 'Arial'; }
    </style>
    """, unsafe_allow_stdio=True)

st.title("🏦 Dinamik Ekip Portföy Yönetimi")

# Veri Saklama Mantığı (Geçici hafıza - Bulutta kalıcı olması için Google Sheets bağlanabilir)
if 'is_listesi' not in st.session_state:
    st.session_state.is_listesi = pd.DataFrame(columns=["Firma", "Kategori", "Aciliyet", "Durum", "Zaman"])

# Yan Panel - Yeni İş Girişi
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
            st.success("İşlem kaydedildi!")
        else:
            st.error("Firma adı boş bırakılamaz!")

# Ana Panel - Liste Görüntüleme
col1, col2 = st.columns([3, 1])

with col1:
    st.subheader("Aktif İş Listesi")
    if not st.session_state.is_listesi.empty:
        # Renklendirme ve Tablo
        df_goster = st.session_state.is_listesi.copy()
        st.dataframe(df_goster, use_container_width=True)
    else:
        st.info("Şu an bekleyen bir işlem yok. Keyifli kahveler! ☕")

with col2:
    st.subheader("İşlem Yönetimi")
    if not st.session_state.is_listesi.empty:
        secilen_index = st.number_input("Güncellenecek Sıra No", min_value=0, max_value=len(st.session_state.is_listesi)-1, step=1)
        if st.button("TAMAMLANDI Olarak İşaretle"):
            st.session_state.is_listesi.at[secilen_index, "Durum"] = "✅ TAMAMLANDI"
            st.rerun()
        
        if st.button("Kaydı Sil"):
            st.session_state.is_listesi = st.session_state.is_listesi.drop(secilen_index).reset_index(drop=True)
            st.rerun()

st.divider()
st.caption("Kuveyttürk Dinamik Ekip Modeli v3.0 - Bulut Versiyon")