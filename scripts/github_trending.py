import os
import requests
from bs4 import BeautifulSoup

run_id = os.environ.get('RUN_ID', '')

try:
    r = requests.get(
        'https://github.com/trending/python',
        headers={'User-Agent': 'Mozilla/5.0'},
        timeout=30
    )
    soup = BeautifulSoup(r.text, 'html.parser')
    repos = soup.select('article.Box-row')
    for i, repo in enumerate(repos[:10]):
        name_el = repo.select_one('h2 a')
        desc_el = repo.select_one('p')
        stars_el = repo.select_one('a.Link--muted span')
        name = name_el.text.strip() if name_el else 'N/A'
        name = ' '.join(name.split())
        desc = desc_el.text.strip() if desc_el else 'No description'
        stars = stars_el.text.strip() if stars_el else '0'
        print(str(i+1) + '. ' + name)
        print('   ' + desc[:80])
        print('   Stars: ' + stars)
        print('')
except Exception as e:
    print('ERROR: ' + str(e))
