import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from io import BytesIO
from datetime import datetime

def generate_km_graph(history):
    if len(history) < 2:
        return None  # 差分がないとグラフは無意味

    km_values = []
    timestamps = []

    for data in history:
        kills = data.get("kills", {}).get("value", 0)
        matches = data.get("matchesPlayed", {}).get("value", 0)

        if matches > 0:
            km = round(kills / matches, 2)
        else:
            km = 0

        km_values.append(km)

        # ISO形式のtimestampをdatetimeに変換
        ts = data.get("timestamp", "")
        try:
            dt = datetime.fromisoformat(ts)
        except ValueError:
            dt = datetime.now()  # フォールバック
        timestamps.append(dt)

    plt.figure(figsize=(6, 4))
    plt.plot(timestamps, km_values, marker='o', color='skyblue')
    plt.title("Kill/Match")
    plt.xlabel("Date")
    plt.ylabel("K/M")
    plt.grid(True)

    # ラベルの自動間引きと斜め表示
    ax = plt.gca()
    ax.xaxis.set_major_locator(mdates.AutoDateLocator())
    ax.xaxis.set_major_formatter(mdates.DateFormatter('%m/%d\n%H:%M'))
    plt.xticks(rotation=45, ha='right')

    plt.tight_layout()

    buffer = BytesIO()
    plt.savefig(buffer, format="png")
    buffer.seek(0)
    plt.close()

    return buffer

def generate_rp_graph(history):
    if len(history) < 2:
        return None  # データが不十分ならスキップ

    rp_values = []
    timestamps = []

    for data in history:
        rp = data.get("rankScore", {}).get("value", 0)
        ts = data.get("timestamp", "")
        try:
            dt = datetime.fromisoformat(ts)
        except ValueError:
            dt = datetime.now()
        rp_values.append(rp)
        timestamps.append(dt)

    plt.figure(figsize=(6, 4))
    plt.plot(timestamps, rp_values, marker='o', color='orange')
    plt.title("Rank Points Over Time")
    plt.xlabel("Date")
    plt.ylabel("RP")
    plt.grid(True)

    ax = plt.gca()
    ax.xaxis.set_major_locator(mdates.AutoDateLocator())
    ax.xaxis.set_major_formatter(mdates.DateFormatter('%m/%d\n%H:%M'))
    plt.xticks(rotation=45, ha='right')

    plt.tight_layout()

    buffer = BytesIO()
    plt.savefig(buffer, format="png")
    buffer.seek(0)
    plt.close()

    return buffer