import json

def save_json(jsonData):
    # save results to json file
    with open('results.json', 'w') as f:
        json.dump(jsonData, f, indent=4)