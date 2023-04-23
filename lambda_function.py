import os
import json
import boto3
import requests

TOKEN = os.environ['DISCORD_BOT_TOKEN']
CHANNEL_NAME = os.environ['CHANNEL_NAME']
ANOTHER_LAMBDA_FUNCTION = os.environ['FUNCTION_ARN']

headers = {
    'Authorization': f'Bot {TOKEN}'
}

api_base_url = 'https://discord.com/api/v10'


def get_members():
    # Get the bot's guilds
    response = requests.get(
        f'{api_base_url}/users/@me/guilds', headers=headers)
    guilds = response.json()
    print(f'Bot is a member of {len(guilds)} guilds: {", ".join([guild["name"] for guild in guilds])}')
    print(f'Channel Name: {CHANNEL_NAME}, Lambda to invoke: {ANOTHER_LAMBDA_FUNCTION}')
    members_present = []

    for guild in guilds:
        # Get the channels in the guild
        response = requests.get(
            f'{api_base_url}/guilds/{guild["id"]}/channels', headers=headers)
        channels = response.json()

        # Get the voice states in the guild
        response = requests.get(
            f'{api_base_url}/guilds/{guild["id"]}/voice-states', headers=headers)
        voice_states = response.json()

        for voice_state in voice_states:
            if 'channel_id' in voice_state and voice_state['channel_id'] in [c['id'] for c in channels if c['type'] == 2 and c['name'] == CHANNEL_NAME] and 'member' in voice_state and 'user' in voice_state['member'] and not voice_state['member']['user']['bot']:
                members_present.append(
                    voice_state['member']['user']['username'])

    return members_present


def lambda_handler(event, context):
    members_present = get_members()

    if members_present:
        print(f'Members in "{CHANNEL_NAME}": {", ".join(members_present)}')

        # Invoke the other Lambda function
        lambda_client = boto3.client('lambda')
        lambda_client.invoke(
            FunctionName=ANOTHER_LAMBDA_FUNCTION,
            InvocationType='Event',
            Payload=json.dumps({"action": "start"})
        )
    else:
        print(f'No members in "{CHANNEL_NAME}".')

    return {
        'statusCode': 200,
        'body': json.dumps(members_present)
    }
