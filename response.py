import random
import datetime

def hello(message):
    options = ["Hi ", "Hey ", "Hello ", "Howdy ", "Hi there ", "Greetings ", "Aloha ", "Bonjour ", "Ciao ", "Hola ", "How's it going? ", "Howdy-do ", "Good day ", "Wassup ", "What's popping? ", "What's up? ", "Hiya ", "What's new? ", "How are you? "]
    current_time = datetime.datetime.now().time().hour
    if current_time > 12:
        options.append("Good Afternoon! ")
    else:
        options.append("Good Morning! ")
    return options[random.randint(0, len(options) - 1)] + message.author.mention