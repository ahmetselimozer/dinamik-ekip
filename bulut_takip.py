import streamlit as st
import pandas as pd

st.set_page_config(page_title="İkitelli Ticari Dinamik Ekip", layout="wide")

st.title("🏦 Dinamik Ekip Paneli")

# Senin az önce attığın ve çalışan o meşhur link:
url = "https://docs.google.com/spreadsheets/d/e/2PACX-1vRpvbLTEaAIgtMaId8eNq6bTDA6rxwti_582SZEHAJu6cD_AzoBb8fZCOYfl_zV3DehPKjWOjmvyV_8/pub?output=csv"

try:
    # Veriyi oku
    df = pd.read_csv(url)
    st.subheader("📋 Aktif İş Listesi")
    st.dataframe(df, use_container_width=True, hide_index=True)
except Exception as e:
    st.error(f"Google bağlantı hatası: {e}")
    st.info("Eğer bu hatayı görüyorsanız, lütfen sağ üstten 'Clear Cache' yapın.")

with st.sidebar:
    st.link_button("🚀 YENİ İŞ KAYDI GİR", "https://docs.google.com/forms/d/1r9odjXloW2hhNqlHm4uo-4dV-aicS4l5s_E9J108s6s/viewform")
