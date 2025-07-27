import os
import datetime
from datetime import timedelta

def get_draw_countdown_from_last_8pm():
    """Kira masa berbaki sebelum draw seterusnya (berdasarkan 8PM)."""
    now = datetime.datetime.now()
    draw_time = now.replace(hour=20, minute=0, second=0, microsecond=0)
    if now > draw_time:
        draw_time += timedelta(days=1)
    return draw_time - now

def load_draws(path="data/draws.txt"):
    """Baca semua draw dari fail. Pulangkan list of dict."""
    if not os.path.exists(path):
        return []
    with open(path) as f:
        lines = f.readlines()
    draws = []
    for line in lines:
        parts = line.strip().split(',')
        if len(parts) < 2:
            continue
        date = parts[0]
        numbers = parts[1:]
        if all(len(n) == 4 and n.isdigit() for n in numbers):
            draws.append({'date': date, 'numbers': numbers})
    return draws

def load_last_draw(path="data/last_draw.txt"):
    """Baca draw terkini (1 hari punya 10 nombor)."""
    if not os.path.exists(path):
        return []
    with open(path) as f:
        lines = f.readlines()
    return [line.strip() for line in lines if line.strip().isdigit() and len(line.strip()) == 4]