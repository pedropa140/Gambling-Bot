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

import gambling_games
from user_database import UserDatabase

async def entrance(message : discord.message.Message, client : discord.Client):
    user_db = UserDatabase()
    await message.channel.send(
    f'''Welcome to the Gambling Center {message.author.mention}
    Are you a returning user? Respond either (YES/NO)
    ''')
    def check(m):
        return m.author == message.author and m.channel == message.channel
    try:
        response = await client.wait_for('message', check=check, timeout=30)
        if response.content.upper() == 'NO':
            await message.channel.send(f'''{response.author.mention} Not Found. Please Choose an Option:```
            (1) Create New User
            (2) Leave
            ```
            ''')
            response = await client.wait_for('message', check=check, timeout=30)
            if response.content == '1':
                if not user_db.find_user(response.author.mention):
                    discord_name = response.author.mention
                    current_date = str(datetime.datetime.now().date())
                    current_time = str(datetime.datetime.now().time())
                    date = f'{current_date}T{current_time}'
                    activity = f'{date} - Created Account on {current_date}'
                    
                    discord_name_cleaned = discord_name.replace('<', '').replace('>', '').replace('@', '')
                    user_db.add_user(response.author.name, discord_name_cleaned, 500, 0, activity, current_date)
                    user_db.add_user_activity(discord_name_cleaned, activity, f'{current_date}T{current_time}')
                    await game_menu(message, client, user_db)
                else:
                    await message.channel.send(f'User [{response.author.mention}] is already created.')
                    await game_menu(message, client, user_db)
            elif response.content == '2':
                return message.channel.send(f'{response.author.mention} has exited.')
            else:
                return message.channel.send(f'[ERROR]: Invalid Response. Program Terminated. Please Try Again.')
            
        elif response.content.upper() == 'YES':
            if user_db.find_user(response.author.mention):
                await message.channel.send(f'Welcome Back {response.author.mention}!')
                await game_menu(message, client, user_db)
            else:
                await message.channel.send(f'''{response.author.mention} Not Found. Please Choose an Option:```
                (1) Create New User
                (2) Leave
                ```
                ''')
                response = await client.wait_for('message', check=check, timeout=30)
                if response.content == '1':
                    discord_name = response.author.mention
                    current_date = str(datetime.datetime.now().date())
                    current_time = str(datetime.datetime.now().time())
                    date = f'{current_date}T{current_time}'
                    activity = f'{date} - Created Account on {current_date}'
                    
                    discord_name_cleaned = discord_name.replace('<', '').replace('>', '').replace('@', '')
                    user_db.add_user(response.author.name, discord_name_cleaned, 500, 0, activity, current_date)
                    user_db.add_user_activity(discord_name_cleaned, activity, f'{current_date}')
                    await message.channel.send(f'{discord_name} created new player.')
                    await game_menu(message, client, user_db)
                elif response.content == '2':
                    await message.channel.send(f'{response.author.mention} has exited.')
                else:
                    await message.channel.send(f'[ERROR]: Invalid Response. Program Terminated. Please Try Again.')
        else:
            await message.channel.send(f'[ERROR]: Invalid Response. Program Terminated. Please Try Again.')
       

    except asyncio.TimeoutError:
        await message.channel.send(f'{message.author.mention} has taken too long to respond.')

async def game_menu(message : discord.message.Message, client : discord.Client, user_db : UserDatabase):
    con = True
    def check(m):
        return m.author == message.author and m.channel == message.channel
    while con:
        await message.channel.send(f'''Please Choose an Option:```    
        01. Choose Game
        02. User Info
        03. Check Balance
        04. Add Money
        05. Leaderboard
        06. Check User History
        07. Exit
        ```
        ''')
        response = await client.wait_for('message', check=check, timeout=30)
        discord_name = message.author.mention
        discord_name_cleaned = discord_name.replace('<', '').replace('>', '').replace('@', '')
        if response.content == '1':
            await gambling_games.entrance(message, client, user_db)
        elif response.content == '2':
            user_info = user_db.get_user_info(discord_name_cleaned)
            if user_info:
                print_statement = ""
                for key, value in user_info.items():
                    print_statement += f'{key}: {value}\n'
                await message.channel.send(f'User Info for {discord_name}:\n {print_statement}')
        elif response.content == '3':
            balance = user_db.get_balance(discord_name_cleaned)
            await message.channel.send(f"Balance for {discord_name}: ${balance}")
        elif response.content == '4':
            await message.channel.send("How much are you willing to deposit?")
            amount_to_add = await client.wait_for('message', check=check, timeout=30)
            amount_to_add = int(amount_to_add.content)
            user_db.update_balance(discord_name_cleaned, amount_to_add)
            current_date = str(datetime.datetime.now().date())
            current_time = str(datetime.datetime.now().time())
            date = f'{current_date}T{current_time}'
            activity = f'{date} - Deposited ${amount_to_add} on {current_date}'
            user_db.add_user_activity(discord_name_cleaned, activity, f'{current_date}')
            user_db.update_last_activity(discord_name_cleaned, activity)
        elif response.content == '5':
            leaderboard_data = user_db.get_leaderboard()
            df = pandas.DataFrame(leaderboard_data, columns=["Name", "Total Earnings", "Level"])
            df.index = range(1, len(df) + 1)
            await message.channel.send(f'Leaderboard:\n{df}')
        elif response.content == '6':
            recent_activities_valid = user_db.get_recent_activities(discord_name_cleaned)
            print(f"Recent activities for {discord_name}:")
            print_statement = f'{discord_name}\'s Activity History:\n'
            statements = []
            for activity, timestamp in reversed(recent_activities_valid):
                statements.append(f"- {activity} ({timestamp})")
            
            for activity in range(0, 5):
                print_statement += statements[activity] + '\n'
            await message.channel.send(print_statement)
        elif response.content == '7':
            con = False
            await message.channel.send(f'{response.author.mention} has exited.')
        else:
            con = False
            await message.channel.send(f'[ERROR]: Invalid Response. Program Terminated. Please Try Again.')