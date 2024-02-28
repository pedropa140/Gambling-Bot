import discord
from discord.ext import commands
import os
from dotenv import load_dotenv
import asyncio
import random
import datetime
import pandas
import json

from player import Player
import gambling_games

async def entrance(message : discord.message.Message, client : discord.Client):
    await message.channel.send(
    f'''Welcome to the Gambling Center {message.author.mention}
    Are you a returning user? Respond either (YES/NO)
    '''
    )
    player_dictionary = read_players_from_file("players")
    def check(m):
        return m.author == message.author and m.channel == message.channel
    try:
        response = await client.wait_for('message', check=check, timeout=30)
        if response.content.upper() == 'NO':
            await message.channel.send('''Please Choose an Option:
                                       (1) Create New User
                                       (2) Leave''')
            response = await client.wait_for('message', check=check, timeout=30)
            if response.content == '1':
                # check if they are in the dictionary
                if not find_player(response.author.mention):
                    create_player(message, client, player_dictionary)
                else:
                    await message.channel.send(f'User [{response.author.mention}] is already created.')
                    await play_game(message, client, player_dictionary)
                # if they are then exit to play game
                # else create a new profile
                return NotImplementedError()
            elif response.content == '2':
                await message.channel.send(f'{response.author.mention} has exited.')
            else:
                await message.channel.send(f'[ERROR]: Invalid Response. Program Terminated. Please Try Again.')
            
        elif response.content.upper() == 'YES':
            if find_player(player_dictionary, response.author.mention):
                await message.channel.send(f'Welcome Back {response.author.mention}!')
                await play_game(message, client, player_dictionary)
            else:
                await message.channel.send(f'''{response.author.mention} Not Found. Please Choose an Option:
                                       (1) Create New User
                                       (2) Leave''')
                response = await client.wait_for('message', check=check, timeout=30)
                if response.content == '1':
                    create_player(message, client, player_dictionary)
                    await message.channel.send(f'{response.author.mention} created new player.')
                    await play_game(message, client, player_dictionary)
                elif response.content == '2':
                    return message.channel.send(f'{response.author.mention} has exited.')
                else:
                    return message.channel.send(f'[ERROR]: Invalid Response. Program Terminated. Please Try Again.')
            # check if they are new player
            # if not in dictionary then ask to create user
            # else exit to play game
            # return NotImplementedError()
            # await message.channel.send("returning")
        else:
            await message.channel.send(f'[ERROR]: Invalid Response. Program Terminated. Please Try Again.')

        # If new -> find if they are really new -> ask to create a new user -> or just find old user -> or leave or see if they want to play a game
        # if returning -> 1. check stats 2. start playing 3. delete user 4. add money 5. show who has the most money 6. exit
        # leave

    except asyncio.TimeoutError:
        return message.channel.send(f'{message.author.mention} has taken too long to respond.')


def create_player(message : discord.message.Message, client : discord.Client, player_dictionary : dict):
    discord_name = message.author.mention
    discord_name_cleaned = discord_name.replace('<', '').replace('>', '').replace('@', '')

    name = message.author.name

    current_date = str(datetime.datetime.now().date())
    current_time = str(datetime.datetime.now().time())
    date = f'{current_date}T{current_time}'    
    statistics = []
    activity = f'{date} - Created Account on {current_date}'
    statistics.append(activity)

    newPlayer = Player(name, discord_name_cleaned, 500, 0, statistics, activity, date)
    player_dictionary[discord_name_cleaned] = newPlayer

def delete_player(dictionary: dict, discord_name : str):
    #if in dictionary return true and delete user and say name deleted
    if discord_name in dictionary:
        del dictionary[discord_name]
        return True
    # else return false and say not found
    else:
        return False


def read_players_from_file(directory):
    dictionary = {}
    for filename in os.listdir(directory):
        if filename.endswith(".json"):
            file_path = os.path.join(directory, filename)
            with open(file_path, 'r') as json_file:
                data = json.load(json_file)
                discord_name = data.get('discord_name')
                if discord_name:
                    player = Player(
                        name=data.get('name'),
                        discord_name=data.get('discord_name'),
                        total_earnings=data.get('total_earnings'),
                        balance=data.get('balance'),
                        statistics=data.get('statistics'),
                        last_activity=data.get('last_activity'),
                        date_created=data.get('date_created')
                    )
                    dictionary[discord_name] = player
                else:
                    print(f"Discord name not found in file: {filename}")
    return dictionary

def find_player(dictionary : dict, discord_name : str):
    discord_name_cleaned = discord_name.replace('<', '').replace('>', '').replace('@', '')
    print("Dictionary:", dictionary)
    print("Discord Name:", discord_name_cleaned)
    if discord_name_cleaned in dictionary:
        return True
    else:
        return False

async def play_game(message : discord.message.Message, client : discord.Client, player_dictionary : dict):
    # shows a menu and loops when the game is finished
    # return NotImplementedError()
    await message.channel.send(f'{message.author.mention} playing game.')
    print(player_dictionary)


async def show_leaderboard():
    # show by level and by total earnings
    return NotImplementedError()