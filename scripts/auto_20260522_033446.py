from scrapling import Fetcher
import os

run_id = os.environ.get('RUN_ID', '')
fetcher = Fetcher(auto_match=False)

page = fetcher.get('https://arxiv.org/list/cs.AI/recent', stealthy_headers=True)
items = page.css('dl > dt + dd')
counter = 1

for item in items[:10]:
    title = item.css('div.meta > div.list-title')[0].text.replace('Title: ', '').strip()
    authors = [a.text.strip() for a in item.css('div.meta > div.list-authors a')]
    print(f"{counter}. {title}\n   Authors: {', '.join(authors)}")
    counter += 1