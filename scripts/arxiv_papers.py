import os, requests
from bs4 import BeautifulSoup

run_id = os.environ.get('RUN_ID', '')
nexus_url = os.environ.get('NEXUS_URL', '')
nexus_key = os.environ.get('NEXUS_API_KEY', '')
print('nexus_url set:', bool(nexus_url))

def ask_nexus(prompt):
    try:
        print('calling nexus...')
        r = requests.post(
            nexus_url + '/ask',
            headers={'Content-Type': 'application/json', 'X-API-Key': nexus_key},
            json={'prompt': prompt, 'task': 'ask'},
            timeout=45
        )
        print('nexus status:', r.status_code)
        return r.json().get('response', '')
    except Exception as e:
        print('nexus error:', str(e))
        return ''

try:
    r = requests.get('https://arxiv.org/list/cs.AI/recent',
        headers={'User-Agent': 'Mozilla/5.0'}, timeout=30)
    print('arxiv status:', r.status_code)
    soup = BeautifulSoup(r.text, 'html.parser')
    titles = soup.select('div.list-title.mathjax')
    abstracts = soup.select('p.mathjax')
    authors_list = soup.select('div.list-authors')
    print('titles found:', len(titles))
    combined = ''
    for i, (t, a) in enumerate(zip(titles[:5], authors_list[:5])):
        title = t.text.strip().replace('Title:', '').strip()
        author = a.text.strip().replace('Authors:', '').strip()
        abstract = abstracts[i].text.strip() if i < len(abstracts) else ''
        combined += str(i+1) + '. ' + title + chr(10)
        combined += 'Authors: ' + author[:80] + chr(10)
        combined += 'Abstract: ' + abstract[:300] + chr(10) + chr(10)
    if nexus_url:
        summary = ask_nexus('You are an AI research digest. For each paper below, write 1 sentence on what it does and why it matters. Be concise.' + chr(10) + chr(10) + combined)
        print('ARXIV AI DIGEST')
        print(summary if summary else 'NO SUMMARY RETURNED')
    else:
        print('NO NEXUS URL')
        print(combined)
except Exception as e:
    print('ERROR: ' + str(e))