import os, requests, json
from bs4 import BeautifulSoup

run_id = os.environ.get('RUN_ID', '')
groq_key = os.environ.get('GROQ_API_KEY', '')

try:
    r = requests.get('https://news.ycombinator.com',
        headers={'User-Agent': 'Mozilla/5.0'}, timeout=30)
    soup = BeautifulSoup(r.text, 'html.parser')
    rows = soup.select('tr.athing')
    scores = soup.select('span.score')
    posts = []
    for i, (row, score) in enumerate(zip(rows[:10], scores[:10])):
        title_el = row.select_one('span.titleline a')
        title = title_el.text.strip() if title_el else 'N/A'
        url = title_el.get('href', '') if title_el else ''
        points = score.text.strip()
        posts.append({'title': title, 'url': url, 'points': points})
    combined = ''
    for i, p in enumerate(posts):
        combined += str(i+1) + '. ' + p['title'] + ' (' + p['points'] + ')
'
        combined += 'URL: ' + p['url'] + '

'
    if groq_key:
        resp = requests.post(
            'https://api.groq.com/openai/v1/chat/completions',
            headers={'Authorization': 'Bearer ' + groq_key, 'Content-Type': 'application/json'},
            json={
                'model': 'llama-3.3-70b-versatile',
                'messages': [{
                    'role': 'user',
                    'content': 'You are a tech news curator. For each HackerNews post below, write 1 sentence on why it is interesting or important for a developer. Be concise.

' + combined
                }],
                'max_tokens': 600
            },
            timeout=30
        )
        summary = resp.json()['choices'][0]['message']['content']
        print('HACKERNEWS DIGEST
')
        print(summary)
    else:
        print(combined)
except Exception as e:
    print('ERROR: ' + str(e))
