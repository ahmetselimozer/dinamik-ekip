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

# 3. GOOGLE SHEETS BAĞLANTISI (Form Yanıtlarının Gittiği Dosya)
# Not: Formu bağladığın Sheets dosyasının ID'si buysa devam et, değiştiyse ID'yi güncelle.
SHEET_ID = "1FOy_NSRZUtJIApBe7oirdKSp17qfJk9arb_yOwcPo1g"
SHEET_URL = f"https://docs.google.com/spreadsheets/d/{SHEET_ID}/gviz/tq?tqx=out:csv"

# 4. VERİ ÇEKME
@st.cache_data(ttl=5) # 5 saniyede bir tabloyu tazeler
def verileri_yukle():
    try:
        df = pd.read_csv(SHEET_URL)
        # Sütun isimlerini formun oluşturduğu yapıya göre güzelleştirebilirsin
        return df
    except:
        return pd.DataFrame()

is_listesi = verileri_yukle()

# 5. SOL PANEL - VERİ GİRİŞİ YÖNLENDİRMESİ
with st.sidebar:
    st.header("📌 İşlem Yönetimi")
    st.write("Yeni bir iş kaydetmek için aşağıdaki butonu kullanın. Formu doldurduğunuzda liste otomatik güncellenecektir.")
    
    # Senin Form Linkin (Düzenleme değil, gönderme linki)
    form_link = "https://docs.google.com/forms/d/e/1FAIpQLSe-Xo50-x3Eit4x_2G6-HhG5W5s_E9J108s6s/viewform" # ÖRNEK: Buraya formun 'GÖNDER' kısmındaki linki yapıştırabilirsin
    
    st.link_button("🚀 YENİ İŞ KAYDI GİR", "https://docs.google.com/forms/d/1r9odjXloW2hhNqlHm4uo-4dV-aicS4l5s_E9J108s6s/viewform")
    
    st.divider()
    st.info("Kayıtlar doğrudan Google Sheets'e işlenir ve tüm ekip tarafından eş zamanlı görülür.")

# 6. ANA PANEL - LİSTE GÖRÜNTÜLEME
st.subheader("📋 Aktif İş Takip Listesi")

if not is_listesi.empty:
    # Formun otomatik eklediği 'Zaman Damgası' sütununa göre en yeni işi en üstte göster
    if 'Zaman damgası' in is_listesi.columns:
        is_listesi = is_listesi.sort_values(by='Zaman damgası', ascending=False)
    
    st.dataframe(is_listesi, use_container_width=True, hide_index=True)
else:
    st.info("Henüz bekleyen bir işlem yok veya tablo bağlantısı kuruluyor...")

# 7. ALT BİLGİ
st.divider()
st.caption(f"Veri Kaynağı: Google Sheets | Son Senkronizasyon: {datetime.now().strftime('%H:%M:%S')}")
