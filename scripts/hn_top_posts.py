import os
import requests
from bs4 import BeautifulSoup

run_id = os.environ.get('RUN_ID', '')
nexus_url = os.environ.get('NEXUS_URL', '')
nexus_key = os.environ.get('NEXUS_API_KEY', '')

def ask_nexus(prompt):
    r = requests.post(
        nexus_url + '/ask',
        headers={
            'Content-Type': 'application/json',
            'X-API-Key': nexus_key
        },
        json={
            'prompt': prompt,
            'task': 'ask'
        },
        timeout=30
    )

    r.raise_for_status()

    return r.json().get('response', '')

try:
    r = requests.get(
        'https://news.ycombinator.com',
        headers={'User-Agent': 'Mozilla/5.0'},
        timeout=30
    )

    r.raise_for_status()

    soup = BeautifulSoup(r.text, 'html.parser')

    rows = soup.select('tr.athing')
    scores = soup.select('span.score')

    combined = ''

    for i, (row, score) in enumerate(zip(rows[:10], scores[:10])):
        title_el = row.select_one('span.titleline a')

        title = title_el.text.strip() if title_el else 'N/A'
        url = title_el.get('href', '') if title_el else ''
        points = score.text.strip()

        combined += (
            f"{i+1}. {title} ({points})\n"
            f"URL: {url}\n\n"
        )

    if nexus_url:
        prompt = (
            "You are a tech news curator. "
            "For each Hacker News post below, "
            "write 1 sentence explaining why it is interesting "
            "for developers. Be concise.\n\n"
            + combined
        )

        summary = ask_nexus(prompt)

        print("HACKERNEWS DIGEST\n")
        print(summary)

    else:
        print(combined)

except Exception as e:
    print("ERROR:", str(e))
