import streamlit as st
import pandas as pd
from collections import Counter
from utils import load_last_draw

def show_insight_tab(draws):
    st.header("🔍 Insight Nombor Draw Terkini")

    last_draw = load_last_draw()
    if not last_draw:
        st.warning("⚠️ last_draw.txt tidak dijumpai atau kosong.")
        return

    st.subheader("📌 10 Nombor Terkini")
    st.code('\n'.join(last_draw), language='text')

    # Gabungkan semua digit dari 10 nombor
    digits_all = ''.join(last_draw)
    digit_count = Counter(digits_all)

    st.subheader("📊 Frekuensi Digit")
    df_freq = (
        pd.DataFrame(sorted(digit_count.items()), columns=['Digit', 'Kekerapan'])
        .sort_values(by='Kekerapan', ascending=False)
        .reset_index(drop=True)
    )
    st.dataframe(df_freq, use_container_width=True)

    st.subheader("🔥 Digit Paling Kerap")
    st.code(', '.join(df_freq.head(5)['Digit'].tolist()))

    # Kira mengikut posisi (1 hingga 4)
    st.subheader("📌 Frekuensi Mengikut Posisi")
    pos_counters = [Counter() for _ in range(4)]
    for num in last_draw:
        for i, d in enumerate(num):
            pos_counters[i][d] += 1

    for i, pc in enumerate(pos_counters, 1):
        st.markdown(f"**Posisi {i}:**")
        df_pos = (
            pd.DataFrame(sorted(pc.items()), columns=['Digit', 'Kekerapan'])
            .sort_values(by='Kekerapan', ascending=False)
            .reset_index(drop=True)
        )
        st.dataframe(df_pos, use_container_width=True)