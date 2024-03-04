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
from card import Card, Deck, Hand

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
            # await message.channel.send(f'{response.author.mention} has exited.')
            exit_string = f'{response.author.mention} has exited.'
            exit_embed = discord.Embed(description=exit_string, color=0x50C878)
            file = discord.File('images/icon.png', filename='icon.png')
            exit_embed.set_thumbnail(url='attachment://icon.png')
            exit_embed.set_author(name="Gambling-Bot says:")
            exit_embed.set_footer(text="!exit")
            await message.channel.send(file=file, embed=exit_embed)
            con = False
        else:
            # await message.channel.send(f'[ERROR]: Invalid Response. Program Terminated. Please Try Again.')
            string = f'[ERROR]: Invalid Response. Program Terminated. Please Try Again.'
            embed = discord.Embed(title=string, color=0x50C878)
            file = discord.File('images/icon.png', filename='icon.png')
            embed.set_thumbnail(url='attachment://icon.png')
            embed.set_author(name="Gambling-Bot says:")
            embed.set_footer(text="!game")
            await message.channel.send(file=file, embed=embed)
            con = False

async def gambling_menu(message : discord.message.Message):
    # await message.channel.send(f'''Please choose a game:
    # **!dice** - Players roll a six-sided die to generate a random number. Wagers double if they get a higher number than the dealer.
    # **!coinflip** - Players will guess where the coin will land. Wagers double if they guess the correct 
    # **!blackjack** - Players aim to get as close to 21 as possible without going over, competing against a dealer.
    # **!roulette** - Players bet on where a ball will land on a spinning wheel, with various betting options available.
    # **!slots** - Players spin reels to match symbols and win credits or bonuses.
    # **!guess** - Players try to guess a number within a specified range, receiving hints if needed, until they guess correctly.
    # **!exit** - Exits gambling page.
    # ''')
    menu_title = 'Please choose a game:'
    # menu_string = f'''**!dice** - Players roll a six-sided die to generate a random number. Wagers double if they get a higher number than the dealer.
    # **!coinflip** - Players will guess where the coin will land. Wagers double if they guess the correct 
    # **!blackjack** - Players aim to get as close to 21 as possible without going over, competing against a dealer.
    # **!roulette** - Players bet on where a ball will land on a spinning wheel, with various betting options available.
    # **!slots** - Players spin reels to match symbols and win credits or bonuses.
    # **!guess** - Players try to guess a number within a specified range, receiving hints if needed, until they guess correctly.
    # **!exit** - Exits gambling page.
    # '''
    embed = discord.Embed(title=menu_title, description= '\n', color=0x50C878)
    file = discord.File('images/icon.png', filename='icon.png')
    embed.set_thumbnail(url='attachment://icon.png')
    embed.set_author(name="Gambling-Bot says:")
    embed.add_field(name="**!dice**", value="Players roll a six-sided die to generate a random number. Wagers double if they get a higher number than the dealer.", inline= False)
    embed.add_field(name="**!coinflip**", value="Players will guess where the coin will land. Wagers double if they guess the correct ", inline= False)
    embed.add_field(name="**!blackjack**", value="Players aim to get as close to 21 as possible without going over, competing against a dealer.", inline= False)
    embed.add_field(name="**!roulette**", value="Players bet on where a ball will land on a spinning wheel, with various betting options available.", inline= False)
    embed.add_field(name="**!slots**", value="Players spin reels to match symbols and win credits or bonuses.", inline= False)
    embed.add_field(name="**!guess**", value="Players try to guess a number within a specified range, receiving hints if needed, until they guess correctly.", inline= False)
    embed.add_field(name="**!exit**", value="Exits gambling page.", inline= False)
    embed.set_footer(text="!game")
    await message.channel.send(file=file, embed=embed)

# DICE
async def dice(message : discord.message.Message, client: discord.Client, user_db : UserDatabase):
    def check(m):
        return m.author == message.author and m.channel == message.channel
    # await message.channel.send("How much are you wagering?")
    string = f"How much are you wagering?"
    embed = discord.Embed(title=string, color=0x50C878)
    file = discord.File('images/icon.png', filename='icon.png')
    embed.set_thumbnail(url='attachment://icon.png')
    embed.set_author(name="Gambling-Bot says:")
    embed.set_footer(text="!dice")
    await message.channel.send(file=file, embed=embed)
    response = await client.wait_for('message', check=check, timeout=30)
    discord_name = response.author.mention
    discord_name_cleaned = discord_name.replace('<', '').replace('>', '').replace('@', '')
    originalBalance = user_db.get_balance(discord_name_cleaned)
    if response.content.isdigit() and int(response.content) <= originalBalance:
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
                # await message.channel.send(f'{discord_name} won ${wage} defeating the dealer {user_total} to {dealer_total}')
                string = f'{discord_name} won ${wage} defeating the dealer {user_total} to {dealer_total}'
                embed = discord.Embed(description=string, color=0x50C878)
                file = discord.File('images/icon.png', filename='icon.png')
                embed.set_thumbnail(url='attachment://icon.png')
                embed.set_author(name="Gambling-Bot says:")
                embed.set_footer(text="!dice")
                await message.channel.send(file=file, embed=embed)
            elif user_total < dealer_total:
                user_db.update_balance(discord_name_cleaned, -wage)
                current_date = str(datetime.datetime.now().date())
                current_time = str(datetime.datetime.now().time())
                date = f'{current_date}T{current_time}'
                activity = f'{date} - Lost ${wage} playing dice on {current_date}'
                user_db.add_user_activity(discord_name_cleaned, activity, f'{current_date}')
                user_db.update_last_activity(discord_name_cleaned, activity)
                # await message.channel.send(f'{discord_name} lost ${wage} losing the dealer {user_total} to {dealer_total}')
                string = f'{discord_name} lost ${wage} losing the dealer {user_total} to {dealer_total}'
                embed = discord.Embed(description=string, color=0x50C878)
                file = discord.File('images/icon.png', filename='icon.png')
                embed.set_thumbnail(url='attachment://icon.png')
                embed.set_author(name="Gambling-Bot says:")
                embed.set_footer(text="!dice")
                await message.channel.send(file=file, embed=embed)
            elif user_total == dealer_total:
                # do not change any money
                # update transactions and change latest history
                current_date = str(datetime.datetime.now().date())
                current_time = str(datetime.datetime.now().time())
                date = f'{current_date}T{current_time}'
                activity = f'{date} - Drew ${wage} playing dice on {current_date}'
                user_db.add_user_activity(discord_name_cleaned, activity, f'{current_date}')
                user_db.update_last_activity(discord_name_cleaned, activity)
                # await message.channel.send(f'{discord_name} drew the dealer {user_total} to {dealer_total}')
                string = f'{discord_name} drew the dealer {user_total} to {dealer_total}'
                embed = discord.Embed(description=string, color=0x50C878)
                file = discord.File('images/icon.png', filename='icon.png')
                embed.set_thumbnail(url='attachment://icon.png')
                embed.set_author(name="Gambling-Bot says:")
                embed.set_footer(text="!dice")
                await message.channel.send(file=file, embed=embed)
            
        else:
            # await message.channel.send("[ERROR]: Inavlid Input. Program Terminated. Please Try Again.")
            string = f'[ERROR]: Invalid Input. Program Terminated. Please Try Again.'
            embed = discord.Embed(title=string, color=0x50C878)
            file = discord.File('images/icon.png', filename='icon.png')
            embed.set_thumbnail(url='attachment://icon.png')
            embed.set_author(name="Gambling-Bot says:")
            embed.set_footer(text="!dice")
            await message.channel.send(file=file, embed=embed)
    else:
        # await message.channel.send("[ERROR]: Inavlid Input. Program Terminated. Please Try Again.")
        string = f'[ERROR]: Wager is larger than current balance. Program Terminated. Please Try Again.'
        embed = discord.Embed(title=string, color=0x50C878)
        file = discord.File('images/icon.png', filename='icon.png')
        embed.set_thumbnail(url='attachment://icon.png')
        embed.set_author(name="Gambling-Bot says:")
        embed.set_footer(text="!dice")
        await message.channel.send(file=file, embed=embed)

