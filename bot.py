import discord
from discord.ext import commands
import os
from dotenv import load_dotenv
import asyncio
import random
import datetime

import regular_responses

# https://discord.com/oauth2/authorize?client_id=1193596778151432312&permissions=1084479764544&scope=bot

load_dotenv()

def run_discord_bot():
    TOKEN = os.getenv('DISCORD_TOKEN')
    intents = discord.Intents.default()
    intents.message_content = True
    client = discord.Client(intents = intents)

    
    @client.event
    async def on_ready():
        print(f'{client.user} is now running!')
    
    @client.event
    async def on_message(message : discord.message.Message):
        if message.author == client.user:
            return
        username = str(message.author)
        user_message = str(message.content)
        channel = str(message.channel)
        print(f'{username} said: "{user_message}" ({channel})')

        if client.user.mentioned_in(message):
            message_content = str(message.content)
            parts = message_content.split()
            if len(parts) >= 2:
                command = parts[1]
                message.content = command
            if message.content.startswith('!'):
                await process_command(message, client)

    async def process_command(message : discord.message.Message, client : discord.Client):
        command, *args = message.content.split()
        
        if command == '!hello':
            await regular_responses.hello(message)
        elif command == '!roll_dice':
            await regular_responses.roll_dice(message, client)
        elif command == '!help':
            await regular_responses.help(message, client)

    client.run(TOKEN)
    
