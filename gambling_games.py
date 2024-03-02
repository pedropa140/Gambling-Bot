import discord
from discord.ext import commands
import os
from dotenv import load_dotenv
import asyncio
import random
import datetime
import pandas
import json
import math
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
        elif content == '!slots':
            await slots(response, client, user_db)
        elif content == '!guess':
            await guess(response, client, user_db)
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
    originalBlanace = user_db.get_balance(discord_name_cleaned)
    if response.content.isdigit() and int(response.content) <= originalBlanace:
        wage = int(response.content)
        if user_db.is_wager_valid(discord_name_cleaned, wage):
            user_dice1 = random.randint(1,6)
            user_dice2 = random.randint(1,6)
            user_total = user_dice1 + user_dice2
            dealer_dice1 = random.randint(1,6)
            dealer_dice2 = random.randint(1,6)
            dealer_total = dealer_dice1 + dealer_dice2
            if user_total > dealer_total:
                user_db.update_balance(discord_name_cleaned, wage)
                current_date = str(datetime.datetime.now().date())
                current_time = str(datetime.datetime.now().time())
                date = f'{current_date}T{current_time}'
                activity = f'{date} - Won ${wage} playing dice on {current_date}'
                user_db.add_user_activity(discord_name_cleaned, activity, f'{current_date}')
                user_db.update_last_activity(discord_name_cleaned, activity)
                user_db.update_total_earnings(discord_name_cleaned, wage)
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
    originalBlanace = user_db.get_balance(discord_name_cleaned)
    if response.content.isdigit() and int(response.content) <= originalBlanace:
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
            user_db.update_total_earnings(discord_name_cleaned, wage)
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
    # create cards
    # when getting a new card also add it to the list to insert to the back of the deck
    # double deck maybe?
    # split
    # surrender
    # insurance
    # double down

# ROULETTE
async def roulette(message : discord.message.Message, client: discord.Client, user_db : UserDatabase):
    def check(m):
        return m.author == message.author and m.channel == message.channel

