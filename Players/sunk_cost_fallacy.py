import math

from Players.optimal_player import OptimalPlayer
from constants import DEFAULT_BET

PI = math.pi


class SunkCostFallacyPlayer(OptimalPlayer):

    def __init__(self, name: str, start_capital: int):
        super().__init__(name, start_capital)
        self.start_money = start_capital

    @staticmethod
    def get_sunk_cost_coefficient(lost_money_pct):
        return 1 + (math.cos(1.5 * lost_money_pct) *
                    (0.99 - math.cos(PI * (lost_money_pct + 0.2) ** 2)))

    @property
    def start_bet_amount(self):
        lost_money_pct = (self.start_money - self.money) / self.start_money
        sunk_cost_coef = self.get_sunk_cost_coefficient(lost_money_pct)
        capped_sunk_cost_coef = max((1, sunk_cost_coef))

        return int(DEFAULT_BET * capped_sunk_cost_coef)
