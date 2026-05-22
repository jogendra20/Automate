from scrapling import Fetcher

fetcher = Fetcher(auto_match=False)

page = fetcher.get('https://arxiv.org/list/cs.AI/recent', stealthy_headers=True)
papers = page.css('div#content dl dt + dd')
count = 0

for paper in papers[:10]:
    title = paper.css('div.meta div.list-title.mathjax')[0].text_content().strip().replace("Title: ", "")
    authors = paper.css('div.meta div.list-authors')[0].text_content().strip().replace("Authors:", "").strip()
    count += 1
    print(f"{count}. Title: {title}")
    print(f"   Authors: {authors}")