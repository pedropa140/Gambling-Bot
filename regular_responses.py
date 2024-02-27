import discord
from discord.ext import commands
import os
from dotenv import load_dotenv
import asyncio
import random
import datetime

async def hello(message : discord.message.Message):
    options = ["Hi ", "Hey ", "Hello ", "Howdy ", "Hi there ", "Greetings ", "Aloha ", "Bonjour ", "Ciao ", "Hola ", "How's it going? ", "Howdy-do ", "Good day ", "Wassup ", "What's popping? ", "What's up? ", "Hiya ", "What's new? ", "How are you? "]
    current_time = datetime.datetime.now().time().hour
    if current_time > 12:
        options.append("Good Afternoon! ")
    else:
        options.append("Good Morning! ")
    await message.channel.send(options[random.randint(0, len(options) - 1)] + message.author.mention)

async def roll_dice(message : discord.message.Message, client : discord.Client):
    def check(m):
        return m.author == message.author and m.channel == message.channel
    try:
        await message.channel.send("How many sides should the dice have?")
        response = await client.wait_for('message', check=check, timeout=30)
        sides = int(response.content)
        if sides <= 0:
            await message.channel.send("Number of sides must be a positive integer.")
            return
        await message.channel.send(f'{message.author.mention}, you rolled a {random.randint(1, sides)} on a {sides}-sided die!')
    except asyncio.TimeoutError:
        return message.channel.send(f'{message.author.mention} has taken too long to respond.')

async def coin(message : discord.message.Message):
    result = ''
    randomNumber = random.randint(1, 2)
    if randomNumber == 1:
        result = 'heads'
    else:
        result = 'tails'
    await message.channel.send(f'{message.author.mention} has flipped a {result}!')

async def help(message : discord.message.Message, client : discord.Client):
    helpResponse = f'''
        **How to use {client.user.name}**
        **!hello**: returns a welcoming message.
        **!roll_dice**: Rolls a six-sided dice and returns a random number.
        **!help**: Displays this help message.
    '''
    await message.channel.send(helpResponse)