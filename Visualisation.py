import numpy as np
import matplotlib.pyplot as plt
from Structure.Blockchain import Blockchain
from Structure.Block import Block
import utils

self.__nb_simulations = kwargs['nb_simulations']
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
self.__all_blocks_mined = []


def revenue_cost_time(revenue: list, cost: list, ) -> None:
    print("first method")


def difficulty_time(nb_simulations: int, B_list: list, window_size: int = 2016, alpha: float, gamma: float) -> None:
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
    # plot difficulty v.s. epochs
    plt.plot(B_list, block_difficulty_periods, label="alpha: " +
             str(alpha) + " gamma: " + str(gamma))
    plt.xlabel("Epochs ({} blocks / epoch)".format(window_size))
    plt.ylabel("Mining Difficulty Level")
    plt.legend()
    plt.show()


def alpha_revenue() -> None:
    print("first method")
