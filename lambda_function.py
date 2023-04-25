import os
import discord
from discord.ext import commands, tasks
import boto3
import json
import asyncio

import sys
sys.path.append("/opt/python-modules")

TOKEN = os.environ['DISCORD_BOT_TOKEN']
CHANNEL_NAME = os.environ['CHANNEL_NAME']
FUNCTION_ARN = os.environ['FUNCTION_ARN']

intents = discord.Intents.default()
intents.voice_states = True

bot = discord.Client(intents=intents)

@bot.event
async def on_ready():
    print(f'We have logged in as {bot.user}')
    monitor_voice_channels.start()
    await stop_bot()

@tasks.loop(seconds=5)
async def monitor_voice_channels():
    for guild in bot.guilds:
        for channel in guild.voice_channels:
            if channel.name == CHANNEL_NAME:
                connected_members = channel.members
                if connected_members:
                    print(f'Members Are connected to {channel.name}')
                    await invoke_lambda_start()
                else:
                    print(f'No members connected to {channel.name}')
                    await invoke_lambda_stop()
                    
    monitor_voice_channels.stop()

async def stop_bot():
    print("Stopping bot...")
    await bot.close()

monitor_voice_channels.before_loop
async def before_monitor_voice_channels():
    await bot.wait_until_ready()

async def invoke_lambda_start():
    print("Attempting start")
    client = boto3.client('lambda')
    payload = {"action": "start"}
    response = await client.invoke(FunctionName=FUNCTION_ARN, Payload=json.dumps(payload))  
    return response

async def invoke_lambda_stop():
    print("Attempting stop")
    client = boto3.client('lambda')
    payload = '{"action": "stop"}'
    response = await client.invoke(FunctionName=FUNCTION_ARN, Payload=payload)
    return response


async def main():
    await bot.start(TOKEN)

asyncio.run(main())
