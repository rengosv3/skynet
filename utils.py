import os
import json
from datetime import datetime, timedelta

def save_draws(draws, path="data/draws.txt"):
    """
    Simpan semua draw ke fail teks dalam format JSONL.
    """
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w") as f:
        for d in draws:
            f.write(json.dumps(d) + "\n")

def load_draws(path="data/draws.txt") -> list[dict]:
    """
    Baca semua draw daripada fail JSONL dan pulangkan sebagai list of dict.
    """
    if not os.path.exists(path):
        return []
    with open(path) as f:
        return [json.loads(line.strip()) for line in f if line.strip()]

def load_last_draw(path="data/last_draw.txt") -> list[str]:
    """
    Baca fail last_draw.txt dan pulangkan senarai 10 nombor draw terakhir.
    """
    if not os.path.exists(path):
        return []
    with open(path) as f:
        return [line.strip() for line in f if line.strip()]

def get_draw_countdown_from_last_8pm():
    """
    Kira masa berbaki ke draw berikutnya (setiap 8 malam GMT+8).
    """
    now = datetime.now()
    draw_time = now.replace(hour=20, minute=0, second=0, microsecond=0)
    if now > draw_time:
        draw_time += timedelta(days=1)
    return draw_time - now