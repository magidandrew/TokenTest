import numpy as np
import matplotlib.pyplot as plt
from Structure.Blockchain import Blockchain
from Structure.Block import Block
import utils

# all paramters for reference
'''self.__nb_simulations = kwargs['nb_simulations']
self.__delta = 0  # advance of selfish miners on honest ones
self.__honest_valid_blocks = 0
self.__selfish_valid_blocks = 0
self.__blockchain = Blockchain()
self.__alpha = kwargs['alpha']
self.__gamma = kwargs['gamma']
self.__revenue_ratio = None
self.__orphan_blocks = 0
self.__total_validated_blocks = 0
self.__honest_reward = 0
self.__selfish_reward = 0
self.__Tho = 10
self.__window_size = 2016
self.__breaktime = None
self.__Sn0 = None
self.__B = 1
self.__all_blocks_mined = []'''


def revenue_cost_time(nb_simulations: int, strat: str, revenue: list, cost: list, alpha: float, gamma: float, window_size: int = 2016) -> None:
    # Derive the list of epochs
    block_periods = [self.__window_size for x in range(0, self.__nb_simulations // self.__window_size)] \
        + [self.__nb_simulations % self.__window_size]
    # Make the list of epoch to be strings
    for i in len(block_periods):
        if block_periods[i] == 2016:
            block_periods[i] = "epoch" + str(i) + ": complete"
        else:
            block_periods[i] = "epoch" + str(i) + ": incomplete"

    # Revenue v.s. Epoch
    plt.bar(revenue, block_periods, color="red", width=0.4,
            label="alpha: " + str(alpha) + " gamma: " + str(gamma))

    plt.xlabel("Epochs ({} blocks / epoch)".format(window_size))
    plt.ylabel("Revenue")
    plt.title("Revenue of {} v.s. Time".format(strat))
    plt.legend()
    plt.show()

    # Cost v.s. Epoch
    plt.bar(cost, block_periods, color="red", width=0.4,
            label="alpha: " + str(alpha) + " gamma: " + str(gamma))

    plt.xlabel("Epochs ({} blocks / epoch)".format(window_size))
    plt.ylabel("Cost")
    plt.title("Cost of {} v.s. Time".format(strat))
    plt.legend()
    plt.show()

    gross = revenue - cost
    # Gross v.s. Epoch
    plt.bar(gross, block_periods, color="red", width=0.4,
            label="alpha: " + str(alpha) + " gamma: " + str(gamma))

    plt.xlabel("Epochs ({} blocks / epoch)".format(window_size))
    plt.ylabel("Gross Profit")
    plt.title("Gross Profit of {} v.s. Time".format(strat))
    plt.legend()
    plt.show()


def difficulty_time(nb_simulations: int, strat: str, B_list: list, alpha: float, gamma: float, window_size: int = 2016) -> None:
    # Derive the list of epochs
    block_difficulty_periods = [self.__window_size for x in range(0, self.__nb_simulations // self.__window_size)] \
        + [self.__nb_simulations % self.__window_size]

    # Make the list of epoch to be strings
    for i in len(block_difficulty_periods):
        if block_difficulty_periods[i] == 2016:
            epoch = "epoch" + str(i) + ": complete"
        else:
            epoch = "epoch" + str(i) + ": incomplete"
    # TODO: check if len(B_list) == len(block_dfficulty_period)
    # Difficulty v.s. Epochs
    plt.plot(B_list, block_difficulty_periods, label="alpha: " +
             str(alpha) + " gamma: " + str(gamma))
    plt.xlabel("Epochs ({} blocks / epoch)".format(window_size))
    plt.ylabel("Mining Difficulty Level")
    plt.title("Difficulty Level of {} v.s. Time".format(strat))
    plt.legend()
    plt.show()


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
