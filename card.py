import random

class Card:
    def __init__(self, suit, rank):
        self.suit = suit
        self.rank = rank

    def __str__(self):
        return f"{self.rank} of {self.suit}"

class Deck:
    def __init__(self, num_decks):
        self.num_decks = num_decks
        self.cards = []
        self.populate()

    def populate(self):
        suits = ['Hearts', 'Diamonds', 'Clubs', 'Spades']
        ranks = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'Jack', 'Queen', 'King', 'Ace']
        for _ in range(self.num_decks):
            for suit in suits:
                for rank in ranks:
                    self.cards.append(Card(suit, rank))

    def shuffle(self):
        random.shuffle(self.cards)

    def deal_card(self):
        return self.cards.pop()

    def add_used_cards(self, used_cards):
        self.cards.extend(used_cards)
        random.shuffle(self.cards)

class Hand:
    def __init__(self):
        self.cards = []
        self.value = 0

    def add_card(self, card):
        self.cards.append(card)
        self.update_value()

    def update_value(self):
        self.value = 0
        num_aces = 0
        for card in self.cards:
            if card.rank == 'Ace':
                num_aces += 1
            elif card.rank in ['Jack', 'Queen', 'King']:
                self.value += 10
            else:
                self.value += int(card.rank)
        for _ in range(num_aces):
            if self.value + 11 <= 21:
                self.value += 11
            else:
                self.value += 1

    def __str__(self):
        hand_str = ""
        for card in self.cards:
            hand_str += str(card) + "\n"
        return hand_str