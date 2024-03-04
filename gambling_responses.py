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
    # await message.channel.send(
    # f'''Welcome to the Gambling Center {message.author.mention}
    # Are you a returning user? Respond either (YES/NO)
    # ''')
    entrance_embed_string = f'''Welcome to the Gambling Center {message.author.mention}
    Are you a returning user? Respond either:
    '''
    entrance_embed = discord.Embed(description=entrance_embed_string, color=0x00FFFF)
    file = discord.File('images/icon.png', filename='icon.png')
    entrance_embed.set_thumbnail(url='attachment://icon.png')
    entrance_embed.set_author(name="Gambling-Bot says:")
    entrance_embed.add_field(name="**Yes**", value="If you are a returning user", inline= False)
    entrance_embed.add_field(name="**No**", value="If you are a new user", inline= False)
    entrance_embed.set_footer(text="!gambling")
    await message.channel.send(file=file, embed=entrance_embed)
    def check(m):
        return m.author == message.author and m.channel == message.channel
    try:
        response = await client.wait_for('message', check=check, timeout=30)
        if response.content.upper() == 'NO':
            # await message.channel.send(f'''{response.author.mention} Please Choose an Option:```
            # (1) Create New User
            # (2) Leave
            # ```
            # ''')
            no_string = f'''{response.author.mention} Please Choose an Option:
            '''
            no_embed = discord.Embed(description=no_string, color=0x00FFFF)
            file = discord.File('images/icon.png', filename='icon.png')
            no_embed.set_thumbnail(url='attachment://icon.png')
            no_embed.set_author(name="Gambling-Bot says:")
            no_embed.add_field(name="**!create**", value="Creates a new profile for Discord user.", inline= False)
            no_embed.add_field(name="**!exit**", value="Exits creation of profile.", inline= False)
            no_embed.set_footer(text="!gambling")
            await message.channel.send(file=file, embed=no_embed)
            response = await client.wait_for('message', check=check, timeout=30)
            if response.content == '!create':
                if not user_db.find_user(response.author.mention):
                    discord_name = response.author.mention
                    current_date = str(datetime.datetime.now().date())
                    current_time = str(datetime.datetime.now().time())
                    date = f'{current_date}T{current_time}'
                    activity = f'{date} - Created Account on {current_date}'
                    
                    discord_name_cleaned = discord_name.replace('<', '').replace('>', '').replace('@', '')
                    user_db.add_user(response.author.name, discord_name_cleaned, 500, 0, activity, current_date)
                    user_db.add_user_activity(discord_name_cleaned, activity, f'{current_date}T{current_time}')
                    newaccount_string = f'''{response.author.mention} has created a new account!
                    '''
                    newaccount_embed = discord.Embed(description=newaccount_string, color=0x00FFFF)
                    file = discord.File('images/icon.png', filename='icon.png')
                    newaccount_embed.set_thumbnail(url='attachment://icon.png')
                    newaccount_embed.set_author(name="Gambling-Bot says:")
                    newaccount_embed.set_footer(text="!create")
                    await message.channel.send(file=file, embed=newaccount_embed)
                    await game_menu(message, client, user_db)
                else:
                    # await message.channel.send(f'User [{response.author.mention}] is already created.')
                    created_account_string = f'User [{response.author.mention}] is already created.'
                    created_account_embed = discord.Embed(description=created_account_string, color=0x00FFFF)
                    file = discord.File('images/icon.png', filename='icon.png')
                    created_account_embed.set_thumbnail(url='attachment://icon.png')
                    created_account_embed.set_author(name="Gambling-Bot says:")
                    created_account_embed.set_footer(text="!gambling")
                    await message.channel.send(file=file, embed=created_account_embed)
                    await game_menu(message, client, user_db)
            elif response.content == '!exit':
                # await message.channel.send(f'{response.author.mention} has exited.')
                exit_string = f'{response.author.mention} has exited.'
                exit_embed = discord.Embed(description=exit_string, color=0x00FFFF)
                file = discord.File('images/icon.png', filename='icon.png')
                exit_embed.set_thumbnail(url='attachment://icon.png')
                exit_embed.set_author(name="Gambling-Bot says:")
                exit_embed.set_footer(text="!exit")
                await message.channel.send(file=file, embed=exit_embed)
                return
            else:
                # await message.channel.send(f'[ERROR]: Invalid Response. Program Terminated. Please Try Again.')
                string = f'[ERROR]: Invalid Response. Program Terminated. Please Try Again.'
                embed = discord.Embed(title=string, color=0x00FFFF)
                file = discord.File('images/icon.png', filename='icon.png')
                embed.set_thumbnail(url='attachment://icon.png')
                embed.set_author(name="Gambling-Bot says:")
                embed.set_footer(text="!gambling")
                await message.channel.send(file=file, embed=embed)
                return
            
        elif response.content.upper() == 'YES':
            if user_db.find_user(response.author.mention):
                # await message.channel.send(f'Welcome Back {response.author.mention}!')
                string = f'Welcome Back {response.author.mention}!'
                embed = discord.Embed(description=string, color=0x00FFFF)
                file = discord.File('images/icon.png', filename='icon.png')
                embed.set_thumbnail(url='attachment://icon.png')
                embed.set_author(name="Gambling-Bot says:")
                embed.set_footer(text="!gambling")
                await message.channel.send(file=file, embed=embed)
                await game_menu(message, client, user_db)
            else:
                # await message.channel.send(f'''{response.author.mention} Not Found. Please Choose an Option:
                # ''')
                string = f'''{response.author.mention} Not Found. Please Choose an Option:'''
                embed = discord.Embed(description=string, color=0x00FFFF)
                file = discord.File('images/icon.png', filename='icon.png')
                embed.set_thumbnail(url='attachment://icon.png')
                embed.set_author(name="Gambling-Bot says:")
                embed.add_field(name="**!create**", value="Creates a new profile for Discord user.", inline= False)
                embed.add_field(name="**!exit**", value="Exits creation of profile.", inline= False)
                embed.set_footer(text="!gambling")
                await message.channel.send(file=file, embed=embed)
                response = await client.wait_for('message', check=check, timeout=30)
                if response.content == '!create':
                    discord_name = response.author.mention
                    current_date = str(datetime.datetime.now().date())
                    current_time = str(datetime.datetime.now().time())
                    date = f'{current_date}T{current_time}'
                    activity = f'{date} - Created Account on {current_date}'
                    
                    discord_name_cleaned = discord_name.replace('<', '').replace('>', '').replace('@', '')
                    user_db.add_user(response.author.name, discord_name_cleaned, 500, 0, activity, current_date)
                    user_db.add_user_activity(discord_name_cleaned, activity, f'{current_date}')
                    # await message.channel.send(f'{discord_name} created new player.')
                    string = f'{discord_name} created new player.'
                    embed = discord.Embed(description=string, color=0x00FFFF)
                    file = discord.File('images/icon.png', filename='icon.png')
                    embed.set_thumbnail(url='attachment://icon.png')
                    embed.set_author(name="Gambling-Bot says:")
                    embed.set_footer(text="!create")
                    await message.channel.send(file=file, embed=embed)
                    await game_menu(message, client, user_db)
                elif response.content == '!exit':
                    # await message.channel.send(f'{response.author.mention} has exited.')
                    exit_string = f'{response.author.mention} has exited.'
                    exit_embed = discord.Embed(description=exit_string, color=0x00FFFF)
                    file = discord.File('images/icon.png', filename='icon.png')
                    exit_embed.set_thumbnail(url='attachment://icon.png')
                    exit_embed.set_author(name="Gambling-Bot says:")
                    exit_embed.set_footer(text="!exit")
                    await message.channel.send(file=file, embed=exit_embed)
                    return
                else:
                    # await message.channel.send(f'[ERROR]: Invalid Response. Program Terminated. Please Try Again.')
                    string = f'[ERROR]: Invalid Response. Program Terminated. Please Try Again.'
                    embed = discord.Embed(title=string, color=0x00FFFF)
                    file = discord.File('images/icon.png', filename='icon.png')
                    embed.set_thumbnail(url='attachment://icon.png')
                    embed.set_author(name="Gambling-Bot says:")
                    embed.set_footer(text="!gambling")
                    await message.channel.send(file=file, embed=embed)
                    return
        else:
            # await message.channel.send(f'[ERROR]: Invalid Response. Program Terminated. Please Try Again.')
            string = f'[ERROR]: Invalid Response. Program Terminated. Please Try Again.'
            embed = discord.Embed(title=string, color=0x00FFFF)
            file = discord.File('images/icon.png', filename='icon.png')
            embed.set_thumbnail(url='attachment://icon.png')
            embed.set_author(name="Gambling-Bot says:")
            embed.set_footer(text="!gambling")
            await message.channel.send(file=file, embed=embed)
            return
       

    except asyncio.TimeoutError:
        # await message.channel.send(f'{message.author.mention} has taken too long to respond.')
        f'{message.author.mention} has taken too long to respond.'
        embed = discord.Embed(description=string, color=0xFF5733)
        file = discord.File('images/icon.png', filename='icon.png')
        embed.set_thumbnail(url='attachment://icon.png')
        embed.set_author(name="Gambling-Bot says:")
        embed.set_footer(text="!gambling")
        await message.channel.send(file=file, embed=embed)

