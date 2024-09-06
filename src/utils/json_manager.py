# src/utils/json_utils.py
import os
import json

def load_json(file_path):
    if os.path.exists(file_path):
        with open(file_path, 'r') as f:
            return json.load(f)
    return {}

def save_json(data, file_path):
    with open(file_path, 'w') as f:
        json.dump(data, f, indent=4)