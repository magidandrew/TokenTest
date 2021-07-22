import argparse
import sys
import numpy as np
from Structures import Block, Blockchain
import utils
import logging


class SelfishMining:
    # TODO: these values can be implemented in an abstract class if it makes sense and is easier
    def __init__(self, **kwargs):
        self.__nb_simulations = kwargs['nb_simulations']
        self.__delta = 0  # advance of selfish miners on honest ones
        self.__private_chain = 0  # length of private chain RESET at each validation
        self.__public_chain = 0  # length of public chain RESET at each validation
        self.__honest_valid_blocks = 0
        self.__selfish_valid_blocks = 0
        self.__counter = 1
        self.__blockchain = Blockchain()

        # Set Parameters
        self.__alpha = kwargs['alpha']
        self.__gamma = kwargs['gamma']

        # For Results
        self.__revenue_ratio = None
        self.__orphan_blocks = 0
        self.__total_validated_blocks = 0

        # For Rewards
        self.__honest_reward = 0
        self.__selfish_reward = 0

        # For difficulty adjustment
        self.__Tho = 10
        self.__n0 = 2016
        # self.__breaktime = None
        self.__Sn0 = None
        self.__B = 1
        self.__current_timestamp = 0
        self.__all_blocks_mined = []
        self.__last_timestamp_changed = 0

        # # Writing down results?
        # self.__write = d.get('write', False)
        # # Display to console results?
        # self.__display = d.get('display', False)

    def simulate(self):
        block_difficulty_periods = [self.__n0 for x in range(0, self.__nb_simulations // self.__n0)] \
                          + [self.__nb_simulations % self.__n0]

        # TODO: HOW ARE WE DETERMINING DIFFICULTY
        difficulty = .5

        # Each difficulty adjustment is a mining period
        for blocks_in_window in block_difficulty_periods:
            # Only run for the number of simulation steps in each window
            for sim_step in range(blocks_in_window):
                # Find whether selfish-miner or honest-miner finds block first
                results = utils.get_winner(alpha=self.__alpha, gamma=self.__gamma, difficulty=difficulty)

                self.__blockchain.add_block(Block(results['time']))

                if results['winner'] == 'honest':
                    self.__honest_valid_blocks += 1
                elif results['winner'] == 'selfish':
                    self.__delta += 1
                    self.__private_chain += 1




        # FIXME: Figure out what the selfish miner does when validated blocks exceeds 2016 (does he publish or throw those away?)
        # FIXME: In this case, selfish miner will publish only his first block to potentially win the fork, and has to discard his subsequent blocks in his selfish chain
        # FIXME: since they will no longer be valid (difficulty is encoded into the header)


def main() -> None:
    program_description = "Selfish Mining Simulator"
    implemented_mining_techniques = ["lead-stubborn", "intermittent", "smart"]

    parser = argparse.ArgumentParser(description=program_description)
    parser.add_argument('-n', '--num_blocks', required=True, type=int, help="Number of blocks to run the simulation on")
    parser.add_argument('-a', '--alpha', required=True, type=float, help="HashPower of Selfish Miner")
    parser.add_argument('-g', '--gamma', required=True, type=float,
                        help="Percentage of Honest Miners that mine on selfish chain")
    parser.add_argument("-m", "--method", required=True, type=str,
                        help="Type of mining method: ({})".format(", ".join(implemented_mining_techniques)))
    parser.add_argument('-d', action="store_true", help="Display stuff")


    args = parser.parse_args()

    if len(sys.argv) == 1:
        parser.print_usage()

    a = SelfishMining(**{'nb_simulations': 10, 'alpha': .3, 'gamma': .2})
    a.simulate()


if __name__ == "__main__":
    # logging.basicConfig(level=logging.DEBUG)
    main()
