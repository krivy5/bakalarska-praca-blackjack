import time
import matplotlib

from Players.random_player import RandomPlayer

matplotlib.use('TkAgg')
import matplotlib.pyplot as plt

from Players.anchoring_player import AnchoringPlayer, l
from Players.optimal_player import OptimalPlayer
from Players.sunk_cost_fallacy import SunkCostFallacyPlayer
from constants import Outcomes
from game import Game
from player import Player
from table import Table


def get_win_rate(simulated_player: Player, players_in_table=None, number_of_rounds=1000):
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


def save_amount_history_data(player: Player, file_name='modeled_data/amount_history.txt'):
    with open(file_name, "w") as f:
        text = ""
        for c, amount in enumerate(player.history.amount_history):
            text += f"{c}\t{amount}\n"
        f.write(text)


def plot_values(player: Player,
                xlabel='Position',
                ylabel='Value',
                title='Value vs Position',
                marker=None,
                linewidth=0.5,
                linestyle='-',
                grid=True,
                figsize=(8, 5),
                **plot_kwargs):

    values = player.history.amount_history

    positions = list(range(len(values)))
    plt.figure(figsize=figsize)
    plt.plot(positions, values,
             linewidth=linewidth,
             marker=marker,
             linestyle=linestyle,
             **plot_kwargs)

    if grid:
        plt.grid(True, linestyle='--', alpha=0.5)
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.title(title)
    plt.tight_layout()
    plt.show()


# sunk = SunkCostFallacyPlayer("sunk", 1_000_000)
# get_win_rate(sunk, number_of_rounds=100_000)
# # save_amount_history_data(player=sunk, file_name="modeled_data/sunk_amount_history_1m_100k.txt")
# plot_values(sunk, title='klam utopenych nakladov')
# print(sunk.money)

# opt = OptimalPlayer("OptimalPlayer", 1_000_000)
# get_win_rate(opt, number_of_rounds=100_000)
# # save_amount_history_data(player=opt, file_name="modeled_data/opt_amount_history_1m_100k.txt")
# plot_values(opt, title='OPT')
# print(opt.money)

rnd = RandomPlayer("RandomPlayer", 10_000_000)
get_win_rate(rnd, number_of_rounds=100_000)
# save_amount_history_data(player=rnd, file_name="modeled_data/rnd_amount_history_1m_100k.txt")
plot_values(rnd, title='RND')
print(rnd.money)


# o, h = [], []
# for i in range(100):
#     optimal_player = OptimalPlayer("norik", 1_000_000)
#     get_win_rate(optimal_player, number_of_rounds=100_000)
#     o.append(optimal_player.money)
#     # save_amount_history_data(optimal_player, "modeled_data/opt_amount_history.txt")
#     # print()
#
#     hot_hand_fallacy_player = HotHandFallacyPlayer("norik", 1_000_000)
#     get_win_rate(hot_hand_fallacy_player, number_of_rounds=100_000)
#     h.append(hot_hand_fallacy_player.money)
#     # save_amount_history_data(hot_hand_fallacy_player, "modeled_data/hot_amount_history.txt")
#     print("i =", i)
#
# print(o)
# print(h)
# avail_player = AvailabilityHeuristicPlayer("norik", 1_000_000)
# print(get_win_rate(avail_player, number_of_rounds=100_000))
# save_amount_history_data(avail_player, "modeled_data/avail_amount_history.txt")
# print()
