import json

def load_api_keys(filename='config.json'):
    with open(filename) as f:
        config = json.load(f)
    return config['api_key'], config['api_secret']
