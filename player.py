from constants import GameActions, Outcomes
from history import History
from hand import PlayerHand


class Player:
    def __init__(self, name: str, start_capital: int):
        self.name = name
        self.money = start_capital

        self.hands = [PlayerHand()]
        self.history = History()
        self.table = None

        self.outcomes_stats = {
            Outcomes.win: 0,
            Outcomes.draw: 0,
            Outcomes.loss: 0,
        }

    def __str__(self):
        return f"Name:{self.name}: money:{self.money}; cards:{self.hands}"

    def __repr__(self):
        return f"Name:{self.name}: money:{self.money}; cards:{self.hands}"

    @property
    def active(self) -> bool:
        return self.money > 0

    @property
    def start_hand(self) -> PlayerHand:
        return self.hands[0]

    @property
    def current_bet(self):
        return sum(map(lambda x: x.amount, self.hands))

    @property
    def valid_hands(self) -> list[PlayerHand]:
        return [hand for hand in self.hands if hand.valid]

    def add_money(self, money: int) -> None:
        self.money += money

    def subtract_money(self, money: int) -> int:
        deducted = min(self.money, money)
        self.money -= deducted
        return deducted

    def reset(self):
        self.hands = self.hands[:1]
        self.start_hand.clear()

    def make_moves(self, hand=None):  # TODO REFACTOR
        if hand is None:
            hand = self.start_hand

        player_value = hand.optimal_value

        if self.can_split(hand) and self.want_split(hand):
            self.history.add_to_pre_assigned(player_value, GameActions.split)
            self.split(hand)
            return

        if self.can_double_down(hand) and self.want_double_down(hand):
            self.history.add_to_pre_assigned(player_value, GameActions.double_down)
            self.double_down(hand)
            return

        while hand.valid:
            action = self.get_current_action(hand)

            player_value = hand.optimal_value
            if action == GameActions.stand:
                self.history.add_to_pre_assigned(player_value, action)
                break
            elif action == GameActions.hit:
                self.history.add_to_pre_assigned(player_value, action)
                self.hit(hand)

    def hit(self, hand: PlayerHand):
        next_card = self.table.get_random_cards(number_of_cards=1)[0]
        hand.add_card(next_card)

    def double_down(self, hand: PlayerHand):
        next_card = self.table.get_random_cards(number_of_cards=1)[0]
        hand.add_card(next_card)

        self.subtract_money(hand.amount)
        hand.set_amount(hand.amount * 2)

    def split(self, hand: PlayerHand):  # TODO REFACTOR
        second_hand = PlayerHand()
        second_hand.set_amount(hand.amount)

        new_card1, new_card2 = self.table.get_random_cards(number_of_cards=2)
        old_card1, old_card2 = hand.cards[0], hand.cards[1]

        hand.clear()
        hand.set_cards([old_card1, new_card1])
        second_hand.set_cards([old_card2, new_card2])

        self.hands.append(second_hand)

        self.subtract_money(hand.amount)
        self.make_moves(hand)
        self.make_moves(second_hand)

    def can_split(self, hand: PlayerHand) -> bool:
        return self.money >= hand.amount and hand.equal_start_hand()

    def can_double_down(self, hand: PlayerHand) -> bool:
        return self.money >= hand.amount

    #################################################################

    @property
    def start_bet_amount(self) -> int:
        return self.start_hand.amount  # TODO zmen logiku

    def want_split(self, hand: PlayerHand) -> bool:
        inp = input(f"Do you want to split (True, False) {hand}?: ")
        return True if inp.lower() == "true" else False

    def want_double_down(self, hand: PlayerHand) -> bool:
        inp = input(f"Would you like to double down (True, False) {hand}?: ")
        return True if inp.lower() == "true" else False

    def get_current_action(self, hand: PlayerHand) -> GameActions:
        move = input(f"Type move ('hit' or 'stand'), ({hand}) {hand.optimal_value}: ")
        return GameActions(move)

    def process_round(self, hand: PlayerHand, outcome: Outcomes):
        self.outcomes_stats[outcome] += 1

        if outcome == Outcomes.win:
            self.add_money(hand.win_amount)
        elif outcome == Outcomes.draw:
            self.add_money(hand.draw_amount)

        self.history.add_to_outcome_history(outcome)
        self.history.add_to_amount_history(self.money)
        self.history.process_pre_aassigned_outcomes(outcome)
