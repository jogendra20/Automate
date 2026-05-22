import os
from bs4 import BeautifulSoup
from scrapling import Fetcher

try:
    run_id = os.getenv('RUN_ID', '')
    fetcher = Fetcher(auto_match=False)
    page = fetcher.get('https://news.ycombinator.com', stealthy_headers=True)
    soup = BeautifulSoup(page.html_content, 'html.parser')
    items = soup.select('tr.athing')
    result = []

    for item in items:
        title = item.select_one('a.storylink')
        score_span = item.find_next_sibling('tr').select_one('span.score')
        if title and score_span:
            title_text = title.text.strip()
            points = score_span.text.strip()
            result.append((title_text, points))
            if len(result) >= 10:
                break

    for i, (title, points) in enumerate(result, 1):
        print(f"{i}. {title} - {points}")
except Exception as e:
    print(f"ERROR: {e}")