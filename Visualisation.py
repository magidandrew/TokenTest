import numpy as np
import matplotlib.pyplot as plt
from Structure.Blockchain import Blockchain
from Structure.Block import Block
import utils
import sys


def revenue_cost_time(nb_simulations: int, strat: str, revenue: list, cost: list, alpha: float, gamma: float, window_size: int = 2016) -> None:
    # Derive the list of epochs
    block_periods = [window_size for x in range(0, nb_simulations // window_size)] \
        + [nb_simulations % window_size]
    # Make the list of epoch to be strings
    for i in range(len(block_periods)):
        if block_periods[i] == 2016:
            block_periods[i] = "epoch" + str(i+1) + ": complete"
        else:
            block_periods[i] = "epoch" + str(i+1) + ": incomplete"

    plt.figure(figsize=[6.4, 15.8])

    if len(block_periods) != len(revenue):
        sys.exit(
            "ERROR: The number of simulations(nb_simulations) does not match with the revenue")

    # Revenue v.s. Epoch
    plt.bar(block_periods, revenue, color="red", width=0.4,
            label="alpha: " + str(alpha) + " gamma: " + str(gamma))

    for i in range(len(block_periods)):
        plt.text(i, revenue[i], revenue[i], ha="center", va="bottom")

    plt.xlabel("Epochs ({} blocks / epoch)".format(window_size))
    plt.xticks(rotation=15)
    plt.ylabel("Revenue")
    plt.title("Revenue of {} v.s. Time".format(strat))
    plt.legend()
    plt.show()

    if len(block_periods) != len(cost):
        sys.exit(
            "ERROR: The number of simulations(nb_simulations) does not match with the cost")

    # Cost v.s. Epoch
    plt.bar(block_periods, cost, color="green", width=0.4,
            label="alpha: " + str(alpha) + " gamma: " + str(gamma))

    for i in range(len(block_periods)):
        plt.text(i, cost[i], cost[i], ha="center", va="bottom")

    plt.xlabel("Epochs ({} blocks / epoch)".format(window_size))
    plt.xticks(rotation=15)
    plt.ylabel("Cost")
    plt.title("Cost of {} v.s. Time".format(strat))
    plt.legend()
    plt.show()

    gross = [revenue[i] - cost[i] for i in range(len(revenue))]

    # Gross v.s. Epoch
    gross_pos = [gross[i] if gross[i] > 0 else 0 for i in range(len(gross))]
    gross_neg = [gross[i] if gross[i] < 0 else 0 for i in range(len(gross))]

    if len(block_periods) != len(gross):
        sys.exit(
            "ERROR: The number of simulations(nb_simulations) does not match with the revenue or cost")

    plt.bar(block_periods, gross_pos, color='red', width=0.4,
            label="Positive Profit with " + "alpha: " + str(alpha) + " gamma: " + str(gamma))
    plt.bar(block_periods, gross_neg, color='green', width=0.4,
            label="Negative Profit with "+"alpha: " + str(alpha) + " gamma: " + str(gamma))

    for i in range(len(block_periods)):
        plt.text(i, gross[i], gross[i], ha="center", va="bottom")

    plt.xlabel("Epochs ({} blocks / epoch)".format(window_size))
    plt.axhline(y=0, color='black', linestyle='-')
    plt.xticks(rotation=15)
    plt.ylabel("Gross Profit")
    plt.title("Gross Profit of {} v.s. Time".format(strat))
    plt.legend()
    plt.show()


def difficulty_time(nb_simulations: int, strat: str, difficulty_list: list, alpha: float, gamma: float, window_size: int = 2016) -> None:
    # Derive the list of epochs
    block_periods = [window_size for x in range(0, nb_simulations // window_size)] \
        + [nb_simulations % window_size]

    # Make the list of epoch to be strings
    for i in range(len(block_periods)):
        if block_periods[i] == 2016:
            block_periods[i] = "epoch" + str(i) + ": complete"
        else:
            block_periods[i] = "epoch" + str(i) + ": incomplete"

    # print(block_periods)
    # print(difficulty_list)
    if len(block_periods) != len(difficulty_list):
        sys.exit(
            "ERROR: The number of simulations(nb_simulations) does not match with the difficulty_list")

    # Difficulty v.s. Epochs
    plt.figure(figsize=[6.4, 15.8])

    plt.plot(block_periods, difficulty_list, color='maroon', label="Difficulty Level with alpha: " +
             str(alpha) + " gamma: " + str(gamma))

    for i in range(len(block_periods)):
        plt.text(i, difficulty_list[i],
                 difficulty_list[i], ha="right", va="center")

    plt.xlabel("Epochs ({} blocks / epoch)".format(window_size))
    plt.xticks(rotation=15)
    plt.axhline(y=1, color='red', linestyle='-')
    plt.ylabel("Mining Difficulty Level")
    plt.title("Difficulty Level of {} v.s. Time".format(strat))
    plt.legend()
    plt.show()


'''


def alpha_revenue(strat: str, revenue_mean_list: list, cost_mean_list: list, alpha_list: list, gamma: float) -> None:
    # Revenue v.s. Alpha
    plt.plot(revenue_mean_list, alpha_list, label="gamma" + str(gamma))

    plt.xlabel("Alpha level")
    plt.ylabel("Revenue")
    plt.title("Revenue of {} v.s. Alpha Level".format(strat))
    plt.legend()
    plt.show()

    # Cost v.s. Alpha
    plt.plot(cost_mean_list, alpha_list, label="gamma" + str(gamma))

    plt.xlabel("Alpha level")
    plt.ylabel("Cost")
    plt.title("Cost of {} v.s. Alpha Level".format(strat))
    plt.legend()
    plt.show()

    # Gross Profit v.s. Alpha
    gross_mean_list = revenue_mean_list - cost_mean_list
    plt.plot(gross_mean_list, alpha_list, label="gamma" + str(gamma))

    plt.xlabel("Alpha level")
    plt.ylabel("Gross Profit")
    plt.title("Gross Profit of {} v.s. Alpha Level".format(strat))
    plt.legend()
    plt.show()
'''