async def game_menu(message : discord.message.Message, client : discord.Client, user_db : UserDatabase):
    con = True
    def check(m):
        return m.author == message.author and m.channel == message.channel
    try:
        while con:
            title = f'{message.author.name}!'
            string = f'''Please Choose an Option:'''
            # 01. Choose Game
            # 02. User Info
            # 03. Check Balance
            # 04. Add Money
            # 05. Leaderboard
            # 06. Check User History
            # 07. Exit
            embed = discord.Embed(title=title, description=string, color=0x00FFFF)
            file = discord.File('images/icon.png', filename='icon.png')
            embed.set_thumbnail(url='attachment://icon.png')
            embed.set_author(name="Gambling-Bot says:")
            embed.add_field(name="**!game**", value="Choose a gambling game.", inline= False)
            embed.add_field(name="**!userinfo**", value="Returns Discord user's info.", inline= False)
            embed.add_field(name="**!balance**", value="Returns Discord user's current balance.", inline= False)
            embed.add_field(name="**!addmoney**", value="Adds money to Discord user's account.", inline= False)
            embed.add_field(name="**!leaderboard**", value="Shows the leaderboard of current players.", inline= False)
            embed.add_field(name="**!history**", value="Shows Discord user's gambling account history.", inline= False)
            embed.add_field(name="**!delete**", value="Deletes Discord user from database.", inline= False)
            embed.add_field(name="**!exit**", value="Exits gambling center.", inline= False)
            embed.set_footer(text="!gambling")
            await message.channel.send(file=file, embed=embed)
            # await message.channel.send(f'''Please Choose an Option:```    
            # 01. Choose Game
            # 02. User Info
            # 03. Check Balance
            # 04. Add Money
            # 05. Leaderboard
            # 06. Check User History
            # 07. Exit
            # ```
            # ''')
            response = await client.wait_for('message', check=check, timeout=30)
            discord_name = message.author.mention
            discord_name_cleaned = discord_name.replace('<', '').replace('>', '').replace('@', '')
            if response.content == '!game':
                await gambling_games.entrance(message, client, user_db)
            elif response.content == '!userinfo':
                user_info = user_db.get_user_info(discord_name_cleaned)
                if user_info:
                    print_statement = ""
                    for key, value in user_info.items():
                        print_statement += f'{key}: {value}\n'
                    # await message.channel.send(f'User Info for {discord_name}:\n {print_statement}')
                    userinfo_string = f'User Info for {discord_name}:\n {print_statement}'
                    userinfo_embed = discord.Embed(description=userinfo_string, color=0x00FFFF)
                    file = discord.File('images/icon.png', filename='icon.png')
                    userinfo_embed.set_thumbnail(url='attachment://icon.png')
                    userinfo_embed.set_author(name="Gambling-Bot says:")
                    userinfo_embed.set_footer(text="!userinfo")
                    await message.channel.send(file=file, embed=userinfo_embed)
            elif response.content == '!balance':
                balance = user_db.get_balance(discord_name_cleaned)
                # await message.channel.send(f"Balance for {discord_name}: ${balance}")
                balance_string = f"Balance for {discord_name}: ${balance}"
                balance_embed = discord.Embed(description=balance_string, color=0x00FFFF)
                file = discord.File('images/icon.png', filename='icon.png')
                balance_embed.set_thumbnail(url='attachment://icon.png')
                balance_embed.set_author(name="Gambling-Bot says:")
                balance_embed.set_footer(text="!balance")
                await message.channel.send(file=file, embed=balance_embed)
            elif response.content == '!addmoney':
                question_string = "How much are you willing to deposit?"
                addMoney_embed = discord.Embed(description=question_string, color=0x00FFFF)
                file = discord.File('images/icon.png', filename='icon.png')
                addMoney_embed.set_thumbnail(url='attachment://icon.png')
                addMoney_embed.set_author(name="Gambling-Bot says:")
                addMoney_embed.set_footer(text="!addmoney")
                await message.channel.send(file=file, embed=addMoney_embed)
                amount_to_add = await client.wait_for('message', check=check, timeout=30)
                amount_to_add = int(amount_to_add.content)
                user_db.update_balance(discord_name_cleaned, amount_to_add)
                current_date = str(datetime.datetime.now().date())
                current_time = str(datetime.datetime.now().time())
                date = f'{current_date}T{current_time}'
                activity = f'{date} - Deposited ${amount_to_add} on {current_date}'
                user_db.add_user_activity(discord_name_cleaned, activity, f'{current_date}')
                user_db.update_last_activity(discord_name_cleaned, activity)

                question_string = f'Added {amount_to_add} to {message.author.mention}'
                addMoney_embed = discord.Embed(description=question_string, color=0x00FFFF)
                file = discord.File('images/icon.png', filename='icon.png')
                addMoney_embed.set_thumbnail(url='attachment://icon.png')
                addMoney_embed.set_author(name="Gambling-Bot says:")
                addMoney_embed.set_footer(text="!addmoney")
                await message.channel.send(file=file, embed=addMoney_embed)
            elif response.content == '!leaderboard':
                leaderboard_data = user_db.get_leaderboard()
                df = pandas.DataFrame(leaderboard_data, columns=["Name", "Total Earnings", "Level"])
                df.index = range(1, len(df) + 1)
                # await message.channel.send(f'Leaderboard:\n{df}')
                leaderboard_title = 'Leaderboard'
                leaderboard_string = f'{df}'
                leaderboard_embed = discord.Embed(title=leaderboard_title, description=leaderboard_string, color=0x00FFFF)
                file = discord.File('images/icon.png', filename='icon.png')
                leaderboard_embed.set_thumbnail(url='attachment://icon.png')
                leaderboard_embed.set_author(name="Gambling-Bot says:")
                leaderboard_embed.set_footer(text="!leaderboard")
                await message.channel.send(file=file, embed=leaderboard_embed)
            elif response.content == '!history':
                recent_activities_valid = user_db.get_recent_activities(discord_name_cleaned)
                print(f"Recent activities for {discord_name}:")
                print_statement = f'{discord_name}\'s Activity History:\n'
                statements = []
                for activity, timestamp in reversed(recent_activities_valid):
                    statements.append(f"- {activity} ({timestamp})")
                if len(statements) < 5:
                    for activity in range(0, len(statements)):
                        print_statement += statements[activity] + '\n'
                else:
                    for activity in range(0, 5):
                        print_statement += statements[activity] + '\n'
                # await message.channel.send(print_statement)
                history_title = 'History'
                history_string = print_statement
                history_embed = discord.Embed(title=history_title, description=history_string, color=0x00FFFF)
                file = discord.File('images/icon.png', filename='icon.png')
                history_embed.set_thumbnail(url='attachment://icon.png')
                history_embed.set_author(name="Gambling-Bot says:")
                history_embed.set_footer(text="!history")
                await message.channel.send(file=file, embed=history_embed)
            elif response.content == '!delete':
                user_db.delete_user(discord_name_cleaned)
                delete_title = 'History'
                delete_string = f'{message.author.mention} has been deleted.'
                delete_embed = discord.Embed(title=delete_title, description=delete_string, color=0x00FFFF)
                file = discord.File('images/icon.png', filename='icon.png')
                delete_embed.set_thumbnail(url='attachment://icon.png')
                delete_embed.set_author(name="Gambling-Bot says:")
                delete_embed.set_footer(text="!history")
                await message.channel.send(file=file, embed=delete_embed)
                con = False
            elif response.content == '!exit':
                con = False
                # await message.channel.send(f'{response.author.mention} has exited.')
                exit_string = f'{response.author.mention} has exited.'
                exit_embed = discord.Embed(description=exit_string, color=0x00FFFF)
                file = discord.File('images/icon.png', filename='icon.png')
                exit_embed.set_thumbnail(url='attachment://icon.png')
                exit_embed.set_author(name="Gambling-Bot says:")
                exit_embed.set_footer(text="!exit")
                await message.channel.send(file=file, embed=exit_embed)
            else:
                con = False
                # await message.channel.send(f'[ERROR]: Invalid Response. Program Terminated. Please Try Again.')
                string = f'[ERROR]: Invalid Response. Program Terminated. Please Try Again.'
                embed = discord.Embed(title=string, color=0x00FFFF)
                file = discord.File('images/icon.png', filename='icon.png')
                embed.set_thumbnail(url='attachment://icon.png')
                embed.set_author(name="Gambling-Bot says:")
                embed.set_footer(text="!gambling")
                await message.channel.send(file=file, embed=embed)
    except asyncio.TimeoutError:
        # await message.channel.send(f'{message.author.mention} has taken too long to respond.')
        f'{message.author.mention} has taken too long to respond.'
        embed = discord.Embed(description=string, color=0xFF5733)
        file = discord.File('images/icon.png', filename='icon.png')
        embed.set_thumbnail(url='attachment://icon.png')
        embed.set_author(name="Gambling-Bot says:")
        embed.set_footer(text="!gambling")
        await message.channel.send(file=file, embed=embed)