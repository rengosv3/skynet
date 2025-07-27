import requests
from bs4 import BeautifulSoup

def test_scrape(date_str):
    url = f"https://gdlotto.net/results/ajax/_result.aspx?past=1&d={date_str}"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
    }
    print(f"Testing date: {date_str}")
    try:
        resp = requests.get(url, headers=headers, timeout=10)
        print("Status:", resp.status_code)
        soup = BeautifulSoup(resp.text, "html.parser")
        spans = soup.find_all("span")
        numbers = []
        seen = set()
        for tag in spans:
            txt = tag.text.strip()
            if txt.isdigit() and len(txt) == 4 and txt not in seen:
                numbers.append(txt)
                seen.add(txt)
        print("Jumpa nombor:", numbers)
    except Exception as e:
        print("❌ Ralat:", e)

test_scrape("2025-07-22")