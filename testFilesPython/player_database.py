import sqlite3
import json

class PlayerDatabase:
    def __init__(self, db_file):
        self.conn = sqlite3.connect(db_file)
        self.cursor = self.conn.cursor()
        self.create_table()

    def create_table(self):
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS players (
                                id INTEGER PRIMARY KEY,
                                name TEXT,
                                discord_name TEXT,
                                balance INTEGER,
                                total_earnings INTEGER,
                                level INTEGER,
                                statistics TEXT,
                                last_activity TEXT,
                                date_created TEXT)''')
        self.conn.commit()

    def add_player(self, name, discord_name, balance, total_earnings, statistics, last_activity, date_created):
        level = self.calculate_level(total_earnings)
        self.cursor.execute('''INSERT INTO players 
                               (name, discord_name, balance, total_earnings, level, statistics, last_activity, date_created)
                               VALUES (?, ?, ?, ?, ?, ?, ?, ?)''',
                            (name, discord_name, balance, total_earnings, level, statistics, last_activity, date_created))
        self.conn.commit()

    def update_player(self, discord_name, balance=None, total_earnings=None, statistics=None, last_activity=None):
        update_query = '''UPDATE players SET'''
        update_params = []

        if balance is not None:
            update_query += ' balance = ?,'
            update_params.append(balance)

        if total_earnings is not None:
            update_query += ' total_earnings = ?, level = ?,'
            update_params.extend([total_earnings, self.calculate_level(total_earnings)])

        if statistics is not None:
            update_query += ' statistics = ?,'
            update_params.append(json.dumps(statistics))

        if last_activity is not None:
            update_query += ' last_activity = ?,'
            update_params.append(last_activity)
        update_query = update_query.rstrip(',')
        update_query += ' WHERE discord_name = ?'
        update_params.append(discord_name)
        self.cursor.execute(update_query, update_params)
        self.conn.commit()

    def delete_player(self, discord_name):
        self.cursor.execute('''DELETE FROM players WHERE discord_name = ?''', (discord_name,))
        self.conn.commit()
        print(f"Player '{discord_name}' deleted from the database.")

    def calculate_level(self, total_earnings):
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

    def get_player_info(self, discord_name):
        self.cursor.execute('''SELECT * FROM players WHERE discord_name = ?''', (discord_name,))
        player_info = self.cursor.fetchone()
        return player_info

# # Example usage
# db = PlayerDatabase('players.db')
# db.add_player("John Doe", "johndoe#1234", 1000, 5000, '{"wins": 10, "losses": 5}', "2024-02-28", "2024-01-01")

# # Query player information
# player_info = db.get_player_info("johndoe#1234")
# print("Player Information:")
# print(player_info)
