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
    roulette_numbers = {
        "0": {"!color": "green", "!parity": "even", "!column": "NA", "!row": "NA", "!group": "NA", "!range": "NA"},
        "00": {"!color": "green", "!parity": "even", "!column": "NA", "!row": "NA", "!group": "NA", "!range": "NA"},
        "1": {"!color": "red", "!parity": "odd", "!column": "1st", "!row": "1st", "!group": "1st 12", "!range": "1 to 18"},
        "2": {"!color": "black", "!parity": "even", "!column": "2nd", "!row": "1st", "!group": "1st 12", "!range": "1 to 18"},
        "3": {"!color": "red", "!parity": "odd", "!column": "3rd", "!row": "1st", "!group": "1st 12", "!range": "1 to 18"},
        "4": {"!color": "black", "!parity": "even", "!column": "1st", "!row": "2nd", "!group": "1st 12", "!range": "1 to 18"},
        "5": {"!color": "red", "!parity": "odd", "!column": "2nd", "!row": "2nd", "!group": "1st 12", "!range": "1 to 18"},
        "6": {"!color": "black", "!parity": "even", "!column": "3rd", "!row": "2nd", "!group": "1st 12", "!range": "1 to 18"},
        "7": {"!color": "red", "!parity": "odd", "!column": "1st", "!row": "3rd", "!group": "1st 12", "!range": "1 to 18"},
        "8": {"!color": "black", "!parity": "even", "!column": "2nd", "!row": "3rd", "!group": "1st 12", "!range": "1 to 18"},
        "9": {"!color": "red", "!parity": "odd", "!column": "3rd", "!row": "3rd", "!group": "1st 12", "!range": "1 to 18"},
        "10": {"!color": "black", "!parity": "even", "!column": "1st", "!row": "4th", "!group": "1st 12", "!range": "1 to 18"},
        "11": {"!color": "black", "!parity": "odd", "!column": "2nd", "!row": "4th", "!group": "1st 12", "!range": "1 to 18"},
        "12": {"!color": "red", "!parity": "even", "!column": "3rd", "!row": "4th", "!group": "1st 12", "!range": "1 to 18"},
        "13": {"!color": "black", "!parity": "odd", "!column": "1st", "!row": "5th", "!group": "2nd 12", "!range": "1 to 18"},
        "14": {"!color": "red", "!parity": "even", "!column": "2nd", "!row": "5th", "!group": "2nd 12", "!range": "1 to 18"},
        "15": {"!color": "black", "!parity": "odd", "!column": "3rd", "!row": "5th", "!group": "2nd 12", "!range": "1 to 18"},
        "16": {"!color": "red", "!parity": "even", "!column": "1st", "!row": "6th", "!group": "2nd 12", "!range": "1 to 18"},
        "17": {"!color": "black", "!parity": "odd", "!column": "2nd", "!row": "6th", "!group": "2nd 12", "!range": "1 to 18"},
        "18": {"!color": "red", "!parity": "even", "!column": "3rd", "!row": "6th", "!group": "2nd 12", "!range": "1 to 18"},
        "19": {"!color": "red", "!parity": "odd", "!column": "1st", "!row": "7th", "!group": "2nd 12", "!range": "19 to 36"},
        "20": {"!color": "black", "!parity": "even", "!column": "2nd", "!row": "7th", "!group": "2nd 12", "!range": "19 to 36"},
        "21": {"!color": "red", "!parity": "odd", "!column": "3rd", "!row": "7th", "!group": "2nd 12", "!range": "19 to 36"},
        "22": {"!color": "black", "!parity": "even", "!column": "1st", "!row": "8th", "!group": "2nd 12", "!range": "19 to 36"},
        "23": {"!color": "red", "!parity": "odd", "!column": "2nd", "!row": "8th", "!group": "2nd 12", "!range": "19 to 36"},
        "24": {"!color": "black", "!parity": "even", "!column": "3rd", "!row": "8th", "!group": "3rd 12", "!range": "19 to 36"},
        "25": {"!color": "red", "!parity": "odd", "!column": "1st", "!row": "9th", "!group": "3rd 12", "!range": "19 to 36"},
        "26": {"!color": "black", "!parity": "even", "!column": "2nd", "!row": "9th", "!group": "3rd 12", "!range": "19 to 36"},
        "27": {"!color": "red", "!parity": "odd", "!column": "3rd", "!row": "9th", "!group": "3rd 12", "!range": "19 to 36"},
        "28": {"!color": "black", "!parity": "even", "!column": "1st", "!row": "10th", "!group": "3rd 12", "!range": "19 to 36"},
        "29": {"!color": "black", "!parity": "odd", "!column": "2nd", "!row": "10th", "!group": "3rd 12", "!range": "19 to 36"},
        "30": {"!color": "red", "!parity": "even", "!column": "3rd", "!row": "10th", "!group": "3rd 12", "!range": "19 to 36"},
        "31": {"!color": "black", "!parity": "odd", "!column": "1st", "!row": "11th", "!group": "3rd 12", "!range": "19 to 36"},
        "32": {"!color": "red", "!parity": "even", "!column": "2nd", "!row": "11th", "!group": "3rd 12", "!range": "19 to 36"},
        "33": {"!color": "black", "!parity": "odd", "!column": "3rd", "!row": "11th", "!group": "3rd 12", "!range": "19 to 36"},
        "34": {"!color": "red", "!parity": "even", "!column": "1st", "!row": "12th", "!group": "3rd 12", "!range": "19 to 36"},
        "35": {"!color": "black", "!parity": "odd", "!column": "2nd", "!row": "12th", "!group": "3rd 12", "!range": "19 to 36"},
        "36": {"!color": "red", "!parity": "even", "!column": "3rd", "!row": "12th", "!group": "3rd 12", "!range": "19 to 36"}
    }

    con = True
    total_bet = 0
    discord_name = message.author.mention
    discord_name_cleaned = discord_name.replace('<', '').replace('>', '').replace('@', '')
    originalBlanace = user_db.get_balance(discord_name_cleaned)
    bet_list = []
    error = False
    while con and not error:        
        wage = 0
        await message.channel.send(f'''
        Where do you want to wager?
        !number - bet on a number
        !color - bet on red or black
        !parity - bet on even or odd
        !column - to bet on what column the number is. i.e., number 24 is on row 3
        !row - to bet on what row the number is. i.e., number 24 is on row 8
        !group - to bet either on 1-12 or 13-24 or 25-36
        !range - to bet on a number from 1-18 or 19-36
        !endbets - to complete betting wagers
        ''')
        response_where = await client.wait_for('message', check=check, timeout=30)
        response_where_content = response_where.content
        if response_where_content == '!number':
            await message.channel.send("What number do you want to wager on?")
            response_event = await client.wait_for('message', check=check, timeout=30)
            number = ''
            if response_event.content.isdigit():
                number = int(response_event.content)
                if number < -1 and number > 37:
                    await message.channel.send("[ERROR]: Number has to be between 0 - 36. Program Terminated. Please Try Again.")
                    error = True
            else:
                await message.channel.send("[ERROR]: Inavlid Input. Program Terminated. Please Try Again.")
                error = True
            await message.channel.send(f"How much are you wagering for {number}?")
            response_wage = await client.wait_for('message', check=check, timeout=30)
            if response_wage.content.isdigit():
                wage += int(response_wage.content)
                if wage + total_bet > originalBlanace:
                    await message.channel.send("[ERROR]: Total bet over player's balance. Program Terminated. Please Try Again.")
                    error = True
                else:
                    total_bet += wage
                    single_payout  = 35
                    bet = (response_where_content, number, wage, single_payout)
                    bet_list.append(bet)
        elif response_where_content == '!color':
            await message.channel.send("What color do you want to wager on? (red | black)")
            response_event = await client.wait_for('message', check=check, timeout=30)
            color = ''
            if response_event.content == 'red':
                color = 'red'
            elif response_event.content == 'black':
                color = 'black'
            else:
                await message.channel.send("[ERROR]: Inavlid Input. Program Terminated. Please Try Again.")
                error = True
            await message.channel.send(f"How much are you wagering for {color}?")
            response_wage = await client.wait_for('message', check=check, timeout=30)
            if response_wage.content.isdigit():
                wage += int(response_wage.content)
                if wage + total_bet > originalBlanace:
                    await message.channel.send("[ERROR]: Total bet over player's balance. Program Terminated. Please Try Again.")
                    error = True
                else:
                    total_bet += wage
                    color_payout  = 1
                    bet = (response_where_content, color, wage, color_payout)
                    bet_list.append(bet)                    
        elif response_where_content == '!parity':
            await message.channel.send("What parity do you want to wager on? (even | odd)")
            response_event = await client.wait_for('message', check=check, timeout=30)
            parity = ''
            if response_event.content == 'odd':
                parity = 'odd'
            elif response_event.content == 'even':
                parity = 'even'
            else:
                await message.channel.send("[ERROR]: Inavlid Input. Program Terminated. Please Try Again.")
                error = True
            await message.channel.send(f"How much are you wagering for {parity}?")
            response_wage = await client.wait_for('message', check=check, timeout=30)
            if response_wage.content.isdigit():
                wage += int(response_wage.content)
                if wage + total_bet > originalBlanace:
                    await message.channel.send("[ERROR]: Total bet over player's balance. Program Terminated. Please Try Again.")
                    error = True
                else:
                    total_bet += wage
                    even_payout = 1
                    bet = (response_where_content, parity, wage, even_payout)
                    bet_list.append(bet)
        elif response_where_content == '!column':
            await message.channel.send("What column do you want to wager on? (1st | 2nd | 3rd)")
            response_event = await client.wait_for('message', check=check, timeout=30)
            column = ''
            if response_event.content == '1st':
                column = '1st'
            elif response_event.content == '2nd':
                column = '2nd'
            elif response_event.content == '3rd':
                column = '3rd'
            else:
                await message.channel.send("[ERROR]: Inavlid Input. Program Terminated. Please Try Again.")
                error = True
            await message.channel.send(f'How much are you wagering for {column} column?')
            response_wage = await client.wait_for('message', check=check, timeout=30)
            if response_wage.content.isdigit():
                wage += int(response_wage.content)
                if wage + total_bet > originalBlanace:
                    await message.channel.send("[ERROR]: Total bet over player's balance. Program Terminated. Please Try Again.")
                    error = True
                else:
                    total_bet += wage
                    column_payout = 2
                    bet = (response_where_content, column, wage, column_payout)
                    bet_list.append(bet)
        elif response_where_content == '!row':
            await message.channel.send("What row do you want to wager on? (1st | 2nd | 3rd | 4th | 5th | 6th | 7th | 8th | 9th | 10th | 11th | 12th)")
            response_event = await client.wait_for('message', check=check, timeout=30)
            row = ''
            if response_event.content == '1st':
                row = '1st'
            elif response_event.content == '2nd':
                row = '2nd'
            elif response_event.content == '3rd':
                row = '3rd'
            elif response_event.content == '4th':
                row = '4th'
            elif response_event.content == '5th':
                row = '5th'
            elif response_event.content == '6th':
                row = '6th'
            elif response_event.content == '7th':
                row = '7th'
            elif response_event.content == '8th':
                row = '8th'
            elif response_event.content == '9th':
                row = '9th'
            elif response_event.content == '10th':
                row = '10th'
            elif response_event.content == '11th':
                row = '11th'
            elif response_event.content == '12th':
                row = '12th'
            else:
                await message.channel.send("[ERROR]: Inavlid Input. Program Terminated. Please Try Again.")
                error = True
            await message.channel.send(f'How much are you wagering for {row} column?')
            response_wage = await client.wait_for('message', check=check, timeout=30)
            if response_wage.content.isdigit():
                wage += int(response_wage.content)
                if wage + total_bet > originalBlanace:
                    await message.channel.send("[ERROR]: Total bet over player's balance. Program Terminated. Please Try Again.")
                    error = True
                else:
                    total_bet += wage
                    street_payout  = 11
                    bet = (response_where_content, row, wage, street_payout)
                    bet_list.append(bet)
        elif response_where_content == '!group':
            await message.channel.send("What group do you want to wager on? (1st 12 | 2nd 12 | 3rd 12)")
            response_event = await client.wait_for('message', check=check, timeout=30)
            group = ''
            if response_event.content == '1st 12':
                group = '1st 12'
            elif response_event.content == '2nd 12':
                group = '2nd 12'
            elif response_event.content == '3rd 12':
                group = '3rd 12'
            else:
                await message.channel.send("[ERROR]: Inavlid Input. Program Terminated. Please Try Again.")
                error = True
            await message.channel.send(f"How much are you wagering for {group}?")
            response_wage = await client.wait_for('message', check=check, timeout=30)
            if response_wage.content.isdigit():
                wage += int(response_wage.content)
                if wage + total_bet > originalBlanace:
                    await message.channel.send("[ERROR]: Total bet over player's balance. Program Terminated. Please Try Again.")
                    error = True
                else:
                    total_bet += wage
                    group_payout  = 2
                    bet = (response_where_content, group, wage, group_payout)
                    bet_list.append(bet)
        elif response_where_content == '!range':
            await message.channel.send("What range do you want to wager on? (1 to 18 | 19 to 36)")
            response_event = await client.wait_for('message', check=check, timeout=30)
            range_bet = ''
            if response_event.content == '1 to 18':
                range_bet = '1 to 18'
            elif response_event.content == '19 to 36':
                range_bet = '19 to 36'
            else:
                await message.channel.send("[ERROR]: Inavlid Input. Program Terminated. Please Try Again.")
                error = True
            await message.channel.send(f"How much are you wagering for {range_bet}?")
            response_wage = await client.wait_for('message', check=check, timeout=30)
            if response_wage.content.isdigit():
                wage += int(response_wage.content)
                if wage + total_bet > originalBlanace:
                    await message.channel.send("[ERROR]: Total bet over player's balance. Program Terminated. Please Try Again.")
                    error = True
                else:
                    total_bet += wage
                    range_payout = 1
                    bet = (response_where_content, range_bet, wage, range_payout)
                    bet_list.append(bet)
        elif response_where_content == '!endbets':
            con = False
            await message.channel.send("No more bets.")
        else:
            con = False
            await message.channel.send("[ERROR]: Total bet over player's balance. Program Terminated. Please Try Again.")
            error = True
        bet_list = list(set(bet_list))
        
    def get_payout(bet):
        return bet[3]
    sorted_bets = sorted(bet_list, key=get_payout, reverse=True)
    print(sorted_bets)
    if error == False:
        spinned_number = random.choice(list(roulette_numbers))
        color = roulette_numbers[spinned_number]["!color"]
        parity = roulette_numbers[spinned_number]["!parity"]
        column = roulette_numbers[spinned_number]["!column"]
        row = roulette_numbers[spinned_number]["!row"]
        group = roulette_numbers[spinned_number]["!group"]
        number_range = roulette_numbers[spinned_number]["!range"]
        found = False
        total = 0
        for bet in sorted_bets:
            command = bet[0]
            if command == '!number':
                if spinned_number == bet[1]:
                    total += bet[2] * bet[3]
                    user_db.update_total_earnings(discord_name_cleaned, total)
                    continue
                else:
                    total -= bet[2]
            elif command == '!row':
                if color == bet[1]:
                    total += bet[2] * bet[3]
                    user_db.update_total_earnings(discord_name_cleaned, total)
                    continue
                else:
                    total -= bet[2]            
            elif command == '!column':
                if color == bet[1]:
                    total += bet[2] * bet[3]
                    user_db.update_total_earnings(discord_name_cleaned, total)
                    continue
                else:
                    total -= bet[2]
                    
            elif command == '!group':
                if color == bet[1]:
                    total += bet[2] * bet[3]
                    user_db.update_total_earnings(discord_name_cleaned, total)
                    continue
                else:
                    total -= bet[2]
                      
            elif command == '!color':
                if color == bet[1]:
                    total += bet[2] * bet[3]
                    user_db.update_total_earnings(discord_name_cleaned, total)
                    continue
                else:
                    total -= bet[2]
            elif command == '!range':
                if color == bet[1]:
                    total += bet[2] * bet[3]
                    user_db.update_total_earnings(discord_name_cleaned, total)
                    continue
                else:
                    total -= bet[2]
            elif command == '!parity':
                if color == bet[1]:
                    total += bet[2] * bet[3]
                    user_db.update_total_earnings(discord_name_cleaned, total)
                    continue
                else:
                    total -= bet[2]
        if total > -1:
            user_db.update_balance(discord_name_cleaned, total)
            current_date = str(datetime.datetime.now().date())
            current_time = str(datetime.datetime.now().time())
            date = f'{current_date}T{current_time}'
            activity = f'{date} - Won ${total} playing roulette on {current_date}'
            user_db.add_user_activity(discord_name_cleaned, activity, f'{current_date}')
            user_db.update_last_activity(discord_name_cleaned, activity)
            await message.channel.send(f'{discord_name} won ${total} playing roulette.')
        else:
            user_db.update_balance(discord_name_cleaned, total)
            current_date = str(datetime.datetime.now().date())
            current_time = str(datetime.datetime.now().time())
            date = f'{current_date}T{current_time}'
            activity = f'{date} - Lost ${abs(total)} playing roulette on {current_date}'
            user_db.add_user_activity(discord_name_cleaned, activity, f'{current_date}')
            user_db.update_last_activity(discord_name_cleaned, activity)
            await message.channel.send(f'{discord_name} lost ${abs(total)} playing roulette.')
    else:
        print("errors")

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