import os
import requests

run_id = os.environ.get('RUN_ID', '')

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
            }
        }
    }
    '''
    r = requests.post(
        'https://leetcode.com/graphql',
        json={'query': query},
        headers={
            'User-Agent': 'Mozilla/5.0',
            'Content-Type': 'application/json',
            'Referer': 'https://leetcode.com'
        },
        timeout=30
    )
    data = r.json()['data']['activeDailyCodingChallengeQuestion']
    q = data['question']
    tags = ', '.join([t['name'] for t in q['topicTags']])
    ac_rate = round(float(q['acRate']), 1)
    print('LEETCODE DAILY')
    print('Title: ' + q['title'])
    print('Difficulty: ' + q['difficulty'])
    print('Tags: ' + tags)
    print('Acceptance: ' + str(ac_rate) + '%')
    print('Link: https://leetcode.com' + data['link'])
except Exception as e:
    print('ERROR: ' + str(e))
