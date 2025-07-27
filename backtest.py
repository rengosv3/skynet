import pandas as pd
from prediction import generate_predictions

def run_backtest(draws, strategy='frequency', recent_n=30, rounds=10):
    """
    Jalankan backtest pada sejumlah draw terkebelakang.
    
    Args:
        draws: Senarai semua draw (list of dict)
        strategy: Nama strategi ('frequency', 'hotcold', 'smartpattern')
        recent_n: Bilangan draw terkini untuk kiraan strategi
        rounds: Bilangan draw lampau untuk diuji
    
    Returns:
        DataFrame hasil backtest, bilangan matched full 4D
    """
    results = []
    matched_count = 0
    
    for i in range(rounds):
        end_idx = -i - 1
        start_idx = end_idx - recent_n
        if abs(start_idx) > len(draws):
            break
        
        subset = draws[start_idx:end_idx]
        if len(subset) < recent_n:
            continue
        
        target = draws[end_idx]['numbers']  # 10 nombor sebenar draw ke-(i+1)
        try:
            predicted = generate_predictions(subset, strategy=strategy, recent_n=recent_n, top_n=10)
        except Exception as e:
            predicted = []
        
        match = set(predicted) & set(target)
        full_match = len(match)

        results.append({
            'Draw Date': draws[end_idx]['date'],
            'Matched': full_match,
            'Target': ', '.join(target),
            'Predicted': ', '.join(predicted)
        })

        if full_match > 0:
            matched_count += 1

    df = pd.DataFrame(results)
    return df, matched_count