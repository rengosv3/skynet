import requests
from bs4 import BeautifulSoup
from datetime import datetime, timedelta
from utils import save_draws

def get_10_numbers(date_str: str) -> list[str] | None:
    """
    Scrape kesemua 10 nombor dari 1st hingga Special berdasarkan tarikh YYYY-MM-DD.
    Pulangkan list of 10 nombor 4-digit atau None jika gagal.
    """
    url = f"https://gdlotto.net/results/ajax/_result.aspx?past=1&d={date_str}"
    try:
        resp = requests.get(url, headers={"User-Agent": "Mozilla/5.0"}, timeout=10)
        if resp.status_code != 200:
            print(f"❌ Status {resp.status_code} untuk {date_str}")
            return None
        soup = BeautifulSoup(resp.text, "html.parser")
        ids = ["1stPz", "2ndPz", "3rdPz", "SpPz1", "SpPz2", "SpPz3", "SpPz4", "SpPz5", "SpPz6", "SpPz7"]
        numbers = []
        for pid in ids:
            tag = soup.find("span", id=pid)
            num = tag.text.strip() if tag else ""
            if num.isdigit() and len(num) == 4:
                numbers.append(num)
        if len(numbers) == 10:
            return numbers
        print(f"❌ Gagal lengkap scrape {date_str}, dapat {len(numbers)} nombor")
    except Exception as e:
        print(f"❌ Ralat: {e}")
    return None

def generate_date_list(n_days=200):
    today = datetime.today()
    return [(today - timedelta(days=i)).strftime("%Y-%m-%d") for i in range(n_days)]

def update_draws(n_days=200):
    dates = generate_date_list(n_days)
    all_draws = []

    for d in dates:
        nums = get_10_numbers(d)
        if nums:
            all_draws.append({
                "date": d,
                "numbers": nums
            })

    if not all_draws:
        return "❌ Tiada draw berjaya diambil."

    all_draws.sort(key=lambda x: x["date"])
    save_draws(all_draws)

    # Simpan draw terakhir ke last_draw.txt
    with open("data/last_draw.txt", "w") as f:
        for num in all_draws[-1]["numbers"]:
            f.write(num + "\n")

    return f"✅ {len(all_draws)} draw berjaya dikemaskini."