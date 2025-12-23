import json
import os

AbsPath = "/html/body/div/div/div/div[2]/div/div/div/div[1]/div[2]/div[2]/button"
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


        print("Keys:", data.keys())
except FileNotFoundError:
    print("File not found:", JSON_PATH)
except json.JSONDecodeError:
    print("Error: failed to decode json")
    
    
    
print(f"Something ------------------- {data['graph']}")