# SLOT MACHINE
async def slots(message : discord.message.Message, client: discord.Client, user_db : UserDatabase):
    def check(m):
        return m.author == message.author and m.channel == message.channel
    await message.channel.send("How much are you wagering per spin?")
    response = await client.wait_for('message', check=check, timeout=30)
    discord_name = response.author.mention
    discord_name_cleaned = discord_name.replace('<', '').replace('>', '').replace('@', '')
    originalBlanace = user_db.get_balance(discord_name_cleaned)
    if response.content.isdigit() and int(response.content) <= originalBlanace:
        newBalance = user_db.get_balance(discord_name_cleaned)
        wage = int(response.content)
        con = True
        grid = [[random.choice(['Cherry', 'Bell', 'Bar', 'Lemon', 'Orange', 'Star', 'Apple']) for _ in range(3)] for _ in range(3)]
        # result_grid = [' | '.join(row) + '\n' + '-' * 11 for row in grid]
        result_grid = []
        result_grid.append(('-' * 11) + '\n')
        for row in grid:
            result = ' | '.join(row) + '\n'
            result_grid.append(result)
            result_grid.append(('-' * 11) + '\n')
        await message.channel.send(f'''\nYour Balance is: ${newBalance}. Here is the slot machine:
        {''.join(result_grid)}
        Enter an option: (!spin - spin the slot | !change - to change wager amount | !exit - cash out of slot machine)
        ''')
        while newBalance > 0 and con and wage <= newBalance:            
            response = await client.wait_for('message', check=check, timeout=30)
            user_response = response.content
            if user_response == '!spin':
                symbols = set()
                for row in grid:
                    if len(set(row)) == 1 and row[0] != ' ':
                        symbols.add(row[0])
                if grid[0][0] == grid[1][1] == grid[2][2] and grid[0][0] != ' ':
                    symbols.add(grid[0][0])
                if grid[0][2] == grid[1][1] == grid[2][0] and grid[0][2] != ' ':
                    symbols.add(grid[0][2])
                matches = symbols
                if matches:
                    payouts = {'Cherry': 1, 'Bell': 1.5, 'Bar': 2, 'Lemon': 0.5, 'Orange': 0.5, 'Star': 4, 'Apple': 3}
                    payout = 0
                    for symbol in matches:
                        payout += payouts.get(symbol, 0)
                    newBalance += payout * wage
                    result_price = f'Congratulations! You won $ {payout * wage}\n'
                    user_db.update_total_earnings(discord_name_cleaned, payout * wage)
                else:
                    result_price = f'Sorry, you didn\'t win anything this time.\n'
                    payout = -wage
                newBalance += payout
            elif user_response == '!change':
                await message.channel.send("How much are you wagering per spin?")
                response = await client.wait_for('message', check=check, timeout=30)
                if response.content.isdigit() and int(response.content) <= newBalance:
                    wage = int(response.content)
                    await message.channel.send(f'Wager amount changed to ${wage}')
                result_price = ''
            elif user_response == '!exit':
                await message.channel.send(f'{response.author.mention} has exited.')
                break
            else:
                await message.channel.send("[ERROR]: Inavlid Input. Program Terminated. Please Try Again.")
                break
            
            if newBalance > 0 and wage <= newBalance:
                grid = [[random.choice(['Cherry', 'Bell', 'Bar', 'Lemon', 'Orange', 'Star', 'Apple']) for _ in range(3)] for _ in range(3)]
                result_grid = []
                result_grid.append(('-' * 11) + '\n')
                for row in grid:
                    result = ' | '.join(row) + '\n'
                    result_grid.append(result)
                    result_grid.append(('-' * 11) + '\n')
                await message.channel.send(f'''{result_price}Your Balance is: ${newBalance}. Here is the slot machine:
                {''.join(result_grid)}
                Enter an option: (!spin - spin the slot | !change - to change wager amount | !exit - cash out of slot machine)
                ''')
            else:
                await message.channel.send(f'''"Game over! {discord_name} ran out of money."''')
        difference = newBalance - originalBlanace
        if difference > -1:
            user_db.update_balance(discord_name_cleaned, difference)
            current_date = str(datetime.datetime.now().date())
            current_time = str(datetime.datetime.now().time())
            date = f'{current_date}T{current_time}'
            activity = f'{date} - Won ${difference} playing slots on {current_date}'
            user_db.add_user_activity(discord_name_cleaned, activity, f'{current_date}')
            user_db.update_last_activity(discord_name_cleaned, activity)
            await message.channel.send(f'{discord_name} won ${difference} playing slots.')
        else:
            user_db.update_balance(discord_name_cleaned, difference)
            current_date = str(datetime.datetime.now().date())
            current_time = str(datetime.datetime.now().time())
            date = f'{current_date}T{current_time}'
            activity = f'{date} - Lost ${abs(difference)} playing slots on {current_date}'
            user_db.add_user_activity(discord_name_cleaned, activity, f'{current_date}')
            user_db.update_last_activity(discord_name_cleaned, activity)
            await message.channel.send(f'{discord_name} lost ${abs(difference)} playing slots.')

