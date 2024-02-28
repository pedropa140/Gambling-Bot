from player import Player
import json
import datetime
import time
import random
discord_name = '<@525874420703559702>'
discord_name_cleaned = discord_name.replace('<', '').replace('>', '').replace('@', '')

name = 'thecoconutwater'
current_datetime = datetime.datetime.now()

current_date = str(current_datetime.date())
current_time = str(current_datetime.time())
date = f'{current_date}T{current_time}'      
statistics = []
activity = f'{date} - Created Account on {date}'
statistics.append(activity)
newPlayer = Player(name, discord_name_cleaned, 500, 0, statistics, activity, date)
i = 0
while i < 5:
    total_earnings = 0
    time.sleep(5)
    current_datetime = datetime.datetime.now()
    current_date = str(current_datetime.date())
    current_time = str(current_datetime.time())
    reward = random.randint(-5000, 5000)
    if reward > -1:
        total_earnings = reward
    date = f'{current_date}T{current_time}' 
    activity = f'{date} - ${reward}'
    i += 1
    newPlayer.update_player(reward, total_earnings, activity)

newPlayer.to_json_file()