import random

def get_dummy_data(platform="origin", username="DummyUser"):
    kills = random.randint(1000, 2000)
    matches = random.randint(200, 400)
    rank_score = random.randint(1000, 10000)
    level = random.randint(50, 500)
    rank_name = random.choice(['Bronze 4', 'Silver 2', 'Gold 1', 'Platinum 4', 'Diamond 3'])

    return {
        "data": {
            "platformInfo": {
                "platformUserHandle": username,
                "platformSlug": platform
            },
            "segments": [{
                "metadata": {"name": "Lifetime"},
                "stats": {
                    "kills": {
                        "value": kills,
                        "displayValue": f"{kills:,}"
                    },
                    "matchesPlayed": {
                        "value": matches,
                        "displayValue": f"{matches:,}"
                    },
                    "level": {
                        "value": level,
                        "displayValue": str(level)
                    },
                    "rankScore": {
                        "value": rank_score,
                        "displayValue": f"{rank_score:,}",
                        "metadata": {
                            "rankName": rank_name
                        }
                    }
                }
            }]
        }
    }
