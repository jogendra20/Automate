import os, requests
from bs4 import BeautifulSoup
import sys
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))
from nexus_client import NexusClient

run_id = os.environ.get('RUN_ID', '')
nexus_url = os.environ.get('NEXUS_URL', '')
nexus_key = os.environ.get('NEXUS_API_KEY', '')

def ask_nexus(prompt):
    return NexusClient.from_env().ask(prompt)

try:
    r = requests.get('https://github.com/trending/python',
        headers={'User-Agent': 'Mozilla/5.0'}, timeout=30)
    soup = BeautifulSoup(r.text, 'html.parser')
    repos = soup.select('article.Box-row')
    combined = ''
    for i, repo in enumerate(repos[:10]):
        name_el = repo.select_one('h2 a')
        desc_el = repo.select_one('p')
        stars_el = repo.select_one('a.Link--muted span')
        name = ' '.join(name_el.text.split()) if name_el else 'N/A'
        desc = desc_el.text.strip() if desc_el else 'No description'
        stars = stars_el.text.strip() if stars_el else '0'
        combined += str(i+1) + '. ' + name + chr(10)
        combined += 'Desc: ' + desc[:100] + chr(10)
        combined += 'Stars: ' + stars + chr(10) + chr(10)
    if nexus_url and nexus_key:
        summary = ask_nexus('You are a tech curator. For each trending GitHub repo below, write 1 sentence on what it does and why developers should care. Be concise.' + chr(10) + chr(10) + combined)
        print('GITHUB TRENDING DIGEST')
        print(summary)
    else:
        print(combined)
except Exception as e:
    print('ERROR: ' + str(e))
