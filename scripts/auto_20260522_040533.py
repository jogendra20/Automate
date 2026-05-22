import os
from scrapling import Fetcher

run_id = os.environ.get('RUN_ID', '')

fetcher = Fetcher(auto_match=False)

def extract_papers():
    response = fetcher.get('https://arxiv.org/list/cs.AI/recent', stealthy_headers=True)
    papers = response.css('div#content dl article')
    for paper in papers[:10]:
        title = paper.css('div.list-title.mathjax::text').get()
        title = title.strip().replace("Title: ", "")
        print(f"Title: {title}")
        paper_response = fetcher.get(paper.css('div.meta div.list-title.mathjax a::attr(href)').get(), stealthy_headers=True)
        authors = paper_response.html.split("Authors:")[1].split("</pre>")[0].strip()
        print(f"Authors: {authors}")
        print()

fetcher.get('https://arxiv.org/list/cs.AI/recent', stealthy_headers=True)
extract_papers()
fetcher.save_response('https://arxiv.org/list/cs.AI/recent', 'page.html')
print()