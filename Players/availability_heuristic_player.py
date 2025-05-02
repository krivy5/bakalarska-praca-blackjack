import random

from Players.optimal_player import OptimalPlayer
from constants import GameActions, DEFAULT_BET, Outcomes
from utilities import PlayerHand


class AvailabilityHeuristicPlayer(OptimalPlayer):

    @property
    def start_bet_amount(self):
        return DEFAULT_BET

    # def want_split(self, hand: PlayerHand) -> bool:
    #     if not hand.equal_start_hand():
    #         return False
    #     card_value = hand.first_card.value

    def get_current_action(self, hand: PlayerHand) -> GameActions:
        MINIMUM_WIN_RATE = 0.583    # calculated to optimal moves making

        history_win_rate, recommended_move = self.history.get_regular_move(hand.optimal_value)

        if history_win_rate < MINIMUM_WIN_RATE or random.random() > history_win_rate:
            return super().get_current_action(hand)
        # print("teraz taham stade", history_win_rate, hand)
        return recommended_move
