import argparse
import sys

import numpy as np

class SelfishMining:
    def __init__(self, **d):
        self.__nb_simulations = d['nb_simulations']
        self.__delta = 0  # advance of selfish miners on honest ones
        self.__privateChain = 0  # length of private chain RESET at each validation
        self.__publicChain = 0  # length of public chain RESET at each validation
        self.__honestValidBlocks = 0
        self.__selfishValidBlocks = 0
        self.__counter = 1

        # Set Parameters
        self.__alpha = d['alpha']
        self.__gamma = d['gamma']

        # For results
        self.__revenueRatio = None
        self.__orphanBlocks = 0
        self.__totalValidatedBlocks = 0

        # For difficulty adjustment
        self.__Tho = 10
        self.__n0 = 2016
        # self.__breaktime = None
        self.__Sn0 = None
        self.__B = 1
        self.__currentTimestamp = 0
        self.__allBlocksMined = []
        self.__lastTimestampDAchanged = 0

        # Writing down results?
        self.__write = d.get('write', False)
        # Display to console results?
        self.__display = d.get('display', False)


if __name__ == "__main__":
    program_description = "Selfish Mining Simulator"
    implemented_mining_techniques = ["lead-stubborn", "intermittent", "smart"]

    parser = argparse.ArgumentParser(description=program_description)
    parser.add_argument('-n', '--num_blocks', required=True, type=int, help="Number of blocks to run the simulation on")
    parser.add_argument('-a', '--alpha', required=True, type=float, help="Hashpower of Selfish Miner")
    parser.add_argument('-g', '--gamma', required=True, type=float,
                        help="Percentage of Honest Miners that mine on selfish chain")
    parser.add_argument("-m", "--method", required=True, type=str,
                        help="Type of mining method: ({})".format(", ".join(implemented_mining_techniques)))
    parser.add_argument('-d', action="store_true", help="Display stuff")

    args = parser.parse_args()

    if len(sys.argv) == 1:
        parser.print_usage()
