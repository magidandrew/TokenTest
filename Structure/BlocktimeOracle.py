import numpy as np

# FIXME: IMPORT STATEMENTS DON'T QUITE WORK HERE
from Agents.AbstractAgent import AbstractAgent
# from Agents.SelfishAgent import SelfishAgent
# from Agents.HonestAgent import HonestAgent
# from Agents.SmartAgent import SmartAgent
from collections import deque
from Structure.Block import Block


class BlocktimeOracle:
    INIT_SIZE = 100

    def __init__(self, *agents: AbstractAgent, difficulty):
        self.difficulty: float = difficulty
        self.agents = agents
        # TODO: Do we actually need this?
        self.__current_time = 0.0

        self.extend()

    def extend(self, fork_delta: float = 0.0):
        all_times_arr = []

        # Iterate over each agent and create mining times
        for agent in self.agents:
            # Starts generating times after the current global time
            agent_times = [agent.get_block_time(self.difficulty) for _ in range(BlocktimeOracle.INIT_SIZE)]
            # Get the cumulative sums
            agent_times = np.cumsum(agent_times)

            # Start the times from when we last left off
            self.__current_time += fork_delta
            agent_times = agent_times + self.__current_time
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
            self.extend()
        self.__current_time = self.peek_left()[1]  # must index the time in the tuple, hence [1]
        winning_agent, mining_time = self.allTimes.popleft()
        transmission = Block(mining_timestamp=mining_time,
                             # FIXME: this needs to be accounted for
                             timestamp_of_last_block= 0.0,
                             # timestamp_of_last_block=self.blockchain.get_global_time_of_chain(),
                             winning_agent=winning_agent)
        return transmission

    def fork(self, difficulty: float, agents: list(AbstractAgent)) -> (AbstractAgent, float):

        # A function that looks at the participating agents and adds the neccesary defectors.
        def process_defectors(agents):
            for agent in agents:
                if agent.type == 'honest':
                    # TODO: split honest miner into a defector and a residual honest miner. Add these new params to the agent class
            pass

        min_time = 1000000
        winning_agent = None
        agents = process_defectors(agents)
        for agent in agents:
            if agent.is_forking:
                agent_mine_time = agent.get_block_time(difficulty)
                if min_time > agent_mine_time:
                    min_time = agent_mine_time
                    winning_agent = agent




    # scrap the entire existing deque and generate a new deque
    def fork_next_time(self) -> (AbstractAgent, float):
        self.allTimes.clear()

        # results = {'time': None, 'winner': None, 'block': None, 'type': None}
        # attack_times = {}

        def _is_active(agent: AbstractAgent):
            # FIXME: this should be cleaner (whether a method of abstract class or a __name__ implementation)
            if agent.get_type().split("_")[0] == 'smart':
                if not agent.is_mining:
                    return False
            return True

        # TODO: what does this do?
        # for agent in self.agents:
        #     if _is_active(agent):
        #         attack_times[agent.get_type()] = agent.get_block_time(difficulty)
        #     else:
        #         attack_times[agent.get_type()] = 100000
        #
        # results['winner'], results['time'] = min(attack_times.items(), key=lambda x: x[1])
        # results['type'] = results['winner'].split('_')[0]
        #
        # return results
        winning_time: float = 0  # ?? Some value?
        self.extend(fork_delta=winning_time)

    def reset(self) -> (AbstractAgent, float):
        self.allTimes.clear()
        self.extend()

    def __is_empty(self) -> bool:
        return True if len(self.allTimes) == 0 else False

    def peek_right(self) -> (AbstractAgent, float):
        # lookup O(1)
        return self.allTimes[-1]

    def peek_left(self) -> (AbstractAgent, float):
        # lookup O(1)
        return self.allTimes[0]


if __name__ == "__main__":
    test_deque = BlocktimeOracle(SelfishAgent(.3), HonestAgent(.7), difficulty=.4)
    for _ in range(10):
        print(test_deque.next_time())
