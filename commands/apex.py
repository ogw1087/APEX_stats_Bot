from data.storage import update_user_data, get_user_history
from data.dummy_data import get_dummy_data
from data.api import get_apex_stats_from_api
from utils.graph import generate_km_graph, generate_rp_graph
import discord

async def handle_apex_stats(ctx, platform: str, username: str):
    await ctx.defer()  # 応答遅延に備えてデファー

    key = f"{platform}:{username}"

    # === tracker.gg API ===
    data = get_apex_stats_from_api(platform, username)

    # === ダミーデータ ===
    #data = get_dummy_data(platform, username)

    if 'data' not in data:
        await ctx.respond("データ取得に失敗しました。")
        return

    stats = data['data']['segments'][0]['stats']                    # 取得JSONでの総合データ位置(以降は各レジェンドデータ 将来的に対応予定)
    level = stats.get('level', {}).get('value', 0)                  # レベル
    kills = stats.get('kills', {}).get('value', 0)                  # キル数
    matches = stats.get('matchesPlayed', {}).get('value', 0)        # マッチ数
    rank_score = stats.get('rankScore', {}).get('value', 0)         # ランクスコア（RP）
    rank_metadata = stats.get('rankScore', {}).get('metadata', {})
    rank_name = rank_metadata.get('rankName', 'N/A')                # ランク名
    username = data['data']['platformInfo']['platformUserHandle']   # ユーザー表示名（platformInfoから取得）

    if matches == 0:
        await ctx.respond("ようこそApexマッチへ！", ephemeral=True)
        return

    # データ保存
    update_user_data(platform, username, stats)

    # 差分比較
    history = get_user_history(platform, username)
    diff = get_latest_diff(history)

    # 結果送信（パブリック）
    await ctx.respond(
        f"**{username}（{platform}）の戦績**\n"
        f"キル数: {kills}\n"
        f"マッチ数: {matches}\n"
        f"K/M（現在）: {round(kills / matches, 2)}\n"
        f"ランク: {rank_name}（RP: {rank_score}）"
    )

    # プライベートで差分送信
    if diff:
        msg = (
            f"🔎 **直近の戦績差分**\n"
            f"・キル差分: {diff['delta_kills']}\n"
            f"・マッチ差分: {diff['delta_matches']}\n"
            f"・期間K/M: {diff['delta_km'] if diff['delta_km'] else 'N/A'}\n"
            f"・ランク: {diff['rank']}（RP: {diff['rank_score']}）\n"
            f"・RP差分: {diff['delta_rp']}"
        )
        await ctx.user.send(msg)
        # 差分があった場合、K/Mグラフも送信
        graph_image = generate_km_graph(history)
        if graph_image:
            file = discord.File(fp=graph_image, filename="km_trend.png")
            await ctx.user.send("📈 **K/M 推移グラフ**", file=file)

        rp_graph_image = generate_rp_graph(history)
        if rp_graph_image:
            file = discord.File(fp=rp_graph_image, filename="rp_graph.png")
            await ctx.user.send("🏆 **RP 推移グラフ**", file=file)
    else:
        await ctx.user.send("初回取得のため差分はありません。")

def get_latest_diff(history):
    if len(history) < 2:
        return None  # 差分不可
    latest = history[-1]
    prev = history[-2]

    kills_diff = latest["kills"]["value"] - prev["kills"]["value"]
    matches_diff = latest["matchesPlayed"]["value"] - prev["matchesPlayed"]["value"]
    rp_diff = latest["rankScore"]["value"] - prev["rankScore"]["value"]

    km_diff = round(kills_diff / matches_diff, 2) if matches_diff > 0 else None

    return {
        "delta_kills": kills_diff,
        "delta_matches": matches_diff,
        "delta_km": km_diff,
        "rank": latest["rankScore"]["metadata"].get("rankName", "N/A"),
        "rank_score": latest["rankScore"]["value"],
        "delta_rp": rp_diff
    }