from collections import namedtuple
import random
from strategy import Strategy
from golf import Deck

random.seed(1337)


class SameColumnStrategy(Strategy):
    def flip_initial_cards(self, hand):
        column = random.randint(0, 2)
        hand[column].flipped = True
        hand[column + 3].flipped = True


class DifferentColumnsStrategy(Strategy):
    def flip_initial_cards(self, hand):
        flipped_indices = random.sample(range(6), 2)
        for index in flipped_indices:
            hand[index].flipped = True


class HybridStrategy(Strategy):
    def flip_initial_cards(self, hand):
        column = random.randint(0, 2)
        hand[column].flipped = True
        if hand[column].rank == "2":
            other_columns = [i for i in range(3) if i != column]
            other_column = random.choice(other_columns)
            flip_index = random.choice([other_column, other_column + 3])
            hand[flip_index].flipped = True
        else:
            hand[column + 3].flipped = True


def calculate_score(hand, see_all=False):
    score = 0

    for i in range(3):
        top_card = hand[i]
        bottom_card = hand[i + 3]

        # if they are the same score is 0
        if top_card.rank == bottom_card.rank:
            if top_card.rank != "2":
                continue

        col_score = 0
        if top_card.flipped:
            col_score += top_card.value()

        if bottom_card.flipped:
            col_score += bottom_card.value()

        if see_all:
            score += top_card.value() + bottom_card.value()
        else:
            score += col_score

    return score


def print_formatted_hand(hand):
    print("Hand:")
    print("┌───┐ ┌───┐ ┌───┐")
    print(
        "│{:^3}│ │{:^3}│ │{:^3}│".format(
            str(hand[0]) if hand[0].flipped else "?",
            str(hand[1]) if hand[1].flipped else "?",
            str(hand[2]) if hand[2].flipped else "?",
        )
    )
    print("└───┘ └───┘ └───┘")
    print("┌───┐ ┌───┐ ┌───┐")
    print(
        "│{:^3}│ │{:^3}│ │{:^3}│".format(
            str(hand[3]) if hand[3].flipped else "?",
            str(hand[4]) if hand[4].flipped else "?",
            str(hand[5]) if hand[5].flipped else "?",
        )
    )
    print("└───┘ └───┘ └───┘")
    print()


def play_game(strategy, verbose):
    deck = Deck()
    discard_pile = []
    hand = [deck.draw() for _ in range(6)]

    strategy.flip_initial_cards(hand)

    while not all(card.flipped for card in hand):
        known_cards = [card for card in hand if card.flipped]
        unknown_cards = [card for card in hand if not card.flipped]

        current_score = calculate_score(hand)
        best_move = None
        best_score = current_score

        # draw a new card from the deck
        new_card = deck.draw()
        pickup_card = discard_pile[-1] if len(discard_pile) > 0 else None
        new_card.flipped = True  # The drawn card is always visible

        # check replacing known cards with the new card
        for i, card in enumerate(known_cards):
            temp_hand = hand.copy()
            temp_hand[hand.index(card)] = new_card
            new_score = calculate_score(temp_hand)

            if new_score < best_score:
                best_score = new_score
                best_move = ("replace", hand.index(card))

        # check flipping unknown cards
        for card in unknown_cards:
            temp_hand = hand.copy()
            temp_hand[hand.index(card)].flipped = True
            new_score = calculate_score(temp_hand)

            if new_score < best_score:
                best_score = new_score
                best_move = ("flip", hand.index(card))

            temp_hand[hand.index(card)].flipped = False

        # execute best move
        if best_move:
            if best_move[0] == "replace":
                index = best_move[1]
                discard_pile.append(hand[index])
                hand[index] = new_card
            else:  # flip
                hand[best_move[1]].flipped = True
                discard_pile.append(new_card)
        else:
            # if no improvement, flip a random unknown card and discard the new card
            unflipped = [card for card in hand if not card.flipped]
            if unflipped:
                random.choice(unflipped).flipped = True
            discard_pile.append(new_card)

        if verbose:
            print_formatted_hand(hand)
            print(f"Drawn card {new_card}")
            print(f"Pickup card {pickup_card}")

            if best_move:
                action, card_index = best_move
                print(f"Best move was {action} on {temp_hand[card_index]}")
            else:
                print(f"Best move was None")

            print(f"Current score: {calculate_score(hand)}")
            print(f"Len of discards: {len(discard_pile)}")

    final_score = calculate_score(hand)
    if verbose:
        print(f"Final Score {final_score}\n")
    return final_score
