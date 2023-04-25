import os
import discord
from discord.ext import commands, tasks
import asyncio
import json
import boto3

import sys
sys.path.append("/opt/python-modules")

TOKEN = os.environ['DISCORD_BOT_TOKEN']
CHANNEL_NAME = os.environ['CHANNEL_NAME']
FUNCTION_ARN = os.environ['FUNCTION_ARN']

intents = discord.Intents.default()
intents.voice_states = True

bot = discord.Client(intents=intents)

# Initialize the Lambda client
lambda_client = boto3.client('lambda')

@bot.event
async def on_ready():
    print(f'We have logged in as {bot.user}')
    await monitor_voice_channels()

async def monitor_voice_channels():
    for guild in bot.guilds:
        for channel in guild.voice_channels:
            if channel.name == CHANNEL_NAME:
                connected_members = channel.members
                if connected_members:
                    print(f'Members Are connected to {channel.name}')
                    # Invoke Lambda function
                    await invoke_lambda_start()
                else:
                    print(f'No members connected to {channel.name}')
                    await invoke_lambda_stop()

async def invoke_lambda_start():
    payload = {
        "action": "start"
    }
    lambda_client.invoke(
        FunctionName=FUNCTION_ARN,
        InvocationType='Event',
        Payload=json.dumps(payload)
    )

async def invoke_lambda_stop():
    payload = {
        "action": "stop"
    }
    lambda_client.invoke(
        FunctionName=FUNCTION_ARN,
        InvocationType='Event',
        Payload=json.dumps(payload)
    )

async def stop_bot():
    print("Stopping bot...")
    await bot.close()

async def main():
    await bot.start(TOKEN)

# AWS Lambda handler
def lambda_handler(event, context):
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
