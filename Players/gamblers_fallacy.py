import math

from Players.optimal_player import OptimalPlayer
from constants import DEFAULT_BET, Outcomes


class GamblersFallacyPlayer(OptimalPlayer):

    @property
    def start_bet_amount(self) -> int:
        return int(self.gamblers_fallacy_coefficient * DEFAULT_BET)

    @property
    def gamblers_fallacy_coefficient(self):
        streak = self.current_loss_streak
        if streak == 0:
            return 1
        return 1 + 2 * math.log10(streak) ** 3

    @property
    def current_loss_streak(self):
        streak = 0
        for outcome in reversed(self.history.outcome_history):
            if outcome != Outcomes.loss:
                break
            streak += 1
        return streak
