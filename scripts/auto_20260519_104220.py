import requests
from bs4 import BeautifulSoup
import pandas as pd

url = "https://www.nseindia.com/market-data/top-gainers-equities"
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
    "Accept": "*/*",
    "Referer": "https://www.nseindia.com",
}

session = requests.Session()
session.get("https://www.nseindia.com", headers=headers, timeout=10)
res = session.get(url, headers=headers, timeout=10)
soup = BeautifulSoup(res.text, 'lxml')
table = soup.find('table', {'id': 'topgainer-Table'})

data = []
rows = table.find_all('tr')[1:] if table else []
for row in rows:
    cols = row.find_all('td')
    if len(cols) >= 5:
        data.append([
            cols[0].get_text(strip=True),
            cols[1].get_text(strip=True),
            cols[2].get_text(strip=True),
            cols[3].get_text(strip=True),
            cols[4].get_text(strip=True)
        ])

df = pd.DataFrame(data, columns=['Symbol', 'LTP', 'Chg', 'Chg%', 'Volume'])
print(df.values.tolist())