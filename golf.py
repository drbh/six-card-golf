import random


class Card:
    def __init__(self, rank, suit):
        self.rank = rank
        self.suit = suit
        self.flipped = False

    def __repr__(self):
        return f"{self.rank}{self.suit}"

    def value(self):
        if self.rank in ["J", "Q"]:
            return 10
        elif self.rank == "K":
            return 0
        elif self.rank == "A":
            return 1
        elif self.rank == "2":
            return -2
        else:
            return int(self.rank)

    def copy(self):
        new_card = Card(self.rank, self.suit)
        new_card.flipped = self.flipped
        return new_card


class Deck:
    def __init__(self):
        ranks = ["A", "2", "3", "4", "5", "6", "7", "8", "9", "10", "J", "Q", "K"]
        suits = ["♠", "♥", "♦", "♣"]
        self.cards = [Card(rank, suit) for rank in ranks for suit in suits]
        random.shuffle(self.cards)

    def draw(self):
        return self.cards.pop()
