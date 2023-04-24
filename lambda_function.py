import os
import discord
from discord.ext import commands, tasks

TOKEN = os.environ['DISCORD_BOT_TOKEN']
CHANNEL_NAME = os.environ['CHANNEL_NAME']

intents = discord.Intents.default()
intents.voice_states = True

bot = commands.Bot(command_prefix='!', intents=intents)

@bot.event
async def on_ready():
    print(f'We have logged in as {bot.user}')
    monitor_voice_channels.start()

@tasks.loop(seconds=120)
async def monitor_voice_channels():
    for guild in bot.guilds:
        for channel in guild.voice_channels:
            if channel.name == CHANNEL_NAME:
                connected_members = channel.members
                if connected_members:
                    print(f'Members connected to {channel.name}:')
                    for member in connected_members:
                        print(member)
                else:
                    print(f'No members connected to {channel.name}')

monitor_voice_channels.before_loop
async def before_monitor_voice_channels():
    await bot.wait_until_ready()

bot.run(TOKEN)
