import streamlit as st
import pandas as pd

from utils import (
    get_draw_countdown_from_last_8pm,
    load_draws,
    load_last_draw
)
from draw_scraper import update_draws
from prediction import generate_predictions
from backtest import run_backtest
from digit_rank import show_digit_rank_tab
from insight import show_insight_tab
from analisis import show_analisis_tab

st.set_page_config(page_title="GD4D Predictor", layout="wide")
st.title("🔮 GD4D Predictor")
st.markdown(f"⏳ Next draw in: `{str(get_draw_countdown_from_last_8pm()).split('.')[0]}`")

# Update Draws
col1, col2 = st.columns(2)
with col1:
    if st.button("📥 Update Draw Terkini"):
        msg = update_draws()
        st.success(msg)
with col2:
    st.markdown("""
    <a href="https://batman11.net/RegisterByReferral.aspx?MemberCode=BB1845" target="_blank">
      <button style="width:100%;padding:0.6em;font-size:16px;background:#4CAF50;color:white;border:none;border-radius:5px;">
        📝 Register Sini Batman 11 dan dapatkan BONUS!!!
      </button>
    </a>
    """, unsafe_allow_html=True)

# Load Draws
draws = load_draws()
if not draws:
    st.warning("⚠️ Sila klik 'Update Draw Terkini' untuk mula.")
    st.stop()

st.info(f"📅 Tarikh terakhir: **{draws[-1]['date']}** | 📊 Jumlah draw: **{len(draws)}**")

tabs = st.tabs([
    "Insight",
    "Ramalan",
    "Backtest",
    "Digit Rank",
    "Senarai Draw",
    "Analisis",
    "Semak Fail"
])

# Tab 1: Insight
with tabs[0]:
    show_insight_tab(draws)

# Tab 2: Ramalan
with tabs[1]:
    st.header("🔮 Ramalan Nombor 4D")
    strat = st.selectbox("Strategi:", ['frequency', 'hotcold', 'smartpattern'])
    recent_n = st.slider("Bilangan draw terkini:", 10, len(draws), 30)
    
    try:
        preds = generate_predictions(draws, strategy=strat, recent_n=recent_n, top_n=10)
        st.success("10 Nombor Ramalan:")
        st.code('\n'.join(preds), language='text')
    except Exception as e:
        st.error(str(e))

# Tab 3: Backtest
with tabs[2]:
    st.header("🔁 Ujian Backtest")
    strat = st.selectbox("Strategi:", ['frequency', 'hotcold', 'smartpattern'], key="bt_strat")
    recent_n = st.slider("Draw terkini:", 10, len(draws), 30, key="bt_n")
    rounds = st.slider("Bilangan backtest:", 5, 50, 10, key="bt_rounds")
    
    if st.button("🚀 Jalankan Backtest"):
        df_bt, matched = run_backtest(draws, strategy=strat, recent_n=recent_n, rounds=rounds)
        st.success(f"🎯 Full match (4D): {matched} dari {rounds}")
        st.dataframe(df_bt, use_container_width=True)

# Tab 4: Digit Rank
with tabs[3]:
    show_digit_rank_tab(draws)

# Tab 5: Senarai Draw
with tabs[4]:
    st.header("📋 Senarai Draw")
    draw_df = pd.DataFrame(draws)
    st.slider("Tunjuk draw terkini sebanyak berapa?", 10, len(draw_df), 30, key="draw_slider")
    st.dataframe(draw_df, use_container_width=True)

# Tab 6: Analisis
with tabs[5]:
    show_analisis_tab(draws)

# Tab 7: Semak Fail
with tabs[6]:
    st.header("📁 Semak Fail Simpanan")
    files = [
        "data/last_draw.txt",
        "data/draws.txt",
        "data/digit_rank_p1.txt"
    ]
    for f in files:
        st.subheader(f"📄 {f}")
        try:
            with open(f) as fp:
                content = fp.read()
                st.code(content, language='text')
        except Exception as e:
            st.error(f"❌ Gagal baca fail: {str(e)}")