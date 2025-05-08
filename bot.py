import os
import discord
from discord import option
from dotenv import load_dotenv
from commands.apex import handle_apex_stats

load_dotenv()
TOKEN = os.getenv("DISCORD_TOKEN")

bot = discord.Bot()

@bot.event
async def on_ready():
    print(f"Logged in as {bot.user}")

@bot.slash_command(name="apex", description="APEXの戦績を取得します")
@option(
    "platform",
    description="プラットフォームを選んでください",
    required=True,
    choices=["origin", "psn", "xbl"]
)
@option("username", description="プレイヤーのユーザー名", required=True)
async def apex(ctx, platform: str, username: str):
    await handle_apex_stats(ctx, platform, username)

bot.run(TOKEN)