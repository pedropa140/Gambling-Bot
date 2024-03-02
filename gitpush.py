import subprocess
import datetime

def format_number(num):
    if num < 10:
        return f"0{num}"
    else:
        return str(num)

def git_push(branch="master"):
    try:
        subprocess.run(["git", "add", "."], check=True)
        current = datetime.datetime.now()
        current_date = current.date()
        current_hour = current.time()
        year = current_date.year
        month = format_number(current_date.month)
        day = format_number(current_date.day)
        hour = format_number(current_hour.hour)
        minute = format_number(current_hour.minute)
        second = format_number(current_hour.second)
        date = f'{year}{month}{day}T{hour}:{minute}:{second}'
        print(date)
        commit_message = input("Enter your commit message: ")
        message = f'{date} - {commit_message}'
        subprocess.run(["git", "commit", "-m", message], check=True)
        subprocess.run(["git", "push"], check=True)

        print("git push successful!")

    except subprocess.CalledProcessError as e:
        print(f"Error: {e}")
        print("git push failed.")

if __name__ == "__main__":
    git_push()
