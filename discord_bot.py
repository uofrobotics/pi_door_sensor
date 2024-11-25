# imports
import json
import asyncio
import time
from discord.ext import commands, tasks
import discord as dis
import os
from dotenv import load_dotenv

load_dotenv()

TOKEN = os.getenv('TOKEN')
SERVER_ID = os.getenv('SERVER_ID')
CHANNEL_ID = os.getenv('CHANNEL_ID')

# Turn bot online
class Client(commands.Bot):
    async def on_ready(self):
        print(f'Logged on as {self.user}!')

# Load initial door status
def load_door_status():
    with open('door-state.json', 'r') as file:
        data = json.load(file)
    return data['door_status']

intents = dis.Intents.default()
intents.message_content = True
client = Client(command_prefix="!", help_command=None, intents=intents)
GUILD_ID = dis.Object(id=SERVER_ID)

# Task to update channel name based on door status
@tasks.loop(minutes=1)
async def update_channel_name():
    channel = client.get_channel(CHANNEL_ID)#Replace with your channel ID
    time.sleep(15)
    inp = load_door_status()
    #rename channel
    if inp == 1:
        await channel.edit(name="Door Open 🟢")
    elif inp == 0:
        await channel.edit(name="Door Closed 🔴")

@client.event
async def on_ready():
    print(f'Logged on as {client.user}!')
    update_channel_name.start()  # Start the loop

client.run(TOKEN)

