import math
import random

from Players.optimal_player import OptimalPlayer
from constants import GameActions
from utilities import PlayerHand
from card import Card


class AnchoringPlayer(OptimalPlayer):

    @staticmethod
    def start_cards_sum(hand: PlayerHand):
        return hand.first_card + hand.second_card

    def get_anchoring_coefficient(self, hand: PlayerHand):
        x = self.start_cards_sum(hand)
        y = hand.optimal_value
        return math.log(((x + 5) ** (-1)) + 0.06) + math.log(y ** -1) + 5

    def get_current_action(self, hand: PlayerHand):
        default_action = super().get_current_action(hand)

        anchoring_valid = default_action in (GameActions.stand,
                                             GameActions.double_down)
        l[1] += 1
        if anchoring_valid and random.random() < self.get_anchoring_coefficient(hand):
            l[0] += 1
            return GameActions.hit

        return default_action


l = [0, 0]
# a = AnchoringPlayer("norik", 1000)
# h = PlayerHand()
#
# karty = [Card("2",  "d"), Card("3",  "d"), Card("4",  "d")
#          , Card("5", "d"), Card("6", "d"), Card("7", "d")
#          , Card("8", "d"), Card("9", "d"), Card("T", "d")]
#
# visited = set()
# for c1 in karty:
#     for c2 in karty:
#         for c3 in karty:
#             for c4 in karty:
#                 h.set_cards([c1, c2, c3, c4])
#                 if 12 <= h.optimal_value <= 21 and (h.first_card + h.second_card, h.optimal_value) not in visited:
#                     visited.add((h.first_card + h.second_card, h.optimal_value))
#                     print("Karty ->", h.cards, h.first_card + h.second_card, h.optimal_value)
#                     print("Koeficient ->", a.get_anchoring_coefficient(h))
#                     print()


# h.set_cards([Card("2", "d"), Card("2", "d"), Card("8", "d")])
# print("0.9 ->", a.get_anchoring_coefficient(h))
# h.set_cards([Card("2", "d"), Card("2", "d"), Card("6", "d"), Card("5", "d")])
# print("0.6 ->", a.get_anchoring_coefficient(h))
# h.set_cards([Card("2", "d"), Card("2", "d"), Card("6", "d"), Card("T", "d")])
# print("0.1 ->", a.get_anchoring_coefficient(h))
#
# h.set_cards([Card("2", "d"), Card("4", "d"), Card("6", "d")])
# print("0.8 ->", a.get_anchoring_coefficient(h))
# h.set_cards([Card("2", "d"), Card("4", "d"), Card("4", "d"), Card("5", "d")])
# print("0.5 ->", a.get_anchoring_coefficient(h))
# h.set_cards([Card("2", "d"), Card("4", "d"), Card("4", "d"), Card("T", "d")])
# print("0.05 ->", a.get_anchoring_coefficient(h))
#
# h.set_cards([Card("2", "d"), Card("6", "d"), Card("4", "d")])
# print("0.7 ->", a.get_anchoring_coefficient(h))
# h.set_cards([Card("2", "d"), Card("6", "d"), Card("2", "d"), Card("5", "d")])
# print("0.4 ->", a.get_anchoring_coefficient(h))
# h.set_cards([Card("2", "d"), Card("6", "d"), Card("2", "d"), Card("T", "d")])
# print("0.01 ->", a.get_anchoring_coefficient(h))
#
# h.set_cards([Card("2", "d"), Card("T", "d")])
# print("0.5 ->", a.get_anchoring_coefficient(h))
# h.set_cards([Card("2", "d"), Card("T", "d"), Card("3", "d")])
# print("0.35 ->", a.get_anchoring_coefficient(h))
# h.set_cards([Card("2", "d"), Card("T", "d"), Card("4", "d"), Card("4", "d")])
# print("0.01 ->", a.get_anchoring_coefficient(h))

# 4 | 12 | 0.9
# 4 | 15 | 0.6
# 4 | 20 | 0.1

# 6 | 12 | 0.8
# 6 | 15 | 0.5
# 6 | 20 | 0.05

# 8 | 12 | 0.7
# 8 | 15 | 0.4
# 8 | 20 | 0.01

# 12 | 12 | 0.5
# 12 | 15 | 0.35
# 12 | 20 | 0.01

#         return math.log(((x + 5) ** (-1)) + 0.06) + math.log(y ** -1) + 5
# koeficient sa moze zmenit