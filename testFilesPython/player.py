import discord
from discord.ext import commands
import os
from dotenv import load_dotenv
import asyncio
import random
import datetime
import json

class Player:
    def __init__(self, name : str, discord_name : str, balance : int, total_earnings : int, statistics : list, last_activity : str, date_created : str):
        self.name = name
        self.discord_name = discord_name
        self.balance = balance
        self.total_earnings = total_earnings
        def calculate_level(total_earnings):
            levels_thresholds = [
                0, 1000, 2500, 5000, 7500, 10000, 12500, 15000, 17500, 20000, 22500,
                27500, 30000, 32500, 35000, 37500, 40000, 42500, 45000, 47500, 50000,
                55000, 60000, 65000, 70000, 75000, 100000, 150000, 200000, 250000, 500000,
                750000, 1000000, 1250000, 1500000, 1750000, 2000000, 2500000, 5000000, 
                7500000, 10000000, 25000000, 50000000, 10000000, 25000000, 50000000, 
                75000000, 100000000, 1000000000, 10000000000
            ]
            for level, threshold in enumerate(levels_thresholds, start=-1):
                if total_earnings < threshold:
                    return level
            return len(levels_thresholds)
        self.level = calculate_level(total_earnings)
        self.statistics = statistics
        self.last_activity = last_activity
        self.date_created = date_created
    
    def name(self):
        return self._name

    def name(self, value : str):
        self._name = value

    def discord_name(self):
        return self._discord_name

    def discord_name(self, value : str):
        self._discord_name = value

    def balance(self):
        return self._balance

    def balance(self, value : int):
        self._balance = value

    def total_earnings(self):
        return self.total_earnings

    def total_earnings(self, value : int):
        self.total_earnings = value

    def level(self):
        return self.level

    def statistics(self):
        return self._statistics

    def statistics(self, value : list):
        self._statistics = value

    def last_activity(self):
        return self._last_activity

    def last_activity(self, value : str):
        self._last_activity = value

    def date_created(self):
        return self._date_created

    def date_created(self, value : str):
        self._date_created = value

    def level_up(self, earnings: int):
        def calculate_level(total_earnings) -> int:
            levels_thresholds = [
                0, 1000, 2500, 5000, 7500, 10000, 12500, 15000, 17500, 20000, 22500,
                27500, 30000, 32500, 35000, 37500, 40000, 42500, 45000, 47500, 50000,
                55000, 60000, 65000, 70000, 75000, 100000, 150000, 200000, 250000, 500000,
                750000, 1000000, 1250000, 1500000, 1750000, 2000000, 2500000, 5000000, 
                7500000, 10000000, 25000000, 50000000, 10000000, 25000000, 50000000, 
                75000000, 100000000, 1000000000, 10000000000
            ]
            for level, threshold in enumerate(levels_thresholds, start=-1):
                if total_earnings < threshold:
                    return level
            return len(levels_thresholds)
        self.level = calculate_level(earnings)

    def update_player(self, reward: int, earnings: int, last_activity: str):
        self.balance += reward
        if reward > 0:
            self.total_earnings += earnings
        self.last_activity = last_activity
        self.statistics.insert(0, last_activity)
        self.level_up(self.total_earnings)

    # show player info
    def show_info():
        return NotADirectoryError()
    
    # show last five statistics
        
    def to_json_file(self):
        player_data = {
            "name": self.name,
            "discord_name": self.discord_name,
            "balance": self.balance,
            "total_earnings": self.total_earnings,
            "level": self.level,
            "statistics": self.statistics,
            "last_activity": self.last_activity,
            "date_created": self.date_created
        }

        if not os.path.exists("players"):
            os.makedirs("players")

        file_path = os.path.join("players", f"{self.discord_name}.json")
        with open(file_path, "w") as file:
            json.dump(player_data, file, indent=4)
        
        print(f"JSON file created for {self.name} at: {file_path}")