
from playwright.sync_api import sync_playwright 
from playwright.sync_api import expect

#to scrape elements
def scrape_elements(url, selector):
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        page.goto(url)
        
        elements = page.query_selector_all(selector)
        data = []

        for el in elements:
            attrs = {}
            for name in el.evaluate("e => [...e.attributes].map(a => a.name)"):
                value = el.get_attribute(name)
                attrs[name] = value

            text = el.text_content()
            if text:
                print('here1')
                text = ' '.join(text.split())  # collapse whitespace
            else:
                print('here2')
                text = ''

            data.append({
                "tag": el.evaluate("e => e.tagName").lower(),
                "attrs": attrs,
                "text": text
            })

        browser.close()
        return data
    


