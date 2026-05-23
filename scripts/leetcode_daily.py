import os, requests
from bs4 import BeautifulSoup

run_id = os.environ.get('RUN_ID', '')
groq_key = os.environ.get('GROQ_API_KEY', '')

try:
    query = '''
    query {
        activeDailyCodingChallengeQuestion {
            date
            link
            question {
                title
                difficulty
                topicTags { name }
                acRate
                content
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
    problem_info = (
        'Title: ' + q['title'] + '
'
        'Difficulty: ' + q['difficulty'] + '
'
        'Tags: ' + tags + '
'
        'Acceptance: ' + str(ac_rate) + '%
'
        'Problem:
' + content_text
    )
    if groq_key:
        resp = requests.post(
            'https://api.groq.com/openai/v1/chat/completions',
            headers={'Authorization': 'Bearer ' + groq_key, 'Content-Type': 'application/json'},
            json={
                'model': 'llama-3.3-70b-versatile',
                'messages': [{
                    'role': 'user',
                    'content': 'You are a coding coach. For this LeetCode problem give: 1) What pattern/approach to use 2) Key insight in 1 sentence 3) Time complexity. No code, just hints.

' + problem_info
                }],
                'max_tokens': 300
            },
            timeout=30
        )
        hint = resp.json()['choices'][0]['message']['content']
        print('LEETCODE DAILY')
        print('Title: ' + q['title'])
        print('Difficulty: ' + q['difficulty'])
        print('Tags: ' + tags)
        print('Acceptance: ' + str(ac_rate) + '%')
        print('Link: https://leetcode.com' + data['link'])
        print('
COACH HINTS:')
        print(hint)
    else:
        print(problem_info)
except Exception as e:
    print('ERROR: ' + str(e))
