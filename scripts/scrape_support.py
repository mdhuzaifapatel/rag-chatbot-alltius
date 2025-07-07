import json
import os
from playwright.sync_api import sync_playwright
from urllib.parse import urljoin, urlparse

BASE_URL = "https://www.angelone.in/support"
visited = set()
results = []

def is_valid_url(url):
    return url.startswith(BASE_URL)

def scrape_page(page, url):
    if url in visited:
        return
    visited.add(url)

    try:
        page.goto(url, timeout=20000)
        page.wait_for_load_state("networkidle")

        # Expand any accordions or tabs if needed (optional)
        for btn in page.query_selector_all("button, div[role=button]"):
            try:
                btn.click()
            except:
                pass

        content = page.content()
        text = page.inner_text("body")
        results.append({
            "url": url,
            "text": text
        })

        # Find and follow links
        anchors = page.query_selector_all("a")
        for a in anchors:
            href = a.get_attribute("href")
            if href:
                full_url = urljoin(BASE_URL, href)
                if is_valid_url(full_url):
                    scrape_page(page, full_url)
    except Exception as e:
        print(f"Error scraping {url}: {e}")

def main():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        scrape_page(page, BASE_URL)
        browser.close()

    with open("../data/web_pages/support_data.json", "w") as f:
        json.dump(results, f, indent=2)

if __name__ == "__main__":
    main()