# COIN FLIP
async def coinflip(message : discord.message.Message, client: discord.Client, user_db : UserDatabase):
    def check(m):
        return m.author == message.author and m.channel == message.channel
    # await message.channel.send("How much are you wagering?")
    string = f"How much are you wagering?"
    embed = discord.Embed(title=string, color=0x50C878)
    file = discord.File('images/icon.png', filename='icon.png')
    embed.set_thumbnail(url='attachment://icon.png')
    embed.set_author(name="Gambling-Bot says:")
    embed.set_footer(text="!coinflip")    
    await message.channel.send(file=file, embed=embed)
    response = await client.wait_for('message', check=check, timeout=30)
    discord_name = response.author.mention
    discord_name_cleaned = discord_name.replace('<', '').replace('>', '').replace('@', '')
    originalBalance = user_db.get_balance(discord_name_cleaned)
    if response.content.isdigit() and int(response.content) <= originalBalance:
        wage = int(response.content)
        # await message.channel.send("What is your prediction? (heads | tails)")
        string = "What is your prediction? (heads | tails)"
        embed = discord.Embed(title=string, color=0x50C878)
        file = discord.File('images/icon.png', filename='icon.png')
        embed.set_thumbnail(url='attachment://icon.png')
        embed.set_author(name="Gambling-Bot says:")
        embed.set_footer(text="!coinflip")
        await message.channel.send(file=file, embed=embed)
        coin = ['heads', 'tails']
        prediction = random.randint(0, 1)
        result = coin[prediction]
        response = await client.wait_for('message', check=check, timeout=30)
        if response.content.lower() == result and response.content.lower() in coin:
            user_db.update_balance(discord_name_cleaned, wage)
            current_date = str(datetime.datetime.now().date())
            current_time = str(datetime.datetime.now().time())
            date = f'{current_date}T{current_time}'
            activity = f'{date} - Won ${wage} playing coin flip on {current_date}'
            user_db.add_user_activity(discord_name_cleaned, activity, f'{current_date}')
            user_db.update_last_activity(discord_name_cleaned, activity)
            user_db.update_total_earnings(discord_name_cleaned, wage)
            # await message.channel.send(f'{discord_name} won ${wage} guessing {result} in coins')
            string = f'{discord_name} won ${wage} guessing {result} in coins'
            embed = discord.Embed(description=string, color=0x50C878)
            file = discord.File('images/icon.png', filename='icon.png')
            embed.set_thumbnail(url='attachment://icon.png')
            embed.set_author(name="Gambling-Bot says:")
            embed.set_footer(text="!coinflip")
            await message.channel.send(file=file, embed=embed)
        elif response.content.lower() != result and response.content.lower() in coin:
            user_db.update_balance(discord_name_cleaned, -wage)
            current_date = str(datetime.datetime.now().date())
            current_time = str(datetime.datetime.now().time())
            date = f'{current_date}T{current_time}'
            activity = f'{date} - Lost ${wage} playing coin flip on {current_date}'
            user_db.add_user_activity(discord_name_cleaned, activity, f'{current_date}')
            user_db.update_last_activity(discord_name_cleaned, activity)
            # await message.channel.send(f'{discord_name} lost ${wage} guessing {result} in coins')
            string = f'{discord_name} lost ${wage} guessing {result} in coins'
            embed = discord.Embed(description=string, color=0x50C878)
            file = discord.File('images/icon.png', filename='icon.png')
            embed.set_thumbnail(url='attachment://icon.png')
            embed.set_author(name="Gambling-Bot says:")
            embed.set_footer(text="!coinflip")
            await message.channel.send(file=file, embed=embed)
        else:
            # await message.channel.send("[ERROR]: Inavlid Input. Program Terminated. Please Try Again.")
            string = f'[ERROR]: Invalid Input. Program Terminated. Please Try Again.'
            embed = discord.Embed(title=string, color=0x50C878)
            file = discord.File('images/icon.png', filename='icon.png')
            embed.set_thumbnail(url='attachment://icon.png')
            embed.set_author(name="Gambling-Bot says:")
            embed.set_footer(text="!coinfip")
            await message.channel.send(file=file, embed=embed)
    else:
        string = f'[ERROR]: Wager is larger than current balance. Program Terminated. Please Try Again.'
        embed = discord.Embed(title=string, color=0x50C878)
        file = discord.File('images/icon.png', filename='icon.png')
        embed.set_thumbnail(url='attachment://icon.png')
        embed.set_author(name="Gambling-Bot says:")
        embed.set_footer(text="!coinfip")
        await message.channel.send(file=file, embed=embed)

