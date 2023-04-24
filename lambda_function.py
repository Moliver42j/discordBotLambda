import os
import json
import boto3
import requests

TOKEN = os.environ['DISCORD_BOT_TOKEN']

headers = {
    'Authorization': f'Bot {TOKEN}'
}

api_base_url = 'https://discord.com/api/v10'


def get_members():
    members = []
    response = requests.get(
        f'{api_base_url}/users/@me/guilds', headers=headers)
    guilds = response.json()
    for guild in guilds:
        guild_id = guild['id']  # extract the guild ID from the guild dictionary
        # Get the guild's members
        print(f'guild: {guild_id}')
        response = requests.get(
            f'{api_base_url}/guilds/{guild_id}/members?limit=1000', headers=headers)
        members_data = response.json()

        # Append all usernames to the list
        for member in members_data:
            members.append(member['user']['username'])

    return members


def lambda_handler(event, context):
    members = get_members()

    if members:
        print(f'Total members in the guild: {len(members)}')

    return {
        'statusCode': 200,
        'body': json.dumps(members)
    }
