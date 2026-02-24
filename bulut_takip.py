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

# 3. SENİN GÖNDERDİĞİN DOĞRUDAN FORM YANITLARI LİNKİ
# Bu link gid=1341056098 parametresiyle tam olarak formun yazdığı sayfayı okur.
CSV_URL = "https://docs.google.com/spreadsheets/d/e/2PACX-1vRpvbLTEaAIgtMaId8eNq6bTDA6rxwti_582SZEHAJu6cD_AzoBb8fZCOYfl_zV3DehPKjWOjmvyV_8/pub?gid=1341056098&single=true&output=csv"

# 4. VERİ ÇEKME FONKSİYONU
@st.cache_data(ttl=2) # 2 saniyede bir güncellenir
def verileri_yukle():
    try:
        # Cache'i atlatmak için her seferinde zaman damgası ekleyerek en taze veriyi çekiyoruz
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
        # Boş satırları temizle
        is_listesi = is_listesi.dropna(how='all')
        
        # Zaman damgası varsa en yeni işi en üste al
        if 'Zaman damgası' in is_listesi.columns:
            # Önce tarihi doğru formata çevirip sonra sıralayalım
            is_listesi['Zaman damgası'] = pd.to_datetime(is_listesi['Zaman damgası'])
            is_listesi = is_listesi.sort_values(by='Zaman damgası', ascending=False)
        
        st.dataframe(is_listesi, use_container_width=True, hide_index=True)
    else:
        st.info("Henüz bekleyen bir işlem yok. Form üzerinden ilk kaydı girdiğinizde burada görünecektir.")
else:
    st.error("Veri çekme sırasında bir sorun oluştu. Lütfen Google Sheets 'Web'de Yayınla' ayarlarını kontrol edin.")

# 7. ALT BİLGİ
st.divider()
st.caption(f"İkitelli Ticari Şubesi | Son Güncelleme: {datetime.now().strftime('%H:%M:%S')}")