# BLACKJACK
async def blackjack(message : discord.message.Message, client: discord.Client, user_db : UserDatabase):
    def check(m):
        return m.author == message.author and m.channel == message.channel
    # await message.channel.send("Enter number of decks to use (1, 2, 6, or 8): ")
    string = "Enter number of decks to use (1, 2, 6, or 8): "
    embed = discord.Embed(title=string, color=0x50C878)
    file = discord.File('images/icon.png', filename='icon.png')
    embed.set_thumbnail(url='attachment://icon.png')
    embed.set_author(name="Gambling-Bot says:")
    embed.set_footer(text="!blackjack")
    await message.channel.send(file=file, embed=embed)
    num_decks = await client.wait_for('message', check=check, timeout=30)
    num_decks_number = int(num_decks.content)
    if num_decks_number not in [1, 2, 6, 8]:
        # await message.channel.send("Invalid number of decks. Please choose 1, 2, 6, or 8.")
        string = "Invalid number of decks. Please choose 1, 2, 6, or 8."
        embed = discord.Embed(title=string, color=0x50C878)
        file = discord.File('images/icon.png', filename='icon.png')
        embed.set_thumbnail(url='attachment://icon.png')
        embed.set_author(name="Gambling-Bot says:")
        embed.set_footer(text="!blackjack")
        await message.channel.send(file=file, embed=embed)
        return
    deck = Deck(num_decks_number)
    con = True
    
    discord_name = message.author.mention
    discord_name_cleaned = discord_name.replace('<', '').replace('>', '').replace('@', '')
    originalBalance = user_db.get_balance(discord_name_cleaned)
    newBalance = user_db.get_balance(discord_name_cleaned)
    wage = 0
    while con:
        # await message.channel.send("How much are you wagering?")
        string = f"Pick an option:"
        embed = discord.Embed(title=string, color=0x50C878)
        file = discord.File('images/icon.png', filename='icon.png')
        embed.set_thumbnail(url='attachment://icon.png')
        embed.set_author(name="Gambling-Bot says:")
        embed.add_field(name="!exit", value='Exits blackjack page.')
        embed.add_field(name='!continue', value='Continues blackjack game.')
        embed.set_footer(text="!blackjack")    
        await message.channel.send(file=file, embed=embed)
        response = await client.wait_for('message', check=check, timeout=30)
        if response.content == '!exit':
            # await message.channel.send(f'{response.author.mention} has exited.')
            exit_string = f'{response.author.mention} has exited.'
            exit_embed = discord.Embed(description=exit_string, color=0x50C878)
            file = discord.File('images/icon.png', filename='icon.png')
            exit_embed.set_thumbnail(url='attachment://icon.png')
            exit_embed.set_author(name="Gambling-Bot says:")
            exit_embed.set_footer(text="!exit")
            await message.channel.send(file=file, embed=exit_embed)
            break
        string = f"How much are you wagering?"
        embed = discord.Embed(title=string, color=0x50C878)
        file = discord.File('images/icon.png', filename='icon.png')
        embed.set_thumbnail(url='attachment://icon.png')
        embed.set_author(name="Gambling-Bot says:")
        embed.set_footer(text="!blackjack")    
        await message.channel.send(file=file, embed=embed)
        response = await client.wait_for('message', check=check, timeout=30)
        if response.content.isdigit() and int(response.content) <= newBalance:
            wage = int(response.content)
            deck.shuffle()
            player_hand = Hand()
            dealer_hand = Hand()

            player_hand.add_card(deck.deal_card())
            player_hand.add_card(deck.deal_card())

            dealer_hand.add_card(deck.deal_card())
            dealer_hand.add_card(deck.deal_card())
            # await message.channel.send(f'''Dealer's Hand
            # One Card Faced Down
            # {dealer_hand.cards[1]}
            # Your Hand:
            # {player_hand}
            # ''')
            string = f'''Dealer's Hand\nOne Card Faced Down\n{dealer_hand.cards[1]}\n\nYour Hand:\n{player_hand}'''
            embed = discord.Embed(title=string, color=0x50C878)
            file = discord.File('images/icon.png', filename='icon.png')
            embed.set_thumbnail(url='attachment://icon.png')
            embed.set_author(name="Gambling-Bot says:")
            embed.set_footer(text="!blackjack")    
            await message.channel.send(file=file, embed=embed)
            while player_hand.value < 21:
                # await message.channel.send("Do you want to (h)it or (s)tand? ")
                string = 'Do you want to:'
                embed = discord.Embed(title=string, color=0x50C878)
                file = discord.File('images/icon.png', filename='icon.png')
                embed.set_thumbnail(url='attachment://icon.png')
                embed.set_author(name="Gambling-Bot says:")
                embed.add_field(name="**hit**", inline=False)
                embed.add_field(name="**stand**", inline=False)
                embed.set_footer(text="!blackjack")    
                await message.channel.send(file=file, embed=embed)
                action = await client.wait_for('message', check=check, timeout=30)
                action_event = action.content
                if action_event == 'hit':
                    player_hand.add_card(deck.deal_card())
                    # await message.channel.send("\nYour Hand:")
                    # await message.channel.send(player_hand)
                    string = 'Your Hand:\n {player_hand}'
                    embed = discord.Embed(title=string, color=0x50C878)
                    file = discord.File('images/icon.png', filename='icon.png')
                    embed.set_thumbnail(url='attachment://icon.png')
                    embed.set_author(name="Gambling-Bot says:")
                    embed.set_footer(text="!blackjack")    
                    await message.channel.send(file=file, embed=embed)
                elif action_event == 'stand':
                    break

            if player_hand.value > 21:
                # await message.channel.send("You bust! Dealer wins.")
                embed = discord.Embed(title="You bust! Dealer wins.", color=0x50C878)
                file = discord.File('images/icon.png', filename='icon.png')
                embed.set_thumbnail(url='attachment://icon.png')
                embed.set_author(name="Gambling-Bot says:")
                embed.set_footer(text="!blackjack")    
                await message.channel.send(file=file, embed=embed)
                deck.add_used_cards(player_hand.cards + dealer_hand.cards)
                continue

            # await message.channel.send(f'''Dealer's Hand:
            # {dealer_hand}
            # ''')
            string = f'''Dealer's Hand:\n{dealer_hand}'''
            embed = discord.Embed(description= string, color=0x50C878)
            file = discord.File('images/icon.png', filename='icon.png')
            embed.set_thumbnail(url='attachment://icon.png')
            embed.set_author(name="Gambling-Bot says:")
            embed.set_footer(text="!blackjack")    
            await message.channel.send(file=file, embed=embed)
            deck.add_used_cards(player_hand.cards + dealer_hand.cards)
            while dealer_hand.value < 17:
                dealer_hand.add_card(deck.deal_card())
                await message.channel.send(dealer_hand)

            if dealer_hand.value > 21 or dealer_hand.value < player_hand.value:
                # await message.channel.send("You win!")
                embed = discord.Embed(title= "You win!", color=0x50C878)
                file = discord.File('images/icon.png', filename='icon.png')
                embed.set_thumbnail(url='attachment://icon.png')
                embed.set_author(name="Gambling-Bot says:")
                embed.set_footer(text="!blackjack")    
                await message.channel.send(file=file, embed=embed)
                user_db.update_total_earnings(discord_name_cleaned, wage)
                newBalance += wage
            elif dealer_hand.value == player_hand.value:
                # await message.channel.send("It's a tie!")
                embed = discord.Embed(title= "It's a tie!", color=0x50C878)
                file = discord.File('images/icon.png', filename='icon.png')
                embed.set_thumbnail(url='attachment://icon.png')
                embed.set_author(name="Gambling-Bot says:")
                embed.set_footer(text="!blackjack")    
                await message.channel.send(file=file, embed=embed)
            else:
                # await message.channel.send("Dealer wins.")
                embed = discord.Embed(title= "Dealer wins.", color=0x50C878)
                file = discord.File('images/icon.png', filename='icon.png')
                embed.set_thumbnail(url='attachment://icon.png')
                embed.set_author(name="Gambling-Bot says:")
                embed.set_footer(text="!blackjack")    
                await message.channel.send(file=file, embed=embed)
                newBalance -= wage
        else:
            # await message.channel.send("[ERROR]: Wager over current balance. Program Terminated. Please Try Again.")
            embed = discord.Embed(title= "[ERROR]: Wager over current balance. Program Terminated. Please Try Again.", color=0x50C878)
            file = discord.File('images/icon.png', filename='icon.png')
            embed.set_thumbnail(url='attachment://icon.png')
            embed.set_author(name="Gambling-Bot says:")
            embed.set_footer(text="!blackjack")    
            await message.channel.send(file=file, embed=embed)
            con = False
        
        deck.add_used_cards(player_hand.cards + dealer_hand.cards)
    difference = newBalance - originalBalance
    if difference >= originalBalance and wage != 0:
        user_db.update_balance(discord_name_cleaned, wage)
        current_date = str(datetime.datetime.now().date())
        current_time = str(datetime.datetime.now().time())
        date = f'{current_date}T{current_time}'
        activity = f'{date} - Won ${wage} playing blackjack on {current_date}'
        user_db.add_user_activity(discord_name_cleaned, activity, f'{current_date}')
        user_db.update_last_activity(discord_name_cleaned, activity)
        # await message.channel.send(f'{discord_name} won ${difference} in blackjack')
        string = f'{discord_name} won ${difference} in blackjack'
        embed = discord.Embed(description=string, color=0x50C878)
        file = discord.File('images/icon.png', filename='icon.png')
        embed.set_thumbnail(url='attachment://icon.png')
        embed.set_author(name="Gambling-Bot says:")
        embed.set_footer(text="!blackjack")    
        await message.channel.send(file=file, embed=embed)
    else:
        user_db.update_balance(discord_name_cleaned, -wage)
        current_date = str(datetime.datetime.now().date())
        current_time = str(datetime.datetime.now().time())
        date = f'{current_date}T{current_time}'
        activity = f'{date} - Lost ${wage} playing blackjack on {current_date}'
        user_db.add_user_activity(discord_name_cleaned, activity, f'{current_date}')
        user_db.update_last_activity(discord_name_cleaned, activity)
        # await message.channel.send(f'{discord_name} lost ${difference} in blackjack')
        string = f'{discord_name} lost ${difference} in blackjack'
        embed = discord.Embed(description=string, color=0x50C878)
        file = discord.File('images/icon.png', filename='icon.png')
        embed.set_thumbnail(url='attachment://icon.png')
        embed.set_author(name="Gambling-Bot says:")
        embed.set_footer(text="!blackjack")    
        await message.channel.send(file=file, embed=embed)

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
    originalBalance = user_db.get_balance(discord_name_cleaned)
    bet_list = []
    error = False
    while con and not error:        
        wage = 0
        # await message.channel.send(f'''
        # Where do you want to wager?
        # !number - bet on a number
        # !color - bet on red or black
        # !parity - bet on even or odd
        # !column - to bet on what column the number is. i.e., number 24 is on row 3
        # !row - to bet on what row the number is. i.e., number 24 is on row 8
        # !group - to bet either on 1-12 or 13-24 or 25-36
        # !range - to bet on a number from 1-18 or 19-36
        # !endbets - to complete betting wagers
        # ''')
        string = "Where do you want to wager?"
        embed = discord.Embed(title=string, color=0x50C878)
        file = discord.File('images/icon.png', filename='icon.png')
        embed.set_thumbnail(url='attachment://icon.png')
        embed.set_author(name="Gambling-Bot says:")
        embed.add_field(name="!number", value="bet on a number", inline=False)
        embed.add_field(name="!color", value="bet on red or black", inline=False)
        embed.add_field(name="!parity", value="bet on even or odd", inline=False)
        embed.add_field(name="!column", value="to bet on what column the number is. i.e., number 24 is on row 3", inline=False)
        embed.add_field(name="!row", value="to bet on what row the number is. i.e., number 24 is on row 8", inline=False)
        embed.add_field(name="!group", value="to bet either on 1-12 or 13-24 or 25-36", inline=False)
        embed.add_field(name="!range", value="to bet on a number from 1-18 or 19-36", inline=False)
        embed.add_field(name="!endbets", value="to complete betting wagers", inline=False)
        embed.set_footer(text="!roulette")    
        await message.channel.send(file=file, embed=embed)
        response_where = await client.wait_for('message', check=check, timeout=30)
        response_where_content = response_where.content
        if response_where_content == '!number':
            # await message.channel.send("What number do you want to wager on?")
            string = "What number do you want to wager on?"
            embed = discord.Embed(title=string, color=0x50C878)
            file = discord.File('images/icon.png', filename='icon.png')
            embed.set_thumbnail(url='attachment://icon.png')
            embed.set_author(name="Gambling-Bot says:")
            embed.set_footer(text="!roulette")    
            await message.channel.send(file=file, embed=embed)
            response_event = await client.wait_for('message', check=check, timeout=30)
            number = ''
            if response_event.content.isdigit():
                number = int(response_event.content)
                if number < -1 and number > 37:
                    # await message.channel.send("[ERROR]: Number has to be between 0 - 36. Program Terminated. Please Try Again.")
                    string = "[ERROR]: Number has to be between 0 - 36. Program Terminated. Please Try Again."
                    embed = discord.Embed(title=string, color=0x50C878)
                    file = discord.File('images/icon.png', filename='icon.png')
                    embed.set_thumbnail(url='attachment://icon.png')
                    embed.set_author(name="Gambling-Bot says:")
                    embed.set_footer(text="!roulette")    
                    await message.channel.send(file=file, embed=embed)
                    error = True
            else:
                # await message.channel.send("[ERROR]: Inavlid Input. Program Terminated. Please Try Again.")
                string = "[ERROR]: Inavlid Input. Program Terminated. Please Try Again."
                embed = discord.Embed(title=string, color=0x50C878)
                file = discord.File('images/icon.png', filename='icon.png')
                embed.set_thumbnail(url='attachment://icon.png')
                embed.set_author(name="Gambling-Bot says:")
                embed.set_footer(text="!roulette")    
                await message.channel.send(file=file, embed=embed)
                error = True
            # await message.channel.send(f"How much are you wagering for {number}?")
            string = f"How much are you wagering for {number}?"
            embed = discord.Embed(title=string, color=0x50C878)
            file = discord.File('images/icon.png', filename='icon.png')
            embed.set_thumbnail(url='attachment://icon.png')
            embed.set_author(name="Gambling-Bot says:")
            embed.set_footer(text="!roulette")    
            await message.channel.send(file=file, embed=embed)
            response_wage = await client.wait_for('message', check=check, timeout=30)
            if response_wage.content.isdigit():
                wage += int(response_wage.content)
                if wage + total_bet > originalBalance:
                    # await message.channel.send("[ERROR]: Total bet over player's balance. Program Terminated. Please Try Again.")
                    string = "[ERROR]: Total bet over player's balance. Program Terminated. Please Try Again."
                    embed = discord.Embed(title=string, color=0x50C878)
                    file = discord.File('images/icon.png', filename='icon.png')
                    embed.set_thumbnail(url='attachment://icon.png')
                    embed.set_author(name="Gambling-Bot says:")
                    embed.set_footer(text="!roulette")    
                    await message.channel.send(file=file, embed=embed)
                    error = True
                else:
                    total_bet += wage
                    single_payout  = 35
                    bet = (response_where_content, number, wage, single_payout)
                    bet_list.append(bet)
        elif response_where_content == '!color':
            # await message.channel.send("What color do you want to wager on? (red | black)")
            string = "What color do you want to wager on? (red | black)"
            embed = discord.Embed(title=string, color=0x50C878)
            file = discord.File('images/icon.png', filename='icon.png')
            embed.set_thumbnail(url='attachment://icon.png')
            embed.set_author(name="Gambling-Bot says:")
            embed.add_field(name="red", value="", inline=False)
            embed.add_field(name="black", value="", inline=False)
            embed.set_footer(text="!roulette")    
            await message.channel.send(file=file, embed=embed)
            response_event = await client.wait_for('message', check=check, timeout=30)
            color = ''
            if response_event.content == 'red':
                color = 'red'
            elif response_event.content == 'black':
                color = 'black'
            else:
                # await message.channel.send("[ERROR]: Inavlid Input. Program Terminated. Please Try Again.")
                string = "[ERROR]: Inavlid Input. Program Terminated. Please Try Again."
                embed = discord.Embed(title=string, color=0x50C878)
                file = discord.File('images/icon.png', filename='icon.png')
                embed.set_thumbnail(url='attachment://icon.png')
                embed.set_author(name="Gambling-Bot says:")
                embed.set_footer(text="!roulette")    
                await message.channel.send(file=file, embed=embed)
                error = True
            # await message.channel.send(f"How much are you wagering for {color}?")
            string = f"How much are you wagering for {color}?"
            embed = discord.Embed(title=string, color=0x50C878)
            file = discord.File('images/icon.png', filename='icon.png')
            embed.set_thumbnail(url='attachment://icon.png')
            embed.set_author(name="Gambling-Bot says:")
            embed.set_footer(text="!roulette")    
            await message.channel.send(file=file, embed=embed)
            response_wage = await client.wait_for('message', check=check, timeout=30)
            if response_wage.content.isdigit():
                wage += int(response_wage.content)
                if wage + total_bet > originalBalance:
                    # await message.channel.send("[ERROR]: Total bet over player's balance. Program Terminated. Please Try Again.")
                    string = "[ERROR]: Total bet over player's balance. Program Terminated. Please Try Again."
                    embed = discord.Embed(title=string, color=0x50C878)
                    file = discord.File('images/icon.png', filename='icon.png')
                    embed.set_thumbnail(url='attachment://icon.png')
                    embed.set_author(name="Gambling-Bot says:")
                    embed.set_footer(text="!roulette")    
                    await message.channel.send(file=file, embed=embed)
                    error = True
                else:
                    total_bet += wage
                    color_payout  = 1
                    bet = (response_where_content, color, wage, color_payout)
                    bet_list.append(bet)                    
        elif response_where_content == '!parity':
            # await message.channel.send("What parity do you want to wager on? (even | odd)")
            string = "What parity do you want to wager on? (even | odd)"
            embed = discord.Embed(title=string, color=0x50C878)
            file = discord.File('images/icon.png', filename='icon.png')
            embed.set_thumbnail(url='attachment://icon.png')
            embed.set_author(name="Gambling-Bot says:")
            embed.add_field(name="even", value="", inline=False)
            embed.add_field(name="odd", value="", inline=False)
            embed.set_footer(text="!roulette")    
            await message.channel.send(file=file, embed=embed)
            response_event = await client.wait_for('message', check=check, timeout=30)
            parity = ''
            if response_event.content == 'odd':
                parity = 'odd'
            elif response_event.content == 'even':
                parity = 'even'
            else:
                # await message.channel.send("[ERROR]: Inavlid Input. Program Terminated. Please Try Again.")
                string = "[ERROR]: Inavlid Input. Program Terminated. Please Try Again."
                embed = discord.Embed(title=string, color=0x50C878)
                file = discord.File('images/icon.png', filename='icon.png')
                embed.set_thumbnail(url='attachment://icon.png')
                embed.set_author(name="Gambling-Bot says:")
                embed.set_footer(text="!roulette")    
                await message.channel.send(file=file, embed=embed)
                error = True
            # await message.channel.send(f"How much are you wagering for {parity}?")
            string = f"How much are you wagering for {parity}?"
            embed = discord.Embed(title=string, color=0x50C878)
            file = discord.File('images/icon.png', filename='icon.png')
            embed.set_thumbnail(url='attachment://icon.png')
            embed.set_author(name="Gambling-Bot says:")
            embed.set_footer(text="!roulette")    
            await message.channel.send(file=file, embed=embed)
            response_wage = await client.wait_for('message', check=check, timeout=30)
            if response_wage.content.isdigit():
                wage += int(response_wage.content)
                if wage + total_bet > originalBalance:
                    # await message.channel.send("[ERROR]: Total bet over player's balance. Program Terminated. Please Try Again.")
                    string = "[ERROR]: Total bet over player's balance. Program Terminated. Please Try Again."
                    embed = discord.Embed(title=string, color=0x50C878)
                    file = discord.File('images/icon.png', filename='icon.png')
                    embed.set_thumbnail(url='attachment://icon.png')
                    embed.set_author(name="Gambling-Bot says:")
                    embed.set_footer(text="!roulette")    
                    await message.channel.send(file=file, embed=embed)
                    error = True
                else:
                    total_bet += wage
                    even_payout = 1
                    bet = (response_where_content, parity, wage, even_payout)
                    bet_list.append(bet)
        elif response_where_content == '!column':
            # await message.channel.send("What column do you want to wager on? (1st | 2nd | 3rd)")
            string = "What column do you want to wager on?"
            embed = discord.Embed(title=string, color=0x50C878)
            file = discord.File('images/icon.png', filename='icon.png')
            embed.set_thumbnail(url='attachment://icon.png')
            embed.set_author(name="Gambling-Bot says:")
            embed.add_field(name="1st", value="", inline=False)
            embed.add_field(name="2nd", value="", inline=False)
            embed.add_field(name="3rd", value="", inline=False)
            embed.set_footer(text="!roulette")    
            await message.channel.send(file=file, embed=embed)
            response_event = await client.wait_for('message', check=check, timeout=30)
            column = ''
            if response_event.content == '1st':
                column = '1st'
            elif response_event.content == '2nd':
                column = '2nd'
            elif response_event.content == '3rd':
                column = '3rd'
            else:
                # await message.channel.send("[ERROR]: Inavlid Input. Program Terminated. Please Try Again.")
                string = "[ERROR]: Inavlid Input. Program Terminated. Please Try Again."
                embed = discord.Embed(title=string, color=0x50C878)
                file = discord.File('images/icon.png', filename='icon.png')
                embed.set_thumbnail(url='attachment://icon.png')
                embed.set_author(name="Gambling-Bot says:")
                embed.set_footer(text="!roulette")    
                await message.channel.send(file=file, embed=embed)
                error = True
            # await message.channel.send(f'How much are you wagering for {column} column?')
            string = f'How much are you wagering for {column} column?'
            embed = discord.Embed(title=string, color=0x50C878)
            file = discord.File('images/icon.png', filename='icon.png')
            embed.set_thumbnail(url='attachment://icon.png')
            embed.set_author(name="Gambling-Bot says:")
            embed.set_footer(text="!roulette")    
            await message.channel.send(file=file, embed=embed)
            response_wage = await client.wait_for('message', check=check, timeout=30)
            if response_wage.content.isdigit():
                wage += int(response_wage.content)
                if wage + total_bet > originalBalance:
                    # await message.channel.send("[ERROR]: Total bet over player's balance. Program Terminated. Please Try Again.")
                    string = "[ERROR]: Total bet over player's balance. Program Terminated. Please Try Again."
                    embed = discord.Embed(title=string, color=0x50C878)
                    file = discord.File('images/icon.png', filename='icon.png')
                    embed.set_thumbnail(url='attachment://icon.png')
                    embed.set_author(name="Gambling-Bot says:")
                    embed.set_footer(text="!roulette")    
                    await message.channel.send(file=file, embed=embed)
                    error = True
                else:
                    total_bet += wage
                    column_payout = 2
                    bet = (response_where_content, column, wage, column_payout)
                    bet_list.append(bet)
        elif response_where_content == '!row':
            # await message.channel.send("What row do you want to wager on? (1st | 2nd | 3rd | 4th | 5th | 6th | 7th | 8th | 9th | 10th | 11th | 12th)")
            string = "What row do you want to wager on?"
            embed = discord.Embed(title=string, color=0x50C878)
            file = discord.File('images/icon.png', filename='icon.png')
            embed.set_thumbnail(url='attachment://icon.png')
            embed.set_author(name="Gambling-Bot says:")
            embed.add_field(name="1st", value="", inline=False)
            embed.add_field(name="2nd", value="", inline=False)
            embed.add_field(name="3rd", value="", inline=False)
            embed.add_field(name="4th", value="", inline=False)
            embed.add_field(name="5th", value="", inline=False)
            embed.add_field(name="6th", value="", inline=False)
            embed.add_field(name="7th", value="", inline=False)
            embed.add_field(name="8th", value="", inline=False)
            embed.add_field(name="9th", value="", inline=False)
            embed.add_field(name="10th", value="", inline=False)
            embed.add_field(name="11th", value="", inline=False)
            embed.add_field(name="12th", value="", inline=False)
            embed.set_footer(text="!blackjack")    
            await message.channel.send(file=file, embed=embed)
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
                # await message.channel.send("[ERROR]: Inavlid Input. Program Terminated. Please Try Again.")
                string = "[ERROR]: Total bet over player's balance. Program Terminated. Please Try Again."
                embed = discord.Embed(title=string, color=0x50C878)
                file = discord.File('images/icon.png', filename='icon.png')
                embed.set_thumbnail(url='attachment://icon.png')
                embed.set_author(name="Gambling-Bot says:")
                embed.set_footer(text="!roulette")    
                await message.channel.send(file=file, embed=embed)
                error = True
            # await message.channel.send(f'How much are you wagering for {row} column?')
            string = f'How much are you wagering for {row} column?'
            embed = discord.Embed(title=string, color=0x50C878)
            file = discord.File('images/icon.png', filename='icon.png')
            embed.set_thumbnail(url='attachment://icon.png')
            embed.set_author(name="Gambling-Bot says:")
            embed.set_footer(text="!roulette")    
            await message.channel.send(file=file, embed=embed)
            response_wage = await client.wait_for('message', check=check, timeout=30)
            if response_wage.content.isdigit():
                wage += int(response_wage.content)
                if wage + total_bet > originalBalance:
                    # await message.channel.send("[ERROR]: Total bet over player's balance. Program Terminated. Please Try Again.")
                    string = "[ERROR]: Total bet over player's balance. Program Terminated. Please Try Again."
                    embed = discord.Embed(title=string, color=0x50C878)
                    file = discord.File('images/icon.png', filename='icon.png')
                    embed.set_thumbnail(url='attachment://icon.png')
                    embed.set_author(name="Gambling-Bot says:")
                    embed.set_footer(text="!roulette")    
                    await message.channel.send(file=file, embed=embed)
                    error = True
                else:
                    total_bet += wage
                    street_payout  = 11
                    bet = (response_where_content, row, wage, street_payout)
                    bet_list.append(bet)
        elif response_where_content == '!group':
            # await message.channel.send("What group do you want to wager on? (1st 12 | 2nd 12 | 3rd 12)")
            string = "What group do you want to wager on? (1st 12 | 2nd 12 | 3rd 12)"
            embed = discord.Embed(title=string, color=0x50C878)
            file = discord.File('images/icon.png', filename='icon.png')
            embed.set_thumbnail(url='attachment://icon.png')
            embed.set_author(name="Gambling-Bot says:")
            embed.add_field(name="1st 12", value="", inline=False)
            embed.add_field(name="2nd 12", value="", inline=False)
            embed.add_field(name="3rd 12", value="", inline=False)
            embed.set_footer(text="!roulette")    
            await message.channel.send(file=file, embed=embed)
            response_event = await client.wait_for('message', check=check, timeout=30)
            group = ''
            if response_event.content == '1st 12':
                group = '1st 12'
            elif response_event.content == '2nd 12':
                group = '2nd 12'
            elif response_event.content == '3rd 12':
                group = '3rd 12'
            else:
                # await message.channel.send("[ERROR]: Inavlid Input. Program Terminated. Please Try Again.")
                string = "[ERROR]: Inavlid Input. Program Terminated. Please Try Again."
                embed = discord.Embed(title=string, color=0x50C878)
                file = discord.File('images/icon.png', filename='icon.png')
                embed.set_thumbnail(url='attachment://icon.png')
                embed.set_author(name="Gambling-Bot says:")
                embed.set_footer(text="!roulette")    
                await message.channel.send(file=file, embed=embed)
                error = True
            # await message.channel.send(f"How much are you wagering for {group}?")
            string = f"How much are you wagering for {group}?"
            embed = discord.Embed(title=string, color=0x50C878)
            file = discord.File('images/icon.png', filename='icon.png')
            embed.set_thumbnail(url='attachment://icon.png')
            embed.set_author(name="Gambling-Bot says:")
            embed.set_footer(text="!roulette")    
            await message.channel.send(file=file, embed=embed)
            response_wage = await client.wait_for('message', check=check, timeout=30)
            if response_wage.content.isdigit():
                wage += int(response_wage.content)
                if wage + total_bet > originalBalance:
                    # await message.channel.send("[ERROR]: Total bet over player's balance. Program Terminated. Please Try Again.")
                    string = "[ERROR]: Total bet over player's balance. Program Terminated. Please Try Again."
                    embed = discord.Embed(title=string, color=0x50C878)
                    file = discord.File('images/icon.png', filename='icon.png')
                    embed.set_thumbnail(url='attachment://icon.png')
                    embed.set_author(name="Gambling-Bot says:")
                    embed.set_footer(text="!roulette")    
                    await message.channel.send(file=file, embed=embed)
                    error = True
                else:
                    total_bet += wage
                    group_payout  = 2
                    bet = (response_where_content, group, wage, group_payout)
                    bet_list.append(bet)
        elif response_where_content == '!range':
            # await message.channel.send("What range do you want to wager on? (1 to 18 | 19 to 36)")
            string = "What range do you want to wager on? (1 to 18 | 19 to 36)"
            embed = discord.Embed(title=string, color=0x50C878)
            file = discord.File('images/icon.png', filename='icon.png')
            embed.set_thumbnail(url='attachment://icon.png')
            embed.set_author(name="Gambling-Bot says:")
            embed.add_field(name="1 to 18", value="", inline=False)
            embed.add_field(name="19 to 36", value="", inline=False)
            embed.set_footer(text="!roulette")    
            await message.channel.send(file=file, embed=embed)
            response_event = await client.wait_for('message', check=check, timeout=30)
            range_bet = ''
            if response_event.content == '1 to 18':
                range_bet = '1 to 18'
            elif response_event.content == '19 to 36':
                range_bet = '19 to 36'
            else:
                # await message.channel.send("[ERROR]: Inavlid Input. Program Terminated. Please Try Again.")
                string = "[ERROR]: Inavlid Input. Program Terminated. Please Try Again."
                embed = discord.Embed(title=string, color=0x50C878)
                file = discord.File('images/icon.png', filename='icon.png')
                embed.set_thumbnail(url='attachment://icon.png')
                embed.set_author(name="Gambling-Bot says:")
                embed.set_footer(text="!roulette")    
                await message.channel.send(file=file, embed=embed)
                error = True
            # await message.channel.send(f"How much are you wagering for {range_bet}?")
            string = f"How much are you wagering for {range_bet}?"
            embed = discord.Embed(title=string, color=0x50C878)
            file = discord.File('images/icon.png', filename='icon.png')
            embed.set_thumbnail(url='attachment://icon.png')
            embed.set_author(name="Gambling-Bot says:")
            embed.set_footer(text="!blackjack")    
            await message.channel.send(file=file, embed=embed)
            response_wage = await client.wait_for('message', check=check, timeout=30)
            if response_wage.content.isdigit():
                wage += int(response_wage.content)
                if wage + total_bet > originalBalance:
                    # await message.channel.send("[ERROR]: Total bet over player's balance. Program Terminated. Please Try Again.")
                    string = "[ERROR]: Total bet over player's balance. Program Terminated. Please Try Again."
                    embed = discord.Embed(title=string, color=0x50C878)
                    file = discord.File('images/icon.png', filename='icon.png')
                    embed.set_thumbnail(url='attachment://icon.png')
                    embed.set_author(name="Gambling-Bot says:")
                    embed.set_footer(text="!roulette")    
                    await message.channel.send(file=file, embed=embed)
                    error = True
                else:
                    total_bet += wage
                    range_payout = 1
                    bet = (response_where_content, range_bet, wage, range_payout)
                    bet_list.append(bet)
        elif response_where_content == '!endbets':
            con = False
            # await message.channel.send("No more bets.")
            string = "No more bets."
            embed = discord.Embed(title=string, color=0x50C878)
            file = discord.File('images/icon.png', filename='icon.png')
            embed.set_thumbnail(url='attachment://icon.png')
            embed.set_author(name="Gambling-Bot says:")
            embed.set_footer(text="!roulette")    
            await message.channel.send(file=file, embed=embed)
        else:
            con = False
            # await message.channel.send("[ERROR]: Total bet over player's balance. Program Terminated. Please Try Again.")
            string = "[ERROR]: Total bet over player's balance. Program Terminated. Please Try Again."
            embed = discord.Embed(title=string, color=0x50C878)
            file = discord.File('images/icon.png', filename='icon.png')
            embed.set_thumbnail(url='attachment://icon.png')
            embed.set_author(name="Gambling-Bot says:")
            embed.set_footer(text="!roulette")    
            await message.channel.send(file=file, embed=embed)
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
                if row == bet[1]:
                    total += bet[2] * bet[3]
                    user_db.update_total_earnings(discord_name_cleaned, total)
                    continue
                else:
                    total -= bet[2]            
            elif command == '!column':
                if column == bet[1]:
                    total += bet[2] * bet[3]
                    user_db.update_total_earnings(discord_name_cleaned, total)
                    continue
                else:
                    total -= bet[2]
                    
            elif command == '!group':
                if group == bet[1]:
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
                if number_range == bet[1]:
                    total += bet[2] * bet[3]
                    user_db.update_total_earnings(discord_name_cleaned, total)
                    continue
                else:
                    total -= bet[2]
            elif command == '!parity':
                if parity == bet[1]:
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
            # await message.channel.send(f'{discord_name} won ${total} playing roulette.')            
            string = f'{discord_name} won ${total} playing roulette.'
            embed = discord.Embed(description=string, color=0x50C878)
            file = discord.File('images/icon.png', filename='icon.png')
            embed.set_thumbnail(url='attachment://icon.png')
            embed.set_author(name="Gambling-Bot says:")
            embed.set_footer(text="!roulette")    
            await message.channel.send(file=file, embed=embed)
        else:
            user_db.update_balance(discord_name_cleaned, total)
            current_date = str(datetime.datetime.now().date())
            current_time = str(datetime.datetime.now().time())
            date = f'{current_date}T{current_time}'
            activity = f'{date} - Lost ${abs(total)} playing roulette on {current_date}'
            user_db.add_user_activity(discord_name_cleaned, activity, f'{current_date}')
            user_db.update_last_activity(discord_name_cleaned, activity)
            # await message.channel.send(f'{discord_name} lost ${abs(total)} playing roulette.')
            string = f'{discord_name} lost ${abs(total)} playing roulette.'
            embed = discord.Embed(description=string, color=0x50C878)
            file = discord.File('images/icon.png', filename='icon.png')
            embed.set_thumbnail(url='attachment://icon.png')
            embed.set_author(name="Gambling-Bot says:")
            embed.set_footer(text="!roulette")    
            await message.channel.send(file=file, embed=embed)
    else:
        print("errors")

