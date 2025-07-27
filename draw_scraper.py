import requests
from bs4 import BeautifulSoup

def get_10_numbers(date_str: str):
    url = f"https://gdlotto.net/results/ajax/_result.aspx?past=1&d={date_str}"
    try:
        resp = requests.get(url, headers={"User-Agent": "Mozilla/5.0"}, timeout=10)
        print(f"Status {resp.status_code} - {date_str}")
        soup = BeautifulSoup(resp.text, "html.parser")
        spans = soup.find_all("span")
        numbers = []
        seen = set()
        for tag in spans:
            text = tag.text.strip()
            if text.isdigit() and len(text) == 4 and text not in seen:
                numbers.append(text)
                seen.add(text)
        print(f"📅 {date_str} → Jumpa {len(numbers)} nombor: {numbers}")
        return numbers  # ← ini penting untuk sistem lain guna
    except Exception as e:
        print(f"❌ Error {date_str}: {e}")
        return None

# Uji satu tarikh
get_10_numbers("2025-07-22")