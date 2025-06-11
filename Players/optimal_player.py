from hand import PlayerHand
from player import Player
from constants import GameActions, DEFAULT_BET

MY_CARDS = 'my_cards'
DEALER_CARD = 'dealer_card'
ACE_RANK = 'A'

ALWAYS_SPLIT = {8, 11}
NEVER_SPLIT = {4, 5, 10}
CONDITIONS_SPLIT = [
    {MY_CARDS: {2, 3, 7}, DEALER_CARD: {2, 3, 4, 5, 6, 7}},
    {MY_CARDS: {6}, DEALER_CARD: {2, 3, 4, 5, 6}},
    {MY_CARDS: {9}, DEALER_CARD: {2, 3, 4, 5, 6, 8, 9}},
]

CONDITIONS_DOUBLE_DOWN = [
    {MY_CARDS: {9}, DEALER_CARD: {3, 4, 5, 6}},
    {MY_CARDS: {10}, DEALER_CARD: {2, 3, 4, 5, 6, 7, 8, 9}},
    {MY_CARDS: {11}, DEALER_CARD: {2, 3, 4, 5, 6, 7, 8, 9, 10}},
]
CONDITIONS_DOUBLE_DOWN_WITH_ACE = [
    {MY_CARDS: {13, 14}, DEALER_CARD: {5, 6}},
    {MY_CARDS: {15, 16}, DEALER_CARD: {4, 5, 6}},
    {MY_CARDS: {17, 18}, DEALER_CARD: {3, 4, 5, 6}},
]

ALWAYS_HIT = {5, 6, 7, 8, 9, 10, 11}
ALWAYS_HIT_WITH_ACE = {13, 14, 15, 16, 17}
CONDITIONS_HIT = [
    {MY_CARDS: {13, 14, 15, 16}, DEALER_CARD: {7, 8, 9, 10, 11}},
    {MY_CARDS: {12}, DEALER_CARD: {2, 3, 7, 8, 9, 10, 11}}
]
CONDITIONS_HIT_WITH_ACE = [
    {MY_CARDS: {18}, DEALER_CARD: {9, 10, 11}},
]


class OptimalPlayer(Player):

    @property
    def start_bet_amount(self):
        return DEFAULT_BET

    def want_split(self, hand: PlayerHand) -> bool:
        if not hand.equal_start_hand():
            return False
        card_value = hand.first_card.value

        if card_value in ALWAYS_SPLIT:
            return True
        elif card_value in NEVER_SPLIT:
            return False

        dealer_upcard_value = self.table.dealer_hand.optimal_value
        for condition in CONDITIONS_SPLIT:
            if (card_value in condition[MY_CARDS] and
                    dealer_upcard_value in condition[DEALER_CARD]):
                return True
        return False

    def want_double_down(self, hand: PlayerHand) -> bool:
        dealer_value = self.table.dealer_hand.optimal_value
        hand_value = hand.optimal_value
        conditions = CONDITIONS_DOUBLE_DOWN_WITH_ACE if hand.contains_rank(ACE_RANK) \
            else CONDITIONS_DOUBLE_DOWN

        for condition in conditions:
            if (hand_value in condition[MY_CARDS] and
                    dealer_value in condition[DEALER_CARD]):
                return True
        return False

    def get_current_action(self, hand: PlayerHand) -> GameActions:
        dealer_value = self.table.dealer_hand.optimal_value
        hand_value = hand.optimal_value
        have_ace = hand.contains_rank(ACE_RANK)

        if have_ace and hand_value in ALWAYS_HIT_WITH_ACE:
            return GameActions.hit
        elif not have_ace and hand_value in ALWAYS_HIT:
            return GameActions.hit

        conditions = CONDITIONS_HIT_WITH_ACE if have_ace else CONDITIONS_HIT
        for condition in conditions:
            if (hand_value in condition[MY_CARDS] and
                    dealer_value in condition[DEALER_CARD]):
                return GameActions.hit

        return GameActions.stand
