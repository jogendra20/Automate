import os
from scrapling import Fetcher
import pandas as pd

run_id = os.environ.get('RUN_ID', '')

fetcher = Fetcher(auto_match=False)
page = fetcher.get('https://arxiv.org/list/cs.AI/recent', stealthy_headers=True)
rows = page.css('dl > dd')
titles = []
for row in rows:
    title = row.css('meta > div.list-title').text
    if 'Title: ' in title:
        title = title.replace('Title: ', '').strip()
    titles.append(title)
    if len(titles) >= 10:
        break

print("Titles:")
for title in titles:
    print(title)

df = pd.DataFrame({'Titles': titles})
print(df.head())
df.to_csv('titles.csv', index=False)