import requests

headers = {"User-Agent": "Mozilla/5.0"}
res = requests.get(
    "https://api.tickertape.in/stocks/screener/filter",
    params={"sortBy": "change_percent", "sortOrder": "desc", "limit": 10},
    headers=headers,
    timeout=10
)
data = res.json()
result = []
for item in data.get("data", {}).get("stocks", []):
    result.append([
        item.get("ticker"),
        item.get("close"),
        item.get("change_percent")
    ])
print(result)