# GUESS THE NUMBER
async def guess(message : discord.message.Message, client: discord.Client, user_db : UserDatabase):
    def check(m):
        return m.author == message.author and m.channel == message.channel
    await message.channel.send("How much are you wagering?")
    response = await client.wait_for('message', check=check, timeout=30)
    discord_name = response.author.mention
    discord_name_cleaned = discord_name.replace('<', '').replace('>', '').replace('@', '')
    originalBlanace = user_db.get_balance(discord_name_cleaned)
    if response.content.isdigit() and int(response.content) <= originalBlanace:
        wage = int(response.content)
        await message.channel.send("What stake do you want to do? (1) (0 - 10) **1x Multiplier** | (2) (0 - 50) **5x Multiplier** | (3) (0 - 100) **10x Multiplier**)")
        response = await client.wait_for('message', check=check, timeout=30)
        if response.content == '1':
            await message.channel.send("Please give a number between 0 - 10")
            random_number = random.randint(0, 10)
            response = await client.wait_for('message', check=check, timeout=30)
            if response.content == random_number:
                user_db.update_balance(discord_name_cleaned, wage)
                current_date = str(datetime.datetime.now().date())
                current_time = str(datetime.datetime.now().time())
                date = f'{current_date}T{current_time}'
                activity = f'{date} - Won ${wage} playing guess the number on {current_date}'
                user_db.add_user_activity(discord_name_cleaned, activity, f'{current_date}')
                user_db.update_last_activity(discord_name_cleaned, activity)
                user_db.update_total_earnings(discord_name_cleaned, wage)
                await message.channel.send(f'{discord_name} won ${wage} guessing {random_number} in guessing the number')
            else:
                user_db.update_balance(discord_name_cleaned, -wage)
                current_date = str(datetime.datetime.now().date())
                current_time = str(datetime.datetime.now().time())
                date = f'{current_date}T{current_time}'
                activity = f'{date} - Lost ${wage} playing guess the number on {current_date}'
                user_db.add_user_activity(discord_name_cleaned, activity, f'{current_date}')
                user_db.update_last_activity(discord_name_cleaned, activity)
                await message.channel.send(f'{discord_name} lost ${wage} guessing {random_number} in guessing the number')
        elif response.content == '2':
            await message.channel.send("Please give a number between 0 - 50")
            random_number = random.randint(0, 50)
            response = await client.wait_for('message', check=check, timeout=30)
            if response.content == random_number:
                user_db.update_balance(discord_name_cleaned, wage * 5)
                current_date = str(datetime.datetime.now().date())
                current_time = str(datetime.datetime.now().time())
                date = f'{current_date}T{current_time}'
                activity = f'{date} - Won ${wage * 5} playing guess the number on {current_date}'
                user_db.add_user_activity(discord_name_cleaned, activity, f'{current_date}')
                user_db.update_last_activity(discord_name_cleaned, activity)
                user_db.update_total_earnings(discord_name_cleaned, wage * 5)
                await message.channel.send(f'{discord_name} won ${wage * 5} guessing {random_number} in guessing the number')
            else:
                user_db.update_balance(discord_name_cleaned, -wage)
                current_date = str(datetime.datetime.now().date())
                current_time = str(datetime.datetime.now().time())
                date = f'{current_date}T{current_time}'
                activity = f'{date} - Lost ${wage} playing guess the number on {current_date}'
                user_db.add_user_activity(discord_name_cleaned, activity, f'{current_date}')
                user_db.update_last_activity(discord_name_cleaned, activity)
                await message.channel.send(f'{discord_name} lost ${wage} guessing {random_number} in guessing the number')
        elif response.content == '3':
            await message.channel.send("Please give a number between 0 - 100")
            random_number = random.randint(0, 100)
            response = await client.wait_for('message', check=check, timeout=30)
            if response.content == random_number:
                user_db.update_balance(discord_name_cleaned, wage * 10)
                current_date = str(datetime.datetime.now().date())
                current_time = str(datetime.datetime.now().time())
                date = f'{current_date}T{current_time}'
                activity = f'{date} - Won ${wage * 10} playing guess the number on {current_date}'
                user_db.add_user_activity(discord_name_cleaned, activity, f'{current_date}')
                user_db.update_last_activity(discord_name_cleaned, activity)
                user_db.update_total_earnings(discord_name_cleaned, wage * 10)
                await message.channel.send(f'{discord_name} won ${wage * 10} guessing {random_number} in guessing the number')
            else:
                user_db.update_balance(discord_name_cleaned, -wage)
                current_date = str(datetime.datetime.now().date())
                current_time = str(datetime.datetime.now().time())
                date = f'{current_date}T{current_time}'
                activity = f'{date} - Lost ${wage} playing guess the number on {current_date}'
                user_db.add_user_activity(discord_name_cleaned, activity, f'{current_date}')
                user_db.update_last_activity(discord_name_cleaned, activity)
                await message.channel.send(f'{discord_name} lost ${wage} guessing {random_number} in guessing the number')
        else:
            await message.channel.send("[ERROR]: Inavlid Input. Program Terminated. Please Try Again.")