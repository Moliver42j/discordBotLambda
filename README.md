# Discord Bot Lambda Function
## This code is a simple Discord bot that triggers an AWS Lambda function to start and stop a game server.

## Requirements
- Python 3.x
- Discord.py
- Boto3
- AWS account

## Setup
- Clone or download the code from the repository.
- Install the required packages using pip: pip install -r - requirements.txt.
- Create a Discord bot and obtain its token.
- Create an AWS Lambda function and set its permissions to - allow invocation from the Discord bot.
- Replace the FunctionName parameter in the lambda_client.- invoke() method with the name of your Lambda function.
- Set the value of the 'DISCORD_BOT_TOKEN' environment - variable to your Discord bot's token.
- Run the code using python3 lambda_function.py.
## Usage
The bot listens for two commands:

- /startZomboid: Starts the game server by triggering the Lambda function with a payload of {"action": "start"}.
- /stopZomboid: Stops the game server by triggering the Lambda function with a payload of {"action": "stop"}.

When a command is received, the bot prints a message to the console and triggers the Lambda function with the corresponding payload.