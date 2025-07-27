import itertools
import os
from collections import Counter
import pandas as pd

# === Base Generators ===

def _frequency_base(draws, recent_n=30):
    counters = [Counter() for _ in range(4)]
    recent = draws[-recent_n:]
    for d in recent:
        for num in d['numbers']:
            for i, digit in enumerate(num):
                counters[i][digit] += 1
    return [[d for d, _ in c.most_common(5)] for c in counters]

def _polarity_shift_base(draws, recent_n=30):
    recent = draws[-recent_n:]
    past = draws[-2*recent_n:-recent_n] if len(draws) >= 2*recent_n else draws[: -recent_n]
    rec_counters = [Counter() for _ in range(4)]
    past_counters = [Counter() for _ in range(4)]
    for d in recent:
        for num in d['numbers']:
            for i, digit in enumerate(num):
                rec_counters[i][digit] += 1
    for d in past:
        for num in d['numbers']:
            for i, digit in enumerate(num):
                past_counters[i][digit] += 1
    bases = []
    for pos in range(4):
        delta = {digit: rec_counters[pos][digit] - past_counters[pos][digit]
                 for digit in map(str, range(10))}
        top5 = sorted(delta, key=lambda x: -delta[x])[:5]
        bases.append(top5)
    return bases

def _hybrid_base(draws, recent_n=30):
    f = _frequency_base(draws, recent_n)
    p = _polarity_shift_base(draws, recent_n)
    combined = []
    for pos in range(4):
        cnt = Counter(f[pos] + p[pos])
        combined.append([d for d, _ in cnt.most_common(5)])
    return combined

def _break_base():
    result = []
    for i in range(1, 5):
        path = f"data/digit_rank_p{i}.txt"
        if not os.path.exists(path):
            raise FileNotFoundError(f"{path} tidak wujud")
        df = pd.read_csv(path, sep='\t')
        subset = df[(df['Rank'] >= 6) & (df['Rank'] <= 10)]
        result.append(subset['Digit'].astype(str).tolist())
    return result

def _hitfq_base(draws, recent_n=30):
    counters = [Counter() for _ in range(4)]
    recent = draws[-recent_n:]
    for d in recent:
        for num in d['numbers']:
            for i, digit in enumerate(num):
                counters[i][digit] += 1
    base = []
    for c in counters:
        ranked = sorted(c.items(), key=lambda x: (-x[1], int(x[0])))
        base.append([d for d, _ in ranked[:5]])
    return base

def _smartpattern_base(draws):
    bases = [
        _frequency_base(draws, 50),
        _polarity_shift_base(draws, 50),
        _hybrid_base(draws, 40),
        _hitfq_base(draws, 30)
    ]
    result = []
    for pos in range(4):
        cnt = Counter()
        for b in bases:
            cnt.update(b[pos])
        result.append([d for d, _ in cnt.most_common(5)])
    return result

# === Generate N full 4D predictions ===

def generate_by_frequency(draws, recent_n=30, top_n=13):
    base = _frequency_base(draws, recent_n)
    combos = [''.join(p) for p in itertools.product(*base)]
    return combos[:top_n]

def generate_by_polarity_shift(draws, recent_n=30, top_n=13):
    base = _polarity_shift_base(draws, recent_n)
    combos = [''.join(p) for p in itertools.product(*base)]
    return combos[:top_n]

def generate_by_hybrid(draws, recent_n=30, top_n=13):
    base = _hybrid_base(draws, recent_n)
    combos = [''.join(p) for p in itertools.product(*base)]
    return combos[:top_n]

def generate_by_break(draws, top_n=13):
    base = _break_base()
    combos = [''.join(p) for p in itertools.product(*base)]
    return combos[:top_n]

def generate_by_hitfq(draws, recent_n=30, top_n=13):
    base = _hitfq_base(draws, recent_n)
    combos = [''.join(p) for p in itertools.product(*base)]
    return combos[:top_n]

def generate_by_smartpattern(draws, top_n=13):
    base = _smartpattern_base(draws)
    combos = [''.join(p) for p in itertools.product(*base)]
    return combos[:top_n]