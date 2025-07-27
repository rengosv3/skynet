import streamlit as st
import pandas as pd
from collections import Counter

def analyse_number(draws, number):
    if not number.isdigit() or len(number) != 4:
        return None

    digits = list(number)
    last_hit = None
    for i, draw in enumerate(reversed(draws)):
        if number in draw['numbers']:
            last_hit = i
            break

    # Kira frekuensi setiap digit mengikut posisi
    freq_pos = [Counter() for _ in range(4)]
    for draw in draws:
        for num in draw['numbers']:
            for i, d in enumerate(num):
                freq_pos[i][d] += 1

    details = []
    score = 0
    for i, d in enumerate(digits):
        pos_freq = freq_pos[i]
        rank = sorted(pos_freq.items(), key=lambda x: -x[1])
        rank_dict = {digit: idx + 1 for idx, (digit, _) in enumerate(rank)}
        r = rank_dict.get(d, None)
        fq = pos_freq.get(d, 0)

        if r is not None:
            if r <= 3:
                status = "🔥 Hot"
                score += 2
            elif r <= 6:
                status = "🙂 Neutral"
                score += 1
            else:
                status = "❄️ Cool"
        else:
            status = "❄️ Cool"

        details.append({
            "Posisi": i+1,
            "Digit": d,
            "Kekerapan": fq,
            "Ranking": r if r else "-",
            "Status": status
        })

    # Tambah bonus jika pernah kena
    if last_hit is not None and last_hit <= 15:
        score += 2

    recommendation = "✅ Main" if score >= 5 else "❌ Jangan Main"

    return {
        "score": score,
        "recommendation": recommendation,
        "last_hit": last_hit,
        "details": details
    }

def show_analysis_tab(draws):
    st.header("🧠 Analisis Nombor 4D")

    max_n = len(draws)
    recent_n = st.slider("Bilangan draw terkini untuk analisis", 10, max_n, 30)
    recent_draws = draws[-recent_n:]

    number = st.text_input("Masukkan nombor 4D untuk analisis (cth: 1234)", max_chars=4)

    if number:
        result = analyse_number(recent_draws, number)
        if not result:
            st.error("❌ Sila masukkan nombor 4-digit yang sah.")
            return

        st.subheader(f"Hasil Analisis untuk: `{number}`")
        st.metric("Skor Pemarkahan", result["score"])
        st.metric("Syor", result["recommendation"])
        st.metric("Draw terakhir muncul", f"{result['last_hit']} draw lalu" if result["last_hit"] is not None else "❌ Tidak Pernah Kena")

        st.subheader("Butiran Per Posisi")
        st.table(pd.DataFrame(result["details"]))