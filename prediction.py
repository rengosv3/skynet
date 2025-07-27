from strategies import (
    generate_by_frequency,
    generate_by_polarity_shift,
    generate_by_hybrid,
    generate_by_break,
    generate_by_smartpattern,
    generate_by_hitfq
)

strategy_functions = {
    "frequency": generate_by_frequency,
    "polarity_shift": generate_by_polarity_shift,
    "hybrid": generate_by_hybrid,
    "break": generate_by_break,
    "smartpattern": generate_by_smartpattern,
    "hitfq": generate_by_hitfq
}

def generate_predictions(draws: list[dict], method: str = "hybrid") -> list[str]:
    """
    Hasilkan 10 nombor ramalan berdasarkan strategi.
    """
    if method not in strategy_functions:
        raise ValueError(f"Strategi tidak dikenali: {method}")
    
    return strategy_functions[method](draws)
    
def auto_select_strategy(draws, recent_n=30):
    """
    Pilih strategi terbaik berdasarkan hit count terhadap last_draw.
    Kembalikan (best_strategy, scores_dict).
    """
    from .strategies import (
        generate_by_frequency,
        generate_by_polarity_shift,
        generate_by_hybrid,
        generate_by_break,
        generate_by_hitfq,
        generate_by_smartpattern
    )

    strategy_funcs = {
        "frequency": generate_by_frequency,
        "polarity_shift": generate_by_polarity_shift,
        "hybrid": generate_by_hybrid,
        "break": generate_by_break,
        "hitfq": generate_by_hitfq,
        "smartpattern": generate_by_smartpattern
    }

    # Simulasikan: gunakan draws[:-1] untuk ramal, banding dengan draws[-1]
    past = draws[:-1]
    actual = set(draws[-1]["numbers"])

    scores = {}
    for name, fn in strategy_funcs.items():
        try:
            preds = fn(past, recent_n=recent_n)
            # hit = berapa dari 10 preds yang ada dalam actual
            scores[name] = sum(1 for p in preds if p in actual)
        except:
            scores[name] = -1

    # cari strategi tertinggi
    best = max(scores, key=scores.get)
    return best, scores