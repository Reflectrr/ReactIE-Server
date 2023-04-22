import json

def save_json(filename, jsonData):
    # save results to json file
    with open(f'./reactions/result_{filename}', 'w') as f:
        json.dump(jsonData, f, indent=4)