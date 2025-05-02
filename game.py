from Players.optimal_player import OptimalPlayer
from constants import BLACKJACK, MINIMUM_DEALER_VALUE, Outcomes
from table import Table


class Game:
    def __init__(self, table: Table, print_process=False):
        self.table = table
        self.print_process = print_process
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
            if self.print_process:
                print("\nZacina kolo.")

            self.play_one_round()
            self.table.reset_table()

            self.update_number_of_rounds()
            # if self.number_of_rounds % 1_00_00 == 0:
            #     print(self.number_of_rounds // 10000)

            if self.print_process:
                print("Koniec hracieho kola.\n")

        if self.print_process:
            print("TOTAL WINNER IS PLAYER WITH THE MOST MONEY", self.table.players)

    def play_one_round(self):
        self.table.set_bets()
        self.table.generate_start_cards()

        self.table.generate_dealer_cards()

        self.players_make_move()

        self.dealer_make_move()
        self.evaluate_players()

        if self.print_process:
            print(self.table.players)

    def players_make_move(self):
        if self.print_process:
            print("DEALER:", self.table.dealer_hand.cards, self.table.dealer_hand.optimal_value)
        for player in self.table.players:
            if player.active:
                player.make_moves()

    def dealer_make_move(self):  # TODO REFACTOR !!!
        while self.table.dealer_hand.optimal_value < MINIMUM_DEALER_VALUE:
            next_card = self.table.get_random_cards(number_of_cards=1)[0]
            self.table.dealer_hand.add_card(next_card)

    def evaluate_players(self):
        if self.print_process:
            print("DEALER:", self.table.dealer_hand, self.table.dealer_hand.optimal_value)

        self.process_players()

    def process_players(self):
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


if __name__ == "__main__":
    money_list = []
    wins_list = []
    for i in range(1):
        p1 = OptimalPlayer("Norik", 100_000)
        t = Table()
        t.add_players([p1])
        a = Game(t, print_process=True)
        a.set_number_of_rounds(10000)
        a.start()

        money_list.append(p1.money)
        wins_list.append(p1.wins)
        print("TU:", p1.wins, p1.draws, p1.losses)
        print("TU MAS_", p1.wins * 10 - p1.losses * 10)

    from collections import Counter

    def get_occurrences(my_list):
        return dict(Counter(my_list))

    dict_money_list = get_occurrences(money_list)
    if money_list:
        print("-----MONEY LIST-----")
        for x, y in sorted(dict_money_list.items()):
            print(x, "->", y)
        print(sum(money_list) / len(money_list))
        print("-----------------")
    else:
        print("THERE IS NO MONEY LIST")

    dict_wins_list = get_occurrences(wins_list)
    if wins_list:
        print("-----WINS LIST-----")
        for x, y in sorted(dict_wins_list.items()):
            print(x, "->", y)
        print(sum(wins_list) / len(wins_list))
        print("-----------------")
    else:
        print("THERE IS NO WINS LIST")
