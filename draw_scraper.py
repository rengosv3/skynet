import requests
from bs4 import BeautifulSoup
from datetime import datetime, timedelta
from utils import save_draws

def get_13_numbers(date_str: str) -> list[str] | None:
    """
    Scrape semua nombor 4-digit unik (maksimum 13) untuk 1 draw.
    """
    url = f"https://gdlotto.net/results/ajax/_result.aspx?past=1&d={date_str}"
    try:
        resp = requests.get(url, headers={"User-Agent": "Mozilla/5.0"}, timeout=10)
        if resp.status_code != 200:
            print(f"❌ Status {resp.status_code} untuk {date_str}")
            return None

        soup = BeautifulSoup(resp.text, "html.parser")
        spans = soup.find_all("span")
        numbers = []
        seen = set()

        for tag in spans:
            text = tag.text.strip()
            if text.isdigit() and len(text) == 4 and text not in seen:
                seen.add(text)
                numbers.append(text)
            if len(numbers) == 13:
                break

        if 10 <= len(numbers) <= 13:
            print(f"✅ {date_str} → Dapat: {numbers}")
            return numbers
        else:
            print(f"❌ {date_str} → Hanya jumpa {len(numbers)} nombor")
            return None

    except Exception as e:
        print(f"❌ Ralat {date_str}: {e}")
        return None

def generate_date_list(n_days=30):
    today = datetime.today()
    dates = []
    for i in range(n_days):
        d = today - timedelta(days=i)
        if d.weekday() in [0, 2, 5, 6]:  # Isnin, Rabu, Sabtu, Ahad
            dates.append(d.strftime("%Y-%m-%d"))
    return dates

def update_draws(n_days=30):
    dates = generate_date_list(n_days)
    all_draws = []

    print(f"\n📅 Memulakan scrape untuk {len(dates)} hari...\n")

    for d in dates:
        nums = get_13_numbers(d)
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