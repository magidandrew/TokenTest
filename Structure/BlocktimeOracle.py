import math
import logging as lg

import numpy as np

# FIXME: IMPORT STATEMENTS DON'T QUITE WORK HERE
from Agents.AbstractAgent import AbstractAgent
from Agents.SelfishAgent import SelfishAgent
# from Agents.HonestAgent import HonestAgent
from collections import deque
from Structure.Block import Block


class BlocktimeOracle:
    INIT_SIZE = 500

    def __init__(self, agents: list[AbstractAgent], difficulty):
        self.difficulty: float = difficulty
        self.agents = agents
        # TODO: Do we actually need this?
        self.current_time = 0.0

        self.remake()

    def remake(self):
        all_times_arr = []

        # Iterate over each agent and create mining times
        for agent in self.agents:
            # Starts generating times after the current global time
            agent_times = [agent.get_block_time(self.difficulty) for _ in range(BlocktimeOracle.INIT_SIZE)]
            # Get the cumulative sums
            agent_times = np.cumsum(agent_times)

            # Start the times from when we last left off
            # self.current_time += fork_delta
            agent_times = agent_times + self.current_time
            # agent_times = agent_times + fork_delta

            # Mark each time with the agent that created it
            # DEBUG
            # agent_times = [(agent.get_type(), agent_times[i]) for i in range(len(agent_times))]
            # ---REAL VERSION---
            agent_times = [(agent, agent_times[i]) for i in range(len(agent_times))]

            all_times_arr += agent_times
        # sorts by agent_times, hence x[1] (second index in tuple)
        all_times_arr.sort(key=lambda x: x[1])

        # We want INIT_SIZE number of block times.
        all_times_arr = all_times_arr[:BlocktimeOracle.INIT_SIZE]

        self.allTimes = deque(all_times_arr)

    def next_time(self) -> Block:
        if self.__is_empty():
            self.remake()
        self.current_time = self.peek_left()[1]  # must index the time in the tuple, hence [1]
        winning_agent, mining_time = self.allTimes.popleft()
        transmission = Block(mining_timestamp=mining_time,
                             # # FIXME: this needs to be accounted for
                             # timestamp_of_last_block= 0.0,
                             # timestamp_of_last_block=self.blockchain.get_global_time_of_chain(),
                             winning_agent=winning_agent)
        return transmission

    def fork(self, difficulty: float, agents: list[AbstractAgent],) -> tuple[AbstractAgent, AbstractAgent, float]:
        min_time = math.inf
        winning_agent = None
        winning_chain_agent = None

        for agent in agents:
            if not agent.is_forking:
                continue
            # Split agent into defector and honest
            if agent.type == "honest":
                agent_mine_time_1 = agent.get_block_time(difficulty, alpha=agent.gamma * agent.alpha)  # honest
                agent_mine_time_2 = agent.get_block_time(difficulty, alpha=(1 - agent.gamma)*agent.alpha) #defectors


                # If the produced times are better than the current recording min_time
                if min(agent_mine_time_1, agent_mine_time_2) < min_time:

                    # honest agents won over the defectors
                    if agent_mine_time_1 < agent_mine_time_2:
                        winning_chain_agent = agent
                        winning_agent = agent
                        min_time = agent_mine_time_1

                    # Defectors won
                    else:
                        min_time = agent_mine_time_2
                        winning_agent = agent
                        # Loop through the agents and choose the other
                        for _agent in agents:
                            if _agent.type != "honest":
                                winning_chain_agent = _agent

            # Otherwise the agent is selfish
            else:
                agent_mine_time = agent.get_block_time(difficulty, alpha=agent.alpha)
                # If the selfish agents time is better than the current recorded min_time
                if agent_mine_time < min_time:
                    min_time = agent_mine_time
                    winning_agent = agent
                    winning_chain_agent = agent

            # add the time to the blockchain oracle global time counter
            # tab back everything that follows
        self.current_time += min_time

        # If a miner is not participating in the fork, they can mine in the meantime.
        # [1] bc we want the float, not the miner
        while self.peek_left()[1] <= self.current_time:
            transmission: Block = self.next_time()
            if not transmission.winning_agent.is_forking:
                transmission.winning_agent.receive_blocks_from_oracle([transmission])

                # Now increment the length of the claimed private chain
                transmission.winning_agent.store_length += 1
                transmission.winning_agent.delta += 1

                transmission.winning_agent.receive_blocks_from_oracle([transmission])
                lg.debug(str(transmission.winning_agent) + " found a block in the meantime")

        # reset the deque of times
        self.remake()

        return winning_chain_agent, winning_agent, min_time







    # def fork(self, difficulty: float, agents: list[AbstractAgent]) -> tuple[AbstractAgent, AbstractAgent, float]:
    #     min_time = math.inf
    #     winning_agent = None
    #     winning_block = None
    #     for agent in agents:
    #         # FIXME: when will is_forking be set to false in another part of the code?
    #         # FIXME: do we even need this?
    #         if agent.is_forking:
    #
    #             winning_agent = agent
    #
    #             if agent.type == "honest":
    #                 agent_mine_time_1 = agent.get_block_time(difficulty, alpha=agent.gamma*agent.alpha) #honest
    #                 agent_mine_time_2 = agent.get_block_time(difficulty, alpha=(1 - agent.gamma)*agent.alpha) #defectors
    #                 agent_mine_time = min(agent_mine_time_2, agent_mine_time_1)
    #
    #                 # if defector wins, it is a selfish win for the prev block
    #                 # if honest wins, winning block is an honest one, if defectors win, it is a selfish win
    #                 if agent_mine_time_1 < agent_mine_time_2:
    #                     winning_block = agent
    #                 else:
    #                     for this_agent in agents:
    #                         # FIXME: not enough to check for the first selfish miner, may be multiple selfish miners
    #                         if this_agent.type == "selfish":
    #                             winning_block = this_agent
    #             else:
    #                 agent_mine_time = agent.get_block_time(difficulty)
    #
    #             if min_time > agent_mine_time:
    #                 min_time = agent_mine_time
    #                 winning_block = agent
    #     return winning_block, winning_agent, min_time

    # scrap the entire existing deque and generate a new deque
    # def fork_next_time(self) -> (AbstractAgent, float):
    #     self.allTimes.clear()
    #
    #     # results = {'time': None, 'winner': None, 'block': None, 'type': None}
    #     # attack_times = {}
    #
    #     def _is_active(agent: AbstractAgent):
    #         # FIXME: this should be cleaner (whether a method of abstract class or a __name__ implementation)
    #         if agent.get_type().split("_")[0] == 'smart':
    #             if not agent.is_mining:
    #                 return False
    #         return True
    #
    #     # TODO: what does this do?
    #     # for agent in self.agents:
    #     #     if _is_active(agent):
    #     #         attack_times[agent.get_type()] = agent.get_block_time(difficulty)
    #     #     else:
    #     #         attack_times[agent.get_type()] = 100000
    #     #
    #     # results['winner'], results['time'] = min(attack_times.items(), key=lambda x: x[1])
    #     # results['type'] = results['winner'].split('_')[0]
    #     #
    #     # return results
    #     winning_time: float = 0  # ?? Some value?
    #     self.extend(fork_delta=winning_time)

    def reset(self) -> (AbstractAgent, float):
        self.allTimes.clear()
        self.remake()

    def __is_empty(self) -> bool:
        return True if len(self.allTimes) == 0 else False

    def peek_right(self) -> (AbstractAgent, float):
        # lookup O(1)
        if self.__is_empty():
            self.remake()
        return self.allTimes[-1]

    def peek_left(self) -> (AbstractAgent, float):
        # lookup O(1)
        if self.__is_empty():
            self.remake()
        return self.allTimes[0]


if __name__ == "__main__":
    pass
    test_deque = BlocktimeOracle(SelfishAgent(.3), difficulty=.4)
    for _ in range(10):
        print(test_deque.next_time())
