import os
import requests
from bs4 import BeautifulSoup

run_id = os.environ.get("RUN_ID", "")

try:
    r = requests.get(
        "https://news.ycombinator.com",
        headers={"User-Agent": "Mozilla/5.0"},
        timeout=30
    )
    soup = BeautifulSoup(r.text, "html.parser")
    rows = soup.select("tr.athing")
    scores = soup.select("span.score")
    for i, (row, score) in enumerate(zip(rows[:10], scores[:10])):
        title_el = row.select_one("span.titleline a")
        title = title_el.text.strip() if title_el else "N/A"
        points = score.text.strip()
        print(f"{i+1}. {title}")
        print(f"   {points}")
        print()
except Exception as e:
    print(f"ERROR: {e}")
