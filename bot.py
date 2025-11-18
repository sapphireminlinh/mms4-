import os
import discord
import requests
import asyncio

TOKEN = os.environ["BOT_TOKEN"]
CHANNEL_ID = int(os.environ["CHANNEL_ID"])

intents = discord.Intents.default()
client = discord.Client(intents=intents)


def get_depth(symbol="BTCUSDT"):
    url = "https://api.binance.com/api/v3/depth"
    params = {"symbol": symbol, "limit": 1000}
    return requests.get(url, params=params).json()


def depth_ratio(depth):
    if "bids" not in depth or "asks" not in depth:
        return None

    bid = sum(float(x[1]) for x in depth["bids"])
    ask = sum(float(x[1]) for x in depth["asks"])
    if ask == 0:
        return None

    return bid / ask


async def scanner():
    await client.wait_until_ready()
    channel = client.get_channel(CHANNEL_ID)

    # Gửi tin nhắn khi bot RUN lần đầu
    await channel.send("🔥 Bot đã khởi động và đang theo dõi orderbook!")

    # Lặp mãi mãi
    while True:
        depth = get_depth("BTCUSDT")
        ratio = depth_ratio(depth)

        if ratio is not None:
            msg = f"📊 Ratio BID/ASK hiện tại: **{ratio:.4f}**"
            await channel.send(msg)

        # ngủ 60s rồi loop tiếp
        await asyncio.sleep(60)


async def status_message():
    await client.wait_until_ready()
    channel = client.get_channel(CHANNEL_ID)

    while True:
        await channel.send("⏰ Bot vẫn đang chạy ổn định (ping 24h).")
        await asyncio.sleep(86400)  # 24 giờ


@client.event
async def on_ready():
    print("Bot đang chạy...")

    # chạy 2 background task song song
    client.loop.create_task(scanner())
    client.loop.create_task(status_message())


client.run(TOKEN)
