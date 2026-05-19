import requests
import pandas as pd

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
    "Accept": "*/*",
    "Referer": "https://www.tickertape.in"
}

res = requests.get(
    "https://api.tickertape.in/stocks/screener/filter",
    params={"sortBy": "change_percent", "sortOrder": "desc", "limit": 10},
    headers=headers,
    timeout=10
)
data = res.json()

gainers = []
for item in data.get("data", {}).get("stocks", []):
    gainers.append({
        "symbol": item.get("ticker"),
        "company_name": item.get("companyName"),
        "close": item.get("close"),
        "change_percent": item.get("change_percent"),
        "volume": item.get("volume")
    })

df = pd.DataFrame(gainers)
print(df)

df.to_csv("top_gainers.csv", index=False)