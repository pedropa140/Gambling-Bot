import os
import json
from player import Player

def read_player_data(directory):
    all_player_data = {}
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
                    all_player_data[discord_name] = player
                else:
                    print(f"Discord name not found in file: {filename}")
    return all_player_data

dictionary = read_player_data("players")
print(dictionary)

for i in dictionary:
    print(dictionary[i].name)
    print(dictionary[i].discord_name)
    print(dictionary[i].balance)
    print(dictionary[i].total_earnings)
    print(dictionary[i].level)
    print(dictionary[i].statistics)
    print(dictionary[i].last_activity)
    print(dictionary[i].date_created)