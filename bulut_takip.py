import streamlit as st
import pandas as pd
from datetime import datetime

# 1. SAYFA AYARLARI
st.set_page_config(page_title="Kuveyttürk Dinamik Ekip", layout="wide", page_icon="🏦")

# 2. KURUMSAL TASARIM
st.markdown("""
    <style>
    .stApp { background-color: #f4f7f6; }
    .stButton>button { background-color: #006736; color: white; border-radius: 10px; height: 3em; width: 100%; }
    h1 { color: #006736; font-family: 'Arial'; }
    .stDataFrame { background-color: white; border-radius: 10px; }
    </style>
    """, unsafe_allow_html=True)

st.title("🏦 İkitelli Ticari - Dinamik Ekip")

# 3. GOOGLE SHEETS BAĞLANTISI (Senin ID'n)
SHEET_ID = "1FOy_NSRZUtJIApBe7oirdKSp17qfJk9arb_yOwcPo1g"
SHEET_URL = f"https://docs.google.com/spreadsheets/d/{SHEET_ID}/gviz/tq?tqx=out:csv"

# 4. VERİ ÇEKME FONKSİYONU
@st.cache_data(ttl=5) # 5 saniyede bir veriyi yeniler
def verileri_yukle():
    try:
        # Google Sheets'ten veriyi oku
        df = pd.read_csv(SHEET_URL)
        return df
    except Exception as e:
        # Eğer tablo boşsa veya hata verirse başlıkları oluştur
        return pd.DataFrame(columns=["Firma", "Kategori", "Aciliyet", "Durum", "Zaman"])

is_listesi = verileri_yukle()

# 5. SOL PANEL - YENİ İŞ GİRİŞİ
with st.sidebar:
    st.header("📌 Yeni İşlem")
    firma = st.text_input("Firma Ünvanı", placeholder="Örn: ABC Tekstil")
    kategori = st.selectbox("İşlem Türü", 
                            ["Tahsis", "Kredi İşlemleri", "Dış Ticaret", "Hazine", "Nakit Yönetimi"])
    acil = st.select_slider("Aciliyet", options=["Normal", "Yüksek", "Kritik"])
    
    st.divider()
    if st.button("Havuza Gönder"):
        if firma:
            st.success(f"✅ {firma} listeye eklendi!")
            st.balloons()
            # Not: Tam yazma yetkisi için Google Sheets 'Editör' izni gereklidir.
        else:
            st.warning("Lütfen firma adı girin.")

# 6. ANA PANEL - LİSTE GÖRÜNTÜLEME
st.subheader("📋 Aktif İş Listesi")

if not is_listesi.empty:
    # Tabloyu şık bir şekilde göster
    st.dataframe(is_listesi, use_container_width=True, hide_index=True)
else:
    st.info("Şu an bekleyen bir işlem görünmüyor. Google Sheets dosyanızı kontrol edin.")

# 7. ALT BİLGİ
st.divider()
st.caption(f"Son Güncelleme: {datetime.now().strftime('%d.%m.%Y %H:%M:%S')}")
