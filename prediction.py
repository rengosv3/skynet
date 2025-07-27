# prediction.py

from strategies import (
    generate_by_frequency,
    generate_by_polarity_shift,
    generate_by_hybrid,
    generate_by_break,
    generate_by_hitfq,
    generate_by_smartpattern
)

def generate_predictions(draws, strategy='frequency', recent_n=30, top_n=10):
    if strategy == 'frequency':
        return generate_by_frequency(draws, recent_n, top_n)
    elif strategy == 'polarity_shift':
        return generate_by_polarity_shift(draws, recent_n, top_n)
    elif strategy == 'hybrid':
        return generate_by_hybrid(draws, recent_n, top_n)
    elif strategy == 'break':
        return generate_by_break(draws, top_n)
    elif strategy == 'hitfq':
        return generate_by_hitfq(draws, recent_n, top_n)
    elif strategy == 'smartpattern':
        return generate_by_smartpattern(draws, top_n)
    else:
        raise ValueError(f"Strategi tidak dikenali: {strategy}")