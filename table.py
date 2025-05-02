import random

from card import Card
from constants import PACK_OF_CARDS, BLACKJACK
from player import Player
from utilities import Hand


class Table:
    def __init__(self):
        self.players: list[Player] = []
        self.cards: list[Card] = list(PACK_OF_CARDS)

        self.dealer_hand = Hand()

        self.wins = 0  # TODO DELETE
        self.draws = 0
        self.loses = 0

    @property
    def active_players(self):
        return len([player for player in self.players if player.active])

    @property
    def dealer_bust(self):
        return self.dealer_hand.optimal_value > BLACKJACK

    def generate_dealer_cards(self) -> None:
        dealer_cards = self.get_random_cards(number_of_cards=1)
        self.dealer_hand.set_cards(dealer_cards)

    def generate_start_cards(self) -> None:
        for player in self.players:
            random_cards = self.get_random_cards(number_of_cards=2)
            player.start_hand.set_cards(random_cards)

    def get_random_cards(self, number_of_cards) -> list[Card]:
        number_of_cards = min(number_of_cards, len(self.cards))
        return random.sample(self.cards, number_of_cards) if self.cards else []

    def reset_table(self):
        self.dealer_hand.clear()
        self.players = [player for player in self.players if player.active]

        for player in self.players:
            player.reset()

    def add_players(self, players: list[Player]):
        for player in players:
            self.players.append(player)
            player.table = self

    def set_bets(self):
        for player in self.players:
            amount = player.start_bet_amount
            player.subtract_money(amount)
            player.start_hand.set_amount(amount)
            # print(player.start_hand.win_amount)
