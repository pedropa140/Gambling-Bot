import random

def main():
    print("Welcome to the Slot Machine Game!")
    balance = 100000
    bet_amount = 50  # Amount to bet on each spin
    while balance > 0:
        grid = [[random.choice(['Cherry', 'Bell', 'Bar', 'Lemon', 'Orange', 'Star', 'Apple']) for _ in range(3)] for _ in range(3)]
        print("\nYour balance is $", balance)
        print("Here's the slot machine:")
        for row in grid:
            print(' | '.join(row))
            print('-' * 11)
        input("Press Enter to spin the reels...")
        symbols = set()
        # Check horizontal matches
        for row in grid:
            if len(set(row)) == 1 and row[0] != ' ':
                symbols.add(row[0])

        # Check diagonal matches
        if grid[0][0] == grid[1][1] == grid[2][2] and grid[0][0] != ' ':
            symbols.add(grid[0][0])
        if grid[0][2] == grid[1][1] == grid[2][0] and grid[0][2] != ' ':
            symbols.add(grid[0][2])
        matches = symbols
        # matches = check_matches(grid)
        if matches:
            payouts = {'Cherry': 1, 'Bell': 1.5, 'Bar': 2, 'Lemon': 0.5, 'Orange': 0.5, 'Star': 4, 'Apple': 3}
            payout = 0
            for symbol in matches:
                payout += payouts.get(symbol, 0)
            balance += payout * bet_amount
            print("Congratulations! You won $", payout * bet_amount)
        else:
            print("Sorry, you didn't win anything this time.")
            payout = -bet_amount  # No matches, so deduct the bet amount as a loss
        balance += payout
    print("Game over! You ran out of money.")

if __name__ == "__main__":
    main()