# SLOT MACHINE
async def slots(message : discord.message.Message, client: discord.Client, user_db : UserDatabase):
    def check(m):
        return m.author == message.author and m.channel == message.channel
    # await message.channel.send("How much are you wagering per spin?")
    string = "How much are you wagering per spin?"
    embed = discord.Embed(title=string, color=0x50C878)
    file = discord.File('images/icon.png', filename='icon.png')
    embed.set_thumbnail(url='attachment://icon.png')
    embed.set_author(name="Gambling-Bot says:")
    embed.set_footer(text="!slots")
    await message.channel.send(file=file, embed=embed)
    response = await client.wait_for('message', check=check, timeout=30)
    discord_name = response.author.mention
    discord_name_cleaned = discord_name.replace('<', '').replace('>', '').replace('@', '')
    originalBalance = user_db.get_balance(discord_name_cleaned)
    if response.content.isdigit() and int(response.content) <= originalBalance:
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
        # await message.channel.send(f'''\nYour Balance is: ${newBalance}. Here is the slot machine:
        # {''.join(result_grid)}
        # Enter an option: (!spin - spin the slot | !change - to change wager amount | !exit - cash out of slot machine)
        # ''')
        string = f'''\nYour Balance is: ${newBalance}. Here is the slot machine:
        {''.join(result_grid)}
        Enter an option'''
        embed = discord.Embed(title=string, color=0x50C878)
        file = discord.File('images/icon.png', filename='icon.png')
        embed.set_thumbnail(url='attachment://icon.png')
        embed.set_author(name="Gambling-Bot says:")
        embed.add_field(name="**!spin**", value="Spins the slot machine.", inline= False)
        embed.add_field(name="**!change**", value="Changes the wager amount of each spin.", inline= False)
        embed.add_field(name="**!exit**", value="Exits the slot machine page.", inline= False)
        embed.set_footer(text="!slots")
        await message.channel.send(file=file, embed=embed)
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
                    # await message.channel.send(f'Wager amount changed to ${wage}')
                    string = f'Wager amount changed to ${wage}'
                    embed = discord.Embed(title=string, color=0x50C878)
                    file = discord.File('images/icon.png', filename='icon.png')
                    embed.set_thumbnail(url='attachment://icon.png')
                    embed.set_author(name="Gambling-Bot says:")
                    embed.set_footer(text="!slots")
                    await message.channel.send(file=file, embed=embed)
                result_price = ''
            elif user_response == '!exit':
                # await message.channel.send(f'{response.author.mention} has exited.')
                exit_string = f'{response.author.mention} has exited.'
                exit_embed = discord.Embed(description=exit_string, color=0x50C878)
                file = discord.File('images/icon.png', filename='icon.png')
                exit_embed.set_thumbnail(url='attachment://icon.png')
                exit_embed.set_author(name="Gambling-Bot says:")
                exit_embed.set_footer(text="!exit")
                await message.channel.send(file=file, embed=exit_embed)
                break
            else:
                # await message.channel.send("[ERROR]: Inavlid Input. Program Terminated. Please Try Again.")
                string = f'[ERROR]: Invalid Input. Program Terminated. Please Try Again.'
                embed = discord.Embed(title=string, color=0x50C878)
                file = discord.File('images/icon.png', filename='icon.png')
                embed.set_thumbnail(url='attachment://icon.png')
                embed.set_author(name="Gambling-Bot says:")
                embed.set_footer(text="!coinfip")
                await message.channel.send(file=file, embed=embed)
                break
            
            if newBalance > 0 and wage <= newBalance:
                grid = [[random.choice(['Cherry', 'Bell', 'Bar', 'Lemon', 'Orange', 'Star', 'Apple']) for _ in range(3)] for _ in range(3)]
                result_grid = []
                result_grid.append(('-' * 11) + '\n')
                for row in grid:
                    result = ' | '.join(row) + '\n'
                    result_grid.append(result)
                    result_grid.append(('-' * 11) + '\n')
                # await message.channel.send(f'''{result_price}Your Balance is: ${newBalance}. Here is the slot machine:
                # {''.join(result_grid)}
                # Enter an option: (!spin - spin the slot | !change - to change wager amount | !exit - cash out of slot machine)
                # ''')
                string = f'''{result_price}Your Balance is: ${newBalance}. Here is the slot machine:
                {''.join(result_grid)}
                Enter an option'''
                embed = discord.Embed(title=string, color=0x50C878)
                file = discord.File('images/icon.png', filename='icon.png')
                embed.set_thumbnail(url='attachment://icon.png')
                embed.set_author(name="Gambling-Bot says:")
                embed.add_field(name="**!spin**", value="Spins the slot machine.")
                embed.add_field(name="**!change**", value="Changes the wager amount of each spin.")
                embed.add_field(name="**!exit**", value="Exits the slot machine page.")
                embed.set_footer(text="!slots")
                print("meep")
                await message.channel.send(file=file, embed=embed)
            else:
                # await message.channel.send(f'''"Game over! {discord_name} ran out of money."''')
                string = f'''"Game over! {discord_name} ran out of money."'''
                embed = discord.Embed(title=string, color=0x50C878)
                file = discord.File('images/icon.png', filename='icon.png')
                embed.set_thumbnail(url='attachment://icon.png')
                embed.set_author(name="Gambling-Bot says:")
                embed.set_footer(text="!slots")
                await message.channel.send(file=file, embed=embed)
        difference = newBalance - originalBalance
        if difference > -1:
            user_db.update_balance(discord_name_cleaned, difference)
            current_date = str(datetime.datetime.now().date())
            current_time = str(datetime.datetime.now().time())
            date = f'{current_date}T{current_time}'
            activity = f'{date} - Won ${difference} playing slots on {current_date}'
            user_db.add_user_activity(discord_name_cleaned, activity, f'{current_date}')
            user_db.update_last_activity(discord_name_cleaned, activity)
            # await message.channel.send(f'{discord_name} won ${difference} playing slots.')
            string = f'{discord_name} won ${difference} playing slots.'
            embed = discord.Embed(title=string, color=0x50C878)
            file = discord.File('images/icon.png', filename='icon.png')
            embed.set_thumbnail(url='attachment://icon.png')
            embed.set_author(name="Gambling-Bot says:")
            embed.set_footer(text="!slots")
            await message.channel.send(file=file, embed=embed)
        else:
            user_db.update_balance(discord_name_cleaned, difference)
            current_date = str(datetime.datetime.now().date())
            current_time = str(datetime.datetime.now().time())
            date = f'{current_date}T{current_time}'
            activity = f'{date} - Lost ${abs(difference)} playing slots on {current_date}'
            user_db.add_user_activity(discord_name_cleaned, activity, f'{current_date}')
            user_db.update_last_activity(discord_name_cleaned, activity)
            # await message.channel.send(f'{discord_name} lost ${abs(difference)} playing slots.')
            string = f'{discord_name} lost ${abs(difference)} playing slots.'
            embed = discord.Embed(title=string, color=0x50C878)
            file = discord.File('images/icon.png', filename='icon.png')
            embed.set_thumbnail(url='attachment://icon.png')
            embed.set_author(name="Gambling-Bot says:")
            embed.set_footer(text="!slots")
            await message.channel.send(file=file, embed=embed)

