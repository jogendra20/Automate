from playwright.sync_api import sync_playwright

try:
    with sync_playwright() as p:
        browser = p.chromium.launch(
            headless=True,
            args=['--no-sandbox', '--disable-dev-shm-usage', '--disable-gpu']
        )
        page = browser.new_page(viewport={'width': 1280, 'height': 800})
        try:
            page.goto(
                "https://examcell.gprec.ac.in/StudentDetails/StudentDetailsLogin.aspx?service=%27Academic%20Performance%27",
                wait_until='domcontentloaded',
                timeout=30000
            )
            inputs = page.locator("input")
            count = inputs.count()

            for i in range(count):
                element = inputs.nth(i)
                print({
                    "type": element.get_attribute("type"),
                    "name": element.get_attribute("name"),
                    "id": element.get_attribute("id"),
                    "value": element.get_attribute("value")
                })

            page.screenshot(path="screenshot.png")
            print("screenshot saved")
        except Exception as e:
            print(f"ERROR: {e}")
            page.screenshot(path="screenshot.png")
            print("screenshot saved")
        finally:
            browser.close()
except Exception as e:
    print(f"ERROR: {e}")