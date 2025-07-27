import streamlit as st
import pandas as pd
from collections import Counter

def compute_digit_rank(draws):
    counters = [Counter() for _ in range(4)]
    for d in draws:
        for num in d['numbers']:
            for i, digit in enumerate(num):
                counters[i][digit] += 1

    ranks = []
    for pos, counter in enumerate(counters):
        total = sum(counter.values())
        rank = sorted(counter.items(), key=lambda x: -x[1])
        for r, (digit, freq) in enumerate(rank, 1):
            pct = freq / total * 100
            status = "🔥 HOT" if r <= 3 else "❄️ COOL" if r >= 8 else "😐 NEUTRAL"
            ranks.append({
                "Posisi": pos + 1,
                "Digit": digit,
                "Kekerapan": freq,
                "Peratus": f"{pct:.1f}%",
                "Status": status,
                "Rank": r
            })
    return pd.DataFrame(ranks)

def compute_hit_frequency(draws):
    all_numbers = []
    for d in draws:
        all_numbers.extend(d["numbers"])
    freq = Counter(all_numbers)
    df = pd.DataFrame(freq.items(), columns=["Nombor", "Kekerapan"])
    df = df.sort_values(by="Kekerapan", ascending=False).reset_index(drop=True)
    return df

def compute_last_hit(draws):
    last_seen = {}
    for i, d in enumerate(reversed(draws)):
        for num in d["numbers"]:
            if num not in last_seen:
                last_seen[num] = i
    df = pd.DataFrame([
        {"Nombor": k, "Last Hit (draw lalu)": v}
        for k, v in last_seen.items()
    ])
    return df.sort_values(by="Last Hit (draw lalu)")

def show_digit_rank_tab(draws):
    st.header("📊 Analisis Digit Rank")

    df_rank = compute_digit_rank(draws)
    for pos in range(1, 5):
        st.subheader(f"Posisi {pos}")
        st.dataframe(df_rank[df_rank["Posisi"] == pos].reset_index(drop=True), use_container_width=True)

    st.header("📈 Hit Frequency")
    df_freq = compute_hit_frequency(draws)
    st.dataframe(df_freq.head(50), use_container_width=True)
    st.bar_chart(df_freq.set_index("Nombor").head(20))

    st.header("📍 Last Hit")
    df_last = compute_last_hit(draws)
    st.dataframe(df_last.head(50), use_container_width=True)