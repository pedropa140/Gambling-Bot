import sqlite3

class UserDatabase:
    def __init__(self, db_name='user_data.db'):
        self.conn = sqlite3.connect(db_name)
        self.c = self.conn.cursor()
        self.create_tables()

    def create_tables(self):
        self.c.execute('''CREATE TABLE IF NOT EXISTS users
                          (id INTEGER PRIMARY KEY,
                           name TEXT,
                           discord_name TEXT UNIQUE,
                           balance REAL,
                           total_earnings REAL,
                           level INTEGER,
                           last_activity TEXT,
                           date_created TEXT)''')

        self.c.execute('''CREATE TABLE IF NOT EXISTS user_activity
                          (id INTEGER PRIMARY KEY,
                           discord_name TEXT,
                           activity TEXT,
                           timestamp TEXT)''')
        self.conn.commit()

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

    def add_user(self, name, discord_name, balance, total_earnings, last_activity, date_created):
        level = self.calculate_level(total_earnings)
        self.c.execute("INSERT INTO users (name, discord_name, balance, total_earnings, level, last_activity, date_created) VALUES (?, ?, ?, ?, ?, ?, ?)",
                       (name, discord_name, balance, total_earnings, level, last_activity, date_created))
        self.conn.commit()

    def add_user_activity(self, discord_name, activity, timestamp):
        self.c.execute("INSERT INTO user_activity (discord_name, activity, timestamp) VALUES (?, ?, ?)",
                       (discord_name, activity, timestamp))
        self.conn.commit()
    
    def update_total_earnings(self, discord_name, earnings_delta):
        self.c.execute("SELECT total_earnings FROM users WHERE discord_name=?", (discord_name,))
        result = self.c.fetchone()
        if result is not None:
            current_total_earnings = result[0]

            new_total_earnings = current_total_earnings + earnings_delta
            self.c.execute("UPDATE users SET total_earnings=? WHERE discord_name=?", (new_total_earnings, discord_name))

            if new_total_earnings >= 0:
                new_level = self.calculate_level(new_total_earnings)
                self.c.execute("UPDATE users SET level=? WHERE discord_name=?", (new_level, discord_name))

            self.conn.commit()
        else:
            print(f"No user found with Discord name '{discord_name}'.")
    
    def find_user(self, discord_name):
        discord_name_cleaned = discord_name.replace('<', '').replace('>', '').replace('@', '')
        self.c.execute("SELECT COUNT(*) FROM users WHERE discord_name=?", (discord_name_cleaned,))
        count = self.c.fetchone()[0]
        return count > 0
    
    def delete_user(self, discord_name):
        self.c.execute("DELETE FROM users WHERE discord_name=?", (discord_name,))
        self.c.execute("DELETE FROM user_activity WHERE discord_name=?", (discord_name,))
        self.conn.commit()

    def get_user_info(self, discord_name):
        self.c.execute("SELECT discord_name, name, balance, total_earnings, level, last_activity, date_created FROM users WHERE discord_name=?", (discord_name,))
        user_info = self.c.fetchone()
        if user_info:
            return {
                "Discord Name": user_info[0],
                "Name": user_info[1],
                "Balance": user_info[2],
                "Total Earnings": user_info[3],
                "Level": user_info[4],
                "Last Activity": user_info[5],
                "Date Created": user_info[6]
            }
        else:
            print(f"No user found with Discord name '{discord_name}'")
            return None

    def get_balance(self, discord_name):
        self.c.execute("SELECT balance FROM users WHERE discord_name=?", (discord_name,))
        balance = self.c.fetchone()
        if balance:
            return balance[0]
        else:
            print(f"No user found with Discord name '{discord_name}'")
            return None
        
    def update_balance(self, discord_name, amount):
        current_balance = self.get_balance(discord_name)
        if current_balance is not None:
            new_balance = current_balance + amount
            self.c.execute("UPDATE users SET balance=? WHERE discord_name=?", (new_balance, discord_name))
            self.conn.commit()
            print(f"Balance updated successfully for {discord_name}. New balance: {new_balance}")
        else:
            print(f"Failed to update balance for {discord_name}. User not found.")


    def get_leaderboard(self, limit=10):
        self.c.execute("SELECT name, discord_name, total_earnings FROM users ORDER BY total_earnings DESC LIMIT ?", (limit,))
        leaderboard = self.c.fetchall()
        return leaderboard
    
    def get_recent_activities(self, discord_name, limit=5):
        self.c.execute("SELECT activity, timestamp FROM user_activity WHERE discord_name=? ORDER BY timestamp DESC LIMIT ?", (discord_name, limit))
        recent_activities = self.c.fetchall()
        return recent_activities
    
    def close_connection(self):
        self.conn.close()

def main():
    user_db = UserDatabase()
    
    user_db.close_connection()

if __name__ == "__main__":
    main()