# GUESS THE NUMBER
async def guess(message : discord.message.Message, client: discord.Client, user_db : UserDatabase):
    def check(m):
        return m.author == message.author and m.channel == message.channel
    # await message.channel.send("How much are you wagering?")
    string = f"How much are you wagering?"
    embed = discord.Embed(title=string, color=0x50C878)
    file = discord.File('images/icon.png', filename='icon.png')
    embed.set_thumbnail(url='attachment://icon.png')
    embed.set_author(name="Gambling-Bot says:")
    embed.set_footer(text="!guess")
    await message.channel.send(file=file, embed=embed)
    response = await client.wait_for('message', check=check, timeout=30)
    discord_name = response.author.mention
    discord_name_cleaned = discord_name.replace('<', '').replace('>', '').replace('@', '')
    originalBalance = user_db.get_balance(discord_name_cleaned)
    if response.content.isdigit() and int(response.content) <= originalBalance:
        wage = int(response.content)
        # await message.channel.send("What stake do you want to do? (1) (0 - 10) **1x Multiplier** | (2) (0 - 50) **5x Multiplier** | (3) (0 - 100) **10x Multiplier**)")
        title = "What stake do you want to do?"
        embed = discord.Embed(title=title, description= '\n', color=0x50C878)
        file = discord.File('images/icon.png', filename='icon.png')
        embed.set_thumbnail(url='attachment://icon.png')
        embed.set_author(name="Gambling-Bot says:")
        embed.add_field(name="**1x**", value="(0 - 10) **1x Multiplier**", inline= False)
        embed.add_field(name="**5x**", value="(0 - 50) **5x Multiplier**", inline= False)
        embed.add_field(name="**10x**", value="(0 - 100) **10x Multiplier**)", inline= False)
        embed.set_footer(text="!guess")
        await message.channel.send(file=file, embed=embed)
        response = await client.wait_for('message', check=check, timeout=30)
        if response.content == '1x':
            # await message.channel.send("Please give a number between 0 - 10")
            title = "Please give a number between 0 - 10"
            embed = discord.Embed(title=title, description= '\n', color=0x50C878)
            file = discord.File('images/icon.png', filename='icon.png')
            embed.set_thumbnail(url='attachment://icon.png')
            embed.set_author(name="Gambling-Bot says:")
            embed.set_footer(text="!guess")
            await message.channel.send(file=file, embed=embed)
            random_number = random.randint(0, 10)
            response = await client.wait_for('message', check=check, timeout=30)
            if response.content == random_number:
                user_db.update_balance(discord_name_cleaned, wage)
                current_date = str(datetime.datetime.now().date())
                current_time = str(datetime.datetime.now().time())
                date = f'{current_date}T{current_time}'
                await message.channel.send(file=file, embed=embed)
                activity = f'{date} - Won ${wage} playing guess the number on {current_date}'
                user_db.add_user_activity(discord_name_cleaned, activity, f'{current_date}')
                user_db.update_last_activity(discord_name_cleaned, activity)
                user_db.update_total_earnings(discord_name_cleaned, wage)
                # await message.channel.send(f'{discord_name} won ${wage} guessing {random_number} in guessing the number')
                string = f'{discord_name} won ${wage} guessing {random_number} in guessing the number'
                embed = discord.Embed(description= string, color=0x50C878)
                file = discord.File('images/icon.png', filename='icon.png')
                embed.set_thumbnail(url='attachment://icon.png')
                embed.set_author(name="Gambling-Bot says:")
                embed.set_footer(text="!guess")
                await message.channel.send(file=file, embed=embed)
            else:
                user_db.update_balance(discord_name_cleaned, -wage)
                current_date = str(datetime.datetime.now().date())
                current_time = str(datetime.datetime.now().time())
                date = f'{current_date}T{current_time}'
                activity = f'{date} - Lost ${wage} playing guess the number on {current_date}'
                user_db.add_user_activity(discord_name_cleaned, activity, f'{current_date}')
                user_db.update_last_activity(discord_name_cleaned, activity)
                # await message.channel.send(f'{discord_name} lost ${wage} guessing {random_number} in guessing the number')
                string = f'{discord_name} lost ${wage} guessing {random_number} in guessing the number'
                embed = discord.Embed(description= string, color=0x50C878)
                file = discord.File('images/icon.png', filename='icon.png')
                embed.set_thumbnail(url='attachment://icon.png')
                embed.set_author(name="Gambling-Bot says:")
                embed.set_footer(text="!guess")
                await message.channel.send(file=file, embed=embed)
        elif response.content == '5x':
            # await message.channel.send("Please give a number between 0 - 50")
            title = "Please give a number between 0 - 50"
            embed = discord.Embed(title=title, description= '\n', color=0x50C878)
            file = discord.File('images/icon.png', filename='icon.png')
            embed.set_thumbnail(url='attachment://icon.png')
            embed.set_author(name="Gambling-Bot says:")
            embed.set_footer(text="!guess")
            await message.channel.send(file=file, embed=embed)
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
                # await message.channel.send(f'{discord_name} won ${wage * 5} guessing {random_number} in guessing the number')
                string = f'{discord_name} won ${wage * 5} guessing {random_number} in guessing the number'
                embed = discord.Embed(description= string, color=0x50C878)
                file = discord.File('images/icon.png', filename='icon.png')
                embed.set_thumbnail(url='attachment://icon.png')
                embed.set_author(name="Gambling-Bot says:")
                embed.set_footer(text="!guess")
                await message.channel.send(file=file, embed=embed)
            else:
                user_db.update_balance(discord_name_cleaned, -wage)
                current_date = str(datetime.datetime.now().date())
                current_time = str(datetime.datetime.now().time())
                date = f'{current_date}T{current_time}'
                activity = f'{date} - Lost ${wage} playing guess the number on {current_date}'
                user_db.add_user_activity(discord_name_cleaned, activity, f'{current_date}')
                user_db.update_last_activity(discord_name_cleaned, activity)
                # await message.channel.send(f'{discord_name} lost ${wage} guessing {random_number} in guessing the number')
                string = f'{discord_name} lost ${wage} guessing {random_number} in guessing the number'
                embed = discord.Embed(description= string, color=0x50C878)
                file = discord.File('images/icon.png', filename='icon.png')
                embed.set_thumbnail(url='attachment://icon.png')
                embed.set_author(name="Gambling-Bot says:")
                embed.set_footer(text="!guess")
                await message.channel.send(file=file, embed=embed)
        elif response.content == '10x':
            # await message.channel.send("Please give a number between 0 - 100")
            title = "Please give a number between 0 - 100"
            embed = discord.Embed(title=title, description= '\n', color=0x50C878)
            file = discord.File('images/icon.png', filename='icon.png')
            embed.set_thumbnail(url='attachment://icon.png')
            embed.set_author(name="Gambling-Bot says:")
            embed.set_footer(text="!guess")
            await message.channel.send(file=file, embed=embed)
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
                # await message.channel.send(f'{discord_name} won ${wage * 10} guessing {random_number} in guessing the number')
                string = f'{discord_name} won ${wage * 10} guessing {random_number} in guessing the number'
                embed = discord.Embed(description= string, color=0x50C878)
                file = discord.File('images/icon.png', filename='icon.png')
                embed.set_thumbnail(url='attachment://icon.png')
                embed.set_author(name="Gambling-Bot says:")
                embed.set_footer(text="!guess")
                await message.channel.send(file=file, embed=embed)
            else:
                user_db.update_balance(discord_name_cleaned, -wage)
                current_date = str(datetime.datetime.now().date())
                current_time = str(datetime.datetime.now().time())
                date = f'{current_date}T{current_time}'
                activity = f'{date} - Lost ${wage} playing guess the number on {current_date}'
                user_db.add_user_activity(discord_name_cleaned, activity, f'{current_date}')
                user_db.update_last_activity(discord_name_cleaned, activity)
                # await message.channel.send(f'{discord_name} lost ${wage} guessing {random_number} in guessing the number')
                string = f'{discord_name} lost ${wage} guessing {random_number} in guessing the number'
                embed = discord.Embed(description= string, color=0x50C878)
                file = discord.File('images/icon.png', filename='icon.png')
                embed.set_thumbnail(url='attachment://icon.png')
                embed.set_author(name="Gambling-Bot says:")
                embed.set_footer(text="!guess")
                await message.channel.send(file=file, embed=embed)
        else:
            # await message.channel.send("[ERROR]: Inavlid Input. Program Terminated. Please Try Again.")
            string = f'[ERROR]: Invalid Input. Program Terminated. Please Try Again.'
            embed = discord.Embed(title=string, color=0x50C878)
            file = discord.File('images/icon.png', filename='icon.png')
            embed.set_thumbnail(url='attachment://icon.png')
            embed.set_author(name="Gambling-Bot says:")
            embed.set_footer(text="!guess")
            await message.channel.send(file=file, embed=embed)
    else:
        string = f'[ERROR]: Wager is larger than current balance. Program Terminated. Please Try Again.'
        embed = discord.Embed(title=string, color=0x50C878)
        file = discord.File('images/icon.png', filename='icon.png')
        embed.set_thumbnail(url='attachment://icon.png')
        embed.set_author(name="Gambling-Bot says:")
        embed.set_footer(text="!guess")
        await message.channel.send(file=file, embed=embed)