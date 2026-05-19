import os
from playwright.sync_api import sync_playwright

def scrape_iran_war_news():
    with sync_playwright() as p:
        chromium = p.chromium.launch(
            headless=True,
            args=[
                '--no-sandbox',
                '--disable-dev-shm-usage'
            ]
        )
        page = chromium.new_page()

        # Set user agent and other headers
        user_agent = os.getenv('USER_AGENT', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36')
        page.set_extra_http_headers({
            'User-Agent': user_agent,
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.5',
        })

        # Navigate to Google News for Iran war
        page.goto('https://news.google.com/search?q=iran%20war&hl=en-US&gl=US&ceid=US%3Aen')

        # Extract news headlines
        headlines = page.evaluate('''() => {
            return Array.from(document.querySelectorAll('article')).map(el => {
                const title = el.querySelector('h3')?.innerText;
                const source = el.querySelector('div[role="heading"]')?.innerText;
                const time = el.querySelector('time')?.innerText;
                const link = el.querySelector('a')?.href;
                return { title, source, time, link };
            }).filter(item => item.title && item.link);
        }''')

        # Print results
        for idx, item in enumerate(headlines[:10], 1):
            print(f"News {idx}:")
            print(f"Title: {item['title']}")
            print(f"Source: {item['source']}")
            print(f"Time: {item['time']}")
            print(f"Link: {item['link']}")
            print("-" * 50)

        chromium.close()

if __name__ == '__main__':
    scrape_iran_war_news()