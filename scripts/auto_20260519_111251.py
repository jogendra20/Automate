import requests
import json

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
    "Accept": "application/json",
    "Referer": "https://www.tickertape.in/"
}

res = requests.get(
    "https://api.tickertape.in/stocks/screener/filter",
    params={"sortBy": "change_percent", "sortOrder": "desc", "limit": 10},
    headers=headers,
    timeout=10
)
data = res.json()
for item in data.get("data", {}).get("stocks", []):
    print(item.get("ticker"), item.get("close"), item.get("change_percent"))