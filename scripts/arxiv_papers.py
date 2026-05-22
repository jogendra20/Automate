import os
import requests
from bs4 import BeautifulSoup

run_id = os.environ.get("RUN_ID", "")

try:
    r = requests.get(
        "https://arxiv.org/list/cs.AI/recent",
        headers={"User-Agent": "Mozilla/5.0"},
        timeout=30
    )
    soup = BeautifulSoup(r.text, "html.parser")
    titles = soup.select("div.list-title.mathjax")
    authors = soup.select("div.list-authors")
    for i, (t, a) in enumerate(zip(titles, authors)):
        if i >= 10:
            break
        title = t.text.strip().replace("Title:", "").strip()
        auth = a.text.strip().replace("Authors:", "").strip()
        print(f"{i+1}. {title}")
        print(f"   {auth[:100]}")
        print()
except Exception as e:
    print(f"ERROR: {e}")
