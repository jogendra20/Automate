import os
import requests
import pandas as pd

# NSE API endpoint and cookies
nse_url = "https://www.nseindia.com/api/live-analysis-variations?index=gainers"
nse_header = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
    "Accept": "*/*",
    "Referer": "https://www.nseindia.com"
}
nse_cookie = os.getenv('NSE_COOKIE')

# Session with cookies
try:
    session = requests.Session()
    session.get("https://www.nseindia.com", cookies=nse_cookie, headers=nse_header, timeout=10)
    res = session.get(nse_url, headers=nse_header, timeout=10)
    data = res.json()
    df = pd.DataFrame([item for item in data.get("data", [])])

    # Select top gainers
    top_gainers = df.nlargest(10, "pChange")

    # Print top gainers
    print(top_gainers[["symbol", "lastPrice"]])

    # Save top gainers to csv
    top_gainers.to_csv("top_gainers.csv", index=False)

except requests.exceptions.RequestException as e:
    print(f"Error: {e}")