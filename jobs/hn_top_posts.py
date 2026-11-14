import os
import requests
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

    if nexus_url and nexus_key:
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
