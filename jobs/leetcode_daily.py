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
    query = 'query { activeDailyCodingChallengeQuestion { date link question { title difficulty topicTags { name } acRate content } } }'
    r = requests.post(
        'https://leetcode.com/graphql',
        json={'query': query},
        headers={'User-Agent': 'Mozilla/5.0', 'Content-Type': 'application/json', 'Referer': 'https://leetcode.com'},
        timeout=30
    )
    data = r.json()['data']['activeDailyCodingChallengeQuestion']
    q = data['question']
    tags = ', '.join([t['name'] for t in q['topicTags']])
    ac_rate = round(float(q['acRate']), 1)
    content_text = BeautifulSoup(q.get('content', ''), 'html.parser').get_text()[:800]
    problem_info = 'Title: ' + q['title'] + chr(10) + 'Difficulty: ' + q['difficulty'] + chr(10) + 'Tags: ' + tags + chr(10) + 'Acceptance: ' + str(ac_rate) + '%' + chr(10) + 'Problem:' + chr(10) + content_text
    if nexus_url and nexus_key:
        hint = ask_nexus('You are a coding coach. For this LeetCode problem give: 1) Pattern to use 2) Key insight 3) Time complexity. No code.' + chr(10) + chr(10) + problem_info)
        print('LEETCODE DAILY')
        print('Title: ' + q['title'])
        print('Difficulty: ' + q['difficulty'])
        print('Tags: ' + tags)
        print('Link: https://leetcode.com' + data['link'])
        print(chr(10) + 'COACH HINTS:')
        print(hint)
    else:
        print(problem_info)
except Exception as e:
    print('ERROR: ' + str(e))
