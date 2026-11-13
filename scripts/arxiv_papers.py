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
    r = requests.get('https://arxiv.org/list/cs.AI/recent',
        headers={'User-Agent': 'Mozilla/5.0'}, timeout=30)
    soup = BeautifulSoup(r.text, 'html.parser')
    titles = soup.select('div.list-title.mathjax')
    abstracts = soup.select('p.mathjax')
    authors_list = soup.select('div.list-authors')
    combined = ''
    for i, (t, a) in enumerate(zip(titles[:5], authors_list[:5])):
        title = t.text.strip().replace('Title:', '').strip()
        author = a.text.strip().replace('Authors:', '').strip()
        abstract = abstracts[i].text.strip() if i < len(abstracts) else ''
        combined += str(i+1) + '. ' + title + chr(10)
        combined += 'Authors: ' + author[:80] + chr(10)
        combined += 'Abstract: ' + abstract[:300] + chr(10) + chr(10)
    if nexus_url and nexus_key:
        summary = ask_nexus('You are an AI research digest. For each paper below, write 1 sentence on what it does and why it matters. Be concise.' + chr(10) + chr(10) + combined)
        print('ARXIV AI DIGEST')
        print(summary if summary else combined)
    else:
        print(combined)
except Exception as e:
    print('ERROR: ' + str(e))
