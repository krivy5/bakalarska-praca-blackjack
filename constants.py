from enum import Enum

from card import Card

BLACKJACK = 21
MINIMUM_DEALER_VALUE = 17

DEFAULT_BET = 100

PACK_OF_CARDS = {
    Card("2", "c"), Card("3", "c"), Card("4", "c"),
    Card("5", "c"), Card("6", "c"), Card("7", "c"),
    Card("8", "c"), Card("9", "c"), Card("T", "c"),
    Card("J", "c"), Card("Q", "c"), Card("K", "c"),
    Card("A", "c"),

    Card("2", "d"), Card("3", "d"), Card("4", "d"),
    Card("5", "d"), Card("6", "d"), Card("7", "d"),
    Card("8", "d"), Card("9", "d"), Card("T", "d"),
    Card("J", "d"), Card("Q", "d"), Card("K", "d"),
    Card("A", "d"),

    Card("2", "h"), Card("3", "h"), Card("4", "h"),
    Card("5", "h"), Card("6", "h"), Card("7", "h"),
    Card("8", "h"), Card("9", "h"), Card("T", "h"),
    Card("J", "h"), Card("Q", "h"), Card("K", "h"),
    Card("A", "h"),

    Card("2", "s"), Card("3", "s"), Card("4", "s"),
    Card("5", "s"), Card("6", "s"), Card("7", "s"),
    Card("8", "s"), Card("9", "s"), Card("T", "s"),
    Card("J", "s"), Card("Q", "s"), Card("K", "s"),
    Card("A", "s")
}

ACES = [card for card in PACK_OF_CARDS if card.rank == 'A']


class GameActions(Enum):
    hit = 'hit'
    stand = 'stand'
    double_down = 'double_down'
    split = 'split'


class Outcomes(Enum):
    win = 'win'
    draw = 'draw'
    loss = 'loss'
