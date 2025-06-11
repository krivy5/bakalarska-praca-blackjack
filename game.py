from utilities.constants import MINIMUM_DEALER_VALUE, Outcomes
from table import Table


class Game:
    def __init__(self, table: Table):
        self.table = table
        self.number_of_rounds = None

    def set_number_of_rounds(self, number_of_rounds: int):
        self.number_of_rounds = number_of_rounds

    @property
    def active(self):
        if self.number_of_rounds is None:
            return self.table.active_players
        return self.table.active_players and self.number_of_rounds

    def update_number_of_rounds(self):
        if self.number_of_rounds:
            self.number_of_rounds -= 1

    def start(self):
        while self.active:
            self.play_one_round()
            self.table.reset_table()
            self.update_number_of_rounds()

    def play_one_round(self):
        self.table.set_bets()

        self.table.generate_start_cards()
        self.table.generate_dealer_cards()

        self.players_make_move()
        self.dealer_make_move()

        self.evaluate_players()

    def players_make_move(self):
        for player in self.table.players:
            if player.active:
                player.make_moves()

    def dealer_make_move(self):
        while self.table.dealer_hand.optimal_value < MINIMUM_DEALER_VALUE:
            next_card = self.table.get_random_cards(number_of_cards=1)[0]
            self.table.dealer_hand.add_card(next_card)

    def evaluate_players(self):
        dealer_value = self.table.dealer_hand.optimal_value

        for player in self.table.players:
            for hand in player.hands:
                if not hand.valid:
                    player.process_round(hand, Outcomes.loss)
                elif self.table.dealer_bust or hand.optimal_value > dealer_value:
                    player.process_round(hand, Outcomes.win)
                elif hand.optimal_value == dealer_value:
                    player.process_round(hand, Outcomes.draw)
                else:
                    player.process_round(hand, Outcomes.loss)
