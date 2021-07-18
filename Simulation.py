import numpy as np

class Simulation:

    def __init__(self, **args):
        self.__periods = args['periods']
		self.__delta = 0 # advance of selfish miners on honests'ones
		self.__privateChain = 0 # length of private chain RESET at each validation
		self.__publicChain = 0 # length of public chain RESET at each validation
		self.__honestsValidBlocks = 0
		self.__selfishValidBlocks = 0
		self.__counter = 1
