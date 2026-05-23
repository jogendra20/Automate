import os, requests
from bs4 import BeautifulSoup

run_id = os.environ.get('RUN_ID', '')
nexus_url = os.environ.get('NEXUS_URL', '')
nexus_key = os.environ.get('NEXUS_API_KEY', '')

def ask_nexus(prompt):
    try:
        r = requests.post(
            nexus_url + '/ask',
            headers={'Content-Type': 'application/json', 'X-API-Key': nexus_key},
            json={'prompt': prompt, 'task': 'ask'},
            timeout=45
        )
        return r.json().get('response', '')
    except Exception as e:
        return 'LLM unavailable: ' + str(e)

try:
    r = requests.get('https://github.com/trending/python',
        headers={'User-Agent': 'Mozilla/5.0'}, timeout=30)
    soup = BeautifulSoup(r.text, 'html.parser')
    repos = soup.select('article.Box-row')
    combined = ''
    for i, repo in enumerate(repos[:10]):
        name_el = repo.select_one('h2 a')
        desc_el = repo.select_one('p')
        stars_el = repo.select_one('span.Counter')
        if not stars_el:
            stars_el = repo.find('a', href=lambda x: x and '/stargazers' in x)
        name = ' '.join(name_el.text.split()) if name_el else 'N/A'
        desc = desc_el.text.strip() if desc_el else 'No description'
        stars = stars_el.text.strip() if stars_el else 'N/A'
        combined += str(i+1) + '. ' + name + '
'
        combined += 'Desc: ' + desc[:100] + '
'
        combined += 'Stars: ' + stars + '

'
    if nexus_url:
        summary = ask_nexus('You are a tech curator. For each trending GitHub repo below, write 1 sentence on what it does and why developers should care. Be concise.

' + combined)
        print('GITHUB TRENDING DIGEST
')
        print(summary)
    else:
        print(combined)
except Exception as e:
    print('ERROR: ' + str(e))
