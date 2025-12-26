from playwright.sync_api import sync_playwright
from web_scraper import scrape_elements
from playwright.sync_api import expect




def wait_for_object_is_visible(pageObj, strXpath):
        
    pageObj.goto("https://www.saucedemo.com/")
        

    if pageObj.locator(strXpath).is_visible():
        print("Yes Exist")
        return True
    else:
        print("No")
        return False
        
    



