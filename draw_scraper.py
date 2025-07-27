import requests
from bs4 import BeautifulSoup

def get_10_numbers(date_str: str):
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
                numbers.append(text)
                seen.add(text)
        if len(numbers) == 10:
            print(f"✅ {date_str}: Lengkap 10 nombor.")
            return numbers
        else:
            print(f"❌ {date_str}: Jumpa {len(numbers)} nombor.")
            return None
    except Exception as e:
        print(f"❌ Ralat {date_str}: {e}")
        return None