import os
from scrapling import Fetcher

run_id = os.environ.get('RUN_ID', '')

try:
    fetcher = Fetcher(auto_match=False)
    page = fetcher.get('https://arxiv.org/list/cs.AI/recent', stealthy_headers=True)
    titles = page.css('div.list-title.mathjax')
    authors_list = page.css('div.list-authors')
    for i, (t, a) in enumerate(zip(titles, authors_list)):
        if i >= 10:
            break
        title = t.text.strip().replace('Title:', '').strip()
        authors = a.text.strip().replace('Authors:', '').strip()
        print(f"{i+1}. {title}")
        print(f"   {authors[:100]}")
        print()
except Exception as e:
    print(f"ERROR: {e}")