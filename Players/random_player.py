import random

from Players.optimal_player import OptimalPlayer
from hand import PlayerHand
from constants import GameActions


class RandomPlayer(OptimalPlayer):

    def want_double_down(self, hand: PlayerHand) -> bool:
        return self.random_bool_threshold(1 / 3)

    def want_split(self, hand: PlayerHand) -> bool:
        return self.random_bool_threshold()

    def get_current_action(self, hand: PlayerHand) -> GameActions:
        return GameActions.hit if self.random_bool_threshold() else GameActions.stand

    @staticmethod
    def random_bool_threshold(threshold=0.5) -> bool:
        return random.random() < threshold
