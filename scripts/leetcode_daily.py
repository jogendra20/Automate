import os, requests
from bs4 import BeautifulSoup

run_id = os.environ.get('RUN_ID', '')
nexus_url = os.environ.get('NEXUS_URL', '')
nexus_key = os.environ.get('NEXUS_API_KEY', '')

def ask_nexus(prompt):
    r = requests.post(
        nexus_url + '/ask',
        headers={'Content-Type': 'application/json', 'X-API-Key': nexus_key},
        json={'prompt': prompt, 'task': 'ask'},
        timeout=30
    )
    return r.json().get('response', '')

try:
    query = '''
    query {
        activeDailyCodingChallengeQuestion {
            date link
            question {
                title difficulty
                topicTags { name }
                acRate content
            }
        }
    }
    '''
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
    problem_info = 'Title: ' + q['title'] + '
Difficulty: ' + q['difficulty'] + '
Tags: ' + tags + '
Acceptance: ' + str(ac_rate) + '%
Problem:
' + content_text
    if nexus_url:
        hint = ask_nexus('You are a coding coach. For this LeetCode problem give: 1) Pattern to use 2) Key insight 3) Time complexity. No code.

' + problem_info)
        print('LEETCODE DAILY')
        print('Title: ' + q['title'])
        print('Difficulty: ' + q['difficulty'])
        print('Tags: ' + tags)
        print('Link: https://leetcode.com' + data['link'])
        print('
COACH HINTS:')
        print(hint)
    else:
        print(problem_info)
except Exception as e:
    print('ERROR: ' + str(e))
