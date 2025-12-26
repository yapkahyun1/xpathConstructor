import json
import os
from playwright.sync_api import sync_playwright
from web_scraper import scrape_elements
from playwright.sync_api import expect
from smart_wait import wait_for_object_is_visible


def relative_xpath_constructor(data, stage_number):


    #enter the nodes structure first 
    for node in data.get("nodes", []):
        #enter the data structure
        node_data = node.get("data", {})
        if node_data.get("stage_number") == stage_number:
            actions_data = node_data.get('actions', [])
            for action_item in actions_data:
                element_data = action_item.get('element', {})
                
                print(f'BUILDING RELATIVE XPATH FOR STAGE NUMBER == {stage_number}')

                #getScrapedXpath = str(element_data.get('xpath'))
                # SplitAbsPath = getScrapedXpath.split('/')
                # tagName = SplitAbsPath[len(SplitAbsPath) - 1]



                
                #receivedTagName = 'span'
                tagName = None
                if element_data is None:
                    print("No Element JSON Structure in this Stage")
                    return None
                else:
                    print('Absolute Xpath from JSON: ' + str(element_data.get('xpath')))
                    #get the last element
                    receivedTagName = str(element_data.get('xpath', '')).split('/')[-1]
                    #removed index if required
                    if '[' in receivedTagName:
                        tagName = receivedTagName.split('[')[0]
                        print(f'element <{receivedTagName}> contains index, removed index and the final tagname is <{tagName}>')
                    else:
                        print(f'no index in the element for element <{receivedTagName}>')
                        tagName = receivedTagName
                    


                    
                    

                    attributes_data = element_data.get('attributes', {})


                    #add here if there is more attributes, add by prioritization from highest (left) to the lowest (right)
                    #Will prioritize and build accordingly
                    attr_list = ['id', 'name', 'type', 'value', 'title', 'role', 'placeholder', 'aria-label']
                    for i, attr_name in enumerate(attr_list):
                        final_attrVal = attributes_data.get(attr_name)
                        if final_attrVal:
                            print(f'Attributes <{attr_name}> found, getting values now.........')
                            element_data['xpath'] = f"//{tagName}[@{attr_name}='{final_attrVal}']"
                            return f"//{tagName}[@{attr_name}='{final_attrVal}']"
                        
                            
                        else:
                            # safely check if there is a next attribute
                            if i + 1 < len(attr_list):
                                next_attr = attr_list[i + 1]
                                print(f"No matching attributes for <{attr_name}>, will proceed to check on attributes <{next_attr}>.........")
                            else:
                                print(f"No attributes left in the list to check.")
                                print(f"Will proceed to build relative xpath via text extracted from TEXT_NODES")
                                children_data = element_data.get('children')
                                print("Children JSON here: " + str(children_data))
                                if str(children_data) == '[]':
                                    print("No Children / Text JSON Structure in this Stage")
                                    return None
                                else:
                                    print("Children JSON Structure detected, will proceed to build xpath")
                                    extracted_text_from_json = str(children_data[0].get('text'))
                                    print("Text Extracted from JSON: " + extracted_text_from_json)
                                    element_data['xpath'] = f"//{tagName}[text()='{extracted_text_from_json}']"
                                    return f"//{tagName}[text()='{extracted_text_from_json}']"


                

            break

    
            
#---------------------------------------- RELATIVE XPATH CONSTRUCTOR CORE FUNCTIONS --------------------------------------------------------------------------






#loop through stage number
for i in range(1, 5):
    print(f'Entering Stage Number: {i}')
        

    #to form proper path for the json file and read
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    #print(BASE_DIR)
    JSON_PATH = os.path.join(BASE_DIR, "data.json")
    #print(JSON_PATH)
    print("Looking for:", JSON_PATH)

    try:
        with open(JSON_PATH, "r") as file:
            data = json.load(file)


            #print("Keys:", data.keys())
    except FileNotFoundError:
        print("File not found:", JSON_PATH)
    except json.JSONDecodeError:
        print("Error: failed to decode json")

    #call the functiion and return the relative xpath
    relative_xpath = relative_xpath_constructor(data, i)
    print("Final Output: " + str(relative_xpath))
    #write and update to JSOn for cache related
    with open(JSON_PATH, 'w', encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
        print("✅ JSON updated with new XPath!")
    if i == 4:
        print("NO MORE STAGE NUMBER LEFT ---------- WILL PROCEED TO END THE CONSTRUCTOR FUNCTION")
    else:
        print("CONSTRUCTION COMPLETED ------- Proceed to the next stage")








# # Usage
# url = "https://www.saucedemo.com"
# selector = "//div[@id='login_credentials']"  # Change to your target elements
# scraped_data = scrape_elements(url, selector)

# # Save to JSON
# with open("scraped_data.json", "w", encoding="utf-8") as f:
#     json.dump(scraped_data, f, indent=2, ensure_ascii=False)

# print("✅ JSON file created: scraped_data.json")






#test for smart wait function can integrate prompt mapping and set strict rules for it
#Recommendation:

# ONLY USE VISIBLE ELEMENT INDEXES:
# - If you need an element that's not in the current state.
#   - When the page not fully ready yet, use wait action.
#   - When the object not fully ready yet, use wait_for_object_is_visible function
#   - If you are using wait_for_object_is_visible function, look for True boolean value to check if the object is ready and visible
#   - Do NOT proceed if the wait_for_object_is_visible function returns False boolean value
#   - Take an actions to make it visible (scroll, extract content, navigate, expanding element, etc.)
# - Do NOT use element indexes that you think might exist or that you remember from previous screens

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    page = browser.new_page()
    page.goto("https://www.saucedemo.com/")
    BoolVal = wait_for_object_is_visible(page, "//input[@id='login-button']")
    print(BoolVal)