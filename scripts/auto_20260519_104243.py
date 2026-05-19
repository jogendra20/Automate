import requests
import pandas as pd

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
    "Accept": "*/*",
    "Referer": "https://www.nseindia.com",
}

session = requests.Session()
session.get("https://www.nseindia.com", headers=headers, timeout=10)

res = session.get(
    "https://www.nseindia.com/api/live-analysis-variations?index=gainers",
    headers=headers,
    timeout=10
)

data = res.json()
df = pd.DataFrame(data.get("data", []))

if not df.empty:
    df["pChange"] = pd.to_numeric(df["pChange"], errors="coerce")
    print(df[["symbol", "lastPrice", "pChange", "totalTradedVolume"]].to_string(index=False))