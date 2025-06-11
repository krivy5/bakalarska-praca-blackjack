import random

from Players.optimal_player import OptimalPlayer
from hand import PlayerHand
from constants import GameActions

anchoring_coefficient_matrix = {
    4:  {12: 0.9, 13: 0.85, 14: 0.8, 15: 0.7, 16: 0.6, 17: 0.5, 18: 0.35, 19: 0.2, 20: 0.1},
    5:  {12: 0.85, 13: 0.8, 14: 0.7, 15: 0.6, 16: 0.5, 17: 0.35, 18: 0.2, 19: 0.1, 20: 0.05},
    6:  {12: 0.8, 13: 0.7, 14: 0.6, 15: 0.5, 16: 0.35, 17: 0.2, 18: 0.1, 19: 0.05, 20: 0.03},
    7:  {12: 0.7, 13: 0.6, 14: 0.5, 15: 0.35, 16: 0.2, 17: 0.1, 18: 0.05, 19: 0.03, 20: 0.01},
    8:  {12: 0.6, 13: 0.5, 14: 0.35, 15: 0.2, 16: 0.1, 17: 0.05, 18: 0.03, 19: 0.01},
    9:  {12: 0.5, 13: 0.35, 14: 0.2, 15: 0.1, 16: 0.05, 17: 0.03, 18: 0.01},
    10: {12: 0.35, 13: 0.2, 14: 0.1, 15: 0.05, 16: 0.03, 17: 0.01},
    11: {12: 0.2, 13: 0.1, 14: 0.05, 15: 0.03, 16: 0.01},
    12: {12: 0.1, 13: 0.05, 14: 0.03, 15: 0.01},
    13: {13: 0.03, 14: 0.01},
}


class AnchoringPlayer(OptimalPlayer):

    def __init__(self, name: str, start_capital: int):
        super().__init__(name, start_capital)
        self.number_of_influenced_moves = 0

    @staticmethod
    def start_cards_sum(hand: PlayerHand):
        return hand.first_card + hand.second_card

    def get_anchoring_coefficient(self, hand: PlayerHand):
        x = self.start_cards_sum(hand)
        y = hand.optimal_value

        return anchoring_coefficient_matrix.get(x, dict()).get(y, 0)

    def get_current_action(self, hand: PlayerHand):
        default_action = super().get_current_action(hand)

        anchoring_valid = default_action in (GameActions.stand,
                                             GameActions.double_down)
        if anchoring_valid and random.random() < self.get_anchoring_coefficient(hand):
            self.number_of_influenced_moves += 1
            return GameActions.hit

        return default_action
