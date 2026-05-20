from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    browser = p.chromium.launch(
        headless=True,
        args=["--no-sandbox", "--disable-dev-shm-usage"]
    )
    page = browser.new_page(viewport={"width": 1280, "height": 800})

    page.goto("https://www.tickertape.in/market-mood-index", wait_until="domcontentloaded", timeout=60000)
    page.wait_for_timeout(3000)

    # Go directly to stocks screener with gainers filter
    page.goto("https://www.tickertape.in/screener/equity/pre-built/top-gainers", wait_until="domcontentloaded", timeout=60000)

    # Wait for actual data rows to appear — not a fixed sleep
    try:
        page.wait_for_selector("a[href*='/stocks/']", timeout=20000)
    except:
        print("Timeout waiting for gainers table")
        browser.close()
        exit(1)

    page.wait_for_timeout(2000)

    rows = page.query_selector_all("a[href*='/stocks/']")
    seen = set()
    count = 0
    for row in rows:
        try:
            text = row.inner_text().strip()
            href = row.get_attribute("href") or ""
            # Must be a stock link and have content
            if not text or href in seen or "/stocks/" not in href:
                continue
            seen.add(href)
            lines = [l.strip() for l in text.split("\n") if l.strip()]
            if lines:
                print(" | ".join(lines[:3]))
                count += 1
                if count >= 10:
                    break
        except:
            pass

    if count == 0:
        print("No gainers found — selector may have changed")
        # Screenshot for debug
        page.screenshot(path="debug_gainers.png")

    browser.close()
