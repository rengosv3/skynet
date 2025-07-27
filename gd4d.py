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

# ── Tombol Update Draw ────────────────────────────────────────────────────────
st.header("⚙️ Kemaskini Draw")
n_days = st.slider("Bilangan hari untuk scrape:", 10, 60, 30)
if st.button("📥 Update Draw Terkini"):
    msg = update_draws(n_days=n_days)
    st.success(msg)
st.markdown("---")

# ── Load Draws ────────────────────────────────────────────────────────────────
draws = load_draws()
if not draws:
    st.warning("⚠️ Data draw kosong. Sila kemaskini dahulu.")
    st.stop()

last_draw = load_last_draw()

# ── Info Header ───────────────────────────────────────────────────────────────
st.info(f"📅 Tarikh terakhir: **{draws[-1]['date']}** | 📊 Jumlah draw: **{len(draws)}**")

# ── Tabs ─────────────────────────────────────────────────────────────────────
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
    st.header("🔮 Ramalan 4D")
    strategies = ['frequency', 'polarity_shift', 'hybrid', 'break', 'hitfq', 'smartpattern']
    strat = st.selectbox("Pilih Strategi:", strategies)
    recent_n = st.slider("Bilangan draw terkini untuk base:", 10, len(draws), 30)

    try:
        preds = generate_predictions(draws, method=strat, recent_n=recent_n, top_n=13)
        st.success("🔢 13 Nombor Ramalan:")
        st.code('\n'.join(preds), language='text')
    except Exception as e:
        st.error(f"❌ {e}")

# Tab 3: Backtest
with tabs[2]:
    st.header("🔁 Backtest Base")
    strategies = ['frequency', 'polarity_shift', 'hybrid', 'break', 'hitfq', 'smartpattern']
    strat_bt = st.selectbox("Strategi:", strategies, key="bt_strat")
    recent_bt = st.slider("Draw untuk base:", 10, len(draws), 30, key="bt_n")
    rounds = st.slider("Bilangan backtest:", 5, 50, 10, key="bt_rounds")

    if st.button("🚀 Jalankan Backtest"):
        df_bt, matched = run_backtest(
            draws,
            strategy=strat_bt,
            recent_n=recent_bt,
            rounds=rounds
        )
        st.success(f"🎯 Full match (≥1 hit): {matched} dari {rounds}")
        st.dataframe(df_bt, use_container_width=True)

# Tab 4: Digit Rank
with tabs[3]:
    show_digit_rank_tab(draws)

# Tab 5: Senarai Draw
with tabs[4]:
    st.header("📋 Senarai Draw")
    show_n = st.slider("Tunjuk berapa draw terkini:", 10, len(draws), 30, key="show_draws_n")
    df_all = pd.DataFrame(draws[-show_n:])
    df_all['numbers'] = df_all['numbers'].apply(lambda x: ', '.join(x))
    st.dataframe(df_all, use_container_width=True)

# Tab 6: Analisis
with tabs[5]:
    show_analisis_tab(draws)

# Tab 7: Semak Fail
with tabs[6]:
    st.header("📁 Semak Fail Simpanan")
    files = [
        "data/last_draw.txt",
        "data/draws.txt",
        "data/digit_rank_p1.txt",
        "data/digit_rank_p2.txt",
        "data/digit_rank_p3.txt",
        "data/digit_rank_p4.txt"
    ]
    for f in files:
        st.subheader(f"📄 {f}")
        try:
            with open(f) as fp:
                st.code(fp.read(), language='text')
        except Exception as e:
            st.error(f"❌ Gagal baca {f}: {e}")