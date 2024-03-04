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
    # await message.channel.send(options[random.randint(0, len(options) - 1)] + message.author.mention)
    string = options[random.randint(0, len(options) - 1)] + message.author.mention
    embed = discord.Embed(description=string, color=0xFF5733)
    file = discord.File('images/icon.png', filename='icon.png')
    embed.set_thumbnail(url='attachment://icon.png')
    embed.set_author(name="Gambling-Bot says:")
    embed.set_footer(text="!hello")
    await message.channel.send(file=file, embed=embed)

async def roll_dice(message : discord.message.Message, client : discord.Client):
    def check(m):
        return m.author == message.author and m.channel == message.channel
    try:
        # await message.channel.send("How many sides should the dice have?")
        string = "How many sides should the dice have? Please input a number."
        embed = discord.Embed(description=string, color=0xFF5733)
        file = discord.File('images/icon.png', filename='icon.png')
        embed.set_thumbnail(url='attachment://icon.png')
        embed.set_author(name="Gambling-Bot says:")
        embed.set_footer(text="!roll_dice")
        await message.channel.send(file=file, embed=embed)
        response = await client.wait_for('message', check=check, timeout=30)
        sides = int(response.content)
        if sides <= 0:
            # await message.channel.send("Number of sides must be a positive integer.")
            string = "Number of sides must be a positive integer. Please input a number."
            embed = discord.Embed(description=string, color=0xFF5733)
            file = discord.File('images/icon.png', filename='icon.png')
            embed.set_thumbnail(url='attachment://icon.png')
            embed.set_author(name="Gambling-Bot says:")
            embed.set_footer(text="!roll_dice")
            await message.channel.send(file=file, embed=embed)
            return
        # await message.channel.send(f'{message.author.mention}, you rolled a {random.randint(1, sides)} on a {sides}-sided die!')
        string = f'{message.author.mention}, you rolled a **{random.randint(1, sides)}** on a {sides}-sided die!'
        embed = discord.Embed(description=string, color=0xFF5733)
        file = discord.File('images/icon.png', filename='icon.png')
        embed.set_thumbnail(url='attachment://icon.png')
        embed.set_author(name="Gambling-Bot says:")
        embed.set_footer(text="!roll_dice")
        await message.channel.send(file=file, embed=embed)
    except asyncio.TimeoutError:
        # return message.channel.send(f'{message.author.mention} has taken too long to respond.')
        string = f'{message.author.mention} has taken too long to respond.'
        embed = discord.Embed(description=string, color=0xFF5733)
        file = discord.File('images/icon.png', filename='icon.png')
        embed.set_thumbnail(url='attachment://icon.png')
        embed.set_author(name="Gambling-Bot says:")
        embed.set_footer(text="!roll_dice")
        await message.channel.send(file=file, embed=embed)


async def coin(message : discord.message.Message):
    result = ''
    randomNumber = random.randint(1, 2)
    if randomNumber == 1:
        result = 'heads'
    else:
        result = 'tails'
    # await message.channel.send(f'{message.author.mention} has flipped a {result}!')
    string = f'{message.author.mention} has flipped a **{result}**!'
    embed = discord.Embed(description=string, color=0xFF5733)
    file = discord.File('images/icon.png', filename='icon.png')
    embed.set_thumbnail(url='attachment://icon.png')
    embed.set_author(name="Gambling-Bot says:")
    embed.set_footer(text="!coin")
    await message.channel.send(file=file, embed=embed)

async def help(message : discord.message.Message, client : discord.Client):
    helpResponse = f'''
        **How to use {client.user.name}**
    '''
    # await message.channel.send(helpResponse)
    embed = discord.Embed(title=helpResponse, color=0xFF5733)
    file = discord.File('images/icon.png', filename='icon.png')
    embed.set_thumbnail(url='attachment://icon.png')
    embed.set_author(name="Gambling-Bot says:")
    embed.add_field(name="**!hello**", value="Returns a welcoming message.", inline= False)
    embed.add_field(name="**!roll_dice**", value="Rolls a six-sided dice and returns a random number.", inline= False)
    embed.add_field(name="**!coin**", value="Flips a coin for heads or tails.", inline= False)
    embed.add_field(name="**!gambling**", value="Redirects you to gambling page.", inline= False)
    embed.add_field(name="**!help**", value="Displays this help message.", inline= False)
    embed.set_footer(text="!help")
    await message.channel.send(file=file, embed=embed)