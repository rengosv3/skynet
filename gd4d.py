import streamlit as st
import pandas as pd

from draw_scraper import update_draws
from utils import load_draws, load_last_draw

st.set_page_config(page_title="GD4D Scraper Test", layout="wide")
st.title("🧪 GD4D Scraper & File Viewer")

# Butang update
if st.button("📥 Update Draw Terkini (30 hari terkini sahaja)"):
    msg = update_draws(n_days=30)
    st.success(msg)

# Papar info draw terakhir jika ada
draws = load_draws()
if draws:
    st.info(f"📅 Tarikh terakhir: **{draws[-1]['date']}** | 📊 Jumlah draw: **{len(draws)}**")
else:
    st.warning("❌ Tiada draw berjaya dimuatkan. Klik 'Update Draw Terkini'.")

# Tabs hanya untuk Semak Fail
tab = st.tabs(["📁 Semak Fail"])[0]

with tab:
    st.header("📂 Semak Fail Simpanan")
    files = [
        "data/draws.txt",
        "data/last_draw.txt"
    ]
    for f in files:
        st.subheader(f"📄 {f}")
        try:
            with open(f) as fp:
                content = fp.read()
                st.code(content, language='text')
        except Exception as e:
            st.error(f"❌ Gagal baca fail: {str(e)}")