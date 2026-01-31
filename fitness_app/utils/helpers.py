import json
import os
from user import User

DATA_PATH = "data/users.json"

def ensure_data_folder():
    os.makedirs("data", exist_ok=True)

def load_users():
    ensure_data_folder()
    if not os.path.exists(DATA_PATH):
        return {}
    try:
        with open(DATA_PATH, "r", encoding="utf-8") as f:
            data = json.load(f)
            return {u["username"]: User.from_dict(u) for u in data}
    except:
        return {}

def save_users(users_dict):
    ensure_data_folder()
    data = [user.to_dict() for user in users_dict.values()]
    with open(DATA_PATH, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)