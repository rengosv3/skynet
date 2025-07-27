# draw_scraper.py

import requests
from bs4 import BeautifulSoup

def get_13_numbers(date_str: str):
    url = f"https://gdlotto.net/results/ajax/_result.aspx?past=1&d={date_str}"
    try:
        resp = requests.get(url, headers={"User-Agent": "Mozilla/5.0"}, timeout=10)
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

        if len(numbers) == 13:
            print(f"✅ {date_str} → {numbers}")
            return numbers
        else:
            print(f"❌ Gagal ambil nombor untuk {date_str} (jumpa {len(numbers)})")
            return None
    except Exception as e:
        print(f"❌ Ralat {date_str}: {e}")
        return None