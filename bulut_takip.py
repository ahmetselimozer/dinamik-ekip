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

# 3. DOĞRUDAN CSV YAYIN LİNKİ 
# Senin gönderdiğin pubhtml linkini, uygulamanın okuyabileceği CSV formatına çevirdim:
YAYINLANAN_CSV_LINKI = "https://docs.google.com/spreadsheets/d/e/2PACX-1vRpvbLTEaAIgtMaId8eNq6bTDA6rxwti_582SZEHAJu6cD_AzoBb8fZCOYfl_zV3DehPKjWOjmvyV_8/pub?output=csv"

# 4. VERİ ÇEKME FONKSİYONU
@st.cache_data(ttl=5) # Her 5 saniyede bir yeni veri var mı diye kontrol eder
def verileri_yukle():
    try:
        # Linkin sonuna cache_bust ekleyerek Google'ın eski veriyi önbellekten getirmesini önlüyoruz
        taze_link = f"{YAYINLANAN_CSV_LINKI}&timestamp={datetime.now().timestamp()}"
        df = pd.read_csv(taze_link)
        return df
    except Exception as e:
        return pd.DataFrame()

is_listesi = verileri_yukle()

# 5. SOL PANEL - YENİ KAYIT
with st.sidebar:
    st.header("📌 İşlem Yönetimi")
    st.write("Yeni bir iş girmek için aşağıdaki butonu kullanın. Formu gönderdikten sonra bu sayfa otomatik güncellenir.")
    
    # Senin Google Form linkin
    st.link_button("🚀 YENİ İŞ KAYDI GİR", "https://docs.google.com/forms/d/1r9odjXloW2hhNqlHm4uo-4dV-aicS4l5s_E9J108s6s/viewform")
    
    st.divider()
    st.info("Kayıtlar Google Sheets üzerinde güvenle saklanır.")

# 6. ANA PANEL - TABLO GÖRÜNÜMÜ
st.subheader("📋 Aktif İş Takip Listesi")

if not is_listesi.empty:
    # Boş satırları ve sütunları temizle
    is_listesi = is_listesi.dropna(how='all', axis=0).dropna(how='all', axis=1)
    
    # En yeni kaydı en üstte göster (Zaman damgasına göre)
    if 'Zaman damgası' in is_listesi.columns:
        is_listesi = is_listesi.sort_values(by='Zaman damgası', ascending=False)
        
    st.dataframe(is_listesi, use_container_width=True, hide_index=True)
else:
    st.info("Henüz bir veri bulunamadı. Lütfen form üzerinden ilk kaydı girin.")

# 7. ALT BİLGİ
st.caption(f"Son Senkronizasyon: {datetime.now().strftime('%H:%M:%S')}")
