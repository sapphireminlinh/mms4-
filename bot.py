import discord
import requests
import asyncio
import os

TOKEN = os.environ["BOT_TOKEN"]
CHANNEL_ID = int(os.environ["CHANNEL_ID"])

intents = discord.Intents.default()
client = discord.Client(intents=intents)

def get_depth(symbol="BTCUSDT"):
    url = "https://api.binance.com/api/v3/depth"
    r = requests.get(url, params={"symbol": symbol, "limit": 1000}).json()
    return r

def depth_ratio(depth):
    bid = sum(float(x[1]) for x in depth["bids"])
    ask = sum(float(x[1]) for x in depth["asks"])
    return bid / ask if ask > 0 else 0

async def scanner():
    await client.wait_until_ready()
    channel = client.get_channel(CHANNEL_ID)

    while not client.is_closed():
        depth = get_depth("BTCUSDT")
        ratio = depth_ratio(depth)

        if ratio > 3:
            await channel.send(f"🔥 MM ĐỠ GIÁ MẠNH! Depth Ratio = {ratio:.2f}")

        await asyncio.sleep(5)

@client.event
async def on_ready():
    print(f"Bot {client.user} đã chạy!")

class MyClient(discord.Client):
    async def setup_hook(self):
        # chạy background task đúng cách
        self.loop.create_task(scanner())

client = MyClient(intents=intents)
client.run(TOKEN)
