import streamlit as st
import pandas as pd
from datetime import datetime

# 1. SAYFA AYARLARI
st.set_page_config(page_title="Kuveyttürk Dinamik Ekip", layout="wide", page_icon="🏦")

# 2. KURUMSAL TASARIM
st.markdown("""
    <style>
    .stApp { background-color: #f8f9fa; }
    .stButton>button { background-color: #006736; color: white; border-radius: 10px; height: 3.5em; width: 100%; font-weight: bold; }
    h1 { color: #006736; font-family: 'Arial'; }
    .stDataFrame { background-color: white; border-radius: 10px; box-shadow: 0 2px 4px rgba(0,0,0,0.1); }
    </style>
    """, unsafe_allow_html=True)

st.title("🏦 İkitelli Ticari - Dinamik Ekip Paneli")

# 3. SENİN ÇALIŞAN CSV LİNKİN
CSV_URL = "https://docs.google.com/spreadsheets/d/e/2PACX-1vRpvbLTEaAIgtMaId8eNq6bTDA6rxwti_582SZEHAJu6cD_AzoBb8fZCOYfl_zV3DehPKjWOjmvyV_8/pub?output=csv"

# 4. VERİ ÇEKME FONKSİYONU
@st.cache_data(ttl=2) # 2 saniyede bir veriyi tazeler
def verileri_yukle():
    try:
        # Cache'i atlatmak için her seferinde zaman damgası ekliyoruz
        taze_url = f"{CSV_URL}&cache_bust={datetime.now().timestamp()}"
        df = pd.read_csv(taze_url)
        return df
    except Exception as e:
        return None

is_listesi = verileri_yukle()

# 5. SOL PANEL
with st.sidebar:
    st.header("📌 İşlem Yönetimi")
    st.write("Yeni bir iş kaydetmek için aşağıdaki butonu kullanın:")
    
    # Form linkin
    st.link_button("🚀 YENİ İŞ KAYDI GİR", "https://docs.google.com/forms/d/1r9odjXloW2hhNqlHm4uo-4dV-aicS4l5s_E9J108s6s/viewform")
    
    st.divider()
    st.info("Kayıtlar doğrudan Google Sheets'e işlenir ve panelde anlık görünür.")

# 6. ANA PANEL - LİSTE GÖRÜNTÜLEME
st.subheader("📋 Aktif İş Takip Listesi")

if is_listesi is not None:
    if not is_listesi.empty:
        # Boş satırları temizle ve en yeni kaydı en üste al
        is_listesi = is_listesi.dropna(how='all')
        if 'Zaman damgası' in is_listesi.columns:
            is_listesi = is_listesi.sort_values(by='Zaman damgası', ascending=False)
        
        st.dataframe(is_listesi, use_container_width=True, hide_index=True)
    else:
        st.info("Henüz bekleyen bir işlem yok. Form üzerinden ilk kaydı girebilirsiniz.")
else:
    st.error("Veri çekme sırasında bir sorun oluştu. Lütfen sayfayı yenileyin.")

# 7. ALT BİLGİ
st.divider()
st.caption(f"Veri Kaynağı: Google Sheets | Son Senkronizasyon: {datetime.now().strftime('%H:%M:%S')}")
