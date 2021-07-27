import numpy as np

from Agents.AbstractAgent import AbstractAgent
from Agents.SelfishAgent import SelfishAgent
from Agents.HonestAgent import HonestAgent
from Agents.SmartAgent import SmartAgent
from collections import deque


class DequeOfTimes:
    def __init__(self, *agents: AbstractAgent, difficulty):
        self.difficulty: float = difficulty
        self.allTimes = deque()

        # locals
        INIT_SIZE = 100
        all_times_arr = []

        # Iterate over each agent and create mining times
        for agent in agents:
            agent_times = [agent.get_block_time(self.difficulty) for _ in range(INIT_SIZE)]
            # Get the cumulative sums
            agent_times = np.cumsum(agent_times)

            # Mark each time with the agent that created it
            agent_times = [(agent, agent_times[i]) for i in range(len(agent_times))]

            all_times_arr += agent_times
        # sorts by agent_times, hence x[1] (second index in tuple)
        all_times_arr.sort(key=lambda x: x[1])
        print(all_times_arr)



if __name__=="__main__":
    test_deque = DequeOfTimes(SelfishAgent(.3), difficulty=.4)
