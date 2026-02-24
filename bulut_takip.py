import streamlit as st
import pandas as pd
from datetime import datetime

# 1. SAYFA AYARLARI
st.set_page_config(page_title="Kuveyttürk Dinamik Ekip PRO", layout="wide", page_icon="🏦")

# 2. KURUMSAL VE DİNAMİK TASARIM
st.markdown("""
    <style>
    .stApp { background-color: #f0f2f6; }
    .stButton>button { background-color: #006736; color: white; border-radius: 12px; height: 3.5em; width: 100%; font-weight: bold; border: none; }
    .stButton>button:hover { background-color: #004d28; color: #ffd700; }
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
        # Sütun isimlerindeki boşlukları temizleyelim
        df.columns = df.columns.str.strip()
        return df
    except:
        return None

df = verileri_yukle()

# 4. SOL PANEL (SIDEBAR)
with st.sidebar:
    st.image("https://upload.wikimedia.org/wikipedia/commons/thumb/7/7b/Kuveyt_T%C3%BCrk_logo.svg/2560px-Kuveyt_T%C3%BCrk_logo.svg.png", width=200)
    st.header("📌 Menü")
    st.link_button("🚀 YENİ İŞ KAYDI GİR", "https://docs.google.com/forms/d/1r9odjXloW2hhNqlHm4uo-4dV-aicS4l5s_E9J108s6s/viewform")
    st.divider()
    
    # 3. SEÇENEK: FİLTRELEME VE ÖZET
    st.subheader("📊 Filtreleme")
    durum_filtresi = st.multiselect("Duruma Göre Filtrele", options=["Bekliyor", "Tamamlandı", "İptal"], default=["Bekliyor"])
    
# 5. ÜST ÖZET (METRİKLER)
if df is not None and not df.empty:
    col1, col2, col3 = st.columns(3)
    # Varsayılan sütun isimlerine göre (Formdaki isimlerle eşleşmeli)
    kritik_sayisi = len(df[df['Aciliyet'] == 'Kritik'])
    toplam_is = len(df)
    
    col1.metric("Toplam İşlem", toplam_is)
    col2.metric("Kritik Seviye", kritik_sayisi, delta_color="inverse")
    col3.metric("Hedeflenen", "2026 Planı")

# 6. RENKLENDİRME FONKSİYONU (2. SEÇENEK)
def satır_stili(row):
    if row['Aciliyet'] == 'Kritik':
        return ['background-color: #ffcccc'] * len(row)
    elif row['Aciliyet'] == 'Yüksek':
        return ['background-color: #fff4e5'] * len(row)
    return [''] * len(row)

# 7. ANA TABLO
st.subheader("📋 Güncel Takip Listesi")
if df is not None and not df.empty:
    # Filtreleme uygula (Eğer sütun adı 'Durum' ise)
    if 'Durum' in df.columns:
        df = df[df['Durum'].isin(durum_filtresi)]
    
    # Zaman sıralaması
    if 'Zaman damgası' in df.columns:
        df['Zaman damgası'] = pd.to_datetime(df['Zaman damgası'])
        df = df.sort_values(by='Zaman damgası', ascending=False)

    # Tabloyu stillendirilmiş olarak göster
    styled_df = df.style.apply(satır_stili, axis=1)
    st.dataframe(styled_df, use_container_width=True, hide_index=True)
else:
    st.info("Henüz görüntülenecek veri yok.")

st.divider()
st.caption(f"İkitelli Ticari Şubesi Dijital Dönüşüm Projesi | {datetime.now().year}")
