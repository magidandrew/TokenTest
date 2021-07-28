import numpy as np

# FIXME: IMPORT STATEMENTS DON'T QUITE WORK HERE
from Agents.AbstractAgent import AbstractAgent
from Agents.SelfishAgent import SelfishAgent
from Agents.HonestAgent import HonestAgent
from Agents.SmartAgent import SmartAgent
from collections import deque


class BlocktimeOracle:
    INIT_SIZE = 100

    def __init__(self, *agents: AbstractAgent, difficulty):
        self.difficulty: float = difficulty
        self.agents = agents
        self.__current_time = 0.0

        self.extend()

    def extend(self):
        all_times_arr = []

        # Iterate over each agent and create mining times
        for agent in self.agents:
            # Starts generating times after the current global time
            agent_times = [agent.get_block_time(self.difficulty) for _ in range(BlocktimeOracle.INIT_SIZE)]
            # Get the cumulative sums
            agent_times = np.cumsum(agent_times)

            # Start the times from when we last left off
            agent_times = agent_times + self.__current_time

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

    def next_time(self) -> (AbstractAgent, float):
        if self.__is_empty():
            self.extend()
        self.__current_time = self.peek_left()[1]  # must index the time in the tuple, hence [1]
        return self.allTimes.popleft()

    # scrap the entire existing deque and generate a new deque
    def fork_next_time(self) -> (AbstractAgent, float):
        self.allTimes.clear()
        self.next_time()

    def reset(self) -> (AbstractAgent, float):
        self.allTimes.clear()

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
