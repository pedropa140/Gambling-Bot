<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Crimson+Pro&family=Literata" rel="stylesheet">

<div align=center>
<img src="images/icon.png" alt="icon.png" width="200" height="200">
<h1>Gambling-Bot</h1>
  
## Description

</div>

Gambling-Bot is Discord bot created to simulate the world of gambling. Users can create accounts to keep track of their progress. In addition, users can play gambling games like:

- dice
- roulette
- slots
- flip the coin
- guess the number
- blackjack

<div align=center>
  
## How to install

</div>


Not interested in downloading bot to your computer, you can add bot to your server [here](https://discord.com/oauth2/authorize?client_id=1193596778151432312&permissions=1084479764544&scope=bot)

Follow these steps to run the Discord application and add it to your server.
1. If you are *not* an author, fork the repository [here](https://github.com/pedropa140/Gambling-Bot/fork).
2. Clone the repository.
    ```bash
    git clone https://github.com/pedropa140/Gambling-Bot.git
    ```

3. Install Dependencies
   - Make sure your pip version is up-to-date:
      ```bash
      pip install --upgrade pip
      ```
      ```bash
      pip install -r requirements.txt
      ```
3. Create Discord Application <br>
    - Go to [https://discord.com/developers/applications](https://discord.com/developers/applications)
    - Click on **New Application**
    - Give it a name
    - Agree to [Developer Terms and Services](https://discord.com/developers/docs/policies-and-agreements/developer-terms-of-service) and [Developer Policy](https://discord.com/developers/docs/policies-and-agreements/developer-policy)
    - Go to the **Bot** tab
      - Click on **Reset Token** to receive Discord Application Token
      - Go back to the Github clone and create a **.env** file
      - Type
        
        ```bash
        DISCORD_TOKEN = '**REPLACE WITH DISCORD TOKEN THAT YOU JUST COPIED**'
        ```
    - Go to the **OAuth2** tab
      - For **OAuth2 URL Generator**, click on **bot** on the second column
        - For **General Permissions**, click on
          - **Read Messages/View Channels**
          - **Manage Events**
          - **Create Events**
          - **Moderate Members**
          - **View Server Insights**
          - **View Creator Monetization Insights**
  
      
        - For **Text Permissions**, click on
          - **Send Messages**
          - **Create Public Threads**
          - **Create Private Threads**
          - **Send Messages in Threads**
          - **Send TTS Messages**
          - **Manage Messages**
          - **Manage Threads**
          - **Embed Links**
          - **Attach Files**
          - **Read Message History**
          - **Read Message History**
          - **Mention Everyone**
          - **Use External Emojis**
          - **Use External Stickers**
          - **Add Reactions**
          - **Use Stash Commands**
          - **Use Embedded Activities**
  
      
        - For **Voice Permissions**, click on
          - **Use Embedded Activites**
  
            
      - Copy the **Generated URL** and paste it in your web browser.
      - Click on the Discord server you would like to add the bot into.
        
<div align=center>   
  
## How to run the Gambling-Bot

In a terminal, find the directory where main.py is located and run this command:
</div>

  ```bash
  python main.py
  ```

### Options:

  - **@Gambling-Bot !hello**
    - returns a welcoming message back to the user.
  - **@gambling-Bot !coin**
    - returns either heads or tails back to the user.
  - **@Gambling-Bot !roll_dice**
    - prompts the user on how many sides is the dice and returns a random number back to the user.
  - **@Gambling-Bot !gambling**
    - prompts the user if they are a new user or a returning user
      - **yes**
        - checks if the user is already in the database
        - if not it prompts the user if they want to be in the database
        - if yes, we gather information from the user using their Discord name.
        - **!create**
          - creates the user into the database.
          - **!game**
            - redirects you to the gambling game page.
            - **!dice**
              - players roll a two sided die that generates a random-number from 1 to 6. Players earn money if the sum of the two dies are greater than the dealer's roll.
            - **!coinflip**
              - asks user on if the coin will flip on heads or tails. Players will earn money they guess correctly.
            - **!blackjack**
              - card game where players try to get a hand total as close to 21 as possible without going over, while beating the dealer's hand.
            - **!roulette**
              - casino game where players bet on which numbered compartment a small ball will land in after a spinning wheel comes to a stop.
            - **!slots**
              - casino games where players spin reels containing various symbols, aiming to align them in winning combinations to earn payouts.
            - **!guess**
              - players guess what the generated number will be according to a specific range. The larger the range the bigger the payout.
            - **!exit**
              - exits the gambling page.
          - **!userinfo**
            - returns the Discord user's info.
          - **!balance**
            - returns the user balance and how much money they have.
          - **!addmoney**
            - adds money to the user's balance.
          - **!leaderboard**
            - shows the list of players with the highest amount of total earnings.
          - **!history**
            - shows the **5** most recent activities the user has done.
          - **!delete**
            - deletes the user from the database.
          - **!exit**
            - exits the gambling page.
        - **!exit**
          - does not create a user for the gambling database.
      - **no**
        - prompts the user if they want to create an account.
        - if yes, it would do the same thing as **!create**
        - if no, then it does not create a user for the database.