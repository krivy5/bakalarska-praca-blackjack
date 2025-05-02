import math

from Players.optimal_player import OptimalPlayer
from constants import DEFAULT_BET, Outcomes


class HotHandFallacyPlayer(OptimalPlayer):

    @property
    def start_bet_amount(self) -> int:
        return int(self.hot_hand_coefficient * DEFAULT_BET)

    @property
    def hot_hand_coefficient(self):
        streak = self.get_current_streak()
        if streak == 0:
            return 1
        return 1 + 2 * math.log10(streak) ** 3

    def get_current_streak(self):
        streak = 0
        for outcome in reversed(self.history.outcome_history):
            if outcome != Outcomes.win:
                break
            streak += 1
        return streak


# BET IS COMPUTET BYT THIS (x is streak):
#  y=\log\left(x\right)^{3}\cdot2
