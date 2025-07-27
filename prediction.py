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

def generate_predictions(draws: list[dict], strategy: str = "hybrid", recent_n: int = 30, top_n: int = 13) -> list[str]:
    """
    Hasilkan nombor ramalan berdasarkan strategi.
    """
    if strategy not in strategy_functions:
        raise ValueError(f"Strategi tidak dikenali: {strategy}")
    
    return strategy_functions[strategy](draws, recent_n=recent_n)[:top_n]

def auto_select_strategy(draws, recent_n=30):
    """
    Pilih strategi terbaik berdasarkan hit count terhadap last_draw.
    Kembalikan (best_strategy, scores_dict).
    """
    strategy_funcs = strategy_functions

    past = draws[:-1]
    actual = set(draws[-1]["numbers"])

    scores = {}
    for name, fn in strategy_funcs.items():
        try:
            preds = fn(past, recent_n=recent_n)[:13]
            scores[name] = sum(1 for p in preds if p in actual)
        except:
            scores[name] = -1

    best = max(scores, key=scores.get)
    return best, scores