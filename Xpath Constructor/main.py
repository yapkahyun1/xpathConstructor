import json
import os

AbsPath = "html/body/cimb-app/div/page-login/div[2]/div/div[4]/div/form/div[2]/div[2]/div/input"
print("Absolute Path:", AbsPath)

#to form proper path for the json file and read
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
print(BASE_DIR)
JSON_PATH = os.path.join(BASE_DIR, "data.json")
print(JSON_PATH)
print("Looking for:", JSON_PATH)

try:
    with open(JSON_PATH, "r") as file:
        data = json.load(file)


        #print("Keys:", data.keys())
except FileNotFoundError:
    print("File not found:", JSON_PATH)
except json.JSONDecodeError:
    print("Error: failed to decode json")
    



    


'loop through json and get what is needed'
for node in data.get("nodes", []):
    node_data = node.get("data", {})
    if node_data.get("stage_number") == 2:
        #print("JSON SOURCE HERE ----------------------------------------\n"+str(node_data))
        actions_data = node_data.get('actions', [])
        #print(actions_data)
        for action_item in actions_data:
            element_data = action_item.get('element', 'no data')
            #print(element_data.get('xpath'))
            attributes_data = element_data.get('attributes', 'nothing')
            print(attributes_data)
            attributesFinal = attributes_data.get('id')
            relative_xpath_construct = '//' + 'input' + f"[@id='{attributesFinal}']"
            print("Final Output: " + relative_xpath_construct)






