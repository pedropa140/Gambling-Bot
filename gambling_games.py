import discord
from discord.ext import commands
import os
from dotenv import load_dotenv
import asyncio
import random
import datetime
import pandas
import json
from tabulate import tabulate

from user_database import UserDatabase

async def entrance(message : discord.message.Message, client : discord.client, user_db : UserDatabase):
    con = True
    while con:
        await gambling_menu(message)
        def check(m):
            return m.author == message.author and m.channel == message.channel
        response = await client.wait_for('message', check=check, timeout=30)
        content = response.content

        if content == '!dice':
            await dice(response, client, user_db)
        elif content == '!coinflip':
            await coinflip(response, client, user_db)
        elif content == '!blackjack':
            await blackjack(response, client, user_db)
        elif content == '!roulette':
            await roulette(response, client, user_db)
        elif content == '!slot':
            await slots(response, client, user_db)
        elif content == '!guess':
            await slots(response, client, user_db)
        elif content == '!exit':
            await message.channel.send(f'{response.author.mention} has exited.')
            con = False
        else:
            await message.channel.send(f'[ERROR]: Invalid Response. Program Terminated. Please Try Again.')
            con = False

async def gambling_menu(message : discord.message.Message):
    await message.channel.send(f'''Please choose a game:
    **!dice** - Players roll a six-sided die to generate a random number. Wagers double if they get a higher number than the dealer.
    **!coinflip** - Players will guess where the coin will land. Wagers double if they guess the correct 
    **!blackjack** - Players aim to get as close to 21 as possible without going over, competing against a dealer.
    **!roulette** - Players bet on where a ball will land on a spinning wheel, with various betting options available.
    **!slots** - Players spin reels to match symbols and win credits or bonuses.
    **!guess** - Players try to guess a number within a specified range, receiving hints if needed, until they guess correctly.
    **!exit** - Exits gambling page.
    ''')

# DICE
async def dice(message : discord.message.Message, client: discord.Client, user_db : UserDatabase):
    def check(m):
        return m.author == message.author and m.channel == message.channel
    await message.channel.send("How much are you wagering?")
    response = await client.wait_for('message', check=check, timeout=30)
    discord_name = response.author.mention
    discord_name_cleaned = discord_name.replace('<', '').replace('>', '').replace('@', '')
    if response.content.isdigit():
        wage = int(response.content)
        if user_db.is_wager_valid(discord_name_cleaned, wage):
            user_dice1 = random.randint(1,6)
            user_dice2 = random.randint(1,6)
            user_total = user_dice1 + user_dice2
            dealer_dice1 = random.randint(1,6)
            dealer_dice2 = random.randint(1,6)
            dealer_total = dealer_dice1 + dealer_dice2
            # check if user total is greater total total
            if user_total > dealer_total:
                # add money to balance
                # update transactions and change latest historycurrent_date = str(datetime.datetime.now().date())
                user_db.update_balance(discord_name_cleaned, wage)
                current_date = str(datetime.datetime.now().date())
                current_time = str(datetime.datetime.now().time())
                date = f'{current_date}T{current_time}'
                activity = f'{date} - Won ${wage} playing dice on {current_date}'
                user_db.add_user_activity(discord_name_cleaned, activity, f'{current_date}')
                user_db.update_last_activity(discord_name_cleaned, activity)
                await message.channel.send(f'{discord_name} won ${wage} defeating the dealer {user_total} to {dealer_total}')
            elif user_total < dealer_total:
                user_db.update_balance(discord_name_cleaned, -wage)
                current_date = str(datetime.datetime.now().date())
                current_time = str(datetime.datetime.now().time())
                date = f'{current_date}T{current_time}'
                activity = f'{date} - Lost ${wage} playing dice on {current_date}'
                user_db.add_user_activity(discord_name_cleaned, activity, f'{current_date}')
                user_db.update_last_activity(discord_name_cleaned, activity)
                await message.channel.send(f'{discord_name} lost ${wage} losing the dealer {user_total} to {dealer_total}')
            # if tied
            elif user_total == dealer_total:
                # do not change any money
                # update transactions and change latest history
                current_date = str(datetime.datetime.now().date())
                current_time = str(datetime.datetime.now().time())
                date = f'{current_date}T{current_time}'
                activity = f'{date} - Drew ${wage} playing dice on {current_date}'
                user_db.add_user_activity(discord_name_cleaned, activity, f'{current_date}')
                user_db.update_last_activity(discord_name_cleaned, activity)
                await message.channel.send(f'{discord_name} drew the dealer {user_total} to {dealer_total}')
            
        else:
            await message.channel.send("[ERROR]: Inavlid Input. Program Terminated. Please Try Again.")



# COIN FLIP
async def coinflip(message : discord.message.Message, client: discord.Client, user_db : UserDatabase):
    def check(m):
        return m.author == message.author and m.channel == message.channel
    await message.channel.send("How much are you wagering?")
    response = await client.wait_for('message', check=check, timeout=30)
    discord_name = response.author.mention
    discord_name_cleaned = discord_name.replace('<', '').replace('>', '').replace('@', '')
    if response.content.isdigit():
        wage = int(response.content)
        await message.channel.send("What is your prediction? (heads | tails)")
        coin = ['heads', 'tails']
        prediction = random.randint(0, 1)
        result = coin[prediction]
        response = await client.wait_for('message', check=check, timeout=30)
        if response.content.lower() == result:
            user_db.update_balance(discord_name_cleaned, wage)
            current_date = str(datetime.datetime.now().date())
            current_time = str(datetime.datetime.now().time())
            date = f'{current_date}T{current_time}'
            activity = f'{date} - Won ${wage} playing coin flip on {current_date}'
            user_db.add_user_activity(discord_name_cleaned, activity, f'{current_date}')
            user_db.update_last_activity(discord_name_cleaned, activity)
            await message.channel.send(f'{discord_name} won ${wage} guessing {result} in coins')
        elif response.content.lower() != result:
            user_db.update_balance(discord_name_cleaned, -wage)
            current_date = str(datetime.datetime.now().date())
            current_time = str(datetime.datetime.now().time())
            date = f'{current_date}T{current_time}'
            activity = f'{date} - Lost ${wage} playing coin flip on {current_date}'
            user_db.add_user_activity(discord_name_cleaned, activity, f'{current_date}')
            user_db.update_last_activity(discord_name_cleaned, activity)
            await message.channel.send(f'{discord_name} lost ${wage} guessing {result} in coins')
        else:
            await message.channel.send("[ERROR]: Inavlid Input. Program Terminated. Please Try Again.")

# BLACKJACK
async def blackjack(message : discord.message.Message, client: discord.Client, user_db : UserDatabase):
    def check(m):
        return m.author == message.author and m.channel == message.channel
    return NotImplementedError()

# ROULETTE
async def roulette(message : discord.message.Message, client: discord.Client, user_db : UserDatabase):
    def check(m):
        return m.author == message.author and m.channel == message.channel
    return NotImplementedError()

# SLOT MACHINE
async def slots(message : discord.message.Message, client: discord.Client, user_db : UserDatabase):
    def check(m):
        return m.author == message.author and m.channel == message.channel
    return NotImplementedError()