import json
import os
from datetime import datetime

DATA_FILE = "data/player_data.json"

def load_all_data():
    if not os.path.exists(DATA_FILE):
        return {}
    with open(DATA_FILE, "r", encoding="utf-8") as f:
        return json.load(f)

def save_all_data(data):
    os.makedirs(os.path.dirname(DATA_FILE), exist_ok=True)
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

def update_user_data(platform, username, stats):
    key = f"{platform}:{username}"
    all_data = load_all_data()
    user_entry = all_data.get(key, {
        "username": username,
        "platform": platform,
        "history": []
    })

    # データにタイムスタンプを追加して記録
    stats["timestamp"] = datetime.now().isoformat()
    user_entry["history"].append(stats)
    all_data[key] = user_entry
    save_all_data(all_data)

def get_user_history(platform, username):
    key = f"{platform}:{username}"
    all_data = load_all_data()
    return all_data.get(key, {}).get("history", [])