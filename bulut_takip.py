import streamlit as st
import pandas as pd
from datetime import datetime

st.set_page_config(page_title="Kuveyttürk Dinamik Ekip", layout="wide", page_icon="🏦")

# Şık Tasarım
st.markdown("""
    <style>
    .stApp { background-color: #f8f9fa; }
    .stButton>button { background-color: #006736; color: white; border-radius: 10px; height: 3.5em; width: 100%; }
    h1 { color: #006736; }
    </style>
    """, unsafe_allow_html=True)

st.title("🏦 İkitelli Ticari - Dinamik Ekip")

# --- BURAYA DİKKAT ---
# Web'de Yayınla kısmından aldığın o CSV linkini buraya tırnak içine yapıştır:
CSV_YAYIN_LINKI = "BURAYA_KOPYALADIGIN_CSV_LINKINI_YAPISTIR"

@st.cache_data(ttl=1) # Önbelleği neredeyse sıfırlıyoruz
def veri_cek():
    try:
        # Linkin sonuna benzersiz bir sayı ekleyerek her seferinde taze veri çekiyoruz
        taze_url = f"{CSV_YAYIN_LINKI}&dummy={datetime.now().timestamp()}"
        df = pd.read_csv(taze_url)
        return df
    except Exception as e:
        return None

liste = veri_cek()

with st.sidebar:
    st.header("📌 İşlem Yönetimi")
    st.link_button("🚀 YENİ İŞ KAYDI GİR", "https://docs.google.com/forms/d/1r9odjXloW2hhNqlHm4uo-4dV-aicS4l5s_E9J108s6s/viewform")
    st.divider()
    st.info("Kayıtlar şahsi Google hesabınıza anlık işlenir.")

st.subheader("📋 Güncel İş Listesi")

if liste is not None:
    # Boş satırları temizle
    liste = liste.dropna(how='all')
    st.dataframe(liste, use_container_width=True, hide_index=True)
else:
    # Eğer hala hata alıyorsak, ekranda linki test etmen için bir uyarı verelim
    st.error("⚠️ Veri çekilemedi. Lütfen 'Web'de Yayınla' kısmından CSV seçtiğinizden emin olun.")
    st.info("Eğer CSV linkini koda doğru yapıştırdıysanız, 1-2 dakika içinde Google yayını aktif edecektir.")

st.caption(f"Son Güncelleme: {datetime.now().strftime('%H:%M:%S')}")
