import os
from scrapling import Fetcher

run_id = os.environ.get('RUN_ID', '')

try:
    fetcher = Fetcher(auto_match=False)
    page = fetcher.get('https://arxiv.org/list/cs.AI/recent', stealthy_headers=True)
    print(dir(page))
except Exception as e:
    print(f"ERROR: {e}")