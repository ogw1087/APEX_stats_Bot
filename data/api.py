import os
import requests

def get_apex_stats_from_api(platform, username):
    headers = {'TRN-Api-Key': os.getenv('TRN_API_KEY')}
    url = f'https://public-api.tracker.gg/v2/apex/standard/profile/{platform}/{username}'

    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        return response.json()
    except Exception as e:
        print(f"[API ERROR] {e}")
        return {}