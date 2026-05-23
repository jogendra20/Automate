import os, requests, json
from bs4 import BeautifulSoup

run_id = os.environ.get('RUN_ID', '')
groq_key = os.environ.get('GROQ_API_KEY', '')

try:
    r = requests.get('https://arxiv.org/list/cs.AI/recent',
        headers={'User-Agent': 'Mozilla/5.0'}, timeout=30)
    soup = BeautifulSoup(r.text, 'html.parser')
    titles = soup.select('div.list-title.mathjax')
    abstracts = soup.select('p.mathjax')
    authors_list = soup.select('div.list-authors')
    papers = []
    for i, (t, a) in enumerate(zip(titles[:5], authors_list[:5])):
        title = t.text.strip().replace('Title:', '').strip()
        author = a.text.strip().replace('Authors:', '').strip()
        abstract = abstracts[i].text.strip() if i < len(abstracts) else ''
        papers.append({'title': title, 'authors': author[:80], 'abstract': abstract[:300]})
    combined = ''
    for i, p in enumerate(papers):
        combined += str(i+1) + '. ' + p['title'] + '
'
        combined += 'Authors: ' + p['authors'] + '
'
        combined += 'Abstract: ' + p['abstract'] + '

'
    if groq_key:
        resp = requests.post(
            'https://api.groq.com/openai/v1/chat/completions',
            headers={'Authorization': 'Bearer ' + groq_key, 'Content-Type': 'application/json'},
            json={
                'model': 'llama-3.3-70b-versatile',
                'messages': [{
                    'role': 'user',
                    'content': 'You are an AI research digest. For each paper below, write 1 sentence on what it does and why it matters. Be concise and practical.

' + combined
                }],
                'max_tokens': 600
            },
            timeout=30
        )
        summary = resp.json()['choices'][0]['message']['content']
        print('ARXIV AI DIGEST
')
        print(summary)
    else:
        print(combined)
except Exception as e:
    print('ERROR: ' + str(e))
