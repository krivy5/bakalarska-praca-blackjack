import time
from typing import Optional, List

import matplotlib

from Players.anchoring_player import AnchoringPlayer
from Players.gamblers_fallacy import GamblersFallacyPlayer
from Players.hot_hand_fallacy_player import HotHandFallacyPlayer
from Players.random_player import RandomPlayer
from Players.sunk_cost_fallacy import SunkCostFallacyPlayer
from Players.availability_heuristic_player import AvailabilityHeuristicPlayer

matplotlib.use('TkAgg')
import matplotlib.pyplot as plt

from Players.optimal_player import OptimalPlayer
from constants import Outcomes
from game import Game
from player import Player
from table import Table


def save_amount_history_data(player: Player, file_name='modeled_data/amount_history.txt'):
    with open(file_name, "w") as f:
        text = ""
        for c, amount in enumerate(player.history.amount_history):
            text += f"{c}\t{amount}\n"
        f.write(text)


def plot_values(
    players: List[Player],
    xlabel: str = 'Position',
    ylabel: str = 'Value',
    title: str = 'Value vs Position',
    markers: Optional[List[Optional[str]]] = None,
    linestyles: Optional[List[str]] = None,
    linewidth: float = 0.5,
    grid: bool = True,
    figsize: tuple = (8, 5),
    **plot_kwargs
):
    """
    Plot each player's amount_history on the same graph.

    players      : list of Player
    markers      : optional list of markers (one per player)
    linestyles   : optional list of linestyles (one per player)
    plot_kwargs  : passed to plt.plot for all series (e.g. color, alpha)
    """
    plt.figure(figsize=figsize)

    # default markers/linestyles if not provided
    n = len(players)
    if markers is None:
        markers = [None] * n
    if linestyles is None:
        linestyles = ['-'] * n

    for idx, player in enumerate(players):
        values = player.history.amount_history
        positions = list(range(len(values)))
        plt.plot(
            positions,
            values,
            label=getattr(player, 'name', f'Player {idx+1}'),
            marker=markers[idx],
            linestyle=linestyles[idx],
            linewidth=linewidth,
            **plot_kwargs
        )

    if grid:
        plt.grid(True, linestyle='--', alpha=0.5)
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.title(title)
    plt.legend()
    plt.tight_layout()
    plt.show()


def get_win_rate(simulated_player: Player, players_in_table=None, number_of_rounds=1000, file_name="winrate.txt"):
    if players_in_table is None:
        players_in_table = []

    table = Table()
    table.add_players([simulated_player])
    table.add_players(players_in_table)

    game = Game(table)
    game.set_number_of_rounds(number_of_rounds)

    start_time = time.time()
    print("Win rate simulation started!")

    game.start()

    end_time = time.time()
    print(f"Win rate simulation finished! ({round(end_time - start_time, 2)} seconds)")

    wins = simulated_player.outcomes_stats[Outcomes.win]
    draws = simulated_player.outcomes_stats[Outcomes.draw]
    losses = simulated_player.outcomes_stats[Outcomes.loss]

    total_hands = wins + draws + losses

    print(f"Win percentage: {wins / total_hands * 100:.2f}")
    print(f"Draw percentage: {draws / total_hands * 100:.2f}")
    print(f"Loss percentage: {losses / total_hands * 100:.2f}")

    with (open(file_name, "w") as f):
        for player in table.players:
            wins = player.outcomes_stats[Outcomes.win]
            draws = player.outcomes_stats[Outcomes.draw]
            losses = player.outcomes_stats[Outcomes.loss]

            total_hands = wins + draws + losses

            f.write(f"{player.name}\n")
            f.write(f"Win percentage: {wins / total_hands * 100:.2f}\n")
            f.write(f"Draw percentage: {draws / total_hands * 100:.2f}\n")
            f.write(f"Loss percentage: {losses / total_hands * 100:.2f}\n")
            if isinstance(player, AnchoringPlayer) or isinstance(player, AvailabilityHeuristicPlayer):
                f.write(f"Number of influenced moves: {player.number_of_influenced_moves}\n")
            f.write(f"Money left: {player.money}\n\n")

        for player in table.players:
            f.write(f"{player.name}\n")
            f.write(f"{player.history.records}")
            f.write(f"\n\n")


if __name__ == "__main__":

    start_capital = 10_0000
    number_of_rounds = 1000

    opt = OptimalPlayer("Optimal", start_capital)
    hot = HotHandFallacyPlayer("HotHandFallacy", start_capital)
    sunk = SunkCostFallacyPlayer("SunkCostFallacy", start_capital)
    ava = AvailabilityHeuristicPlayer("AvailabilityHeuristic", start_capital)
    anch = AnchoringPlayer("Anchoring", start_capital)
    gamb = GamblersFallacyPlayer("GamblersFallacy", start_capital)
    rand = RandomPlayer("Random", start_capital)

    get_win_rate(
        simulated_player=rand,
        players_in_table=[opt, hot, sunk, ava, anch, gamb],
        number_of_rounds=number_of_rounds,
        file_name="skuska.txt"
    )
