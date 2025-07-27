import streamlit as st
from draw_scraper import get_10_numbers  # Guna hanya fungsi ini

st.set_page_config(page_title="GD4D Uji Scrape", layout="centered")
st.title("🔎 Ujian Scrape Nombor 4D")

date_str = st.text_input("Masukkan tarikh format YYYY-MM-DD", "2025-07-22")

if st.button("Semak"):
    numbers = get_10_numbers(date_str)
    if numbers:
        st.success(f"✅ {date_str} → Dapat: {numbers}")
    else:
        st.error(f"❌ Gagal ambil nombor untuk {date_str}")