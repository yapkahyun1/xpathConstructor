import json
import os
from playwright.sync_api import sync_playwright
from web_scraper import scrape_elements




def get_first_xpath(data, stage_number):
    #initiaze var make sure its empty before processing
    attr_id = ""
    attr_name = ""
    attr_type = ""
    attr_role = ""
    attr_placeholder = ""
    attr_value = ""
    attr_title = ""
    attr_aria_label = ""






    for node in data.get("nodes", []):
        node_data = node.get("data", {})
        if node_data.get("stage_number") == stage_number:
            actions_data = node_data.get('actions', [])
            for action_item in actions_data:
                element_data = action_item.get('element', {})
                
                print(f'BUILDING RELATIVE XPATH FOR STAGE NUMBER == {stage_number}')

                #getScrapedXpath = str(element_data.get('xpath'))
                # SplitAbsPath = getScrapedXpath.split('/')
                # tagName = SplitAbsPath[len(SplitAbsPath) - 1]



                #get the last element
                #receivedTagName = 'span'
                tagName = None
                if element_data is None:
                    print("No Element JSON Structure in this Stage")
                    return None
                else:
                    print('Absolute Xpath from JSON: ' + str(element_data.get('xpath')))
                    receivedTagName = str(element_data.get('xpath', '')).split('/')[-1]
                    if '[' in receivedTagName:
                        tagName = receivedTagName.split('[')[0]
                        print(f'element <{receivedTagName}> contains index, removed index and the final tagname is <{tagName}>')
                    else:
                        print(f'no index in the element for element <{receivedTagName}>')
                        tagName = receivedTagName
                    


                    
                    

                    attributes_data = element_data.get('attributes', {})
                    #print(attributes_data)
                    # attr_id = attributes_data.get('id')
                    # attr_name = attributes_data.get('name')
                    # attr_type = attributes_data.get('type')
                    # attr_role = attributes_data.get('role')
                    # attr_placeholder = attributes_data.get('placeholder')
                    # attr_value = attributes_data.get('value')
                    # attr_title = attributes_data.get('title')
                    # attr_aria_label = attributes_data.get('aria-label')

                    #add here if there is more attributes, add by prioritization from highest (left) to the lowest (right)
                    attr_list = ['id', 'name', 'type', 'value', 'title', 'role', 'placeholder', 'aria-label']
                    for i, attr_name in enumerate(attr_list):
                        final_attrVal = attributes_data.get(attr_name)
                        if final_attrVal:
                            print(f'Attributes <{attr_name}> found, getting values now.........')
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
                                    return f"//{tagName}[text()='{extracted_text_from_json}']"


                

            break

    
            
#---------------------------------------- RELATIVE XPATH CONSTRUCTOR CORE FUNCTIONS --------------------------------------------------------------------------





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
        



    relative_xpath_construct = get_first_xpath(data, i)
    print("Final Output: " + str(relative_xpath_construct))
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







