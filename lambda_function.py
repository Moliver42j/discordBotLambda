import os
import discord
from discord.ext import commands
import boto3

bot = commands.Bot(command_prefix='/', intents=discord.Intents.all())
lambda_client = boto3.client('lambda', region_name='eu-west-1')

@bot.event
async def on_ready():
    print(f'{bot.user} is connected to Discord!')

@bot.event
async def on_message(message):
    if message.content.startswith('/startZomboid'):
        print(f'Messaged Received: {message.content}')
        # Trigger the Lambda function
        lambda_client.invoke(
            FunctionName='serverSpinupLambda',
            InvocationType='Event',
            Payload='{"action": "start"}'
        )
    if message.content.startswith('/stopZomboid'):
        print('Messaged Received: f{message.content}')
        # Trigger the Lambda function
        lambda_client.invoke(
            FunctionName='serverSpinupLambda',
            InvocationType='Event',
            Payload='{"action": "stop"}'
        )
    await bot.process_commands(message)

bot.run(os.environ['DISCORD_BOT_TOKEN'])
